# 一、HashMap并发：
## 1.1 问题
1. 首先size等公共变量不是原子性的。
2. 扩容时会产生环形链表，导致查询key哈希到环形链表所在桶且不存在该key的情况下会无限循环导致OOM。

## 1.2 扩容原理：
1）扩容
创建一个新的Entry空数组，长度是原数组的2倍。
2）rehash
遍历原Entry数组，把所有的Entry重新Hash到新数组。为什么要重新Hash呢？因为长度扩大以后，Hash的规则也随之改变。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-36088d7c25b8ae0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 1.3 产生问题原因：
假设一个HashMap已经到了Resize的临界点。此时有两个线程A和B，在同一时刻对HashMap进行Put操作：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-ba3b222848704e06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/21580557-b6ab9b8b551c304c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
此时达到Resize条件，两个线程各自进行Rezie的第一步，也就是扩容，假如此时线程B遍历到Entry3对象，刚执行完红框里的这行代码，线程就被挂起。对于线程B来说：
e = Entry3
next = Entry2
这时候线程A畅通无阻地进行着Rehash，当ReHash完成后，结果如下（图中的e和next，代表线程B的两个引用）：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d1a951dc1800471c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

直到这一步，看起来没什么毛病。接下来线程B恢复，继续执行属于它自己的ReHash。线程B刚才的状态是：
>***补充知识点：线程1和线程2在运行时有自己独立的工作内存，互不干扰，线程1本应该不会取到线程2的结果；但是在进行hash操作时会调用sun.misc.Hashing.stringHash32 方法，强制读取主内存，线程2的结果写入主内存后，线程1就会得到改变后的值***

e = Entry3
next = Entry2
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d779e7ba624fd7e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
当执行到上面这一行时，显然 i = 3，因为刚才线程A对于Entry3的hash结果也是3。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-6908f0fa69bb87cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
我们继续执行到这两行，Entry3放入了线程B的数组下标为3的位置，并且e指向了Entry2。此时e和next的指向如下：
e = Entry2
next = Entry2

整体情况如图所示：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-fe52c1e097c45f48.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

接着是新一轮循环，又执行到红框内的代码行：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-ec3838050f1157bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

e = Entry2
next = Entry3
整体情况如图所示：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-e862c6f49d62396c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
接下来执行下面的三行，用头插法把Entry2插入到了线程B的数组的头结点：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-a67b8fc5ff0c1561.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

整体情况如图所示：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-af9980fd09adf71a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第三次循环开始，又执行到红框的代码：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-4b49be187e4ad0fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

e = Entry3
next = Entry3.next = null
最后一步，当我们执行下面这一行的时候，见证奇迹的时刻来临了：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-3fc0df7631ddfa29.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

newTable[i] = Entry2
e = Entry3
Entry2.next = Entry3
Entry3.next = Entry2
链表出现了环形！
整体情况如图所示：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-5ddf59fb532bdef3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

此时，问题还没有直接产生。当调用Get查找一个不存在的Key，而这个Key的Hash结果恰好等于3的时候，由于位置3带有环形链表，所以程序将会进入死循环！

