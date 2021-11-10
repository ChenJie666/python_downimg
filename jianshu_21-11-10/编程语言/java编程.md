\u开头的是一个Unicode码的字符，每一个'\u0000'代表的应该是NULL,输出控制台是一个空格，32以下的都是空格。ASCII码是unicode码的子集。

1 简单。Java语言的语法与C语言和C++语言很接近，使得大多数程序员很容易学习和使用Java。

2 面向对象。Java语言提供类、接口和继承等原语，为了简单起见，只支持类之间的单继承，但支持接口之间的多继承，并支持类与接口之间的实现机制（关键字为implements）。

3 分布式。Java语言支持Internet应用的开发，在基本的Java应用编程接口中有一个网络应用编程接口（java net），它提供了用于网络应用编程的类库，包括URL、URLConnection、Socket、ServerSocket等。Java的RMI（远程方法激活）机制也是开发分布式应用的重要手段。

4 健壮。Java的强类型机制、异常处理、垃圾的自动收集等是Java程序健壮性的重要保证。对指针的包装是Java的明智选择。
引用 -> 安全的指针
5 安全。Java通常被用在网络环境中，为此，Java提供了一个安全机制以防恶意代码的攻击。如：安全防范机制（类ClassLoader），如分配不同的名字空间以防替代本地的同名类、字节代码检查。

6 跨平台。Java程序（后缀为java的文件）在Java平台上被编译为体系结构中立的字节码格式（后缀为class的文件），然后可以在实现这个Java平台的任何系统中运行。


7 性能好。与那些解释型的高级脚本语言相比，Java的性能还是较优的。

8 多线程。在Java语言中，线程是一种特殊的对象，它必须由Thread类或其子（孙）类来创建,目的就是最大化利用CPU。

Overload是方法重载，指的是在同一个类中，方法名称相同，形参列表不同的两个或者多个方法，和返回值类型无关。
Override是方法的重写，指的是子类在继承父类时，当父类的方法体不适用于子类时，子类可重写父类的方法。重写必须遵守方法名和形参列表与父类的被重写的方法相同，而返回值类型可以小于等于父类被重写的方法（如果是基本数据类型和void必须相同），权限修饰符可以大于等于父类被重写的方法，抛出的异常列表可以小于等于父类被重写的方法。



    ~6 = -7的理解：	（1）（~6+1）是-6的补码，
		（2）因为直接存在计算机中，且是负数，所以计算机认为这个是补码，输出时取（-6的补码）的补码得到要输出的数的原码
		（3）于是输出的原码的值为-6，于是（~6+1）=-6，则~6=-7

把字符串转为整数的方法是：String a = “43”; int i = Integer.parseInt(a);
把命令行字符串转为整数的方法是：int n = Integer.parseInt(args[0]);
接收命令行参数的字符方法是：char ch = args[0].charAt(0);
Main(String[] args)获取命令行的字符串存在args的数组中，args数组中存储字符串，args.length代表字符串数组的长度 。输入时用空格分隔。


while(a)等价于while（a！=0）


switch(表达式)中表达式的返回值必须是下述几种类型之一：byte，short，char，int，String, 枚举；


**Char ch 接收常量不用强转，接收变量要强转
**double d = 111111111111错误，因为常数是int型超范围。改为double d = 111111111111L
**十六进制忠实反应二进制（补码）的值，十六进制没有负数


System.out.println('*' + '\t' +'*');
System.out.println("*" + '\t' +'*');


Int n = 10；  
n = n++;
过程：先把n值取出来放在一边，n自加1，再将原n值赋给n。赋值号优先级低，最后运算；
先用后加，先把值取出备用，最后再用这个值。
++i不用开辟临时空间，效率比i++高；

用最有效率的方法算出2乘以8等於几
答：2 << 3   8<<2


short s1 = 1; s1 = s1 + 1;有什么错? short s1 = 1; s1 += 1;有什么区别；
答：short s1 = 1; s1 = s1 + 1; （s1+1运算结果是int型，需要强制转换类型）
short s1 = 1; s1 += 1;（可以正确编译）

Int i = 10;
i = i++;
System.out.println(i);
输出10.

Int型常量可以赋给short型变量（不超范围）
但是Int型变量不可以赋给short型变量
Return返回值是变量
float型float f=3.4是否正确?
答:不正确。精度不准确,应该用强制类型转换，如下所示：float f=(float)3.4

break语句出现在多层嵌套的语句块中时，可以通过标签指明要终止的是哪一层语句块 
	label1: 	{   ……        
	label2:	         {   ……
	label3:			{   ……
				           break label2;
				           ……
					}
			          }
			 } 





