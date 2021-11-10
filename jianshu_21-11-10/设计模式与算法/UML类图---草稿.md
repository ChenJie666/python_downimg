# 一、UML类图
# 1.1 概念
类图(Class diagram)：是显示了模型的静态结构，特别是模型中存在的类、类的内部结构以及它们与其他类的关系等。类图不显示暂时性的信息。类图是面向对象建模的主要组成部分。它既用于应用程序的系统分类的一般概念建模，也用于详细建模，将模型转换成编程代码。类图也可用于数据建模。

# 1.2 类图基础属性
\- 表示private  
\# 表示protected 
\~ 表示default,也就是包权限  
\_ 下划线表示static  
斜体表示抽象  
![image.png](https://upload-images.jianshu.io/upload_images/21580557-6531565891b040d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 1.3 类的关系
**在UML类图中，常见的有以下几种关系: 泛化（Generalization）, 实现（Realization），关联（Association)，聚合（Aggregation），组合(Composition)，依赖(Dependency)。**

**a、实现（Realization）**
表示类对接口的实现。
UML图中实现使用一条带有空心三角箭头的虚线指向接口，如下：
![image](https://upload-images.jianshu.io/upload_images/21580557-7d486ed46c0a4001.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**b、泛化（Generalization）**
表示类与类之间的继承关系、接口与接口之间的继承关系。
UML图中实现使用一条带有空心三角箭头的实线指向基类，如下：
![image](https://upload-images.jianshu.io/upload_images/21580557-97fcee0768da4573.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**c、依赖（Dependency）**
表现为函数中的参数(use a)，是类与类之间的连接，表示一个类依赖于另一个类的定义，其中一个类的变化将影响另外一个类。例如如果A依赖于B，则B体现为局部变量，方法的参数、或静态方法的调用。如电视(TV)依赖于频道(channel)常见的依赖关系如下：
（1）类B以参数的形式传入类A的方法。
（2）类B以局部变量的形式存在于类A的方法中。
（3）类A调用类B的静态方法。
UML图中实现使用一条带有箭头的虚线指向被依赖的类，如下：
![image](https://upload-images.jianshu.io/upload_images/21580557-244f30f90671fe4e.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**d、关联（Association）**
表现为变量(has a)，类与类之间的联接，它使一个类知道另一个类的属性和方法，是依赖关系的特例。例如如果A依赖于B，则B体现为A的全局变量，如person类和company类。

关联关系有双向关联和单向关联：
1、双向关联：两个类都知道另一个类的公共属性和操作。
2、单向关联：只有一个类知道另外一个类的公共属性和操作。
大多数关联应该是单向的，单向关系更容易建立和维护，有助于寻找可服用的类。
UML图中实现使用一条实线连接相同或不同类，如下：
![image](https://upload-images.jianshu.io/upload_images/21580557-87df5116aa2b3ef1.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**e、聚合（Aggregation）**
聚合关系是整体和个体的关系，是关联关系的特例。普通关联关系的两个类处于同一层次上，而聚合关系的两个类处于不同的层次，一个是整体，一个是部分。同时，是一种弱的“拥有”关系。此时整体与部分之间是可分离的，他们可以具有各自的生命周期， 部分可以属于多个整体对象，也可以为多个整体对象共享；比如计算机与CPU、公司与员工的关系等；表现在代码层面，和关联关系是一致的，只能从语义级别来区分。
UML图中实现使用一条带有虚心菱形的线来表示，如下：
![image](https://upload-images.jianshu.io/upload_images/21580557-d5569c8032a6c874.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**f、组合（Composite）**
是关联关系的一种，是比聚合关系强的关联关系。它要求普通的聚合关系中代表整体的对象负责代表部分的对象的生命周期。Composition(组合关系)是一种强的“拥有”关系，体现了严格的部分和整体的关系，部分和整体的生命周期一致。他同样体现整体与部分间的关系，但此时整体与部分是不可分的，整体的生命周期结束也就意味着部分的生命周期结束；比如你和你的大脑，window窗口和frame，在窗口中创建一个frame时必须把它附加到窗口上，当窗口消失时frame也就消失了；表现在代码层面，和关联关系是一致的，只能从语义级别来区分；
UML图中实现使用一条带有实心菱形的线来表示
![image](https://upload-images.jianshu.io/upload_images/21580557-738d3c7b0343d479.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**几种关系所表现的强弱程度依次为：组合>聚合>关联>依赖。**

![image.png](https://upload-images.jianshu.io/upload_images/21580557-368bc62975311020.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



# 二、
