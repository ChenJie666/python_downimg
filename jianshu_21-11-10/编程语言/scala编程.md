>1. 伴生对象中可以写静态方法，但是底层并不是通过静态方法实现的。而是通过饿汉模式创建单例，通过这个单例对象进行方法的调用，实现了静态方法的功能。
>2. 只有伴生类，那么编译之后只会生成一个编译文件。只有伴生对象，那么编译之后会同时生成两个编译文件。

![伴生类编译文件](https://upload-images.jianshu.io/upload_images/21580557-3ff23c2f443d72ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![伴生对象编译文件](https://upload-images.jianshu.io/upload_images/21580557-3edf94f6ac9ba107.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


<br>
<br>
统计相同单词的数量：

方式一：将字符串 * 5，然后再切割

方式二：将每个单词的数量以元组形式存放，再统计

```scala
object Exam22{
  def main(args: Array[String]): Unit = {
    val lineList = List(("Hadoop Hbase Hive",5), ("Hadoop Kafka Hive",4), ("Kafka Hive",3), ("Hive", 2))

    val tuples: List[(String, Int)] = lineList.flatMap {
      case (sentence, count) => sentence.split(" ").map {
        word => (word, count) //将一个数组用map方法之后返回还是一个数组，所以符合flatMap的返回值可迭代要求
      }
    }

    val tuplesH: List[(String, Int)] = tuples.filter {
      case (word, count) => word.contains("H")
    }
    val stringToTuples: Map[String, List[(String, Int)]] = tuplesH.groupBy {
      case (word, count) => word
    }
    val stringToInts: Map[String, List[Int]] = stringToTuples.map {
      case (word,list) => (word,list.map{
        case (word,count) => count
      })
    }
    println(stringToInts)

    val stringToInt: Map[String, Int] = stringToInts.map {
      case (word, list) => (word, list.sum)
    }
    println(stringToInt)

//    val wordSort: List[(String, Int)] = stringToInt.toList.sortBy {
//      case (word, count) => count
//    }
//    println(wordSort)
//
//    println(wordSort.takeRight(2))

    val wordSort: List[(String, Int)] = stringToInt.toList.sortWith {
      case ((s1, c1), (s2, c2)) => c1 > c2
    }
    println(wordSort.take(2))

  }
}
```



 **_  的用法：①包中所有类②系统默认初始化③将函数不执行返回④参数占位符⑤隐藏导入的类⑥标识符⑦绝对路径**⑧case _ 不管什么值都匹配⑨case _:BigInt =>...  当后面不用该变量，不关心变量时，可以用 _ 代替。

**[] 的用法：①protected[包名]②泛型 classOf[] , inInstanceOf[] asInstanceOf[] ，Array[]③实现特质中方法时指向类  super[Operate].insert( )**



![1563934859730](scala.assets/1563934859730.png

![1563934859730](F:/Typora/图片/1563934859730.png)







```scala
枚举类：
package com.atguigu.bigdata.scala.chapter01

import com.atguigu.bigdata.scala.chapter01

object Enumeration {
  def main(args: Array[String]): Unit = {
    println(Color.red)
    Color.printcolor
    val color = new Color
    println(color.name)
  }
}
class Color{
  var name = "zhangsan"
  Color.printcolor
}
object Color extends Enumeration{
  val red: chapter01.Color.Value = Value(1,"red")
  val blue = Value(2,"blue")
  def printcolor {
    println("I'm " + blue)
  }

}
```

	

```scala
小朋友玩游戏：
package com.atguigu.bigdata.scala.chapter01

object ChildPalyGame {
  def main(args: Array[String]): Unit = {	//此处可以删去main方法，让伴生对象继承App特质，也可以									正常执行。好处是main方法会执行主方法外的可执行语言，这样更加清晰。
    Child.JoinGame(Child("zhangsan"))
    Child.JoinGame(Child("lisi"))
    Child.total
  }
}
class Child(var name : String){
  def this(name:String,i:Int){
    this(name:String)
  }
  println("123124")
}
object Child{
  def apply(name: String): Child = new Child(name,1)
  var totalChild = 0
  def JoinGame(child : Child): Unit ={
    println(child.name + " join the game")
    totalChild += 1
  }
  def total(): Unit ={
    println("total " + totalChild + " playing game")
  }
  println("afasdf")
}

编译后的反编译源码：
public final class ChildPalyGame
{
  public static void main(String[] paramArrayOfString)
  {
    ChildPalyGame..MODULE$.main(paramArrayOfString);
  }
}

public final class ChildPalyGame$
{
  public static final  MODULE$ = new ();

  public void main(String[] args) { Child..MODULE$.JoinGame(Child..MODULE$.apply("zhangsan"));
    Child..MODULE$.JoinGame(Child..MODULE$.apply("lisi"));
    Child..MODULE$.total();
  }
}

public class Child
{
  private String name;		//属性都是私有化的，通过对象修改或读取属性是通过set/get方法实现的

  public static void total()
  {
    Child..MODULE$.total();
  }

  public static void JoinGame(Child paramChild)
  {
    Child..MODULE$.JoinGame(paramChild);
  }

  public static void totalChild_$eq(int paramInt)
  {
    Child..MODULE$.totalChild_$eq(paramInt);
  }

  public static int totalChild()
  {
    return Child..MODULE$.totalChild();
  }

  public static Child apply(String paramString)
  {
    return Child..MODULE$.apply(paramString);
  }

  public String name(){  return this.name; } 				//属性的get方法
  public void name_$eq(String x$1) { this.name = x$1; } 	//属性的set方法
  public Child(String name) { Predef..MODULE$.println("123124") } 	//主构造方法
  public Child(String name, int i) { this(name); }					//辅构造方法
}

public final class Child$
{
  public static final  MODULE$ = new ();

  private static int totalChild = 0;

  static
  {
    Predef..MODULE$.println("afasdf"); } 
  public Child apply(String name) { return new Child(name, 1); } 
  public int totalChild() { return totalChild; } 
  public void totalChild_$eq(int x$1) { totalChild = x$1; } 
  public void JoinGame(Child child) {
    Predef..MODULE$.println(14 + child.name() + " join the game");
    totalChild_$eq(totalChild() + 1);
  }
  public void total() {
    Predef..MODULE$.println(19 + "total " + totalChild() + " playing game");
  }
}
```

	scala中，将静态的属性和方法写在伴生对象中，将非静态的属性和方法写在伴生类中。伴生对象在编译后的类中会生成一个静态的自身对象，当我们以静态的方式访问其中的属性和方法时，编译后会通过这个唯一的静态对象调用类中的属性和方法来模拟java中的静态属性和方法。

	因为在底层编译时，object伴生对象也是一个类，将类中的可执行语句都放入到静态代码块中，所以在执行伴生对象的主方法时，会执行主方法外的可执行语句；当加载类时，就会先运行静态代码块中的代码。而伴生类，会将类中的可执行语言放入到主构造器中，所以scala规定必须要通过主构造器创建对象。







当把一个计算结果赋值给一个变量，则编译器会进行类型转化及判断。

当把一个字面量赋值给一个变量，则编译器会进行范围的判定。



var a : short = 50 不用类型转换
var b : float = 50.0f 需要指定类型
var c : short = 'a' + 1 不会报错
var d : short = 10 + 10 不会报错，再编译时会自动相加，编译后只有20，和直接写20的效果一样。如果有变量则会转成int型。

nothing为什么可以返回异常对象，nothing类不是底层类么？



scala基本原则：至简原则

1.使用object关键字声明

	如果使用object声明类，可以编译出两个类，一个是当前类，另外一个是当前类的一个辅助类，执行时，辅助类可以直接构建对象使用（伴生对象），为了模拟静态语法。

2.声明main方法

	2.1必须使用def关键字（definded）声明

	2.2Scala中没有public关键字，默认访问权限就是public

	2.3不需要使用static关键字声明，因为Scala是完全面向对象的语言，所以没有静态语法。

	2.4 用Unit类代替关键字void

	2.5scala中参数命名为   参数名 ： 参数类型

	因为java是强类型语言，一定要加类型；而scala认为类型不那么重要，所以参数类型和返回值类型都放后面

3.打印字符串

	java：  System.out.println(）

	scala： println()       predef预先编译好的功能，println就是其中之一，最终会调用java的IO流。11:40



	println(raw"xxxx\nxxx")	\n不换行，以字符串输出

	println("""xxx

			xxx

			xxx

			""")		以给定的格式打印

println（f"age = $age%.2f"）  f表示格式化，将$age格式化输出 

println(" " * i )  	输出i个空格 ,通过这种表达式，可以只用一个循环就打印出三角形。

println(s"$id,$name")



javap？？javap是jdk自带的反解析工具，可以将javap指令加入到idea中，查看java字节码的反编译码。

javadoc指令生成API文档？通过javadoc 文件名.java，可以提取代码中的注释生成开发文档。

半角空格？半角占一个字节，全角占两个字节，trim去不了全角空格，可以用replace方法将全角空格换成半角空格再用trim去除。



15：00 改变String类中的final修饰的char数组（用反射）

![捕获](scala.assets/捕获.PNG

![捕获](F:/Typora/图片/捕获.PNG)

	

	15:37伴生对象？object类就是一个伴生对象，编译后会生成一个伴生类对象，由主函数调用。可以在伴生类中声明属性。val相当于给变量加了一个final修饰，但是编译后只有属性变量有final，因为局部变量不能用final修饰。



	对于多态的类有多个重载方法，在编译时会选择重载方法，根据的是父类的类型选择重载方法，而不是子类对象的类型



java的object类是any的子类，anyref的父类。



String s = "a" + "b" + "c"  只创建一个常量字符串"abc"，在编译的时候直接编译为“abc”，所以运行时只生成“abc”



16:31为什么变量相加会自动转成int类型？？底层指令不够，因为用ASCII码作为指令集（255），所以为了节省指令集空间，没有short和byte的运算指令。所以只能作int运算操作。



scala中所有数字也都是对象，10+10实际为10.+（10）    1 to 3 实际为1.to(3)，to方法可以指定步长1.to(10,2)步长为2。但是一般写成i <- Range(1,10,2)。





9:20多态的动态绑定只对方法进行绑定，如果有重载的方法，调用方法时指向**对象**的实际的内存，如果对象中没有重写该方法，则指向父类的实际内存，成员变量为指向的内存中的值。如下图中，将注释的部分放开，运行得到的结果为30；注释之后得到的结果为20.

![动态绑定机制](F:/Typora/图片/动态绑定机制.PNG)



10:00

i=i++的字节码反编译码：即用到临时变量存储i的值，i增加1作为i的值。

![捕获3](F:/Typora/图片/捕获3.PNG)

	

 i=i++的底层字节码实现：

	![捕获2](F:/Typora/图片/捕获2.PNG)	常量表中有两个常量args和i，分别占用了1号和2号slot槽位。i=i++ 底层字节码实现，先将i=10压入栈顶，然后将i的值存储到1号槽位，再将1号槽的值加载到栈顶，然后对1号槽位的值自增1。然后进行赋值操作，将栈顶的i=10再次存储到1号槽位。所以最终1号槽位的变量i的值为10；









10:32 BigDecimal（2.1）./3 == 0.7	直接用浮点数2.1运算会损失精度，结果不等于0.7；所以先转成大数（字符串），再调用大数对象的方法进行计算。

一元运算符不提升数据类型



10:48

&用于计算哈希表的slot号（map中和redis的slot计算都会用到），将2^n-1，然后与上哈希值，得到slot号。

当要求的长度是2^n时，用$；当不能保证长度是2^n时，只能取模。所以kafka的分区用取模来计算，因为不能保证分区数为2^n。



15:50？？ 调用一个为空对象的**成员属性或成员方法**，会发生**空指针异常**（即只有对象调用成员属性或成员方法是会发生空指针异常）。



16:17 面向对象编程	对于类的共有的属性，需要将其设为静态属性和方法。



将类中声明的函数称为方法，所以方法有重载和重写的概念。

函数没有重写和重载的概念。



统一访问原则，访问变量和访问函数形式统一。

如果函数声明返回值类型为Unit，那么函数体中的return操作不起作用。



9:15

匿名函数：()->{println("xxx")}	

val f9 = ()=>{println("yyy")}	调用函数f9() ,括号不能省略。

val f9 = (i:Int)=>{println("yyy")}



```scala
  object Scala04_NightMareLevelFunction {
   def main(args: Array[String]): Unit = {
   
   	def f1( name : String ): String = {
        return "Name:" + name
    }
    // 声明函数后，可以将函数体最后一行代码作为函数的返回值，所以return关键字可以省略
    def f2( name : String ): String = {
        "Name:" + name
    }

    // 如果函数可以自动推断出返回值类型，那么返回值类型可以省略
    def f3( name : String ) = {
        "Name:" + name
    }

    // 如果函数逻辑只有一行代码，那么花括号可以省略
    def f4() = "abc"

    // 如果参数列表没有参数，那么参数列表的小括号可以省略
    // val f5 = "bcd"
    // 统一访问原则
    def f5 = "bcd"

    // 如果函数的参数列表已声明，那么调用时可以使用小括号，也可以不使用
    // 如果函数的参数列表未声明，那么调用时不能使用小括号
    //println(f4)

    // 如果函数体中有明确的return操作，那么函数必须声明返回值类型
    def f6( name : String ) = {
        val flg = true
        if ( flg ) {
            "Name:" + name
        } else {
            1
        }

    }

    // 如果函数声明返回值类型为Unit,那么函数体中的return操作不起作用
    def f7(): Unit = {
       return "zhangsan"
    }

    // 如果Unit类型也想省略，可以同时将等号省略
    // 将这样的函数称之为过程
    def f8() {
        return 1
    }
    //println(f8)

    // 如果只关系逻辑，而不关心方法名称，那么函数名称可以省略，def关键字也可以省略
    //()->{println("xxxxxx")}
    // 匿名函数
    //() => {println("yyyyy")}

    // scala语法中，万物皆函数，所以什么都可以是函数
    // 变量也能是函数
    val f9 = (i:Int) => {println("i = " + i)};

    f9(10)
       
       
    val f10 = () => println("yyyyy")
    f10()
    val f11 = (a:Int) => a + 1
    println(f11(1))
  }
 }
```

	匿名函数参数最多为22个（1~22），可以用集合作为参数实现多个参数。

	闭包：当前函数的内部用到了函数之外的变量，为了防止外部变量在函数内失效，将变量包含道函数内部，形成闭合的效果，称之为闭包。即改变了变量的生命周期。科里化中一定会出现闭包。

	因为方法调用方法，一个方法执行完毕之后一定会弹栈，所以方法中定义的变量在弹栈时会失效。

```scala
object Scala05_HellLevelFunction {


    def main(args: Array[String]): Unit = {

        // 地狱版函数式编程
        // TODO 函数的参数是函数
        // 将一个函数作为参数传给另外一个函数
        // 声明的方式 ： 参数名：参数类型
        // f : (Int)=>Unit
        def f( param : (Int)=>Unit ): Unit = {
            param(10)
        }

        // 调用函数
        def ff(i:Int): Unit = {
            println("i = " + i)
        }
        //f(ff)

        def f1( param:()=>Unit ): Unit = {
            param()
        }

        def f11(): Unit = {
            println("f111111")
        }

        //f1( f11 )

        // TODO 将一个函数作为函数的返回值返回,不执行这个函数

        def f22(): Unit = {
            println("f222222")
        }

        // 如果将函数作为返回值返回，需要增加返回值类型
        def f2():()=>Unit = {
            f22
        }

        // 如果想要
        def f222() = {
            f22 _
        }

        //f2()()
        //f222()()

        def f3( i : Int ) = {

            def f33( j : Int ) = {

                def f333( f:(Int, Int)=>Int ) = {
                    f(i, j)
                }

                f333 _
            }

            f33 _
        }

        def innerFunction(x:Int, y:Int): Int = {
            x * y
        }

        println(f3(10)(10)(innerFunction))
        // 使用匿名函数传递参数
        //println(f3(10)(10)((x:Int, y:Int)=>{x+y}))
        //println(f3(10)(10)((x, y)=>{x+y}))
        //println(f3(10)(10)(_*_))

        // 函数柯里化
        def f4(i:Int)(j:Int)(p:(Int,Int)=>Int): Int = {
            p(i, j)
        }

        // 函数闭包：如果函数中使用外部的变量，为了防止变量数据丢失，将变量包含到函数的内部，形成闭合的效果，称之为闭包，可以改变变量的生命周期

        println(f4(5)(10)(_ - _))



    }
}
```

	将方法体内的函数作为返回值返回，而不执行这个函数：

①增加返回值类型为该函数

②如果不指定返回值类型，则在函数后增加"_"符号，表示不执行函数



val f2: (String, Double) => Int = (a: String, b : Double) => a.toInt + b.toInt的含义是：定义一个变量，规定变量的参数列表和返回值；将等号右边的匿名函数赋给该变量。



scala中不能省略返回值类型。因为自己调用自己，推断不出来自己的返回值类型，所以需要添加上返回值类型。



栈滚动异常（stackoverflow）：递归深度过大。

栈内存溢出：多个线程并行时会出现栈内存溢出，没有足够的栈可以分配。

方法区溢出：虚拟机的1/64到1/4的内存分配给方法区，如果加载的类模版过多（如Tomcat）造成方法区溢出。

堆内存溢出：进行fullGC后还是没有足够的堆内存用于创建对象，则堆内存溢出。



栈上分配：将对象创建在栈上，当方法被弹栈时，该对象也会弹栈，可以有效利用内存。

逃逸分析：如果创建的对象被返回到外部的调用函数，那么该对象不能被弹栈，即逃逸出去。那么虚拟机不会在栈上创建该对象，而是在堆中创建。



System.GC能主动调用jvm的GC机制，但是不一定执行，由GC的内部逻辑决定。回收时会调用对象的finilize方法，可以在方法中决定是否继续回收该对象。

G1垃圾回收算法、CMS垃圾回收算法。



```java
public class ReturnTest {
    public static void main(String[] args) {
        System.out.println(test());
    }

    private static int test() {
        int i = 0;
        try {
            return i++;
        }finally {
            return ++i;
        }
    }
}
```

	打印结果为2。return会开一个临时变量，将return的值存储在该临时变量中；第一个return将0存储在临时变量中，i变为1；再执行finally中的return语句，将++i=2存储到临时变量中，然后返回。所以结果为2。







包名  域名的反写+项目名+模块+程序类型，因为在实际开发中对包名要求不严格，可以缩写。

java中包的作用：①对不同类的管理②防止同名包冲突③包访问权限

scala中包的作用：①package关键字可以多次声明②scala源码包和包名没有直接的关系③package可以声明作用域，且子包可以直接访问父包的类，不需要导包④scala将包当成一个对象，即包对象，可以在包对象中创建变量和函数



native修饰符：调用底层的代码实现功能，提高运行效率，解决jvm无法操作硬件的局限。



protected访问权限

```
public class ProtectedClone {
    public static void main(String[] args) {
        AAA aaa = new AAA();

        aaa.clone();
    }
}

class AAA{
//    protected Object clone(){
//        return null;
//    }
}
```

	如果不重写AAA中的clone方法，那么在ProtectedClone类中无法对clone方法进行调用。因为clone方法的**提供者**为对象AAA的父类Object，而clone的**调用者**为ProtectedClone类；AAA的父类与ProtectedClone的没有父子关系，所以不能在ProtectedClone类中调用clone方法；若在AAA中重写clone方法，那么动态绑定机制，AAA对象会调用自己的clone方法，而ProtectedClone和AAA同包，所以ProtectedClone可以调用AAA的clone方法。





el表达式 通过反射调用类属性和方法



	java中用import 可以①导入某个类②导入包中所有的类③导入类的静态属性和方法。import static com.atguigu.bigdata.java.ConstBean.*就可以导入ConstBean类中的所有的静态方法，直接写方法即可，不需要写类名。

	scala中的breaks中的breakable静态方法，可以导入该静态方法import scala.util.control.Breaks._ ，然后直接用该方法。在scala中用伴生对象访问时可以通过类名直接访问方法，模拟静态语法。



	scala赋予import关键字更多功能：①import关键字可以在任意地方使用②可以导入指定包中的类，但是java.lang和scala（predef）中的类不需要导入。③导入指定包中所有的类。在scala中使用_代替java中的*。但是在编译中，只会加载用到的类。④导入指定包中的多个类，可以采用大括号，声明在一行。⑤scala中的import可以导包，如果是包对象，可以访问其属性和方法。⑥scala可以在导类的时候隐藏指定的类 java.util.{HashMap=> _ ,_ _}将HashMap类隐藏。⑦scala可以给导入的类起别名，两种方式为：java.util.{HashMap=>JacaHashMap, _}，type hm = java.util.HashMap⑧scala中包的概念是相对路径，但这样可能会出现冲突。一般采用绝对路径的方式来解决。_      **_ root_**.java.util.HashMap



scala包中的predef伴生对象，在使用时可以省略，包括println、classOf等。

 = classOf[User]	classOf[User]  获取当前User的类的信息，获取方法区的内存。 9:15？？？



D:\MyWork\Program\jdk-8u202\jre\下的lib和classes文件夹		引导类加载器，加载核心类库

D:\MyWork\Program\jdk-8u202\jre\lib\ext\下的jar包和classes文件夹	扩展类加载器，加载扩展类库

classpath	应用类加载器，加载classpath下的类

	双亲委派机制：加载类时，会逐级委派上级加载器，加载其路径下的类，如果启动类加载器找到类则直接加载，没有找到类，会返回null；扩展类加载器再加载路径下的类，找到直接加载类，否则返回异常；应用类加载器再查找路径下的类，找到则直接加载，否则返回classnotfoundexception。为什么获取启动类加载器会返回null，为什么启动类加载器返回null而不是异常？因为启动类加载器不是java实现的，无法返回异常，而扩展类加载器是java实现的。



	scala中的访问权限和java的有区别①protected权限只能由同类或子类访问，同包不能访问②不加访问权限时，默认为public。③scala中没有包访问权限的概念。**private[包名]** ，即包内私有，指明能访问的包的名称（子包也能访问）。

	类的无权限修饰的属性在编译后全都是private的，但同时提供两个公共的方法（set,get），用于访问和修改这个属性。（类似el表达式，通过反射获取对象的方法，通过方法访问对应的属性。）但是框架中有属性对应的方法的名称规范，所以scala提供了**@BeanProperty注释**，来额外生成一对标准名称的getxxx和setxxx方法，以匹配java开发规范。	private修饰的属性，编译后生成private修饰的get、set方法；val修饰的属性，编译后只生成get方法。

	由于在伴生对象中定义的属性都会在编译时生成set和get方法，所以在写方法时需要注意不能和自动生成的方法重复，可以改变参数形成重载。



scala也可以给属性默认初始化，用"_"赋值。

 **_  的用法：①包中所有类②系统默认初始化③将函数不执行返回④参数占位符⑤隐藏导入的类⑥标识符⑦绝对路径**⑧case _ 不管什么值都匹配⑨case _:BigInt =>...  当后面不用该变量，不关心变量时，可以用 _ 代替。

**[] 的用法：①protected[包名]②泛型 classOf[] , inInstanceOf[] asInstanceOf[] ，Array[]③实现特质中方法时指向类  super[Operate].insert( )**



scala常用方法：**isInstanceOf[ ]**判断类型，方括号内是泛型，定义函数时没写小括号，此处也不写小括号 	  			**asInstanceOf[ ]**转换类型

			classOf[User]  获取当前User的类的信息，获取方法区的内存。



构造方法：

	1.apply：

	Range等对象，可以不使用new关键字构建：会调用伴生对象的特殊方法构建对象。可以在伴生对象中定义apply方法，def apply():Emp  = new Emp() 。如果直接写类名，则会编译为  **类名.apply（）**来调用该构造方法返回类对象。如Range(1,10,2)直接返回该数组对象，因为编译时会调用apply方法返回new Range（1,10,2）对象。好处是①增加了整体性②私有化构造方法，通过调用apply获取对象。可以用于单例模式等。③apply不一定要返回本类的对象，可以是其他类的对象。

	用new调用的是构造方法，不用new创建对象则调用apply方法。

	2.构造函数：

	scala语言万物皆对象，万物皆函数。所以class类也是函数，因为类的后面使用小括号声明的参数列表，其实就是构造函数的参数列表。

①构造函数可以有参数②辅构造函数的名称有特殊要求def this（）｛｝③scala中构造函数分为两大类：主构造函数&辅构造函数（使用**this**声明构造函数）④辅助构造函数一定要直接或间接的调用主构造函数，因为类的主体是由主构造函数来初始化的（没有默认无参构造器的说法）。⑤辅助构造方法在调用其他构造方法时，必须**保证已经声明过其他构造方法**。



	构造方法私有化：class User private(){  },类构造器的括号前加private，可以在伴生对象中添加apply方法，**伴生对象可以访问伴生类中的私有属性和方法。**在外面调用apply获取伴生类对象。



	可以将构造参数作为类的属性，但是需要加上var。如class User（**var/val**  username : String）｛  ｝，将传入的参数username作为User类的属性。



	枚举类object Color extends Enumeration 9:33

	伴生对象中的语句都会执行，因为构建对象时会调用函数体。object Test extends App 9:36



类的继承：

```scala 
package com.atguigu.bigdata.scala.chapter01

object Scala1 {
  def main(args: Array[String]): Unit = {

    new Student("zhangsan");
  }
}

class Person(name : String){
  println(name)
}
class Student(name : String) extends Person(name){

}
```

	可以在继承的类的后面直接跟参数，进入子类构造器后就会先调用父类构造器。



抽象类：

	abstract class Parent{  } 就是抽象类，抽象类中的抽象方法：只有声明，没有实现 def  test（）：Unit

	scala中类名前加abstract关键字为抽象类；scala中只有声明没有实现的方法为抽象方法。继承抽象类需要实现抽象方法才能变成实体类，才能构造对象。重写方法需要添加override关键字，但是重写抽象方法不需要override关键字。

	scala中的属性也可以是抽象的。一个类中有抽象属性（声明属性但未初始化），那么这个类为抽象类，抽象属性编译时不会生成属性，而是提供了两个抽象的方法。继承抽象类需要将抽象属性补充完整，其实等同于重写属性的set方法和get方法。	子类**重写父类完整的属性**，但是需要**val修饰**的不可变的完整属性才能重写，也需要**添加override**关键字。

原理：修改和读取age都是调用底层的方法，因为子类中也存在get和set方法， 所以会调用子类的get和set方法，由于动态绑定机制，最终修改和读取的是子类中的重写的属性。局部变量只有在其作用于内才能修改，但是最终修改的是却是子类的属性，所以为了避免这种歧义，将属性用val修饰，如果有修改属性的操作，在编译检查时直接报错。

```
package com.atguigu.bigdata.scala.chapter01

object Scala1 {
  def main(args: Array[String]): Unit = {

    val stu = new Student("zhangsan")
    stu.test()
  }
}

class Person(name : String){
  var age : Int = 20

  def test():Unit = {
    age = 100
    println(age)
  }
}
class Student(name : String) extends Person(name){
  override var age : Int = 30
}
```





特质（类似AOP编程，将相同的？？9:39  ？？）：

	ocp开发原则：即（Open Closed Principle）开闭原则，扩展功能不能修改原有的代码。

	面向接口编程体现在  public static void sum(List list){   }，可以通过需求传入不同类型的集合。



	16:20 AAA.class.getInterfaces().length 利用反射查看是否实现接口



	java中的接口难以理解，所以scala没有接口的概念和关键字。scala将多个类具有的相同的特征从对象中剥离出来，形成一个特殊结构，称之为特质。如果一个对象符合某个特征（特质），那么可以将这个特征“混入”到对象中。	如果有父类，extends继承父类，用with来混入特质。特质中可以由抽象的属性和方法。

	动态混入：创建对象的同时混入特质。在后面跟with + 特征，那么对象中就带有特质，遵循了OCP开发原则，同时扩展了功能，不会对类有影响。

	

多特质的初始化和执行特质中的功能：

	特质可以混入其他特质：如果类存在父类，会首先初始化父类；如果类存在特质， 会首先初始化特质，在进行类的初始化；父类初始化后，如果类存在多个特质，会从左到右一次初始化。**特质只会初始化一次**，如果之前已经初始化了，不会再次初始化。

	初始化顺序从左到右，执行特质中的功能时，是从右向左执行。当前super关键字不是父特质的概念，而是上一个特质的意思（如果最右边的特质没有super，那么是不是全都不会调用？？是）。如果一定要super指向上一级而不是上一个，需要特殊的方式指定 super[Operate].insert( ) 。

```scala
package com.atguigu.bigdata.scala.chapter01

object Scala2 {
  def main(args: Array[String]): Unit = {

    var people = new People
    people.insert()
  }
}
trait Operate {
  def insert (): Unit = {
    println("插入数据")
  }
}
trait DB extends Operate {
  override def insert(): Unit = {
    println("向数据库")
    super.insert()
  }
}
trait File extends Operate {
  override def insert(): Unit = {
    println("向文件中")
    super.insert()
  }
}
class People extends DB with File {

}

输出结果：
    向文件中
    向数据库
    插入数据
```



9:45 	this：Exception => 	规定约束条件，那么添加约束的方法中就可以使用约束类的属性和方法。但是继承该特质的类也有要求。

```scala
object Excep {
  def main(args: Array[String]): Unit = {
  }
}
class Test extends Exception with MyTrait{	//因为约束是异常，所以只能异常类才能继承
  
}

trait MyTrait{
  //约束：
  this:Exception=>
  def test(){
    println(getMessage())
  }
}
```



和scala中的predef伴生对象类似，window.document.getElementById() ，window.alert()在窗口中时，window可以省略。

AOP编程：将业务中的相同的功能剥离出来，以横向的方式交叉的应用到业务中的编程方式。与特质相似。



隐式转换（类型转换）：

```scala
值的类型转换
object Implicit {
  def main(args: Array[String]): Unit = {
    implicit def transform(d:Double):Int={
      d.toInt
    }
    var i : Int = 2.0
    println(i)
  }
}
伴生对象反编译源码：
public final class Implicit$
{
  public static final  MODULE$ = new ();

  public void main(String[] args)
  {
    int i = transform$1(2.0D);				//二次编译时会调用隐式转换
    Predef..MODULE$.println(BoxesRunTime.boxToInteger(i));
  }

  private static final int transform$1(double d)
  {
    return (int)d;
  }
}

类对象的隐式转换方法
object Implicit {
  def main(args: Array[String]): Unit = {
    implicit def mysqlToDB(mysql: MySQL): DB = {
      new DB
    }
    val mysql = new MySQL
    mysql.insert()
    mysql.delete
  }
}
class MySQL {
  def insert(): Unit = {
    println("insert")
  }
}
class DB {
  def delete: Unit = {
    println("delete")
  }
}
隐式类转换
object Implicit {
  def main(args: Array[String]): Unit = {
    val mysql = new MySQL
    mysql.insert
    mysql.delete
  }
  class MySQL{
    def insert: Unit ={
      println("insert..")
    }
  }
  implicit class DB(mysql:MySQL){ //在需要转换的类前加implicit，同时加上需要转化的对象。那么在指定		对象调用该类方法时会转换为该类对象。隐式类不能是顶级的，只能从作用域和继承的类、特质、伴生对象中查找
    def delete: Unit ={
      println("delete..")
    }
  }
}

隐式参数
object Implicit
  def main(args: Array[String]): Unit = {
    implicit var name = "Jack"
    def hello(implicit name:String = "Tom"): Unit ={	//事先加上implicit关键字，后续要改默认														参数，只需要在加一个隐式变量即可
      println(name + " hello")
    }
    hello
  }
}
```

	引用类型强转的类需要有实现或继承关系，所以scala中用隐式转换。如predef中有将string类型转为StringOps类型的隐式转换方法，使其能使用StringOps的类方法。

	scala编译器在发现编译错误时，可以再次尝试使用转换规则重新编译，看看是否能编译通过。**implicit** def transform(d:Double) : Int = {d.toInt} 制定了类型转换规则，在**二次编译**后能自动调用该转换方法。

	隐式转换可以扩展功能，但是**只能有一个参数**（可以通过实现科里化），不能有两个相同的隐式转换。

	隐式变量：在OCP原则下改变函数的默认参数赋值，将隐式属性的值作为默认参数。隐式变量值可以覆盖默认参数（在参数列表中添加关键字implicit），和隐式转化方法一样也不能有两个相同的隐式属性。

	隐式转换的属性、方法和类应从当前对象的作用域找，没找到则从父类和特质和伴生对象中找。





## 集合：

	scala集合分为两大类：可变集合和不可变集合（底层存储数组不可变），默认采用不可变集合。集合有三大类，序列seq、集set和映射map

	scala集合的类型根据包来确定：scala.collection.mutable和scala.collection.immutable

11:39  scala的predef是自动导入的，在predef中将Array类的全限定类名进行重命名为Array，所以直接写Array相当于Array的全限定类名。类似的println方法在predef中定义，所以直接使用println即可。

	

### seq:（Array，ArrayBuffer，List，ListBuffer）

Array是不可变数组，ArrayBuffer是可变数组：

	创建数组时需要添加数组中内容的泛型；如果不加泛型，则类型为Nothing。

```scala
val array:Array[String] = new Array[String](3)		//需要添加泛型，否则内部元素为Nothing类型
//用小括号来访问
array(0) = "1"
array(1) = "2"
array(2) = "3"
println(array(1))
//循环打印
for （elem <- array){
    println(elem)
}
++方法：
val array1 = new Array[AnyVal](3)
    array1(0) = 1
    array1(1) = 2
    array1(2) = 3
val array2:Array[Any] = array.++(array1)	//不可变数组++会生成新的数组，而不会对本身造成影响

//构建数组并初始化
val ints = Array(1,"2",3)	//调用apply方法,能自动推断类型
```

Array（实际是一个String数组）数组的方法：

array.length/update（，）/++()  由于数组不可变，所以++方法会返回一个新的Array数组对象。

array.mkString(",")	将String[]数组装换成字符串，用，分隔。



ArrayBuffer：将数组的包装对象作为参数来构建ArrayBuffer对象。14:17

```scala
    val ints = ArrayBuffer(1,2,3)
    ints.append(5)
    ints.remove(1)
    println(ints(1))

    //遍历集合
//    def f(x:Any) = {
//      println(x)
//    }
//
//    ints.foreach(f)
//    ints.foreach((x:Any)=>{println(x)})	//用匿名函数接收并执行打印
//    ints.foreach((x)=>println(x))
//    ints.foreach(println(_))
    ints.foreach(println)	//至简模式
```

ab.append（,,）/mkString(",")/update（，）/remove（，）

ab(0)=9 和 ab.update(0,9)效果一样。



List：

	List(1,2,3) 有序可重复的不可变集合,会产生新的集合

```scala
不可变List集合
	val numList = List(1,2,3)
//    val ints: List[Int] = numList:+(5)
//    ints.foreach(println)
//
//    val ints1: List[Int] = 5::(numList)
//    ints1.foreach(println)
//
//    val ints2:List[Int] = 5+:(numList)	//同::
//    ints2.foreach(println)
//    numList(1) = 9                 //List只有updated方法，所以直接用numList不行
//    val list: List[Any] = numList.updated(1,"1")
//    list.foreach(println)
//    val list1: List[Int] = numList.drop(2)	//丢弃的数量
//    list1.foreach(println)

//    val numList3: List[Int] = 1::2::3::Nil  //从右向左将数加入到Nil空集合中
//    numList3.foreach(println)
    val numList4 = List(4,5,6)
    val numList5: List[Int] = 1::2::3::numList4:::Nil	//扁平化
    numList5.foreach(println)

```

	Nil是一个集合的对象，是一个空集合。  var list = 1::2::3::Nil 从右向左构建了List（1,2,3）集合。

	val list = 1::2::3::numList:::Nil 三个冒号表示将集合中的元素拆分（称为扁平化）后加入到Nil中。

	list.mkString("-")/++()/:+(5)/::(6)/+:() 将数字调整到前面/updated(,) List集合无法使用小括号方式/

drop（）参数为丢弃的数量/



ListBuffer(1,2,3,4)  可变集合

```scala
    val ints = ListBuffer(1,2,3)
//    ints.update(1,5)
    ints(1) = 5				//可以使用，底层调用update
//    ints.append(5,6)
//    ints.insert(1,0,1,2)  // 第一个数表示插入位置，后续时插入的数据
//    ints.remove(2)          //移除下标为2的数据
//    ints.remove(1,2)        //移除下标为1及其之后的2个数据
//    println(ints(1))        //底层调用了apply构造了不可变数组，输出该数组的指定值
    ints.foreach(println)
```

lb.mkString(",")/update( , ) 或 lb(0)=9 /append()/insert( , )/remove()/



### set:  

	默认为无序不可重复的不可变数组，导入collection.mutable包，mutable.Set为可变数组

```
val ints = Set(1,2,3,4,4,4,5,6)   //调用predef中的immutable.Set的apply方法，是不可变数组
    val ints1 = collection.mutable.Set(1,2,3,4,4,4,5) //创建可变Set集合
    ints1.add(4)
    ints1.update(9,true)
    ints1.update(4,false)   //set集合中的upset可以用于删除数据，第一个参数为删除值，第二个为是否删除
    ints1.remove(3)         //删除指定的数据
    val ints2: mutable.Set[Int] = ints1.-(2)  //返回一个新集合，将2删去
    ints1.foreach(println)
```

	 ms.add()/update()/remove()    .-() 会产生新的数组/



### map:  15：45

	scala的键值对：K -> V，也可以将其写为两个元素的元组（K,V）

```scala
 val stringToInt: Map[String, Int] = Map("a"->1,"b"->2,"c"->3)
    val stringToInt1: Map[String, Int] = stringToInt.+("d"->4) //不可变增加键值对返回新Map对象
    /*Option只有两个对象，None和Some，如果有值为Some，没有为None。None调用其他方法会报错，所以应该调用getOrElse。如果是Some则返回值，如果是None则返回指定的默认值*/
    val maybeInt: Option[Int] = stringToInt.get("a")
    println(maybeInt.getOrElse(0))
    //Map对象已经提供了getOrElse方法，可以直接调用
    println(stringToInt.getOrElse("a",0))

    val stringToInt2 = mutable.Map("a"->1,"b"->2,"c"->3)    //可变的Map集合
    stringToInt2.update("a",11)   //修改某个key的value值
    val i: Int = stringToInt2.getOrElse("a",0)
    stringToInt2.remove("a")
//    println(stringToInt)
//    println(stringToInt.mkString(","))
//    stringToInt.foreach(println)
//	  for(item <- stringToInt){
//		println(item)
//	  }

//获取Map集合中的key的集合和value的集合
    val keys: Iterable[String] = stringToInt.keys
    val set: Set[String] = stringToInt.keySet
    val iterator: Iterator[String] = stringToInt.keysIterator
    val values: Iterable[Int] = stringToInt.values
    val iterator1: Iterator[Int] = stringToInt.valuesIterator
	
	//用元组创建Map集合
    val stringToInt3 = Map(("a",1),("b",2),("c",3))
    //用参数t接收遍历的元组，然后单独取元组的k和v打印出来
    stringToInt3.foreach((t)=>{println(t._1+"="+t._2)})
```

Map集合通过**getOrElse（）**取数据。 .contains(key)判读元素是否存在

Map遍历时，直接写元组 for((k,v), <- map){  ptinltn}  ，实际用到了模式匹配。将元组与（k，v）匹配，然后打印

### **Tuple：**

**元组（元素的组合）,将无关的数据当成一个整体来使用**

```scala
    val tuple: (Int, String, Int) = (1,"zhangsan",22)	//最多放22个元素
    val iterator: Iterator[Any] = tuple.productIterator
    for (elem <- iterator) {
      println(elem)                     //遍历元组
    }
    println(tuple.productElement(1))    //访问元组中的元素
    println(tuple._2)                   //同上
    println(tuple)                      //打印整个元组
```

	（1，"zhangsan",22），最多只能放22个，和函数的参数一样，tuple中还可以放tuple。



如果元组中只有两个元素，称之为对偶或键值对：

	val t = ("a",1)

	val stringToInt1 = Map(("a",1),("b",2)) 	将两元素的元组可以作为键值对放入map中



可以通过 _n  ， productElement  和  productIterator  方式遍历元组。

val (id,age,name) = (1,20,"zhangsan")  ;  println（s“$id,$age,$name)	模式匹配上后赋值，然后输出

### 集合通用的方法：

scala中用==可以比较内容，java中只能比较内存地址。

	.size/length/head/tail/last/init/sum/max/min/product/map/flatMap/filter/groupBy/zip/reduce/fold/foreach/sliding/scan/take/sortWith/sortBy/diff/union/reverse/intersect

java中的length是底层数组的长度，size是元素个数。scala中是一样的。

```scala
val nums: List[Int] = List(1,2,3,4)

    nums.head   //取第一个元素
    nums.tail   //取除了第一个元素的数组
    nums.last   //取最后一个元素
    nums.init   //取除了最后一个元素的数组
    nums.size
    nums.length //scala中size和length一样，都是元素个数

    nums.sum
    nums.max
    nums.min
    nums.product  //乘积

    //sortBy和sortWith排序
    val ints: List[Int] = nums.sortBy((num:Int)=> num) //通过Int型的num来排序，可简写为num=>num，升序排序
	val ints11: List[Int] = nums.sortBy((num:String)=> num.toInt)//将字符串转为int再排序
    println(ints)     //通过指定的规则来排序
    val ints1: List[Int] = nums.sortWith(_>_) //降序排列，_<_为升序排列
    println(ints1)

    //filter过滤器
    val ints2: List[Int] = nums.filter((num)=> num%2 == 1)  //过滤出单数
    println(ints2)
    //过滤出集合中以S开头的单词
    val wordList: List[String] = List("Hadoop","Hbase","Spark","Scala")
    val wordList1: List[String] = wordList.filter((s)=>"S".equals(s.substring(0,1)))
    println(wordList1)

    //map映射方法可以将扁平化数据立体化，yield也有映射功能但是功能不强
    val ints3: List[Int] = nums.map(_*2)  //将集合中所有元素*2映射到新数组中，匿名函数写全为(x:Int)=>x*2
    println(ints3)
    val tuples: List[(Int, Int)] = nums.map((_,1))//将集合中元素映射为元组，匿名函数写全(x:Int)=>(x,1)
    println(tuples)
    //flatMap可以将数据扁平化，在将数组扁平化放入Nil时用到:::也是扁平化
    val list: List[List[Int]] = List(List(1,2),List(3,4),List(5,6))
    val intsToOnceToList = list.flatMap((l:List[Int])=>l)
    println(intsToOnceToList)

    val words: List[String] = List("Hello World","Hello Scala")
    val strings: List[String] = words.flatMap(_.split(" ")) //写全为(s:String)=>s.split(" ")
    println(strings)

    val intToInt = Map(("1",3),("2",4))
    val iterable: immutable.Iterable[Any] = intToInt.flatMap(t=>List(t._1,t._2))
    iterable.foreach(println)
    
//    nums.groupBy()
//    nums.reduce
//    nums.foreach	//集合的循环遍历，没有返回值
//    nums.fold
//    nums.sliding	//把一部分数据作为整体（窗口），对窗口做的操作称为窗口函数，窗口可以滑动。
//    nums.scan		//scan将fold操作的中间过程保存为一个数组
//    nums.take()	//从集合中取前n个数据


//    nums.diff			//两集合的差集（前后顺序对结果有影响）
//    nums.union		//两集合的并集
//    nums.intersect	//两集合的交集
//    nums.reverse      //反转数组
//    nums.zip			//拉链，将对应的数据作为tuple放入集合中
```



```scala
用fold方法将句子中的所有字符按顺序放入到一个集合中：
object FoldExecise {
  def main(args: Array[String]): Unit = {
    val sentence = "AAAAAABBBBCCCDD"
    val arrayBuffer = ArrayBuffer[Char]()
    if(arrayBuffer.isInstanceOf[ArrayBuffer[Char]]){
      println(true)
    }
    //如果参数是集合，每次读取sentence集合时，都会将集合传入
    sentence.foldLeft(arrayBuffer)(putArray)

    println(arrayBuffer)

    def putArray(arr:ArrayBuffer[Char],c:Char) : ArrayBuffer[Char] = {
      println(arr)
      arr.append(c)
      arr
    }
  }
}
```

```scala
统计一个句子中的每个字母的个数：
object FoldExecise2{
  def main(args: Array[String]): Unit = {
    val sentence = "AAAAAABBBBCCCDD"

    def charCount(map : Map[Char,Int],c : Char) : Map[Char,Int] = {
      map + (c->(map.getOrElse(c,0) + 1))
    }

    val charToInt: Map[Char, Int] = sentence.foldLeft(Map[Char, Int]())(charCount)
    charToInt.foreach(t => println(t.productElement(0) + "=" + t._2))

  }
}
统计一个数组中的相同单词的个数：
object WordCount {
  def main(args: Array[String]): Unit = {
    val wordList = List("Hello Spark","Hello Scala","Hello Flink")

    val strings: List[String] = wordList.flatMap(s=>s.split(" "))
    val stringToStrings: Map[String, List[String]] = strings.groupBy(s=>s)
    println(stringToStrings.map(t=>(t._1,t._2.length)))
    println(stringToStrings.foreach(t => (t.productElement(0), t.productElement(1))))
  }
}
统计一个数组中的相同单词的个数（）：
object WordCount1{
  def main(args: Array[String]): Unit = {
    val wordList = List(("Hello Spark",4),("Hello Scala",2),("Hello Flink",3))
    val strings: List[String] = wordList.map(t=>(t._1 + " ")*t._2)
    println(strings.flatMap(_.split(" ")).groupBy(t => t).map(t => (t._1, t._2.size)))
  }
}
```

```scala
将两个Map中的相同key的value相加：
import scala.collection.mutable.Map

object CombineMap {
  def main(args: Array[String]): Unit = {
    val map = Map[String,Int](("a",2),("b",4),("c",1))
    val map1 = Map[String,Int](("a",2),("b",4),("d",1))

    val stringToInt: Map[String, Int] = map.foldLeft(map1) {
//      (map: Map[String, Int], t: (String, Int)) => map.+(t._1 -> (map.getOrElse(t._1, 0) + t._2))
      (map: Map[String, Int], t: (String, Int)) => map(t._1) = map.getOrElse(t._1,0) + t._2
        map
    }
    println(stringToInt)

  }
}
如果是可变的Map，结果的返回值，或参数map1都可以读取到结果。
```

map（key）= value 可以快捷的改变key对应的value值！

fold类型要相同，foldLeft类型可以不同。



```scala
匹配值：
for (ch <- "+-3!") { 
    var sign = 0
    var digit = 0
    ch match {
        case '+' => sign = 1
        case '-' => sign = -1
        case _ if ch.toString.equals("3") => digit = 3	//守卫，如果满足if条件，则匹配该行
        case _ => sign = 2
    }
    println(ch + " " + sign + " " + digit)
}
匹配变量：
val ch = 'V'
ch match {
    case '+' => println("ok~")
    case mychar => println("ok~" + mychar)	将值给到变量并输出
    case _ => println ("ok~~")
}
匹配类型：
val a = 7
val obj = if(a == 1) 1
    else if(a == 2) "2"
    else if(a == 3) BigInt(3)
    else if(a == 4) Map("aa" -> 1)
    else if(a == 5) Map(1 -> "aa")
    else if(a == 6) Array(1, 2, 3)
    else if(a == 7) Array("aa", 1)
    else if(a == 8) Array("aa")

val result = obj match {	//类型匹配不考虑泛型，所以b和c是一样的。Array根据泛型底层是不同的数组
    case a : Int => a		//所以和泛型无关，和数组类型有关。
    case b : Map[String, Int] => "对象是一个字符串-数字的Map集合"
    case c : Map[Int, String] => "对象是一个数字-字符串的Map集合"
    case d : Array[String] => "对象是一个字符串数组"	//Array[String]底层是字符串数组，不是泛型
    case e : Array[Int] => "对象是一个数字数组"		//Array[Int]底层是int数组，不是泛型
    case _ : BigInt => Int.MaxValue				//当不关心变量时，可以用_代替
    case _ => "啥也不是"
}
println(result)
匹配数组：
for (arr <- Array(Array(0), Array(1, 0), Array(0, 1, 0),
Array(1, 1, 0), Array(1, 1, 0, 1))) {
    val result = arr match {
        case Array(0) => "0"
        case Array(x, y) => x + "=" + y	//匹配变量
        case Array(0, _*) => "以0开头和数组"
        case _ => "什么集合都不是"
    }
    println("result = " + result)
} 
匹配列表：
for (list <- Array(List(0), List(1, 0), List(0, 0, 0), List(1, 0, 0))) {
    val result = list match {
        case 0 :: Nil => "0" //
        case x :: y :: Nil => x + " " + y 
        case 0 :: tail => "0 ..." 		//0::tail  以0开头的List列表
        case _ => "something else"
    }
    println(result)
}
匹配元组：
for (pair <- Array((0, 1), (1, 0), (2, 1),(1,0,2))) {
    val result = pair match { 
        case (0, _) => "0 ..." 
        case (y, 0) => y 
        case (a,b) => (b,a)		//匹配变量
        case _ => "other" 
    }
    println(result)
}
匹配对象：
object unapply {
  def main(args: Array[String]): Unit = {
    val number: Double = 36.0
    number match {
      case Square(n) => println(n)	//对象等于36，求参数；调用unapply方法得到构造参数
      case _ => println("nothing matched")
    }
  }
}
object Square {
  def unapply(z: Double): Option[Double] = Some(math.sqrt(z))//返回some匹配成功，none匹配失败
  def apply(z: Double): Double = z * z
}
模式匹配
1.val (id,age,name) = (1,20,"zhangsan");println（s“$id,$age,$name)	模式匹配，然后输出
2.for((k,v), <- map){  ptinltn }   Map遍历时，直接写元组 
3.val arr = Array(1, 7, 2, 9)
  val Array(first, second, _*) = arr 
  println(first, second) 
4.
val map = Map("A"->1, "B"->0, "C"->3)
for ( (k, v) <- map ) {
    println(k + " -> " + v)
}

for ((k, 0) <- map) {
    println(k + " --> " + 0)
}

for ((k, v) <- map if v == 0) {
    println(k + " ---> " + v)
}
5.通过模式匹配得到某个属性的值，主要是代码可读性高，写明了取出姓名
object match2{
  def main(args: Array[String]): Unit = {
    val tuples = List((1,"zs",18),(2,"ls",28),(3,"ww",38))
    val strings: List[String] = tuples.map {	
      case (id, name, age) => name			//此处case不能省略，要和参数列表区分开
    }
    println(strings)
  }
}

样例类

```



val (id,age,name) = (1,20,"zhangsan")  ;  println（s“$id,$age,$name)	模式匹配上后赋值，然后输出



样例类：

样例类用case关键字进行声明，是为模式匹配(对象)而优化的类，构造器中的每一个参数都成为val——除非它被显式地声明为var，自动生成apply、unapply、toString、equals、hashCode和copy方法

```
abstract class Amount
case class Dollar(value: Double) extends Amount 
case class Currency(value: Double, unit: String) extends Amount
case object NoAmount extends Amount 

for (amt <- Array(Dollar(1000.0), Currency(1000.0, "RMB"), NoAmount)) {
    val result = amt match {
        case Dollar(v) => "$" + v
        case Currency(v, u) => v + " " + u
        case NoAmount => ""
    }
    println(amt + ": " + result)
}
```

样例类的copy方法可以将对象复制，Dollar(20.0).copy(value=30.0)  赋值并改变初始值

密封类：如果想让case类的所有子类都必须在申明该类的相同的源文件中定义，可以将样例类的通用超类声明为sealed，这个超类称之为密封类。密封就是不能在其他文件中定义子类。





数组与变长数组的转换：

arr1.toBuffer  //定长数组转可变数组   arr2.toArray  //变长数组转定长数组

scala数组转为java数组：import scala.collection.JavaConversions.bufferAsJavaList

val javaArr = new Processbuilder（arr）

val arrList = javaArr.command（） 

java的List转Scala数组:   import scala.collection.JavaConversions.asScalaBuffer

val scalaArr:mutable.Buffer[String] = arrList



queue:	两个方法enqueue和dequeue

```scala
object Queue1 {
  def main(args: Array[String]): Unit = {
    val queue = new mutable.Queue[String]
    queue.enqueue("1","2","4")
    println(queue.dequeue())
    println(queue.dequeue())
    println(queue.dequeue())
  }
}
```

stream：  只有读取时才会加载，末尾元素遵循lazy惰性加载。

```
object Stream {
  def main(args: Array[String]): Unit = {
    def numsForm(n: BigInt): Stream[BigInt] = {
      n #:: numsForm(n * 2)
    }
    println(numsForm(1))	//Stream(1,?)
    println(numsForm(1).head)	//1
    println(numsForm(1).tail.tail)	//Stream(4,?)
  }
}
```

view：view方法产出一个总是被懒执行的集合。view不会缓存数据，每次都要重新计算，比如遍历View时。如果没有读取，就不会加载计算。

```
val viewSquares2 = (1 to 100).view.map(multiple).filter(eq)
println(viewSquares2)
```



.par	多线程并行执行

```scala
object Thread1{
  def main(args: Array[String]): Unit = {
    (1 to 5).foreach{println}
    println("------------")
    (1 to 5).par.foreach{println}

    val strings1: immutable.IndexedSeq[String] = (1 to 100).map{case _ => (Thread.currentThread().getName)}
    val strings2: ParSeq[String] = (1 to 100).par.map{case _ => Thread.currentThread().getName}
    println(strings1 distinct)
    println(strings2 distinct)
  }
}
```







## 偏函数：

map函数是全量函数，只能对全部数据做转换，所以不能用偏函数。list.collect  支持偏函数。

```scala
object PartialFunction2{
  def main(args: Array[String]): Unit = {
    val list = List(1,2,3,4,"abc")

//    def addOne(x : Any) : Any ={
//      x match {
//        case x:Int => x + 1
//        case _ =>
//      }
//    }


    val unit: PartialFunction[Any, Int] = new PartialFunction[Any, Int] {
      override def isDefinedAt(x: Any): Boolean = {   //过滤需要的数据
        if (x.isInstanceOf[Int]) true
        else false
      }

      override def apply(x: Any) = {      //将返回true的数据交给apply处理
        x.asInstanceOf[Int] + 1
      }
    }
    //map函数是全量函数，所以不支持偏函数。
//    list.map(unit))

    //可以用collect方法
    println(list.collect(unit))
  }
}
```

scala中对偏函数进行了优化，可以简写，直接使用case就可以：

```scala
object PartialFunction3 {
  def main(args: Array[String]): Unit = {
    val list = List(1, 2, 3, 4, "abc")

    val ints: List[Int] = list.collect{case x:Int => x+1}	//通过case实现偏函数的功能
    println(ints)
  }
}
```



## 抽象控制：可以实现对算法的封装

如果参数是函数，且函数参数没有输入值，也没有返回值，即类似def myRunInThread(f1:  => Unit)  函数

```scala
object ChouXiangKongZhi {
  def main(args: Array[String]): Unit = {
    def f(p: => Unit) ={
      p
    }
    f {									调用了方法f，并将f中的代码作为参数执行
      for(elem <- 1 to 10){
        println(elem)
      }
    }
  }
}

```





## 泛型

#### java中：

10:25泛型只能对后续的操作做约束。如果没有用到该对象的类型，则不会报错，用到该对象的类型，则报错。

```java
public class FanXing {
    public static void main(String[] args) {
        List list = new ArrayList();
        list.add(new Emp());

        List<User> users = list;
        users.add(new User());

        System.out.println(users);	//此时users虽然泛型是User，但是users中有Emp对象，打印不报错
    }											//但是循环遍历会报错
}
class User{
}
class Emp{
}
```

传对象：

public static <T extends User> void test(T t) {  System.out.println(t);  }	允许传入User子类，有上限

public static <T super User> void test(T t) {  System.out.println(t);  }	**报错**，不能传父类对象，不合语法

传类型：

public static <T> void test(Class<? extends User> t) {  System.out.println(t);  }	允许传入User子类，有上限

public static <T> void test(Class<? super User>  t) {  System.out.println(t);  }	允许传入User子类，有上限



#### scala中协变和逆变：

java中不允许子类或父类泛型的对象赋值给带泛型的引用。但是scala有协变和逆变。

val a : AAA[User] = new AAA[SubUser] ()

class AAA[+User]  称为协变，可以将AAA的子类泛型的对象赋给AAA的父类泛型的引用

val a : AAA[User] = new AAA[ParentUser] ()

class AAA[-User]  称为逆变，可以将AAA的子类泛型的对象赋给AAA的父类泛型的引用

逆变就是泛型变成其父类，父类的功能少，所以称为逆变。协变相反。



#### scala中的泛型：

def test**[ T  <:  User ]**( T:t ) :Unit = {}  泛型的上限，可以传入子类

def test**[ T  >:  User ]**( T:t ) :Unit = {}  scala中泛型没有下限，可以传入任意类，底层相当于不加泛型。













![线程安全问题](F:/Typora/图片/线程安全问题.PNG)

如上图不会出现线程安全问题，因为main方法压栈，对象创建在栈中，不会有公用属性。

如果将ss创建在类中方法外，则在只有一个类对象时，需要考虑线程安全问题。