Break 是直接跳出循环和switch。可用标签跳出大括号｛｝
![image.png](https://upload-images.jianshu.io/upload_images/21580557-03a19740095045df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/21580557-62b489050c007186.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




class Demo1{
	//交换两数的不同方法（三种）
	public static void main(String[] args){
		
		int m = 1;
		int n = 9;
		
		//第一种（最常规简单）
	/*	int temp = n;
		n = m;
		m = temp;	*/
		
		//第二种（加减法）
	/*	n = n+m;
		m = n-m;
		n = n-m;	*/
		
		//第三种（异或法）最巧妙
		m = m^n;//m中保存两数差异数
		n = m^n;//差异数与n作异或运算得到m的值赋给n
		m = m^n;//n中保存的m的值，差异数与m作异或运算得到n的值赋给m
				//理解的核心是m^n^m = n;
				
		System.out.println(m+"  "+n);
		
	}

写出结果。(关于参数传递)
public class Test      
{ 
	public static void leftshift(int i, int j)
	{ 
   		i+=j; 
	} 
	public static void main(String args[])
	{ 
		int i = 4, j = 2; 
		leftshift(i, j); 
		System.out.println(i); 
	} 
} 
//4  和leftShift函数没关系。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-198fb979f7134782.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



第三章  面向对象编程

![image.png](https://upload-images.jianshu.io/upload_images/21580557-54b848b4677441e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



构造器最大的用处就是在创建对象时执行初始化，当创建一个对象时，系统会为这个对象的实例进行默认的初始化。如果想改变这种默认的初始化，就可以通过自定义构造器来实现。


静态成员：静态类中的成员加入static修饰符，即是静态成员.可以直接使用"类名.静态成员名"访问此静态成员，因为静态成员存在于内存，非静态成员需要实例化才会分配内存，所以静态成员函数不能访问非静态的成员..因为静态成员存在于内存，所以非静态成员函数可以直接访问类中静态的成员.
非静态成员：所有没有加Static的成员都是非静态成员，当类被实例化之后，可以通过实例化的类名进行访问..非静态成员的生存期决定于该类的生存期..而静态成员则不存在生存期的概念，因为静态成员始终驻留在内存中..
![image.png](https://upload-images.jianshu.io/upload_images/21580557-3e2c645d9d38aa1d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


重复调用同一个方法，各参数在内存上的位置不变。

跨类调用静态方法要加限定。如Another.add


我们也可以不定义对象的句柄，而直接调用这个对象的方法。这样的对象叫做匿名对象。
如：new Person().shout(); 
![image.png](https://upload-images.jianshu.io/upload_images/21580557-f9ab8b5bb028dab9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-6fe7ac2c783184c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



字符串的存储：
1).java编译器在将程序编译成字节码的过程中，对遇到的字符串常量"i love china"首先判断其是否在字节码常量池中存在，不存在创建一份，存在的话则不创建，也就是相等的字符串，只保留一份，通过符号引用可以找到它，这样使得程序中的字符串变量s1和s2都是指向常量池中的同一个字符串常量。在运行时jvm会将字节码常量池中的字符串常量存放在方法区中的通常称之为常量池的位置，并且字符串是以字符数组的形式通过索引来访问的。jvm在运行时将s1与s2指向的字符串相对引用地址指向字符串实际的内存地址。
2).对于String s3 = new String("i love china"),String s4 = new String("i love china"),由字节码可以看出其是调用了new指令，jvm会在运行时创建两个不同的对象，s3与s4指向的是不同的对象地址。所以s3==s4比较的结果为false。
其次，对于s3与s4对象的初始化，从字节码看出是调用对象的init方法并且传递的是常量池中”i love china”的引用，那么创建String对象及初始化究竟干了什么，我们可以查看通过查看String的源码及String对象生成的字节码，以便更好的了解对于new String("i love china")时，在对象内部是做了字符串的拷贝还是直接指向该字符串对应的常量池的地址的引用。
从源码中我们看到String类里有个实例变量 char value[],通过构造方法我们可知，对象在初始化时并没有做拷贝操作，只是将传递进来的字符串对象的地址引用赋给了实例变量value。由此我们可以初步的得出结论：即使使用new String("abc")创建了一个字符串对象时，在内存堆中为该对象分配了空间，但是在堆上并没有存储"abc"本身的任何信息，只是初始化了其内部的实例变量到"abc"字符串的引用。其实这样做也是为了节省内存的存储空间，以及提高程序的性能。


一维数组：int[] x  或者int x[]   
二维数组：int[][] y 或者  int[] y[]  或者 int  y[][]


Package 和import的使用：
将被导入的java文件加上“package 当前路径到目标文件路径”，表示打包到该物理地址。申请导入的java文件加上“import 当前路径到目标文件路径.类名”或“import 当前路径到目标文件路径.*”


排序方法的选择
(1)若n较小(如n≤50)，可采用直接插入或直接选择排序。
     当记录规模较小时，直接插入排序较好；否则因为直接选择移动的记录数少于直接插入，应选直接选择排序为宜。

(2)若文件初始状态基本有序(指正序)，则应选用直接插入、冒泡或随机的快速排序为宜；

(3)若n较大，则应采用时间复杂度为O(nlgn)的排序方法：快速排序、堆排序或归并排序。
java.util.Arrays类包含了用来操作数组（比如排序和搜索）的各种方法。Arrays拥有一组static方法。
操作数组的工具类：Arrays
equals()：比较两个array是否相等。array拥有相同元素个数，且所有对应元素两两相等。
fill()：将值填入array中。 
sort()：用来对array进行排序。 
binarySearch()：在排好序的array中寻找元素。 
         另：System.arraycopy()：array的复制。  



冒泡排序结束条件是某一趟排序未出现交换。
排序法	最差时间分析	平均时间复杂度	稳定度	空间复杂度
冒泡排序	O(n2)	O(n2)	稳定	O(1)
快速排序	O(n2)	O(n*log2n)	不稳定	O(log2n)~O(n)
选择排序	O(n2)	O(n2)	不稳定	O(1)
二叉树排序	O(n2)	O(n*log2n)	不一顶	O(n)
插入排序	O(n2)	O(n2)	稳定	O(1)
堆排序	O(n*log2n)	O(n*log2n)	不稳定	O(1)
希尔排序	O	O	不稳定	O(1)


![image.png](https://upload-images.jianshu.io/upload_images/21580557-99c107e95e4f8afa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




设置好package之后，要在cli编译时加上-d 目标路径。就会在目标路径上创建包。
一般
调用的话先将被调用的java文件编译为class文件在调用。所以两个同路径下的文java件可以互相调用，package到不同包里就不能相互调用。需要在主调用的类前加被掉包的全限定路径或者将包中的class文件导入。
如果用package打包不能直接去包内运行，应该加上全限定路径再运行。因为类名已经改变。


Int[] a = {1,2,3,4};
数组静态方法只适用于声明语句和赋值语句在同一条语句。


因为子类继承父类，会继承到父类中的数据，所以必须要看父类是如何对自己的数据进行初始化的。所以子类在进行对象初始化时，先调用父类的构造函数，这就是子类的实例化过程。若子类构造函数中用this来指定调用子类自己的构造函数，那么被调用的构造函数也一样会访问父类中的构造函数。（每一个子类构造内第一行都有默认的语句super()） 

虚拟机帮助我们构建String[] args = new String[];从命令行过去字符串。


可变参数public static int avg(int...values){}    values是一个int型数组
ave(1,3,5,7)相当于将数组｛1,3,5,7｝给到values数组。
即Avg(int[] values = new int[]{1,3,5,7})
ave()相当于将空数组给到values数组
ave(null)相当于将null给到values.即values=null;
注意：可变参数只能放在最后一个。例：avg(String a，int...values){}


this调用本类的方法：new Person首先是创建对象，对象（）可以重载调用构造器进行初始化，那么构造器中的this（）和super（）也可以解释了调用各自的构造器，还有枚举类中的对象（）也可以解释为调用构造器进行初始化。下图中的this就是为初始化的对象进行赋值过程，this对象也可以调用其方法。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-355dc3d7eef64d82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



多态：编译时能通过就能写，但是运行时会将对象引用给到引用，就按照子类运行。
父类中的方法必须和子类中的方法同返回，不然主类调用时因为返回值类型不同编译错误。

NO.	方法名称	类型	描述
1	public Object()	构造	构造方法
2	public boolean equals(Object obj)	普通	对象比较
3	public int hashCode()	普通	取得Hash码
4	public String toString()	普通	对象打印时调用
public String toString()      两种情况会调用（1）对象打印时调用     （2）String str = “字符串拼接”+ p；效果相当于“字符串拼接”+ p.toString



char ch1 = 'A'; char ch2 = 12;int it = 65;
System.out.println("65和'A'是否相等？" + (it == ch1));   相等
System.out.println(“12和ch2是否相等？" + (12 == ch2));   相等
字符运算时会转化为整数（包括赋值运算和）
整数可以直接转char，整数型变量要强转。

System.out.println("str1是否equals str2？"+(str1.equals(str2)));
String类重写了equals的方法，比较字符串内部。此处为true；

System.out.println(“hello” == new java.sql.Date());  直接报错

![image.png](https://upload-images.jianshu.io/upload_images/21580557-4167d1ec276aac2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


1.回到super多级调用需不需要的问题，子类其实继承的是父类以上辈分的方法，需要用super多级调用来追溯到更“原始”的方法往往是特殊情况,实用性不强。
2.super多级调用使得对象的封装性受到了威胁。


多态：相同类项的变量执行同一个方法时，呈现出不同的行为特征这就是多态。

Java中String类通过new创建和直接赋值字符串的区别
方式一：String a = “aaa” ;
方式二：String b = new String(“aaa”);
两种方式都能创建字符串对象，但方式一要比方式二更优。
因为字符串是保存在常量池中的，而通过new创建的对象会存放在堆内存中。
Person p1 = new Person();
p1.name = "atguigu";
Person p2 = new Person();
p2.name = "atguigu"; 
System.out.println(p1.name .equals( p2.name));		/*对象中的name属性指向常量池中的
System.out.println(p1.name == p2.name);   		字符串。所以字符串的引用一样。
System.out.println(p1.name == "atguigu");		
	
String s1 = new String("bcde");		/*s1，s2指向的是GC区中String对象的引用，对象
String s2 = new String("bcde");		中的value属性指向常量池的字符。所以对象的引用
System.out.println(s1==s2);			不同，属性的值相同


public boolean equals(Object obj) 和 ==   的区别：
equals的话，它是属于java.lang.Object类里面的方法，如果该方法没有被重写过默认也是==;我们可以看到String等类的equals方法是被重写过的，而且String类在日常开发中用的比较多，久而久之，形成了equals是比较值的错误观点。

String name = new String(字符串常量);或String name = 字符串常量;
New String会创建String类型的对象，对象中有char数组存放字符串，也有各种方法，当对象调用equals方法时，String中的equals方法会重写继承的equals方法，如果引用地址不相同，则会比较字符串内容是否相同。String中把toString也改写了，返回的是引用，读取引用会读出其所指向的字符串。而一般其他类型会调用继承的toString方法读取全限定类名@哈希地址值。
public class final String{
    public String toString() {   //重写了toString方法
        return this;
}}

	ch = str.toCharArray();		//将字符串转化为数组
	str = String.valueOf(ch);	//将数组转化为字符串




private final char value[];
private int hash; // Default to 0
  public String(String original) {//我们通过new String("abc");把值放入value[]
    this.value = original.value;
    this.hash = original.hash;
  }
理解：value[]是类属性，每次创建字符串都会new一个对象将初始化的字符值存于value中。
”abc”在常量池中创建”对象”,并给value字符数组属性赋初值abc，并返回一个引用到栈中。创建String时将引用给到构造函数，将栈中引用指向的对象中的value中的值给新对象的value属性初始化，完成赋值。字符数组是String类对象的属性。” ”就是一个字符串对象。””.value就是字符串对象中的字符数组属性的引用。
字符串对象由hash值（默认为0）和字符数组value[]还有版本值组成。
字符型由许多常量属性和方法组成。
char v1[] = value;    //字符串中的value引用可以直接给char型引用。


Character型的变量输出：整数转换成字符输出需要调用char类中的方法将数值型的转换成字符输出，而整数型变量则需要造型为character型的才能调用char类中的方法来输出？？？所以需要强转为char型变量。

API（application programming interface）是预先定义的函数，使得虚拟机可以和本地进行交互。包括调用本地的其他语言程序和应用，用native修饰。会影响java的可移植性。



在声明时已经确定了引用的类型，包括其中的属性和方法。如果给其赋不同类型的引用会造成错乱，编译器会报错（父子类会产生多态，编译不会报错，调用虚拟方法Virtual Method Invocation）。
例1：int[][] x = new int[5][];
	int[] y = new int[5];
	x = y;               //报错因为二维数组和一维数组对象引用不同类
例2：char类和String类不能相互赋值，类的对象不同。


char[] ch = new char[] {'a','b','c'};
	String str = "abc";
	System.out.println(ch);					//abc
	System.out.println(ch.toString());		//[C@15db9742
	System.out.println(str);					//abc
	System.out.println(str.toString());		//abc


toString() 方法：
1.  System.out.println(b);
相当于System.out.println(b.toString());

2.		System.out.println(“now=”+now);  
相当于System.out.println(“now=”+now.toString());


java抽象类中可以定义静态的抽象方法吗？
抽象类一定有抽象方法吗？我来说说吧，静态是属于字节码的；一个抽象类可以没有抽象方法，只是为了不让别人来实例化它； 以上两点可以说明，静态方法只要有字节码存在就可以运行，所以抽象类中可以有静态方法。 我再多说一嘴，静态和抽象不能共存与方法上，因为静态属于字节码，不需要对象就可以运行，而抽象方法没有方法体，运行没有意义，所以不能共存。

执行顺序：
静态代码块和类一起加载，所以最先执行并只执行一次。
非静态代码块是包含在构造器中的，但是在父类构造器之后，构造器方法体之前，按顺序执行（包括声明后跟的显示赋值。


public class Something { 
public int addOne(final int x) { 
return ++x;     //出错，因为传入的形参是final型的，不能改变。注意传入的是复制品，与原引用无关
}  } 

final可以在方法中定义，会在常量池创造一个副本，栈中的值出栈后常量池中的会一直保留。但是static是在类加载时执行的，所以方法中定义static没意义，会报错。

构造器不能用final修饰，因为修饰之后不能继承？？


因为接口中的方法都是抽象方法，不会产生冲突。


当print输出任意类（Object）时，会调用对象的toString方法，toString方法得到的字符串就是打印结果。当print输出字符串（字符串其实时String类的对象）或基本数据类型时，会调用对象的继承自String类或基本数据类中的toString方法（重写了Object中的toString方法），因此会打印引用所指向的字符串，字符或数值。其它类型的引用则需人为改写toString方法，否则会输出全限定类名@地址哈希码。


当println(Object x)时（字符串和基本数据类型除外），会调用对象的toString方法，toString方法得到字符串（若没有重写toString方法，会得到全限定类名@地址哈希码的字符串），最后println(Object x)方法中会调用print(s)，将字符串s输出（字符串其实时String类的对象）。若是字符串和基本数据类型则会调用对应的方法输出数值的字符串。总结：字符串和基本数据类型会输出数值对应的字符串。其他引用会输出全限定类名@地址哈希码的字符串，若重写，则输出重写后的字符串。


内部类可以方便的访问外部类，比对象关联更方便的是可以访问外部类的私有成员。常用于监听器？？？ 


枚举类的主要方法：
values()方法：返回枚举类型的对象数组。该方法可以很方便地遍历所有的枚举值。
valueOf(String str)：可以把一个字符串转为对应的枚举类对象。要求字符串必须是枚举类对象的“名字”。如不是，会有运行时异常。

枚举类：枚举类编译时会根据给出的枚举项创建公共静态常量对象和数组（创建的对象默认提供同名字和顺序下标，默认父类构造器包括名字和下标），将创建的对象都放到数组中。调用静态values（）方法会返回复制的数组，调用静态方法valueof（）可以返回输入名字对应的对象的引用。

@Override: 限定重写父类方法, 该注释只能用于方法
@Deprecated: 用于表示某个程序元素(类, 方法等)已过时
@SuppressWarnings: 抑制编译器警告
@interface MyAnnotation{
String name() default “atguigu";     //即name的缺省值为default后的值。
        }
@Retention: 只能用于修饰一个 Annotation 定义, 用于指定该 Annotation 可以保留多长时间（用与限定注解的保留时间。@Retention(RetentionPolicy.SOURCE，RetentionPolicy.CLASS，RetentionPolicy.RUNTIME）
@Target: 用于修饰 Annotation 定义, 用于指定被修饰的 Annotation 能用于修饰哪些程序元素。@Target:({ElementType.TYPE,ElementType.FIELD,ElementType.METHOD,ElementType.PARAMETER,ElementType.CONSTRUCTOR,ElementType.LOCAL_VARIABLE,ElementType.ANNOTATION_TYPE,ElementType.PACKAGE,ElementType.TYPE_PARAMETER,ElementType.TYPE_USE})


Finally语言一定会执行，一般用来释放资源（包括和OS交互占用的内存，打开应用程序）。前句有return，会将return值放到临时空间，再执行finally语句，若finally语句中还有return，会将返回值放到临时空间中取代原值。待方法出栈后再将临时空间的值返回。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-1303e460c1a10373.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


Integer j2 = Integer.decode(str2);用Integer的静态方法decode（）将字符串转化为Integer包装型。
Byte,Short,Long,Character,Float,Double，Boolean同理。
自动装箱，自动拆箱，类型必须匹配
Float f = Float.parseFloat(“12.1”);

String fstr = String.valueOf(2.34f);
String intStr = 5 + “”

装箱：Integer obj1 = new Integer（100）;//手动装箱
      Integer obj2 = 100;//自动装箱
拆箱：int n1 = obj1.intValue();//手动拆箱取出包装型中的值
      int n2 = obj2;//自动拆箱
自动装箱调用函数Integer.valueOf(100)得到int包装型。
Integer j2 = Integer.decode(str2);用Integer的静态方法decode（）将字符串转化为Integer包装型。
String s1 = Integer.toString(314);//将int型转为字符型
int n = Integer.parseInt(str);//将字符串转为int型
包装类在实际开发中用的最多的在于字符串变为基本数据类型。
String类的public String valueOf(int n)可将int型转换为字符串。



String str  = “abc”;与String str1 = new String(“abc”);的区别？??
“abc”在字符串常量池（且常量池中不会出现一样的字符串），new出来的在GC区中。

String str = "atguigu";  str = str + "java";str最终会存在堆中。
“atguigu” + “java” = “atguigujava”最终存在字符串常量池中。


str.indexOf(key)返回key与str的第一次相同处的脚标。若没有相似，返回-1。
str.subString(int beginIndex, int endIndex)beginindex为起始脚标，endindex为结束脚标（不包括此脚标）。
public boolean contains(CharSequence s)对象含有s数组，则返回true，否则为false。

Integer.valueOf()如果范围在-128~127之间，会直接取系统已经创建的对象，节省时间。如果超出范围，会创建新的对象。
（s1+s2）会在GC区，（s1+s2）intern（）会将其放到常量区，如有会返回已有字符串地址。


为什么引用+字符串存在GC区，字符串+字符串存在常量池？


为什么StringBuilder创建新数组直接赋值给原数组？答：若扩容，则会将新的value给到旧的value，不需要对字符串引用进行操作，在方法中自动将value属性改变了，所以value不能用final修饰。



因为String中的value是private和final修饰的，只能在类中访问，所以不能被外部修改。StringBuilder的value只被default修饰，所以可以被同一包内的访问。正常来说String和StringBuilder的value不能被访问，一个是private，一个在lang包内。

String中属性value指向常量池还是GC区？StringBuilder呢？
new String(String origine)时，新对象的value会指向origine的value。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-a56a97e3fb470ead.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果形参是字符串常量：1.new的时候根据该字符串常量参数参数会在常量池创建一个字符串对象，value指向常量池的字符数组2.以该字符串为形参new字符串对象时，将对象value属性指向常量池的字符数组。就是说常量池的字符串对象和GC区的字符串对象指向同一个常量池的字符数组。

String str = “abc”，str也能调用String的方法，说明str也是String类的引用。但是String的value是私有的常量，一般访问不到。

String string = null;
StringBuilder str = new StringBuilder("ab");
System.out.println(string);
System.out.println(str.append(string));
第一个输出null。会直接调方法将空指针指向“null”字符串，结果输出null字符串；
![image.png](https://upload-images.jianshu.io/upload_images/21580557-c2e943372c5d0a61.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

第二个输出“abnull”，会在原数组的基础上加字符‘n’‘u’‘l’‘l’。
如果以String string = null；作为参数new 字符串对象会报错，因为String会调用string.value属性，StringBuilder会调用string.length，都会有空指针异常。

每次改变StringBuilder字符串，都会调用 ensureCapacityInternal，确保长度够大。

执行append方法时StringBuffer在方法前加了一个synchronized修饰，起到同步的作用，可以在多线程环境使用。为此付出的代价就是降低了执行效率。因此，如果在多线程环境可以使用StringBuffer进行字符串连接操作，单线程环境使用StringBuilder，它的效率更高。

System.arraycopy(Object src,int srcPos,Object dest,int destPos,int length)
System.arrayCopy( arr1, 2, arr2, 5, 10);
将arr1数组里从索引为2的元素开始, 复制到数组arr2里的索引为5的位置, 复制的元素个数为10个. 

StringBuffer还有一个直接设置count大小的函数setLength：如果newLength大于count，那么就会在后面添加'\0'补充；如果小于count，就直接使count=newLength。会输出length长度的字符数组，不够用'\0'补齐。


日期类：
1.System类提供的public static long currentTimeMillis() 用来返回当前时间与1970年1月1日0时0分0秒之间以毫秒为单位的时间差。
2.Date( )使用Date类的无参数构造方法创建的对象可以获取本地当前时间。
Date date = new Date();
3.Calendar calendar = Calendar.getInstance();调用getInstance内置工厂方法来获取对象。
SimpleDateFormat d = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
d.format(上述两个对象)用于格式化上述的时间。可以格式化毫秒，相对于1970-1-1来说。.parse方法可以将字符串转化为Date对象。
4.最新的时间类LocalDateTime ldt = LocalDateTime.now();
其格式化器DateTimeFormatter f = DateTimeFormatter.ofPattern("yyyy-MM-dd HH-mm-ss");


//任意一个人输入年龄，就可以判断出他是哪个年龄段的人？
3.数据结构的思想
int age = 22;
String[] arr = {"儿童","少年","青少年","青年","壮年","中年","","","",""};
int id = age/10;
System.out.println(arr[id]);


throw：生成一个异常对象，并抛出。使用在方法内部<->自动抛出异常对象。
throws：异常的处理方式，处理异常的方式，使用在方法声明处的末尾<->try-catch-finally
受检异常一定要写明异常处理方式，即签名跟throws，但抛非受检异常（RunTimeException）可以省略。

同步监视器和共享数据：
同步监视器俗称锁。1.任何一个类的对象都可以充当锁。2.多个线程公用一把锁。
共享数据：多个线程共同操作数据，即为共享数据。需要使用同步机制将操作共享数据的代码包起来，不能包多了，也不能包少了。




多线程：

程序(program)是为完成特定任务、用某种语言编写的一组指令的集合。即指一段静态的代码，静态对象。
进程(process)是程序的一次执行过程，或是正在运行的一个程序。是一个动态的过程：有它自身的产生、存在和消亡的过程。——生命周期。进程作为资源分配的单位，系统在运行时会为每个进程分配不同的内存区域
线程(thread)，进程可进一步细化为线程，是一个程序内部的一条执行路径。线程作为调度和执行的单位，每个线程拥有独立的运行栈和程序计数器(pc)。


新建类继承Thread类，重写run（）方法，new类对象，调用start（）方法。
start（）方法两个作用1.启动一个新线程2.执行run（）方法
但是一个对象的start（）只能执行一次。

Setname是静态么？为什么可以用currentThread调用，也可以对象调用。
重写Run方法中不能抛异常，因为父类没抛异常。

System.out.println(Thread.currentThread().getName() + " " + num++); 此处直接写getName也可以，就是this调用getName方法，但是Thread.currentThread()是什么，写的是本地的文件，为什么能调用getName（）方法，和this什么区别？？？？？static Thread currentThread(): 返回当前线程。在Thread子类中就是this，通常用于主线程和Runnable实现类。因为Runnable实现类一般只有run方法，没有其他属性和方法。


Join怎么在别的线程里调用其他线程的join？？？在主线程中调用分线程的join方法。

实现runnable方式优于继承Thread类
区别：1.java类的单继承性的局限性2.实现Runnable接口的方式更适合多线程有共享数据的方式
共同点：Thread也实现了Runable接口，可以将实现Runnable看作是代理模式。实现Runnable的类是被代理类，Thread是代理类，Runnable是接口。为了执行实现Runnable类的方法，通过new Thread的对象来调用Thread中的方法,若传入了target对象，使target不为null，则调用实现类中的方法。

继承Thread类就是写Thread的子类，然后重写run方法。new子类并调用其中继承与父类的start方法，start方法开启新线程并执行run方法。
实现Runnable类就是Thread和实现类都实现了Runnale接口（只有一个run方法）中的run方法，new实现类的对象target。通过new Thread将实现类的引用target作为参数给到new的对象，将target赋给Thread中的Runnable型属性，该对象调用其类中的start方法建立新线程，并调用run方法，判断参数target是否是null，不是null则调用target中的run方法，在新线程中运行重写后的run方法。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-00f729be7b57813b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Thread关联了实现类，可以通过Thread类代理进行实现类的run方法。返回值可通过FutureTask的get（）方法获得。注意：一个FutureTask对象只能被执行一次，每个FutureTask对象包含一个返回值。

几个线程就要写几个Tread继承类，分布start开启线程，所以不能用对象（this）作为同步锁（不唯一），用类的反射对象作为同步锁。
而实现Runnable方法只需要一个实现类，给多个Thread类作参数，开启多线程是共用一个run方法，所以可以用this（即实现类的对象）作为同步锁。

有三种解决线程安全问题：
1.同步代码块 2.同步方法 3.jdk 5.0新增：Lock锁。
1.synchronized(同步监视器){
             //需要被同步的代码
}
同步监视器俗称锁。要求：1.任何类的对象都可以充当同步监视器。2.多个线程必须公用同一个同步监视器。注意：1.使用同步代码块接口runnable实现解决同步问题，可以考虑使用this  2.使用同步代码块继承extends时慎用this，用类名.class

2.同步方法部分的同步监视器隐藏了，默认是this，要注意this是否唯一。当用同步方法时同步监视器默认是this，但是造成this不唯一。可以用静态方法，同步监视器是类本身，唯一。
静态方法：同步监视器是类本身。
非静态方法：同步监视器是this。

3.Lock锁
private ReentrantLock lock = New ReentrantLock();
try{
lock.lock();
}finally{
Lock.unlock();
}
一般统一将调用的lock方法放在try内,跟上代码块，跟上finally语句执行unlock方法，保证即使出意外也一定会释放锁。
Lock锁和synchronized区别： 
Synchronized涉及同步监视器，多个线程公用唯一的同步监视器。出括号后会自动释放同步监视器。
Lock锁：提供具体的Lock锁的实现类对象。此对象唯一，多个线程共享。必须手动调用unlock释放锁。


1.wait() 、notify()、notifyAll()三个方法的调用者是同步监视器，如果不是会报异常。（如果同步监视器不是this，则在三个方法前面加上同步监视器，如果不加默认为this，会报错）
2.wait() 、notify()、notifyAll()三个方法只能用于同步代码块或同步方法中。不能用于Lock锁中。
3.wait() 、notify()、notifyAll()三个方法定义在Object中，会被继承。！！！



相较于Runnable创建多线程的方式，Callable方式更灵活  1.call（）方法可以声明返回值   2.call（）方法是可以使用throws的方式处理。 3.可以使用泛型指定call（）返回值类型。
Callable多线程的执行，需要借助FutureTask类（FutureTask是Future类的唯一实现类，且FutureTask是Runnable的唯一实现类），FutureTask实现了Runnable接口，然后再用Thread类。
底层实现：Thread对象调用start方法，start方法建立新线程并调用run方法，run方法判断target是否为null，因为构造Thread对象时调用的传入target构造器，所以target不为null，则调用target对象（即图中f）的run方法，FutureTask的run方法会调用r的call方法，最终实现call方法。（FutureTask类中关联了Callable属性，构造FutureTask对象时调用了传入Callable对象的构造器）。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-ee62b67408a3b78c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以用Callable取代Runable；
接收Callable返回值用get

Sleep（）和wait（）异同点：
同：都可以使当前进程进入阻塞状态。
异：施放锁，方法所在类，自动唤醒，使用场景，
1.定义方法所属sleep（）：Thread类中静态方法；wait（）：object中的非静态方法
2.适用范围：sleep任何位置，wait在同步内。
3.在同步代码块或同步方法中wait施放锁，sleep不施放锁。
4.结束阻塞时机不同，wait需要被其他线程唤醒。

Sleep（）和wait（）源码中抛出了InterruptedException异常，所以用的时候要进行处理。



集合
（ArrayList线程不安全Vector安全）要求：向Collection添加对象时必须重写equals方法。
Collection（）的方法:
1.add（Object obj）将元素加入到当前集合中，返回boolean值
2.add（Collection coll）将集合中的元素加入到当前集合中，返回boolean值
3.size（Collection coll）获取集合中元素个数
4.isEmpty（Collection coll）判断集合是否为空，返回boolean数
5.clear(Collection coll):清空当前集合
6.remove（Object obj）移除并返回boolean数。找到并删除第一个就停止。remove是按照equals方法是否返回true来判断是否相等并删除。
7.removeAll（Collection coll）coll中的每个元素都会调用equals方法判断是否删除。返回boolean值

8.contains（Object obj）判断当前集合中是否包含obj元素，返回boolean值
9.containsAll（Collection coll）：判断当前集合中是否包含coll集合中的所有元素，返回boolean值
10.retainAll（Collection coll）：或取当前集合和coll集合的交集，并返回给当前集合。
11.equals（Collection coll）判断当前集合和obj是否相同，需要保证顺序相同。
12.hashCode（）获取当前集合的哈希值。
13.Object array = coll.toArray（） 将当前集合转化为数组。
List list = Arrays.asList(123,456,789）；//将数组转化为List集合
asList（）只能识别类中的元素，如果是int型的数组名，只识别一个，输出为类名@哈希值
14.iterator用于遍历集合元素。
Iterator iterator = coll.iterator；(Iterator是接口，collection和List实现了iterator)
遍历方式：while(iterator.hasNext()){
              System.out.println(iterator.next());}
hasNext（）方法，判断是否有下一个元素。
next（）方法1.指针下移（最开始在-1处）2.读取元素
增强for循环遍历集合会调用迭代器。

Interator实现：Iterator是ArrayList类中的内部类，调用iterator（工厂方法）创建内部类对象，对象调用hasNext方法时，判断指针是否等于size，等于则false。调用next方法时，将外部类中的元素数组复制然后遍历。调用remove时，将指针作为参数，直接调用外部类的remove方法删除指针所指的元素。（不能进行连续的remove方法，应该穿插next（）方法）


remove()参数是int型时会有remove(int index)和remove(Object obj)方法歧义，优先调用remove(int index)

List在Collection之外的方法：
1.void add(int index, Object ele):在index位置插入ele元素
2.boolean addAll(int index, Collection eles):从index位置开始将eles中的所有元素添加进来
3.Object get(int index):获取指定index位置的元素
4.int indexOf(Object obj):返回obj在集合中首次出现的位置
5.int lastIndexOf(Object obj):返回obj在当前集合中末次出现的位置
6.Object remove(int index):移除指定index位置的元素，并返回此元素
7.Object set(int index, Object ele):设置指定index位置的元素为ele
8.List subList(int fromIndex, int toIndex):返回从fromIndex到toIndex位置的左闭右开区间的子集合
9.List subList(int fromIndex,int length);


List<String> list = Arrays.asList(new String[]{“AA”,“BB”,“CC”}
System.out.println(list);//输出[AA,BB,CC]

List<int[]> arr1 = Arrays.asList(new int[]{123,456});
System.out.println(arr1);//输出数组引用的类名@哈希值，只能识别int[]类对象。int[]型数组存
System.out.println(arr1.size());//输出size为1        //储的基本类型变量不是类，无法识别

List arr2 = Arrays.asList(new Integer[]{123,456});
System.out.println(arr2);//输出[123,456],包装类能识别为俩元素
System.out.println(arr2.size());输出size为2

List arr3 = Arrays.asList(123,456);
System.out.println(arr3);//输出[123,456]
System.out.println(arr3.size());输出size为2



 *   总结：
 *   增：add(Object obj)
 *   删：remove(Object obj) / remove(int index)
 *   改：set(int index, Object ele)
 *   查：get(int index)
 *   插：add(int index, Object ele)
 *   长度：size()
 *   遍历：iterator() / 增强for / 普通for

ArrayList（）在java7.0中会构造对象，若不传参，会直接构造大小为10的Objection数组，饿汉式。在8.0中是懒汉式，不传参构造长度为零的数组，传参才扩容为10（不够大则直接扩容为需要的大小）。之后每次扩容为1.5倍（不够大则直接扩容为需要的大小）。
LinkedList（）是双向链表结构。
Vector（）若不传参，会直接构造大小为10的Objection数组。每次扩容为原长度两倍（不够大则直接扩容为需要的大小）。

LinkedList底层实现原理：调用addFirst或addLast时，会调用linkFirst和linkLast方法，将传入的对象作为的元素新建节点对象，并将前后指针指向前后节点。

HashSet底层实现原理：
Set set = new HashSet（）会构造一个大小16的数组，会在数组利用率到达75%时扩容。添加元素a时，先计算a的哈希值1，此哈希值经过某种算法后的得到哈希值2，此哈希值2经过某种算法后得到在数组中的索引位置i，（1）如果此索引位置i上没有元素，元素a添加成功。（2）此位置上有元素b，此时比较元素a和元素b的哈希值2，如果哈希值不同，此时元素a添加成功。如果哈希值相同，此时调用元素a所在类的equals方法，返回值true，则元素添加失败。返回值false，则元素添加成功。（以链表形式添加，java7中新加的在前，java8中新的在后。）
HashSet没有额外添加方法，用的Collection中的方法。
HashSet无序不同于随机，遍历有固定顺序，但和添加顺序无关。但是LinkHashSet遍历顺序和添加顺序一致。无序指的是内存上排序无序。
HashSet添加数据会涉及到HashCode和equals方法判断是否重复。需要重写这两个方法，重写的hashCode和equals方法要保证一致性。而List中添加对象重写equals就行了。
如果两个对象重复，则其hashCode一致，则放到链表中通过equals判断。如果两对象不重复，则其hashCode可能相同，放到链表中通过equals判断。所以HashSet中的数一定不会重复，且比较效率高。hashCode和equals一致性就是尽量使equals不同时hashCode值也不同，使元素在散列表上均匀分布。

TreeSet（）加入对象必须要同类型的，不然会报ClassCastException。底层是红黑树实现，
排序方式1.自然排序：要求元素所在类实现Comparable接口，并实现compareTo（Object obj）。添加对象会调用对象的CompareTo方法比较大小，如果比较元素一样大（compareTo返回值为0），则添加失败。可以不用重写hashCode（）和equals（）方法。

3.定制排序：要求提供Comparable接口实现类，并实现compare（Object obj1，Object obj2）；

如果在使用Arrays.sort(数组)或Collections.sort(Collection集合)方法时，TreeSet和TreeMap时元素默认按照Comparable比较规则排序；也可以单独为Arrays.sort(数组)或Collections.sort(Collection集合)方法时，TreeSet和TreeMap指定Comparator定制比较器对象。



Map：
存储特点：
键值对构成一个Map.Entry，不可重复无序，set存储；
键是无序不可重复的，使用Set存储----key所在类重写hashCode（）和equals（）方法
值是无序可重复的，使用Collection存储---value所在类equals重写
框架：
HashMap：Map的主要实现类：线程不安全，效率高；可以存储null的key和value
LinkedHashMap：HashMap的子类，可以按照添加的元素的先后顺序实现遍历。（使用了双向链表记录）
TreeMap：可以按照添加的元素的指定属性进行排序。
Hashtable：Map的古老实现类；线程安全，效率低；不可以存储null的key和value
Properties：是Hashtable的子类，key和value都是String类型的，常用来处理
HashMap的底层实现原理：
（jdk7）数组+链表：向HsahMap中添加key1-value1.首先调用key1所在类（只比较key的哈希值）的hashCode方法计算哈希值1，使用某种算法得到哈希值2，哈希值2通过某种算法得到其key1-value1在底层table[]中的索引位置：i；（1）如果table[i] == null；则此entry（key1-value1）添加成功。（2）table[i]中存在其他entry，则比较key1和key2的哈希值2，如果哈希值2彼此不同：则entry添加成功（链表形式）；如果和链表上的某一个entry的哈希值2相同，则继续比较二者的equals方法，若equals返回true：使用value1替换相同的哈希值的key的value。如果返回false，继续与该链表上的entry比较。如果都不相同，添加成功。
情况一：将entry添加到数组中
情况二和三：将entry与以后的entry以链表的形式进行存储。
扩容问题：
默认情况下：（new HashMap（））长度为16
当达到临界值（=数组长度*加载因子（默认的加载因子：0.75）时，就考虑扩容，元素个数超过临界就扩容，为原长度两倍。
查询：用key查询value，计算key的哈希值找到数组位置，然后用哈希值对比链表中的entry的key的哈希值，若相同则比较equals，若equals返回ture，则查询方法返回value，若equals返回false，则查询方法返回null；

用put添加entry（key，value）

（jdk8）数组+链表+红黑树（与7的不同点）：
1.new HashMap（）：底层没有创建长度为16的数组
2.当首次调用put（）方法时添加元素时，才在底层创建长度为16的数组。
3.新添加的元素与已有元素以链表形式存储，则旧元素指向新元素。
4.当某索引i的位置上的链表的长度>8且数组长度大于64时，此索引的链表改为红黑树形式存储。


LinkedHashMap：new LinkedHashMap时会调用父类构造器（即HashMap），添加对象put方法也是继承与HashMap，put方法添加对象时会调用newNode方法产生Node类的对象给数组，LinkedHashMap重写了该方法，调用newNode方法会产生Entry类（继承了Node类，新增了before和after属性）的对象给数组，before和after 属性记录了前一个和后一个添加的对象。因此遍历LinkedHashMap会按添加顺序输出。
HashSet底层实现：new HashSet实际new了一个HashMap，当add（e）时，会调用HashMap中的put（K key，V value）方法，key就是加入的对象e，value的值是静态方法中的属性（用new Object（）赋值），即所有e对应一个相同的Object对象。

LinkedHashSet继承自HashMap，构造LinkedHashSet时会调用父类构造器，即new了一个HashMap，添加对象add方法也是继承于父类，调用add方法就会调用HashMap的put方法，调用newNode时会产生Node类对象给数组，但是LinkedHashSet也重写了该方法，调用newNode方法时会产生带首尾指针的节点指向加入的前后对象，因此遍历LinkedHashSet时也可以按添加顺序输出。

当HashMap中的其中一个链的对象个数如果达到了8个，此时如果capacity没有达到64，那么HashMap会先扩容解决，如果已经达到了64，那么这个链会变成树，结点类型由Node变成TreeNode类型。当然，如果当映射关系被移除后，下次resize方法（resize方法用于扩容）时判断树的结点个数低于6个，也会把树再转为链表。

遍历方法1.迭代器2.foreach3.普通for4.直接输出集合引用。底层都要用到迭代器，数组或集合不能是null，会报空指针异常（null.iterator（））。

Map和List重点掌握，Set主要用来过滤数据。

实现排序的方法1.自然排序Comparable  2.定制排序Comparator  3.Arrays.sort;
Arrays.sort(pers,comparator)比较大小不会像TreeSet一样相同的元素（返回值为0）会添加失败，sort排序会保留相同的元素。要排序可重复元素用sort而不是用TreeSet。

增：put（Object obj,Object value）
删：Object remove(Object key)
改：put（Object key,Object value）必须添加if判断id是否存在，防止没有id而添加了此键值对！
     replace（Object key,Object value）
查:Object get(Object key)
长度：size()
遍历：keySet()/values/entrySet()

Set keys = map.keySet();
Collection values = map.values();
Set mappings = map.entrySet();
value v = map.get(key);
Key k = entry.getKey()
value v = entry.getValue()	


Set keys = map.keySet();
Collection values = map.values();
Set mappings = map.entrySet();
value v = map.get(key);
Key k = entry.getKey()
value v = entry.getValue()

Map中获得的value对象是HashMap的内部类的对象(无序可重复)，继承自AbstractCollection，所以不属于List的实现类。


SynchronizedList用法：List synchronizedList = Collections.synchronizedList(list)
synchronizedList方法返回了new synchronizedList对象，内部关联了List，并将参数list赋值，对synchronized操作会调用其类中方法，方法会调用list的方法，但是外部用synchronized包裹实现线程的同步安全。简而言之将返回的synchronizedList对象的方法是将List的方法包裹了synchronized，实现线程安全。

泛型：
在声明类的时候声明泛型的类（可以多个参数），那么下面的方法根据泛型规定了其参数或返回值的类型

父类是泛型，则子类继承的方法和属性也是泛型

调用泛型方法时，指明方法中的参数，与泛型类中的泛型无关。

泛型如果不指定，将被擦除，泛型对应的类型均按照Object处理，但不等价于Object。

异常类不能是泛型的

泛型在继承上的体现：
1.A类是B类的父类，G是具有泛型声明的类或接口，则G<A>与G<B>没有子父类关系
2.A类是B类的父类，则A<G>与B<G>是子父类关系。
因此说泛型Object和省略Object是不同的。
尽管在编译时ArrayList<String>和ArrayList<Integer>是两种类型，但是，在运行时只有一个ArrayList被加载到JVM中。

通配符：A类是B类的父类，则G<A>与G<B>没有子父类关系，他们的共同父类是G<?> 。G<?>类型的只能写入null；可以读取，只能用Object类型的接收。

Java泛型可以保证如果程序在编译时没有发出警告，运行时就不会产生ClassCastException异常。同时，代码更加简洁、健壮。体会：使用泛型的主要优点是能够在编译时而不是在运行时检测错误。

不能使用new E[]。但是可以：E[] elements = (E[])new Object[capacity];
      参考：ArrayList源码中声明：Object[] elementData，而非泛型参数类型数组。？？？？？？？


将G<A>赋值给G<？>，因为不确定A的大小，所以不能给G赋值，只能赋null。G<A>赋值给G<? extends A>,也不能给G赋值；G<A>赋值给G<? super A>，可以给G赋值A或A的子类，因为确定G是A的父类类型，所以可以赋其子类。

不能写一个用到类泛型的静态方法，因为静态方法加载早于类实例化（给泛型赋值晚于静态方法加载）。
泛型方法可以是静态或非静态的。

接口中可以定义默认方法（不是抽象方法，有方法体），用default修饰，不会默认为abstract，而是实体方法，权限还是public（正常接口中的属性都是public static final修饰，方法都是public abstract修饰），java9中新增了私有化的默认方法，接口与抽象类靠拢。




IO流

windows和DOS系统默认使用“\”来表示
UNIX和URL使用“/”来表示
Java中的反斜杠都用\\表示，第一个是转义字符，编译时。

如果不存在该文件，则没有读入内存的文件，length为0，修改时间为0ms。
如果是文件目录的对象，length为0。
相对路径写的文件直接调parent方法拿不到上级文件目录，可以先获取全路径getAbsoluteFile，再调parent方法。

flush（）方法将内存中buffer的内容清空，并将内存中的内容输出，如果不主动调用，会在buffer满时自动输出或者在close（）时输出。

Unicode是内存中的编码，没有标识位，两位代表一个数。Utf-8或GBM是存储和读取的编码，根据内存中的unicode码加上标识位存储在内存中（可以根据unicode码的大小合理分配空间）。
某种编码存储的文件必须用某种编码读入，否则unicode码出错；同样读出什么编码格式，也用什么格式打印，因为存储格式不同，不同格式读取会导致乱码。
GBK对用的编码是根据操作系统决定的。

BufferedReader有特有的方法readLine（），可以读一整行并返回String型。用write（String s）方法写出。

RandomAccessFile实现在某一位置插入几个字符。

ObjectOutputStream和ObjectInputStream不能序列化static和transient修饰的成员变量。

序列化的意义：通过存到硬盘或网络传输类的对象，对方接收后需要还原类并放入内存，但是不同包下有同名的类，这时需要序列号来找到对应的类。实现Serializable接口后会提供默认的序列号，最好自己在写死一个序列号，因为每个类最好都有final型的不同的序列号，以防类属性改变后序列号也改变。

字符流只能传输纯文本。
为什么非文本不能用字符流传。？？

只有转化流会涉及编码解码，节点流只是复制。
输出流和打印流关系？输出到显示器，在调用打印。

getByAddress（）方法怎么用？？？
不主动序列化的影响？？？
如何理解面向对象编程和万事万物皆对象？？？
Java是面向对象的编程语言1.类与对象：Date，String，File，InetAddress，URL   。加载到内存中的类本身也是类的对象2.   java语言与前端---后台---数据库交互都是用对象来操作的

类的封装性描述的是类及类的内部结构被调用时的可见性大小。体现的是：是否建议用户调用
Java的反射机制：描述的是类在被加载以后，是否可以调用的问题。体现的是那些结构被加载在了内存中。


System.out.println(url.getQuery());
获取用户名和密码


三种获取类对象的方式：
1.类名.class
2.类对象.getClass();
3.Class.forName(“全限定类名”);
4.使用类的加载器（了解）：getClassLoader（）.loadClass(“全限定类名”)

基本数据类型也有类名
数组中的元素和纬度一样，则是同一个类。



新特性
接口中可以定义静态方法和默认方法：静态方法只能由接口自己调用，默认方法可以由实现类对象调用

Lambda表达式使用：
1.举例：（o1,o2） -> Integer.compare(o1,o2);
2.格式：
        ->左边为参数
        ->右边为方法体

3.总结：lambda形参列表的数据类型可以省略，如果形参只有一个，可以省略括号
         Lambda体如果只有一行执行语句，则省略一对大括号以及return关键字

4.说明Lambda表达式是作为接口的匿名实现类的对象出现的。

4.如果一个接口中之声明了唯一一个抽象方法，则次接口称为函数式接口
可以使用@FunctionalInterface检验一个接口是否为函数式接口

如果lambda有多条语句，则不能用方法引用



反射的目的就是为了扩展未知的应用。比如你写了一个程序，这个程序定义了一些接口，只要实现了这些接口的dll都可以作为插件来插入到这个程序中。那么怎么实现呢？就可以通过反射来实现。就是把dll加载进内存，然后通过反射的方式来调用dll中的方法。




