# 一、Groovy
Groovy是用于Java虚拟机的一种敏捷的动态语言，可以用于面向对象编程，又可以用作纯粹的脚本语言，具有闭包和动态语言中的其他特性。

与Java比较
- Groovy完全兼容Java的语法
- 分号是可选的
- 类、方法默认是pulic的
- 编译器给属性自动添加了getter/setter方法
- 属性可以直接使用点号获取
- 最后一表达式的值会被做为返回值
- ==等同于equals()，不会有NullPointerExceptions异常


Groovy特性
- assert语句
- 可选类型定义
- 可选括号
- 字符串表达方式多样
- 集合API
- 闭包

## 实体类定义
- 分号可省略
- 类、方法默认是pulic的
- 编译器给属性自动添加了getter/setter方法
- 属性可以直接使用点号获取
```
public class ProjectVersion{
    private int major
    private int minor
    public ProjectVersion(int major,int minor) {
        this.major = major
        this.minor = minor
    }
    public int getMajor(){
        major
    }
    public void setMajor(int major){
        this.major = major
    }
}
ProjectVersion v1 = new ProjectVersion(1,1)
println v1.minor
```

## 可选的类型定义
```
def version = 1
```

## assert
```
assert version == 2
```

## 括号可选
```
println(version)
// 等同于
println version
```

## 字符串
```
def s1 = 'imooc' // 单引号表示普通字符串
def s2 = "gradle version is ${version}" // 双引号可以引入变量
def s3 = '''my name
 is imooc '''   // 三引号可换行表示
```

## 集合api
①list
```
def buildTools=['ant','maven']
buildTools << 'gradle'
assert buildTools.getClass() == ArrayList
assert buildTools.size() == 3
```
②map
```
def buildYears = ['ant':2000, 'maven': 2004]
buildYears.gradle = 2009

println buildYears.gradle
println buildYears['gradle']
assert buildYears.getClass() == LinkedHashMap
```

## 闭包
闭包是一个代码块，同方法一样可以有参也可以无参，可以被赋值给一个变量，也可以当作参数传递给一个方法，像普通方法一样调用。
```
// 闭包1
def c1 = {
    v ->
        println v
}
// 闭包2
def c2 = {
    println 'hello'
}
// 方法1以闭包函数作为参数，调用闭包函数时指定了参数'param'
def method1(Closure closure) {   // Closure不能引入java包
    closure('param')
}
// 方法2以闭包函数作为参数，且直接调用闭包函数
def method2(Closure closure) {
    closure()
}

// 方法调用的是有参闭包函数
method1(c1)
// 方法调用的是无参闭包函数
method2(c2)
// 使用匿名闭包函数
method2 {
    println '闭包'
}
// 使用匿名闭包函数，且函数中调用了其他方法
method2 {
    c2()
}

// 输出得到
param
hello
```

## build.gradle文件解析
```
plugins {
    id 'java'
}

// 调用Project.class类的void setGroup(Object var1)方法给属性赋值
group 'org.example'
version '1.0-SNAPSHOT'

sourceCompatibility = 1.8

// void repositories(Closure var1);是以闭包为参数的方法，省略了括号；{mavenCentral()}是匿名闭包函数；
repositories {  
        // 私服
        maven {
            url "http://chenjie.asia/repository/maven-central/"
            credentials {
                username 'admin'
                password 'admin'
            }
        }
        // 本地仓库
        /*
        ①USER_HOME/.m2/settings.xml
        ②M2_HOME/conf/settings.xml
        ③USER_HOME/.m2/repository
         */
        mavenLocal()
        // 中央仓库
        mavenCentral()
}

// void dependencies(Closure var1);是以闭包为参数的方法，省略了括号；{mavenCentral()}是匿名闭包函数；
dependencies {
    testCompile group: 'junit', name: 'junit', version: '4.12'
}
```
>需要注意顺序，如先加载java插件才能设置sourceCompatibility的值。

