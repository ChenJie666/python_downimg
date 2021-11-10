参考 [https://zhuanlan.zhihu.com/p/31220388](https://zhuanlan.zhihu.com/p/31220388)

<br>
# 一、原理
## 1.1 概念
①**算子的完整的操作：** <数据来源，操作，回调函数>构成的三元组。
②**Stage：** Stream中使用Stage的概念来描述一个完整的操作，并用某种实例化后的PipelineHelper来代表Stage，将具有先后顺序的各个Stage连到一起，就构成了整个流水线。跟Stream相关类和接口的继承关系图示。
③**中间操作和结束操作：** Stream操作分为`中间操作`和`结束操作`。中间操作只是一种标记，只有结束操作才会触发实际计算。
④**有状态和无状态：** 中间操作可以分为`有状态`和`无状态`。无状态中间操作是指元素的处理不受前面元素的影响；有状态的中间操作必须等到所有元素处理之后才知道最终结果，比如排序是有状态操作。
⑤**短路操作和非短路操作：** 结束操作又可以分为`短路操作`和`非短路操作`。短路操作是指不用处理全部元素就可以返回结果，比如找到第一个满足条件的元素。之所以要进行如此精细的划分，是因为底层对每一种情况的处理方式不同。

| Stream操作分类                    |                             |                                                              |
| --------------------------------- | --------------------------- | ------------------------------------------------------------ |
| 中间操作(Intermediate operations) | ①无状态(Stateless)          | unordered() filter() map() mapToInt() mapToLong() mapToDouble() flatMap() flatMapToInt() flatMapToLong() flatMapToDouble() peek() |
|                                   | ②有状态(Stateful)           | distinct() sorted() sorted() limit() skip()                  |
| 结束操作(Terminal operations)     | ①非短路操作                 | forEach() forEachOrdered() toArray() reduce() collect() max() min() count() |
|                                   | ②短路操作(short-circuiting) | anyMatch() allMatch() noneMatch() findFirst() findAny()      |





## 1.2 流程
![流程图](https://upload-images.jianshu.io/upload_images/21580557-fd40b43d5ffb3735.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**概述：**会根据算子的类型来定义，如果时无状态的算子，会

### 1.2.1 用户的操作如何记录？

![image.png](https://upload-images.jianshu.io/upload_images/21580557-6b754d2ec9e4f9f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. Head记录Stream起始操作
2. StatelessOp记录中间操作
3. StatefulOp记录有状态的中间操作
这三个操作实例化会指向其父类AbstractPipeline,也就是在AbstractPipeline中建立了双向链表

注意这里使用的是“操作(operation)”一词，指的是“Stream中间操作”的操作，很多Stream操作会需要一个回调函数（Lambda表达式），因此一个完整的操作是<数据来源，操作，回调函数>构成的三元组。Stream中使用Stage的概念来描述一个完整的操作，并用某种实例化后的PipelineHelper来代表Stage，将具有先后顺序的各个Stage连到一起，就构成了整个流水线。跟Stream相关类和接口的继承关系图示。

还有IntPipeline, LongPipeline, DoublePipeline没在图中画出，这三个类专门为三种基本类型（不是包装类型）而定制的，跟ReferencePipeline是并列关系。图中Head用于表示第一个Stage，即调用诸如Collection.stream()方法产生的Stage，很显然这个Stage里不包含任何操作；StatelessOp和StatefulOp分别表示无状态和有状态的Stage，对应于无状态和有状态的中间操作。

Stream流水线组织结构示意图如下：

![image.png](https://upload-images.jianshu.io/upload_images/21580557-2a6856494fed7fcd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

图中通过Collection.stream()方法得到Head也就是stage0，紧接着调用一系列的中间操作，不断产生新的Stream。这些Stream对象以双向链表的形式组织在一起，构成整个流水线，由于每个Stage都记录了前一个Stage和本次的操作以及回调函数，依靠这种结构就能建立起对数据源的所有操作。这就是Stream记录操作的方式。

### 1.2.2 操作如何叠加？
以上只是解决了操作记录的问题，要想让流水线起到应有的作用我们需要一种将所有操作叠加到一起的方案。你可能会觉得这很简单，只需要从流水线的head开始依次执行每一步的操作（包括回调函数）就行了。这听起来似乎是可行的，但是你忽略了前面的Stage并不知道后面Stage到底执行了哪种操作，以及回调函数是哪种形式。换句话说，只有当前Stage本身才知道该如何执行自己包含的动作。这就需要有某种协议来协调相邻Stage之间的调用关系。

**这种协议由Sink接口完成，Sink接口包含的方法如下表所示：**
| 方法名                          | 作用                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| void begin(long size)           | 开始遍历元素之前调用该方法，通知Sink做好准备。               |
| void end()                      | 所有元素遍历完成之后调用，通知Sink没有更多的元素了。         |
| boolean cancellationRequested() | 是否可以结束操作，可以让短路操作尽早结束。                   |
| void accept(T t)                | 遍历元素时调用，接受一个待处理元素，并对元素进行处理。Stage把自己包含的操作和回调方法封装到该方法里，前一个Stage只需要调用当前Stage.accept(T t)方法就行了。 |

有了上面的协议，相邻Stage之间调用就很方便了，每个Stage都会将自己的操作封装到一个Sink里，前一个Stage只需调用后一个Stage的accept()方法即可，并不需要知道其内部是如何处理的。当然对于有状态的操作，Sink的begin()和end()方法也是必须实现的。比如Stream.sorted()是一个有状态的中间操作，其对应的Sink.begin()方法可能创建一个乘放结果的容器，而accept()方法负责将元素添加到该容器，最后end()负责对容器进行排序。对于短路操作，Sink.cancellationRequested()也是必须实现的，比如Stream.findFirst()是短路操作，只要找到一个元素，cancellationRequested()就应该返回true，以便调用者尽快结束查找。Sink的四个接口方法常常相互协作，共同完成计算任务。实际上Stream API内部实现的的本质，就是如何重载Sink的这四个接口方法。

有了Sink对操作的包装，Stage之间的调用问题就解决了，执行时只需要从流水线的head开始对数据源依次调用每个Stage对应的Sink.{begin(), accept(), cancellationRequested(), end()}方法就可以了。一种可能的Sink.accept()方法流程是这样的：

```
void accept(U u){
    1. 使用当前Sink包装的回调函数处理u
    2. 将处理结果传递给流水线下游的Sink
}
```

Sink接口的其他几个方法也是按照这种[处理->转发]的模型实现。下面我们结合具体例子看看Stream的中间操作是如何将自身的操作包装成Sink以及Sink是如何将处理结果转发给下一个Sink的。先看Stream.map()方法：

```
// Stream.map()，调用该方法将产生一个新的Stream
public final <R> Stream<R> map(Function<? super P_OUT, ? extends R> mapper) {
    ...
    return new StatelessOp<P_OUT, R>(this, StreamShape.REFERENCE,
                                 StreamOpFlag.NOT_SORTED | StreamOpFlag.NOT_DISTINCT) {
        @Override /*opWripSink()方法返回由回调函数包装而成Sink*/
        Sink<P_OUT> opWrapSink(int flags, Sink<R> downstream) {
            return new Sink.ChainedReference<P_OUT, R>(downstream) {
                @Override
                public void accept(P_OUT u) {
                    R r = mapper.apply(u);// 1. 使用当前Sink包装的回调函数mapper处理u
                    downstream.accept(r);// 2. 将处理结果传递给流水线下游的Sink
                }
            };
        }
    };
}
```
上述代码看似复杂，其实逻辑很简单，就是将回调函数mapper包装到一个Sink当中。由于Stream.map()是一个无状态的中间操作，所以map()方法返回了一个StatelessOp内部类对象（一个新的Stream），调用这个新Stream的opWripSink()方法将得到一个包装了当前回调函数的Sink。

例Filter:
```
@Override
public final Stream<P_OUT> filter(Predicate<? super P_OUT> predicate) {
    Objects.requireNonNull(predicate);
    return new StatelessOp<P_OUT, P_OUT>(this, StreamShape.REFERENCE,
                                 StreamOpFlag.NOT_SIZED) {
        @Override
        Sink<P_OUT> opWrapSink(int flags, Sink<P_OUT> sink) {
            return new Sink.ChainedReference<P_OUT, P_OUT>(sink) {
                @Override
                public void begin(long size) {
                    downstream.begin(-1);
                }
                @Override
                public void accept(P_OUT u) {
                    //条件成立则传递给下一个操作,也因为如此所以有状态的操作必须放到
                    //end方法里面
                    if (predicate.test(u))
                        downstream.accept(u);
                }
            };
        }
    };
}
```

再来看一个复杂一点的例子。Stream.sorted()方法将对Stream中的元素进行排序，显然这是一个有状态的中间操作，因为读取所有元素之前是没法得到最终顺序的。抛开模板代码直接进入问题本质，sorted()方法是如何将操作封装成Sink的呢？sorted()一种可能封装的Sink代码如下：

```
// Stream.sort()方法用到的Sink实现
class RefSortingSink<T> extends AbstractRefSortingSink<T> {
    private ArrayList<T> list;// 存放用于排序的元素
    RefSortingSink(Sink<? super T> downstream, Comparator<? super T> comparator) {
        super(downstream, comparator);
    }
    @Override
    public void begin(long size) {
        ...
        // 创建一个存放排序元素的列表
        list = (size >= 0) ? new ArrayList<T>((int) size) : new ArrayList<T>();
    }
    @Override
    public void end() {
        list.sort(comparator);// 只有元素全部接收之后才能开始排序
        downstream.begin(list.size());
        if (!cancellationWasRequested) {// 下游Sink不包含短路操作
            list.forEach(downstream::accept);// 2. 将处理结果传递给流水线下游的Sink
        }
        else {// 下游Sink包含短路操作
            for (T t : list) {// 每次都调用cancellationRequested()询问是否可以结束处理。
                if (downstream.cancellationRequested()) break;
                downstream.accept(t);// 2. 将处理结果传递给流水线下游的Sink
            }
        }
        downstream.end();
        list = null;
    }
    @Override
    public void accept(T t) {
        list.add(t);// 1. 使用当前Sink包装动作处理t，只是简单的将元素添加到中间列表当中
    }
}
```

**上述代码完美的展现了Sink的四个接口方法是如何协同工作的：**
- 1. 首先beging()方法告诉Sink参与排序的元素个数，方便确定中间结果容器的的大小；
- 2. 之后通过accept()方法将元素添加到中间结果当中，最终执行时调用者会不断调用该方法，直到遍历所有元素；
- 3. 最后end()方法告诉Sink所有元素遍历完毕，启动排序步骤，排序完成后将结果传递给下游的Sink；
- 4. 如果下游的Sink是短路操作，将结果传递给下游时不断询问下游cancellationRequested()是否可以结束处理。

<br>
### 1.2.3 叠加之后的操作如何执行？
![image.png](https://upload-images.jianshu.io/upload_images/21580557-289e4c89fa50f5a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Sink完美封装了Stream每一步操作，并给出了[处理->转发]的模式来叠加操作。这一连串的齿轮已经咬合，就差最后一步拨动齿轮启动执行。是什么启动这一连串的操作呢？也许你已经想到了启动的原始动力就是结束操作(Terminal Operation)，一旦调用某个结束操作，就会触发整个流水线的执行。

结束操作之后不能再有别的操作，所以结束操作不会创建新的流水线阶段(Stage)，直观的说就是流水线的链表不会在往后延伸了。结束操作会创建一个包装了自己操作的Sink，这也是流水线中最后一个Sink，这个Sink只需要处理数据而不需要将结果传递给下游的Sink（因为没有下游）。对于Sink的[处理->转发]模型，结束操作的Sink就是调用链的出口。

我们再来考察一下上游的Sink是如何找到下游Sink的。一种可选的方案是在PipelineHelper中设置一个Sink字段，在流水线中找到下游Stage并访问Sink字段即可。但Stream类库的设计者没有这么做，而是设置了一个Sink AbstractPipeline.opWrapSink(int flags, Sink downstream)方法来得到Sink，该方法的作用是返回一个新的包含了当前Stage代表的操作以及能够将结果传递给downstream的Sink对象。为什么要产生一个新对象而不是返回一个Sink字段？这是因为使用opWrapSink()可以将当前操作与下游Sink（上文中的downstream参数）结合成新Sink。试想只要从流水线的最后一个Stage开始，不断调用上一个Stage的opWrapSink()方法直到最开始（不包括stage0，因为stage0代表数据源，不包含操作），就可以得到一个代表了流水线上所有操作的Sink，用代码表示就是这样：

```
// AbstractPipeline.wrapSink()
// 从下游向上游不断包装Sink。如果最初传入的sink代表结束操作，
// 函数返回时就可以得到一个代表了流水线上所有操作的Sink。
final <P_IN> Sink<P_IN> wrapSink(Sink<E_OUT> sink) {
    ...
    for (AbstractPipeline p=AbstractPipeline.this; p.depth > 0; p=p.previousStage) {
        sink = p.opWrapSink(p.previousStage.combinedFlags, sink);
    }
    return (Sink<P_IN>) sink;
}
```

现在流水线上从开始到结束的所有的操作都被包装到了一个Sink里，执行这个Sink就相当于执行整个流水线，执行Sink的代码如下：

```
// AbstractPipeline.copyInto(), 对spliterator代表的数据执行wrappedSink代表的操作。
final <P_IN> void copyInto(Sink<P_IN> wrappedSink, Spliterator<P_IN> spliterator) {
    ...
    if (!StreamOpFlag.SHORT_CIRCUIT.isKnown(getStreamAndOpFlags())) {
        wrappedSink.begin(spliterator.getExactSizeIfKnown());// 通知开始遍历
        spliterator.forEachRemaining(wrappedSink);// 迭代
        wrappedSink.end();// 通知遍历结束
    }
    ...
}
```
上述代码首先调用wrappedSink.begin()方法告诉Sink数据即将到来，然后调用spliterator.forEachRemaining()方法对数据进行迭代（Spliterator是容器的一种迭代器，[参阅](https://github.com/CarpenterLee/JavaLambdaInternals/blob/master/3-Lambda%20and%20Collections.md#spliterator)），最后调用wrappedSink.end()方法通知Sink数据处理结束。逻辑如此清晰。

#### 有状态的中间操作何时执行?
例如sorted()操作,其依赖上一次操作的结果集,按照调用链来说结果集必须在accept()调用完才会产生.那也就说明sorted操作需要在end中,然后再重新开启调用链.

**sorted的end方法:**
```
@Override
 public void end() {
     list.sort(comparator);
     downstream.begin(list.size());
     if (!cancellationWasRequested) {
         list.forEach(downstream::accept);
     }
     else {
         for (T t : list) {
             if (downstream.cancellationRequested()) break;
             downstream.accept(t);
         }
     }
     downstream.end();
     list = null;
 }
```
那么就相当于sorted给原有操作断路了一次,然后又重新接上,再次遍历.


### 1.2.4 执行后的结果（如果有）在哪里？
最后一个问题是流水线上所有操作都执行后，用户所需要的结果（如果有）在哪里？首先要说明的是不是所有的Stream结束操作都需要返回结果，有些操作只是为了使用其副作用(*Side-effects*)，比如使用`Stream.forEach()`方法将结果打印出来就是常见的使用副作用的场景（事实上，除了打印之外其他场景都应避免使用副作用），对于真正需要返回结果的结束操作结果存在哪里呢？

> 特别说明：副作用不应该被滥用，也许你会觉得在Stream.forEach()里进行元素收集是个不错的选择，就像下面代码中那样，但遗憾的是这样使用的正确性和效率都无法保证，因为Stream可能会并行执行。大多数使用副作用的地方都可以使用[归约操作](http://www.cnblogs.com/CarpenterLee/p/5-Streams%20API%28II%29.md)更安全和有效的完成。

```
// 错误的收集方式
ArrayList<String> results = new ArrayList<>();
stream.filter(s -> pattern.matcher(s).matches())
      .forEach(s -> results.add(s));  // Unnecessary use of side-effects!
// 正确的收集方式
List<String>results =
     stream.filter(s -> pattern.matcher(s).matches())
             .collect(Collectors.toList());  // No side-effects!
```
回到流水线执行结果的问题上来，需要返回结果的流水线结果存在哪里呢？这要分不同的情况讨论，下表给出了各种有返回结果的Stream结束操作.

| 返回类型 | 对应的结束操作                    |
| -------- | --------------------------------- |
| boolean  | anyMatch() allMatch() noneMatch() |
| Optional | findFirst() findAny()             |
| 归约结果 | reduce() collect()                |
| 数组     | toArray()                         |

1.  对于表中返回boolean或者Optional的操作（Optional是存放 一个 值的容器）的操作，由于值返回一个值，只需要在对应的Sink中记录这个值，等到执行结束时返回就可以了。
2.  对于归约操作，最终结果放在用户调用时指定的容器中（容器类型通过[收集器](http://www.cnblogs.com/CarpenterLee/p/5-Streams%20API%28II%29.md#%E6%94%B6%E9%9B%86%E5%99%A8)指定）。collect(), reduce(), max(), min()都是归约操作，虽然max()和min()也是返回一个Optional，但事实上底层是通过调用[reduce()](http://www.cnblogs.com/CarpenterLee/p/5-Streams%20API%28II%29.md#%E5%A4%9A%E9%9D%A2%E6%89%8Breduce)方法实现的。
3.  对于返回是数组的情况，毫无疑问的结果会放在数组当中。这么说当然是对的，但在最终返回数组之前，结果其实是存储在一种叫做*Node*的数据结构中的。Node是一种多叉树结构，元素存储在树的叶子当中，并且一个叶子节点可以存放多个元素。这样做是为了并行执行方便。关于Node的具体结构，我们会在下一节探究Stream如何并行执行时给出详细说明。

**结语:**
本文详细介绍了Stream流水线的组织方式和执行过程，学习本文将有助于理解原理并写出正确的Stream代码，同时打消你对Stream API效率方面的顾虑。如你所见，Stream API实现如此巧妙，即使我们使用外部迭代手动编写等价代码，也未必更加高效。

<br>
# 二、IntStream,LongStream,DoubleStream
## 2.1 概念
以上是ReferencePipeline，而IntPipeline、LongPipeline、DoublePipeline与其是并列关系。这4个子类都是抽象类，每个子类下都有3个静态内部类的实现类，Head、StatefulOp、StatelessOp，其中Head用于创建一个全新的流，StatefulOp表示有状态的一类操作，StatelessOp表示无状态的一类操作，这里的有状态是指前面流元素的处理会直接影响后面流元素的处理，多线程并行处理下每次运行的结果都不相同。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-3e5b8d5ceac43e1c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-ac5aafbc49a5471d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Java8支持的流处理的元素类型只有4种，double、int，long和reference类型。IntPipeline、LongPipeline、DoublePipeline专门为三种基本类型（不是包装类型）而定制的。

## 2.2 IntStream用法
### 2.2.1 创建int流
创建int流都是由IntStream接口类中的静态方法完成的，具体如下：
- of / builder： 可指定int流中包含的具体单个元素
- range / rangeClosed ： 将指定范围内的元素都添加到int流中，前者不包含最后一个元素，后者包含
- generate / iterate :  指定生成int流中int元素的生成函数，前者的生成函数没有入参，后者会将前一次调用结果作为下一次调用生成函数的入参
- concat ：将两个int流合并成一个。
```
    @Test
    public void test() throws Exception {
        //包含指定的元素
//        IntStream intStream=IntStream.of(1);
        //返回的int流中的元素是已经排序好的
        IntStream intStream=IntStream.of(1,3,2,5,4,6);
        print("of",intStream);
 
        //从11到16,不包含16
        intStream=IntStream.range(11,16);
        //从11到16,包含16
//        intStream=IntStream.rangeClosed(11,16);
        print("range",intStream);
 
        //包含指定的元素,add方法底层也是调用accept方法，然后返回this
        //返回的int流中的元素顺序与添加顺序一致
        intStream=IntStream.builder().add(23).add(22).add(21).build();
        print("builder", intStream);
 
        //指定一个int生成函数
        //返回的int流中的元素不排序
        intStream=IntStream.generate(()->{
            Random random=new Random();
            return random.nextInt(100);
        }).limit(6);
        print("generate", intStream);
 
        //指定一个int生成函数，前一次执行函数的结果会作为下一次调用函数的入参
        //第一个参数seed就是第一次调用生成函数的入参
        //返回的int流中的元素不排序
        intStream=IntStream.iterate(1,x->{
           int a=2*x;
           if(a>16){
               return a-20;
           }else{
               return a;
           }
        }).limit(6);
        print("iterate", intStream);
    }
 
    @Test
    public void test2() throws Exception {
        IntStream streamA=IntStream.range(11,15);
        IntStream streamB=IntStream.range(6,10);
        //将两个IntStream 合并起来
        //返回的int流的元素顺序与添加的流的元素顺序一致，不排序
        IntStream streamC=IntStream.concat(streamA,streamB);
        print("concat", streamC);
    }
 
    private void print(String start, IntStream intStream){
        System.out.println("print for->"+start);
        intStream.forEach(x->{
            System.out.println(x);
        });
    }
```

### 2.2.2 filter / map / flatMap /peek
filter方法会将filter函数返回false的元素从流中去除，只保留filter函数返回true的元素；
map方法用于对流中的所有元素执行某个修改动作；
peek方法通常用于打印流中的元素，peek函数无返回值；
flatMap方法同map方法，区别在于flatMap函数的返回值是一个IntStream 而非int值，可以在返回的IntStream中包含多个元素，flatMap方法最终返回的IntStream是将每次调用flatMap函数返回的IntStream 合并后的结果。其测试用例如下：
```
    @Test
    public void test3() throws Exception {
        IntStream intStream=IntStream.rangeClosed(1, 10);
        //会保留过滤函数返回true的元素，此处是保留偶数
        intStream=intStream.filter(x->{
           return x%2==0;
        }).peek(x->{ //peek方法指定的函数，以流中的元素为入参，无返回值，即不会修改元素本身
            System.out.println("filter->"+x);
        });
        //对流中的所有元素执行某个修改动作，此处是将所有值加1
        intStream=intStream.map(x->{
            return x+1;
        }).peek(x->{
            System.out.println("map->"+x);
        });
 
        //flatMap同map，区别在于flatMap指定的函数其返回值是一个IntStream，而非一个int值，最终flatMap返回的
        //IntStream是将每次调用flatMap返回的子IntStream合并后的结果
        intStream=intStream.flatMap(x->{
            //返回IntStream时可以返回多个元素
            return IntStream.of(x+3,x+2,x+1);
        }).peek(x->{
            System.out.println("flatMap->"+x);
        });
 
        print("after flatMap", intStream);
    }
```

### 2.2.3 mapToObj / mapToLong / mapToDouble / asLongStream / asDoubleStream
这几个方法都是将int流转换成其他类型的流，mapTo的三个方法可以指定具体的转换函数，as的两个方法不能指定，遵循标准的int到指定类型的转换规则，其实现如下：
```
    @Test
    public void test4() throws Exception {
        IntStream intStream=IntStream.rangeClosed(1, 3);
        intStream.mapToObj(x->{
            return new Age(x);
        }).forEach(x->{
            System.out.println("mapToObj->"+x);
        });
 
        //执行完mapToObj后intStream本身已经关闭了不能继续操作，只能操作其返回的新流
        //此处要继续操作就必须重新初始化一个新的IntStream
        intStream=IntStream.rangeClosed(1, 3);
        intStream.mapToLong(x->{
            return x+1;
        }).forEach(x->{
            System.out.println("mapToLong->"+x);
        });
 
        intStream=IntStream.rangeClosed(1, 3);
        intStream.mapToDouble(x->{
            return x+2;
        }).forEach(x->{
            System.out.println("mapToDouble->"+x);
        });
 
        //同上面的mapToLong，区别在于不能指定转换函数，而是采用标准的int到long类型的转换方法
        intStream=IntStream.rangeClosed(1, 3);
        intStream.asLongStream().forEach(x->{
            System.out.println("asLongStream->"+x);
        });
 
        intStream=IntStream.rangeClosed(1, 3);
        intStream.asDoubleStream().forEach(x->{
            System.out.println("asDoubleStream->"+x);
        });
    }
```

### 2.2.4 forEach / forEachOrdered
这两个方法都是用来遍历流中的元素，跟peek方法不同的是该这两个方法的返回值是void，执行此类返回值为void的方法会触发实际的流处理动作。forEachOrdered同forEach的区别在于并行流处理下，forEachOrdered会保证实际的处理顺序与流中元素的顺序一致，而forEach方法无法保证，默认的串行流处理下，两者无区别，都能保证处理顺序与流中元素顺序一致，测试用例如下：
```
    @Test
    public void test6() throws Exception {
        IntStream intStream=IntStream.of(6,1,3,2,5,4).parallel();
        intStream.forEach(x->{
            System.out.println("forEach->"+x);
        });
 
        //forEachOrdered同forEach，区别在于并行流处理下，forEachOrdered会保证实际的处理顺序与流中元素的顺序一致
        //而forEach方法无法保证，默认的串行流处理下，两者无区别，都能保证处理顺序与流中元素顺序一致
        intStream=IntStream.of(6,1,3,2,5,4).parallel();
        intStream.forEachOrdered(x->{
            System.out.println("forEachOrdered->"+x);
        });
    }
```

### 2.2.5 reduce / collect
reduce方法用于执行类似于累加的操作，上一次调用处理函数的结果会作为入参下一次调用的入参；collect方法的效果跟forEach类似，注意其返回值是调用supplier函数的返回值，该函数在整个流处理过程中只调用一次，参考如下测试用例：
```
    @Test
    public void test7() throws Exception {
        IntStream intStream=IntStream.of(6,1,3,2,5,4);
        OptionalInt optionalInt=intStream.reduce((x, y)->{
            System.out.println("x->"+x+",y->"+y);
            return x+y;
        });
        System.out.println("result->"+optionalInt.getAsInt());
 
        System.out.println("");
 
        intStream=IntStream.of(6,1,3,2,5,4);
        //同第一个reduce方法，区别在于可以指定起始的left，第一个reduce方法使用第一个元素作为起始的left
        int result=intStream.reduce(2,(x, y)->{
            System.out.println("x->"+x+",y->"+y);
            return x+y;
        });
        System.out.println("result->"+result+"\n");
 
        intStream=IntStream.of(6,1,3,2,5,4);
        //同forEach方法，首先调用supplier函数生成一个值，将该值作为accumulator函数的第一个参数，accumulator函数的第二个
        //参数就是流中的元素，注意第三个参数combiner无意义，可置为null
        result=intStream.collect(()->{
            Random random=new Random();
            return random.nextInt(10);
        },(x,y)->{
            System.out.println("ObjIntConsumer x->"+x+",y->"+y);
        },null);
        //返回值是supplier函数生成的值
        System.out.println("collect result->"+result+"\n");
 
    }
```

### 2.2.6 distinct / sorted / limit / skip
distinct用于对流中的元素去重，sorted用于对流中的元素升序排序，limit用于限制流中元素的个数，多余的元素会被丢弃，skip用于跳过前面指定N个元素，参考如下测试用例：
```
  @Test
    public void test8() throws Exception {
        IntStream intStream=IntStream.of(6,1,1,2,5,2,3,3,4,8,6,11,10,9);
        intStream.distinct() //对流中的元素去重
                 .sorted()  //将流中的元素排序，默认升序
                 .skip(3) //跳过前3个元素，此处是跳过1,2,3三个元素
                 .limit(6) //限制流中元素的最大个数
                 .forEach(x->{
                     System.out.println(x);
                 });
 
    }
```

### 2.2.7 sum / min / max / count / average / summaryStatistics
前面5个方法分别是获取流中元素的总和，最小值，最大值，个数和平均值，最后一个summaryStatistics方法是一次调用获取上述属性。测试用例如下：
```
    @Test
    public void test9() throws Exception {
        IntStream intStream=IntStream.of(6,1,1,2,5,2,3,4);
        //取流中元素的最大值
        OptionalInt max=intStream.max();
        System.out.println("max->"+max.getAsInt());
 
        //同其他没有流的方法，max操作会中断流，再对该流执行相关流处理方法会报错synchronizedTest.StreamTest
        intStream=IntStream.of(6,1,1,2,5,2,3,4);
        //取流中元素的最小值
        OptionalInt min=intStream.min();
        System.out.println("max->"+max.getAsInt());
 
        intStream=IntStream.of(6,1,1,2,5,2,3,4);
        //取流中元素的平均值
        OptionalDouble average=intStream.average();
        System.out.println("average->"+average.getAsDouble());
 
        intStream=IntStream.of(6,1,1,2,5,2,3,4);
        //取流中元素的个数
        long count=intStream.count();
        System.out.println("count->"+count);
 
        intStream=IntStream.of(6,1,1,2,5,2,3,4);
        //取流中元素的总和
        int sum=intStream.sum();
        System.out.println("sum->"+sum);
 
        intStream=IntStream.of(6,1,1,2,5,2,3,4);
        //取流中元素的统计情形，即一次返回min,max,count等属性
        IntSummaryStatistics summaryStatistics=intStream.summaryStatistics();
        System.out.println(summaryStatistics.toString());
    }
```

### 2.2.8 anyMatch / allMatch / noneMatch
有任何一个元素匹配，anyMatch返回true；所有元素都匹配时，allMatch返回true；没有一个元素匹配时，noneMatch返回true，参考如下测试用例
```
    @Test
    public void test10() throws Exception {
        IntStream intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        //有任何一个匹配，返回true
        boolean anyMatch=intStream.anyMatch(x->{
            return x%2==0;
        });
        System.out.println("anyMatch->"+anyMatch);
 
        intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        //所有的都匹配，返回true
        boolean allMatch=intStream.allMatch(x->{
            return x%2==0;
        });
        System.out.println("allMatch->"+allMatch);
 
        intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        //所有的都不匹配，返回true
        boolean noneMatch=intStream.noneMatch(x->{
            return x%2==0;
        });
        System.out.println("noneMatch->"+noneMatch);
    }
```

### 2.2.9 findFirst / findAny
findFirst返回流中第一个元素，findAny返回流中的任意一个元素，参考如下用例：
```
    @Test
    public void test11() throws Exception {
        IntStream intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        //返回第一个元素
        OptionalInt result=intStream.findFirst();
        System.out.println("findFirst->"+result.getAsInt());
 
        for(int i=0;i<6;i++) {
            intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
            //返回任意一个元素
            result = intStream.findAny();
            System.out.println("findAny->" + result.getAsInt());
        }
    }
```

### 2.2.10 sequential / parallel
sequential 返回的流是串行处理，parallel返回的流是并行处理，参考如下测试用例：
```
@Test
    public void test12() throws Exception {
        IntStream intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        long start=System.currentTimeMillis();
        //并行处理
        intStream.parallel().forEach(x->{
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(Thread.currentThread().getName()+":"+x);
        });
        System.out.println("parallel time->"+(System.currentTimeMillis()-start));
 
        intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        start=System.currentTimeMillis();
        //默认都是串行处理
        intStream.sequential().forEach(x->{
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println(Thread.currentThread().getName()+":"+x);
        });
        System.out.println("sequential time->"+(System.currentTimeMillis()-start));
    }
```

### 2.2.11 iterator / boxed / toArray
iterator 返回一个元素遍历器实现，boxed 返回一个流中元素的包装类的流，可用mapToObj实现相同的功能，toArray将流中的元素作为一个数组返回，参考如下测试用例：
```
    @Test
    public void test13() throws Exception {
        IntStream intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
 
        //返回一个包装类的流，效果相当于下面的mapToObj方法
//        Stream<Integer> integerStream=intStream.boxed();
        Stream<Integer> integerStream=intStream.mapToObj(x->{
            return new Integer(x);
        });
        integerStream.forEach(x->{
            System.out.println("boxed->"+x);
        });
 
        //返回一个元素遍历器，PrimitiveIterator是继承自Iterator
        intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        PrimitiveIterator.OfInt iterator=intStream.iterator();
        while (iterator.hasNext()){
            System.out.println("iterator->"+iterator.next());
        }
 
        //将流中的元素转换成一个数组
        intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
        int[] results=intStream.toArray();
        System.out.println("toArray->"+Arrays.toString(results));
    }
```

### 2.2.12 close / onClose
close方法会关闭流，并触发所有的onClose方法的执行；onClose方法用于注册一个回调函数，该方法返回一个新的流，可以连续调用注册多个回调函数，close触发时会按照注册的顺序依次执行。参考如下测试用例：
```
    @Test
    public void test14() throws Exception {
        IntStream intStream = IntStream.of(6, 1, 1, 2, 5, 2, 3, 4);
 
        //onClose方法的返回值是一个新的流，可以连续调用onClose，注册多个回调方法
        intStream.onClose(()->{
            System.out.println("intStream isClosed one ");
        }).onClose(()->{
            System.out.println("intStream isClosed two");
        }).onClose(()->{
            System.out.println("intStream isClosed three");
        });
 
        //触发onClose方法注册的多个回调方法的执行,并关闭流
        intStream.close();
        //流已关闭，不能执行流处理动作，forEach执行完成也会关闭流但是不会触发onClose方法的执行
//        intStream.forEach(x->{
//            System.out.println(x);
//        });
        System.out.println("main end");
    }
```



<br>
# 三、效率问题
对80M的文本进行处理，测试结果如下：
| 测试1  | 测试2   | 测试3   | 测试4   | 测试5   |         |
| ------ | ------- | ------- | ------- | ------- | ------- |
| 迭代   | 2601 ms | 2633 ms | 2529 ms | 2602 ms | 2707 ms |
| 串行流 | 1931 ms | 1932 ms | 1923 ms | 1993 ms | 1939 ms |
| 并行流 | 1941 ms | 2134 ms | 2136 ms | 2256 ms | 2151 ms |

**结论：**使用流(Stream)或并行流(parallelStream)效率比循环迭代的效率高。使用IntStream,LongStream,DoubleStream类对底层进行优化，速度最快。

**Stream并行流(计算密集型) > ForkJoin(大数据量) > For循环=Stream串行流**

**注意：**`在IO密集型任务中使用并行流效率不高：`并行流默认都是用同一个默认的ForkJoinPool，这个ForkJoinPool的线程数和CPU的核心数相同。如果是计算密集型的操作，直接使用是没有问题的，因为这个ForkJoinPool会将所有的CPU打满，系统资源是没有浪费的，但是，如果其中还有IO操作或等待操作，这个默认的ForkJoinPool只能消耗一部分CPU，而另外的并行流因为获取不到该ForkJoinPool的使用权，性能将大大降低。可见，默认的ForkJoinPool必须只能处理计算密集型的任务。