<br>
# 二、ConcurrentHashMap(1.7)
参看文章：[https://blog.csdn.net/justloveyou_/article/details/72783008](https://blog.csdn.net/justloveyou_/article/details/72783008)

## 2.1 概念
ConcurrentHashMap是HashMap的一个线程安全的、支持高效并发的版本。在默认理想状态下，ConcurrentHashMap可以支持16个线程执行并发写操作及任意数量线程的读操作。

　　在ConcurrentHashMap进行存取时，首先会定位到具体的段，然后通过对具体段的存取来完成对整个ConcurrentHashMap的存取。特别地，无论是ConcurrentHashMap的读操作还是写操作都具有很高的性能：在进行读操作时不需要加锁，而在写操作时通过锁分段技术只对所操作的段加锁而不影响客户端对其它段的访问。

## 2.2 优势
**ConcurrentHashMap的高效并发机制是通过以下三方面来保证的：**
- 通过锁分段技术保证并发环境下的写操作；
- 通过 HashEntry的不变性、Volatile变量的内存可见性和加锁重读机制保证高效、安全的读操作；
- 通过不加锁和加锁两种方案控制跨段操作的安全性。

<br>
## 2.3 结构
ConcurrentHashMap就是一个Segment数组，而一个Segment实例则是一个小的哈希表。由于Segment类继承于ReentrantLock类，从而使得Segment对象能充当锁的角色，这样，每个 Segment对象就可以守护整个ConcurrentHashMap的若干个桶，其中每个桶是由若干个HashEntry 对象链接起来的链表。通过使用段(Segment)将ConcurrentHashMap划分为不同的部分，ConcurrentHashMap就可以使用不同的锁来控制对哈希表的不同部分的修改，从而允许多个修改操作并发进行, 这正是ConcurrentHashMap锁分段技术的核心内涵。进一步地，如果把整个ConcurrentHashMap看作是一个父哈希表的话，那么每个Segment就可以看作是一个子哈希表，如下图所示：
![image](https://upload-images.jianshu.io/upload_images/21580557-fa4f7dd9f9c817a7.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

　　注意，假设ConcurrentHashMap一共分为2^n 个段，每个段中有2^m 个桶，那么段的定位方式是将key的hash值的高n位与(2^n - 1)相与。在定位到某个段后，再将key的hash值的低m位与(2^m - 1)相与，定位到具体的桶位。

<br>
## 2.4 构造函数
**①ConcurrentHashMap(int initialCapacity, float loadFactor, int concurrencyLevel)**
```
    public ConcurrentHashMap(int initialCapacity,
                             float loadFactor, int concurrencyLevel) {
        if (!(loadFactor > 0) || initialCapacity < 0 || concurrencyLevel <= 0)
            throw new IllegalArgumentException();

        if (concurrencyLevel > MAX_SEGMENTS)              
            concurrencyLevel = MAX_SEGMENTS;

        // Find power-of-two sizes best matching arguments
        int sshift = 0;            // 大小为 lg(ssize) 
        int ssize = 1;            // 段的数目，segments数组的大小(2的幂次方)
        while (ssize < concurrencyLevel) {
            ++sshift;
            ssize <<= 1;
        }
        segmentShift = 32 - sshift;      // 用于定位段
        segmentMask = ssize - 1;      // 用于定位段
        this.segments = Segment.newArray(ssize);   // 创建segments数组

        if (initialCapacity > MAXIMUM_CAPACITY)
            initialCapacity = MAXIMUM_CAPACITY;
        int c = initialCapacity / ssize;    // 总的桶数/总的段数
        if (c * ssize < initialCapacity)
            ++c;
        int cap = 1;     // 每个段所拥有的桶的数目(2的幂次方)
        while (cap < c)
            cap <<= 1;

        for (int i = 0; i < this.segments.length; ++i)      // 初始化segments数组
            this.segments[i] = new Segment<K,V>(cap, loadFactor);
    }
```

**②ConcurrentHashMap(int initialCapacity, float loadFactor)**
```
    public ConcurrentHashMap(int initialCapacity, float loadFactor) {
        this(initialCapacity, loadFactor, DEFAULT_CONCURRENCY_LEVEL);  // 默认并发级别为16
    }
```
**③ConcurrentHashMap(int initialCapacity)**
```
    public ConcurrentHashMap(int initialCapacity) {
        this(initialCapacity, DEFAULT_LOAD_FACTOR, DEFAULT_CONCURRENCY_LEVEL);
    }
```
**④ConcurrentHashMap()**
```
    public ConcurrentHashMap() {
        this(DEFAULT_INITIAL_CAPACITY, DEFAULT_LOAD_FACTOR, DEFAULT_CONCURRENCY_LEVEL);
    }
```
**⑤ConcurrentHashMap(Map<? extends K, ? extends V> m)**
```
    public ConcurrentHashMap(Map<? extends K, ? extends V> m) {
        this(Math.max((int) (m.size() / DEFAULT_LOAD_FACTOR) + 1,
                      DEFAULT_INITIAL_CAPACITY),
             DEFAULT_LOAD_FACTOR, DEFAULT_CONCURRENCY_LEVEL);
        putAll(m);
    }
```

<br>
## 2.5 并发存取
在ConcurrentHashMap中，线程对映射表做读操作时，一般情况下不需要加锁就可以完成，对容器做结构性修改的操作(比如，put操作、remove操作等)才需要加锁。

### 2.5.1 并发写操作 put(key, vlaue)
```
    public V put(K key, V value) {
        if (value == null)
            throw new NullPointerException();
        int hash = hash(key.hashCode());
        return segmentFor(hash).put(key, hash, value, false);
    }
```
当我们向ConcurrentHashMap中put一个Key/Value对时，首先会获得Key的哈希值并对其再次哈希，然后根据最终的hash值定位到这条记录所应该插入的段，定位段的segmentFor()方法源码如下：
```
    final Segment<K,V> segmentFor(int hash) {
        return segments[(hash >>> segmentShift) & segmentMask];
    }
```
segmentFor()方法根据传入的hash值向右无符号右移segmentShift位，然后和segmentMask进行与操作就可以定位到特定的段。在这里，假设Segment的数量(segments数组的长度)是2的n次方(Segment的数量总是2的倍数，具体见构造函数的实现)，那么segmentShift的值就是32-n(hash值的位数是32)，而segmentMask的值就是2^n-1（写成二进制的形式就是n个1）。进一步地，我们就可以得出以下结论：根据key的hash值的高n位就可以确定元素到底在哪一个Segment中。紧接着，调用这个段的put()方法来将目标Key/Value对插到段中，段的put()方法的源码如下所示：
```
    V put(K key, int hash, V value, boolean onlyIfAbsent) {
            lock();    // 上锁
            try {
                int c = count;
                if (c++ > threshold) // ensure capacity
                    rehash();
                HashEntry<K,V>[] tab = table;    // table是Volatile的
                int index = hash & (tab.length - 1);    // 定位到段中特定的桶
                HashEntry<K,V> first = tab[index];   // first指向桶中链表的表头
                HashEntry<K,V> e = first;

                // 检查该桶中是否存在相同key的结点
                while (e != null && (e.hash != hash || !key.equals(e.key)))  
                    e = e.next;

                V oldValue;
                if (e != null) {        // 该桶中存在相同key的结点
                    oldValue = e.value;
                    if (!onlyIfAbsent)
                        e.value = value;        // 更新value值
                }else {         // 该桶中不存在相同key的结点
                    oldValue = null;
                    ++modCount;     // 结构性修改，modCount加1
                    tab[index] = new HashEntry<K,V>(key, hash, first, value);  // 创建HashEntry并将其链到表头
                    count = c;      //write-volatile，count值的更新一定要放在最后一步(volatile变量)
                }
                return oldValue;    // 返回旧值(该桶中不存在相同key的结点，则返回null)
            } finally {
                unlock();      // 在finally子句中解锁
            }
        }
```
从源码中首先可以知道，ConcurrentHashMap对Segment的put操作是加锁完成的。在第二节我们已经知道，Segment是ReentrantLock的子类，因此`Segment本身就是一种可重入的Lock，所以我们可以直接调用其继承而来的lock()方法和unlock()方法对代码进行上锁/解锁`。需要注意的是，这里的加锁操作是针对某个具体的Segment，锁定的也是该Segment而不是整个ConcurrentHashMap。因为插入键/值对操作只是在这个Segment包含的某个桶中完成，不需要锁定整个ConcurrentHashMap。因此，其他写线程对另外15个Segment的加锁并不会因为当前线程对这个Segment的加锁而阻塞。故而 相比较于 HashTable 和由同步包装器包装的HashMap每次只能有一个线程执行读或写操作，ConcurrentHashMap 在并发访问性能上有了质的提高。在理想状态下，ConcurrentHashMap 可以支持 16 个线程执行并发写操作（如果并发级别设置为 16），及任意数量线程的读操作。
在**将Key/Value对插入到Segment之前，首先会检查本次插入会不会导致Segment中元素的数量超过阈值threshold**，如果会，那么就先对Segment进行扩容和重哈希操作，然后再进行插入。重哈希操作暂且不表，稍后详述。第8和第9行的操作就是定位到段中特定的桶并确定链表头部的位置。第12行的while循环用于检查该桶中是否存在相同key的结点，如果存在，就直接更新value值；如果没有找到，则进入21行生成一个新的HashEntry并且把它链到该桶中链表的表头，然后再更新count的值(由于count是volatile变量，所以count值的更新一定要放在最后一步)。
到此为止，除了重哈希操作，ConcurrentHashMap的put操作已经介绍完了。此外，在ConcurrentHashMap中，修改操作还包括putAll()和replace()。其中，putAll()操作就是多次调用put方法，而replace()操作实现要比put()操作简单得多，此不赘述。

### 2.5.2 重哈希操作  rehash()
上面叙述到，在ConcurrentHashMap中使用put操作插入Key/Value对之前，首先会检查本次插入会不会导致Segment中节点数量超过阈值threshold，如果会，那么就先对Segment进行扩容和重哈希操作。特别需要注意的是，ConcurrentHashMap的重哈希实际上是对ConcurrentHashMap的某个段的重哈希，因此ConcurrentHashMap的每个段所包含的桶位自然也就不尽相同。针对段进行rehash()操作的源码如下：
```
     void rehash() {
            HashEntry<K,V>[] oldTable = table;    // 扩容前的table
            int oldCapacity = oldTable.length;
            if (oldCapacity >= MAXIMUM_CAPACITY)   // 已经扩到最大容量，直接返回
                return;

            // 新创建一个table，其容量是原来的2倍
            HashEntry<K,V>[] newTable = HashEntry.newArray(oldCapacity<<1);   
            threshold = (int)(newTable.length * loadFactor);   // 新的阈值
            int sizeMask = newTable.length - 1;     // 用于定位桶
            for (int i = 0; i < oldCapacity ; i++) {
                // We need to guarantee that any existing reads of old Map can
                //  proceed. So we cannot yet null out each bin.
                HashEntry<K,V> e = oldTable[i];  // 依次指向旧table中的每个桶的链表表头

                if (e != null) {    // 旧table的该桶中链表不为空
                    HashEntry<K,V> next = e.next;
                    int idx = e.hash & sizeMask;   // 重哈希已定位到新桶
                    if (next == null)    //  旧table的该桶中只有一个节点
                        newTable[idx] = e;
                    else {    
                        // Reuse trailing consecutive sequence at same slot
                        HashEntry<K,V> lastRun = e;
                        int lastIdx = idx;
                        for (HashEntry<K,V> last = next; last != null; last = last.next) {
                            int k = last.hash & sizeMask;
                            // 寻找k值相同的子链，该子链尾节点与父链的尾节点必须是同一个
                            if (k != lastIdx) {
                                lastIdx = k;
                                lastRun = last;
                            }
                        }

                        // JDK直接将子链lastRun放到newTable[lastIdx]桶中
                        newTable[lastIdx] = lastRun;

                        // 对该子链之前的结点，JDK会挨个遍历并把它们复制到新桶中
                        for (HashEntry<K,V> p = e; p != lastRun; p = p.next) {
                            int k = p.hash & sizeMask;
                            HashEntry<K,V> n = newTable[k];
                            newTable[k] = new HashEntry<K,V>(p.key, p.hash,
                                                             n, p.value);
                        }
                    }
                }
            }
            table = newTable;   // 扩容完成
        }
```
由于扩容是按照2的幂次方进行的，所以扩展前在同一个桶中的元素，现在要么还是在原来的序号的桶里，或者就是原来的序号再加上一个2的幂次方，就这两种选择。根据本文前面对HashEntry的介绍，我们知道链接指针next是final的，因此看起来我们好像只能把该桶的HashEntry链中的每个节点复制到新的桶中(这意味着我们要重新创建每个节点)，但事实上JDK对其做了一定的优化。因为在理论上原桶里的HashEntry链可能存在一条子链，这条子链上的节点都会被重哈希到同一个新的桶中，这样我们只要拿到该子链的头结点就可以直接把该子链放到新的桶中，从而避免了一些节点不必要的创建，提升了一定的效率。因此，JDK为了提高效率，它会首先去查找这样的一个子链，而且这个子链的尾节点必须与原hash链的尾节点是同一个，那么就只需要把这个子链的头结点放到新的桶中，其后面跟的一串子节点自然也就连接上了。对于这个子链头结点之前的结点，JDK会挨个遍历并把它们复制到新桶的链头(只能在表头插入元素)中。特别地，我们注意这段代码：
```
for (HashEntry<K,V> last = next; last != null; last = last.next) {
    int k = last.hash & sizeMask;
    if (k != lastIdx) {
        lastIdx = k;
        lastRun = last;
    }
}
newTable[lastIdx] = lastRun;
```
　　在该代码段中，JDK直接将子链lastRun放到newTable[lastIdx]桶中，难道这个操作不会覆盖掉newTable[lastIdx]桶中原有的元素么？事实上，这种情形时不可能出现的，因为桶newTable[lastIdx]在子链添加进去之前压根就不会有节点存在，这还是因为table的大小是按照2的幂次方的方式去扩展的。假设原来table的大小是2^k 大小，那么现在新table的大小是2^(k+1)大小，而定位桶的方式是:
```
// sizeMask = newTable.length - 1，即 sizeMask = 11...1，共k+1个1。
int idx = e.hash & sizeMask;
```
　　因此这样得到的idx实际上就是key的hash值的低k+1位的值，而原table的sizeMask也全是1的二进制，不过总共是k位，那么原table的idx就是key的hash值的低k位的值。所以，如果元素的hashcode的第k+1位是0，那么元素在新桶的序号就是和原桶的序号是相等的；如果第k+1位的值是1，那么元素在新桶的序号就是原桶的序号加上2^k。因此，JDK直接将子链lastRun放到newTable[lastIdx]桶中就没问题了，因为newTable中新序号处此时肯定是空的。

### 2.5.3 读取实现 get(Object key)
　　与put操作类似，当我们从ConcurrentHashMap中查询一个指定Key的键值对时，首先会定位其应该存在的段，然后查询请求委托给这个段进行处理，源码如下：
```
    public V get(Object key) {
        int hash = hash(key.hashCode());
        return segmentFor(hash).get(key, hash);
    }
```
我们紧接着研读Segment中get操作的源码：
```
    V get(Object key, int hash) {
            if (count != 0) {            // read-volatile，首先读 count 变量
                HashEntry<K,V> e = getFirst(hash);   // 获取桶中链表头结点
                while (e != null) {
                    if (e.hash == hash && key.equals(e.key)) {    // 查找链中是否存在指定Key的键值对
                        V v = e.value;
                        if (v != null)  // 如果读到value域不为 null，直接返回
                            return v;   
                        // 如果读到value域为null，说明发生了重排序，加锁后重新读取
                        return readValueUnderLock(e); // recheck
                    }
                    e = e.next;
                }
            }
            return null;  // 如果不存在，直接返回null
        }
```
　　了解了ConcurrentHashMap的put操作后，上述源码就很好理解了。但是有一个情况需要特别注意，就是链中存在指定Key的键值对并且其对应的Value值为null的情况。在剖析ConcurrentHashMap的put操作时，我们就知道ConcurrentHashMap不同于HashMap，它既不允许key值为null，也不允许value值为null。但是，此处怎么会存在键值对存在且的Value值为null的情形呢？JDK官方给出的解释是，这种情形发生的场景是：**初始化HashEntry时发生的指令重排序导致的，也就是在HashEntry初始化完成之前便返回了它的引用。**这时，JDK给出的解决之道就是加锁重读，源码如下：
```
        V readValueUnderLock(HashEntry<K,V> e) {
            lock();
            try {
                return e.value;
            } finally {
                unlock();
            }
        }
```

### 2.5.4 ConcurrentHashMap 存取小结
　　在ConcurrentHashMap进行存取时，首先会定位到具体的段，然后通过对具体段的存取来完成对整个ConcurrentHashMap的存取。特别地，无论是ConcurrentHashMap的读操作还是写操作都具有很高的性能：在进行读操作时不需要加锁，而在写操作时通过锁分段技术只对所操作的段加锁而不影响客户端对其它段的访问。

## 2.6 读操作不需要加锁的奥秘
HashEntry对象几乎是不可变的(只能改变Value的值)，因为HashEntry中的key、hash和next指针都是final的。这意味着，我们不能把节点添加到链表的中间和尾部，也不能在链表的中间和尾部删除节点。这个特性可以保证：在访问某个节点时，这个节点之后的链接不会被改变，这个特性可以大大降低处理链表时的复杂性。
与此同时，由于HashEntry类的value字段被声明是Volatile的，因此Java的内存模型就可以保证：某个写线程对value字段的写入马上就可以被后续的某个读线程看到。
此外，由于在ConcurrentHashMap中不允许用null作为键和值，所以当读线程读到某个HashEntry的value为null时，便知道产生了冲突 —— 发生了重排序现象，此时便会加锁重新读入这个value值。这些特性互相配合，使得读线程即使在不加锁状态下，也能正确访问 ConcurrentHashMap。

**总的来说，ConcurrentHashMap读操作不需要加锁的奥秘在于以下三点：**
- `用HashEntery对象的不变性来降低读操作对加锁的需求；(final修饰key、hash、next，保证并发修改时原始节点不会改变)`
- `用Volatile变量协调读写线程间的内存可见性；(value和count)`
- `若读时发生指令重排序现象，则加锁重读；(readValueUnderLock)`

**对以上一和二两点的展开：**
1、用HashEntery对象的不变性来降低读操作对加锁的需求
　　非结构性修改操作只是更改某个HashEntry的value字段的值。由于对Volatile变量的写入操作将与随后对这个变量的读操作进行同步，所以当一个写线程修改了某个HashEntry的value字段后，Java内存模型能够保证读线程一定能读取到这个字段更新后的值。所以，写线程对链表的非结构性修改能够被后续不加锁的读线程看到。
　　对ConcurrentHashMap做结构性修改时，实质上是对某个桶指向的链表做结构性修改。如果能够确保在读线程遍历一个链表期间，写线程对这个链表所做的结构性修改不影响读线程继续正常遍历这个链表，那么读/写线程之间就可以安全并发访问这个ConcurrentHashMap。在ConcurrentHashMap中，结构性修改操作包括put操作、remove操作和clear操作，下面我们分别分析这三个操作：
- clear操作只是把ConcurrentHashMap中所有的桶置空，每个桶之前引用的链表依然存在，只是桶不再引用这些链表而已，而链表本身的结构并没有发生任何修改。因此，正在遍历某个链表的读线程依然可以正常执行对该链表的遍历。
- 关于put操作的细节我们在上文已经单独介绍过，我们知道put操作如果需要插入一个新节点到链表中时会在链表头部插入这个新节点，此时链表中的原有节点的链接并没有被修改。也就是说，插入新的健/值对到链表中的操作不会影响读线程正常遍历这个链表。

　下面来分析 remove 操作，先让我们来看看 remove 操作的源代码实现:
```
    public V remove(Object key) {
    int hash = hash(key.hashCode());
        return segmentFor(hash).remove(key, hash, null);
    }
```
　　同样地，在ConcurrentHashMap中删除一个键值对时，首先需要定位到特定的段并将删除操作委派给该段。Segment的remove操作如下所示：
```
        V remove(Object key, int hash, Object value) {
            lock();     // 加锁
            try {
                int c = count - 1;      
                HashEntry<K,V>[] tab = table;
                int index = hash & (tab.length - 1);        // 定位桶
                HashEntry<K,V> first = tab[index];
                HashEntry<K,V> e = first;
                while (e != null && (e.hash != hash || !key.equals(e.key)))  // 查找待删除的键值对
                    e = e.next;

                V oldValue = null;
                if (e != null) {    // 找到
                    V v = e.value;
                    if (value == null || value.equals(v)) {
                        oldValue = v;
                        // All entries following removed node can stay
                        // in list, but all preceding ones need to be
                        // cloned.
                        ++modCount;
                        // 所有处于待删除节点之后的节点原样保留在链表中
                        HashEntry<K,V> newFirst = e.next;
                        // 所有处于待删除节点之前的节点被克隆到新链表中
                        for (HashEntry<K,V> p = first; p != e; p = p.next)
                            newFirst = new HashEntry<K,V>(p.key, p.hash,newFirst, p.value); 

                        tab[index] = newFirst;   // 将删除指定节点并重组后的链重新放到桶中
                        count = c;      // write-volatile，更新Volatile变量count
                    }
                }
                return oldValue;
            } finally {
                unlock();          // finally子句解锁
            }
        }
```
　　Segment的remove操作和前面提到的get操作类似，首先根据散列码找到具体的链表，然后遍历这个链表找到要删除的节点，最后把待删除节点之后的所有节点原样保留在新链表中，把待删除节点之前的每个节点克隆到新链表中。假设写线程执行remove操作，要删除链表的C节点，另一个读线程同时正在遍历这个链表，如下图所示：
![image](https://upload-images.jianshu.io/upload_images/21580557-b1f6263f050bc3b0.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/21580557-0c7616d0b1a61b79?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

　　我们可以看出，删除节点C之后的所有节点原样保留到新链表中；删除节点C之前的每个节点被克隆到新链表中(它们在新链表中的链接顺序被反转了)。因此，在执行remove操作时，原始链表并没有被修改，也就是说，读线程不会受同时执行 remove 操作的并发写线程的干扰。

　　综合上面的分析我们可以知道，无论写线程对某个链表进行结构性修改还是非结构性修改，都不会影响其他的并发读线程对这个链表的访问。

2、用 Volatile 变量协调读写线程间的内存可见性
　　一般地，由于内存可见性问题，在未正确同步的情况下，对于写线程写入的值读线程可能并不能及时读到。下面以写线程M和读线程N来说明ConcurrentHashMap如何协调读/写线程间的内存可见性问题，如下图所示：

![image](https://upload-images.jianshu.io/upload_images/21580557-3d1833713936109c.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

　　假设线程M在写入了volatile变量count后，线程N读取了这个volatile变量。根据 happens-before 关系法则中的程序次序法则，A appens-before 于 B，C happens-before D。根据 Volatile法则，B happens-before C。结合传递性，则可得到：A appens-before 于 B； B appens-before C；C happens-before D。也就是说，写线程M对链表做的结构性修改对读线程N是可见的。虽然线程N是在未加锁的情况下访问链表，但Java的内存模型可以保证：只要之前对链表做结构性修改操作的写线程M在退出写方法前写volatile变量count，读线程N就能读取到这个volatile变量count的最新值。

　　事实上，ConcurrentHashMap就是一个Segment数组，而每个Segment都有一个volatile变量count去统计Segment中的HashEntry的个数。并且，在ConcurrentHashMap中，所有不加锁读方法在进入读方法时，首先都会去读这个count变量。比如我们在上一节提到的get方法：
```
    V get(Object key, int hash) {
            if (count != 0) {            // read-volatile，首先读 count 变量
                HashEntry<K,V> e = getFirst(hash);   // 获取桶中链表头结点
                while (e != null) {
                    if (e.hash == hash && key.equals(e.key)) {    // 查找链中是否存在指定Key的键值对
                        V v = e.value;
                        if (v != null)  // 如果读到value域不为 null，直接返回
                            return v;   
                        // 如果读到value域为null，说明发生了重排序，加锁后重新读取
                        return readValueUnderLock(e); // recheck
                    }
                    e = e.next;
                }
            }
            return null;  // 如果不存在，直接返回null
        }
```

3、小结
　　在ConcurrentHashMap中，所有执行写操作的方法（put、remove和clear）在对链表做结构性修改之后，在退出写方法前都会去写这个count变量；所有未加锁的读操作（get、contains和containsKey）在读方法中，都会首先去读取这个count变量。根据 Java 内存模型，对同一个 volatile 变量的写/读操作可以确保：写线程写入的值，能够被之后未加锁的读线程“看到”。这个特性和前面介绍的HashEntry对象的不变性相结合，使得在ConcurrentHashMap中读线程进行读取操作时基本不需要加锁就能成功获得需要的值。这两个特性以及加锁重读机制的互相配合，不仅减少了请求同一个锁的频率（读操作一般不需要加锁就能够成功获得值），也减少了持有同一个锁的时间（只有读到 value 域的值为 null 时 , 读线程才需要加锁后重读）。

## 2.6 ConcurrentHashMap 的跨段操作
　　在ConcurrentHashMap中，有些操作需要涉及到多个段，比如说size操作、containsValue操作等。以size操作为例，如果我们要统计整个ConcurrentHashMap里元素的大小，那么就必须统计所有Segment里元素的大小后求和。我们知道，Segment里的全局变量count是一个volatile变量，那么在多线程场景下，我们是不是直接把所有Segment的count相加就可以得到整个ConcurrentHashMap大小了呢？显然不能，虽然相加时可以获取每个Segment的count的最新值，但是拿到之后可能累加前使用的count发生了变化，那么统计结果就不准了。所以最安全的做法，是在统计size的时候把所有Segment的put，remove和clean方法全部锁住，但是这种做法显然非常低效。那么，我们还是看一下JDK是如何实现size()方法的吧：
```
    public int size() {
        final Segment<K,V>[] segments = this.segments;
        long sum = 0;
        long check = 0;
        int[] mc = new int[segments.length];
        // Try a few times to get accurate count. On failure due to
        // continuous async changes in table, resort to locking.
        for (int k = 0; k < RETRIES_BEFORE_LOCK; ++k) {
            check = 0;
            sum = 0;
            int mcsum = 0;
            for (int i = 0; i < segments.length; ++i) {
                sum += segments[i].count;   
                mcsum += mc[i] = segments[i].modCount;  // 在统计size时记录modCount
            }
            if (mcsum != 0) {
                for (int i = 0; i < segments.length; ++i) {
                    check += segments[i].count;
                    if (mc[i] != segments[i].modCount) {  // 统计size后比较各段的modCount是否发生变化
                        check = -1; // force retry
                        break;
                    }
                }
            }
            if (check == sum)// 如果统计size前后各段的modCount没变，且两次得到的总数一致，直接返回
                break;
        }
        if (check != sum) { // Resort to locking all segments  // 加锁统计
            sum = 0;
            for (int i = 0; i < segments.length; ++i)
                segments[i].lock();
            for (int i = 0; i < segments.length; ++i)
                sum += segments[i].count;
            for (int i = 0; i < segments.length; ++i)
                segments[i].unlock();
        }
        if (sum > Integer.MAX_VALUE)
            return Integer.MAX_VALUE;
        else
            return (int)sum;
    }
```
　　size方法主要思路是先在没有锁的情况下对所有段大小求和，这种求和策略最多执行RETRIES_BEFORE_LOCK次(默认是两次)：在没有达到RETRIES_BEFORE_LOCK之前，求和操作会不断尝试执行（这是因为遍历过程中可能有其它线程正在对已经遍历过的段进行结构性更新）；在超过RETRIES_BEFORE_LOCK之后，如果还不成功就在持有所有段锁的情况下再对所有段大小求和。事实上，在累加count操作过程中，之前累加过的count发生变化的几率非常小，所以ConcurrentHashMap的做法是先尝试RETRIES_BEFORE_LOCK次通过不锁住Segment的方式来统计各个Segment大小，如果统计的过程中，容器的count发生了变化，则再采用加锁的方式来统计所有Segment的大小。

　　那么，ConcurrentHashMap是如何判断在统计的时候容器的段发生了结构性更新了呢？我们在前文中已经知道，Segment包含一个modCount成员变量，在会引起段发生结构性改变的所有操作(put操作、 remove操作和clean操作)里，都会将变量modCount进行加1，因此，JDK只需要在统计size前后比较modCount是否发生变化就可以得知容器的大小是否发生变化。

　　至于ConcurrentHashMap的跨其他跨段操作，比如contains操作、containsValaue操作等，其与size操作的实现原理相类似，此不赘述。