<br>
# 二、Gradle
![image.png](https://upload-images.jianshu.io/upload_images/21580557-05d4281cc971d61c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 2.1 项目构建
### 2.1.1 打包jar项目
![image.png](https://upload-images.jianshu.io/upload_images/21580557-197fabb955836477.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过Gradle打包成jar，双击Groovy-Tasks-build中的jar即可。如果build.gradle中的插件选择的是java，那么双击build可以达到同样的效果。
```
> Task :compileJava
> Task :processResources NO-SOURCE
> Task :classes
> Task :jar
```
可以看到打包经历了四步，最终可以在build/libs文件夹下可以找到jar包。

### 2.1.2 打包war项目
需要在build.gradle中添加war插件
```
plugins {
    id 'java'
    id 'war'
}

group 'org.example'
version '1.0-SNAPSHOT'

sourceCompatibility = 1.8

repositories {
        // 私服
        maven {
            url "http://chenjie.asia/repository/maven-central/"
            credentials {
                username 'admin'
                password 'admin'
            }
        }
        // 本地仓库
        /*
        ①USER_HOME/.m2/settings.xml
        ②M2_HOME/conf/settings.xml
        ③USER_HOME/.m2/repository
         */
        mavenLocal()
        // 中央仓库
        mavenCentral()
}

dependencies {
    testCompile group: 'junit', name: 'junit', version: '4.12'
}
```

刷新后会出现war选项

![image.png](https://upload-images.jianshu.io/upload_images/21580557-2f464540e6cc73ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

双击war就会开始打war包
```
16:04:39: Executing task 'war'...

> Task :compileJava UP-TO-DATE
> Task :processResources UP-TO-DATE
> Task :classes UP-TO-DATE
> Task :war
```
同样在build/libs下可以找到打完的包。

war包的目录结构如下
```
├── META-INF：存放标签信息
├── WEB-INF：自动生成目录
        └── classes：存放了java字节码文件和resources下的配置文件
        └── lib：存放依赖包
├── index.html
```

将war包放到tomcat的webapps目录下，启动startup.bat，会自动解压war包并完成部署。

## 2.2 构建脚本
### 2.2.1 构建块
Gradle构建中的两个基本概念是项目(project)和任务(task)，每个构建至少包含一个项目，项目中包含一个或多个任务。在多项目构建中，一个项目可以依赖于其他项目；类似的，任务可以形成一个依赖关系图来确保他们的执行顺序。

**项目(project)**
- group、name、version
- plugins、dependencies、repositories、task
- 属性的其他配置方式：ext、gradle.properties

plugins：指定使用的插件
dependencies：声明引入的外部依赖
repositories：依赖的包的仓库
task：声明项目中的任务

**任务(task)**
任务对应org.gradle.api.Task。主要包括任务动作和任务依赖。任务动作定义了一个最小的工作单元。可以定义依赖于其他任务、动作序列和执行条件。

- dependsOn
- doFirst、doLast  <<


我们引入的插件中已经集成了项目和任务，如启动jar打包插件时，会按顺序执行如下任务
```
> Task :compileJava UP-TO-DATE
> Task :processResources UP-TO-DATE
> Task :classes UP-TO-DATE
> Task :jar
```
UP-TO-DATE表示输入没有发生变化，所以跳过当前的步骤。

大多数场景下，我们只需要使用插件即可，只有在插件无法满足需求时，才会需要自己写任务。

### 2.2.2 自定义任务
在build.gradle中添加自定义任务
```
def createDir = {
    path ->
        def dir = new File(path)
        if (!dir.exists()) {
            dir.mkdirs()
        }
}
task makeJavaDir() {
    def paths = ['src/main/java', 'src/main/resources', 'src/test/java', 'src/test/resources']
    doFirst {
        paths.forEach(createDir)
    }
}
task makeWebDir() {
    dependsOn 'makeJavaDir'
    def paths = ['src/main/webapp','src/test/webapp']
    doLast{
        paths.forEach(createDir)
    }
}
```
添加了闭包createDir和自定义任务 makeJavaDir和makeWebDir，且makeWebDir依赖于makeJavaDir 。可以在Tasks-other中找到自定义任务makeJavaDir 和 makeWebDir。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-4c1749ae75cf233e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

双击运行makeWebDir后，可以发现先执行了依赖任务makeJavaDir，然后运行了makeWebDir。


## 2.2.3 构建生命周期

**生命周期为： 初始化 -> 配置 -> 执行**

**配置代码：**即在执行代码前执行的，简单理解就是在doFirst和doLast外的代码；
**执行代码：**简单理解就是在doFirst和doLast中的代码；

![image.png](https://upload-images.jianshu.io/upload_images/21580557-194a8934b6bf569a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上图是在生命周期的每个阶段执行完成后，都会触发一个钩子程序，我们可以通过重写这个钩子程序来完成更加丰富的功能。

## 2.3 依赖管理
几乎所有的基于JVM的软件项目都需要依赖外部类库来重用现有的功能。自动化的依赖管理可以明确依赖的版本，可以解决因传递性依赖带来的版本冲突。

**工件坐标：**即 group、name、version

**常用仓库：** mavenLocal(本地仓库) / mavenCentral(中央仓库) / jcenter(中央仓库) / 自定义maven仓库(私服)
```
// 按配置顺序进行查找
repositories {
    // 私服
    maven {
        url "[私服地址]"
    }
    // 本地仓库
    /* 
    ①USER_HOME/.m2/settings.xml 
    ②M2_HOME/conf/settings.xml
    ③USER_HOME/.m2/repository
     */
    mavenLocal()
    // 中央仓库
    mavenCentral()
}
```

**依赖管理：** 依赖的传递性，版本冲突和作用域（compile/runtime/implementation/testCompile/testRuntime/testImplementation）

**解决版本冲突**
- 查看依赖报告：双击tasks->help->dependencies查看依赖报告
- 排除传递性依赖
   ```
   dependencies {
       compile('org.hibernate:hibernate-core:3.6.3.Final'){
           exclude group:"org.slf4j", module:"slf4j-api"
           //transitive = false  是否传递本身的依赖给宿主程序，默认时true
       }
   }
   ```
- 强制指定一个版本
   ```
   dependencies {
      configurations.all {
          resolutionStrategy{
              force 'org.slf4j:slf4j-api:1.7.24'
          }
      }
   }
   ```
- 修改默认解决策略：
   ```
   dependencies {
      configurations.all {
          resolutionStrategy{
              failOnVersionConflict()
          }
      }
   }
   ```

## 2.4 多项目构建
settings.gradle文件用于多项目构建时，指定当前项目包含的子项目。
```
rootProject.name = 'Groovy'
include 'Mode'
include 'Repository'
include 'Web'
```

### 2.4.1 依赖其他项目
```
dependencies {
    // 表示此项目依赖Mode项目
    compile project(":Mode")
}
```

### 2.4.2 使用父项目同意子项目的配置
**allprojects：**包括父项目和子项目
**subprojects：**只包括子项目，不包括父项目

**①所有项目中应用Java插件**
在父项目的build.gradle中配置
```
allprojects {
    apply plugin: 'java'
    sourceCompatibility = 1.8
    targetCompatibility = 1.8
}
```

**②web子项目打包成War**
在子项目中配置
```
plugin {
    id 'java'
}
```

**③所有项目添加logback日志功能**
在父项目的build.gradle中配置
```
allprojects {
    repositories {
        // 私服
        maven {
            url "http://chenjie.asia/repository/maven-central/"
            credentials {
                username 'admin'
                password 'admin'
            }
        }
        // 本地仓库
        /*
        ①USER_HOME/.m2/settings.xml
        ②M2_HOME/conf/settings.xml
        ③USER_HOME/.m2/repository
         */
        mavenLocal()
        // 中央仓库
        mavenCentral()
    }

    dependencies {
        runtime group: 'ch.qos.logback', name: 'logback-classic', version: '1.2.1'
        testCompile group: 'junit', name: 'junit', version: '4.12'
        compile(group: 'org.hibernate', name: 'hibernate-core', version: '3.6.3.Final'){
            exclude group:"org.slf4j", module:"slf4j-api"
        }
    }
}
```

**④统一配置group和version**
在父项目下创建文件 **gradle.properties**，将group和version作为属性写入文件中
```
group=org.example
version=1.0-SNAPSHOT
```

## 2.5 自动化测试
```
    dependencies {
        testCompile group: 'junit', name: 'junit', version: '4.12'
    }
```
引入测试框架的依赖，其他同maven没啥区别。测试完成后可以在build->reports->index.html中查看页面报告；或在build->test-results中查看xml格式的测试报告。

**测试发现**
- 使用@RunWith
- 使用@Test
- 继承junit.framework.TestCase或groovy.util.GroovyTestCase类

## 2.6 发布
[查看官网配置](https://docs.gradle.org/current/userguide/publishing_maven.html#publishing_maven:tasks)


![image.png](https://upload-images.jianshu.io/upload_images/21580557-d04bad78a9fea485.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以将包部署到本地或直接发布到中央仓库或私有仓库。

**部署到仓库**
引入插件
```
    apply plugin: 'maven-publish'

    publishing {
        publications {
            myPublish(MavenPublication) {
                from components.java
            }
        }
        repositories {
            maven {
                name 'myRepo'
                def releasesRepoUrl = "http://chenjia.asia/repository/maven-releases/"
                def snapshotsRepoUrl = "http://chenjia.asia/repository/maven-snapshots/"
                url = version.endsWith('SNAPSHOT') ? snapshotsRepoUrl : releasesRepoUrl
                credentials {
                    username 'chenjie'
                    password 'chenjie'
                }
            }
        }
    }
```

![image.png](https://upload-images.jianshu.io/upload_images/21580557-7e612bde8d2a03e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- publishMyPublishPublicationToMyRepoRepository：就是我们配置的myPublish方法，MyRepo就是配置的仓库，双击这个选项就会将包推送到远程仓库。可以看到远程仓库中已经部署完成。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-9665c97dd6e80957.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- publishMyPublishPublicationToMavenLocal：就是将包部署到本地仓库，默认路径是`$USER_HOME/.m2/repository`。可以看到已经部署到了本地的maven仓库中。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-ca50fbbf5d9a6b9d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- publishToMavenLocal：将所有包部署到本地
- publish：将所有包推送到远程仓库
