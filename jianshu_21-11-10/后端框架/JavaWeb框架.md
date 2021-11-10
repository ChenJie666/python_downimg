# 一、Web服务器
## 1.1 种类
- IIS：微软开发的Web服务器，Windows中自带

- Tomcat：Tomcat服务器是一个免费开源的Web应用服务器，属于轻量级应用服务器，在中小型系统和并发用户不是很多的场合下被普遍使用，是开发和调试JSP程序的首选。Tomcat运行在JVM之上，它和HTTP服务器一样，绑定IP地址并监听TCP端口，同时还包含以下指责：管理Servlet程序的生命周期将URL映射到指定的Servlet进行处理与Servlet程序合作处理HTTP请求——根据HTTP请求生成HttpServletResponse对象并传递给Servlet进行处理，将Servlet中的HttpServletResponse对象生成的内容返回给浏览器。

- Nginx/Apache：严格的来说，Apache/Nginx 应该叫做「HTTP Server」，一个 HTTP Server 关心的是 HTTP 协议层面的传输和访问控制，所以在 Apache/Nginx 上你可以看到代理、负载均衡等功能；而 Tomcat 则是一个「Application Server」，或者更准确的来说，是一个「Servlet/JSP」应用的容器（Ruby/Python 等其他语言开发的应用也无法直接运行在 Tomcat 上）。

>虽然Tomcat也可以认为是HTTP服务器，但通常它仍然会和Nginx配合在一起使用：动静态资源分离——运用Nginx的反向代理功能分发请求：所有动态资源的请求交给Tomcat，而静态资源的请求（例如图片、视频、CSS、JavaScript文件等）则直接由Nginx返回到浏览器，这样能大大减轻Tomcat的压力。负载均衡，当业务压力增大时，可能一个Tomcat的实例不足以处理，那么这时可以启动多个Tomcat实例进行水平扩展，而Nginx的负载均衡功能可以把请求通过算法分发到各个不同的实例进行处理。

## 1.2 Tomcat服务器
### 1.2.1 目录结构
Tomcat
└─bin  启动脚本
└─conf  配置文件
└─lib  依赖
└─logs  日志
└─temp  临时文件
└─webapps  项目目录
    └─docs
    └─examples
    └─host-manager
    └─manager
    └─ROOT  默认访问的项目
└─work  Tomcat工作目录

### 1.2.2 idea启动Tomcat
![image.png](https://upload-images.jianshu.io/upload_images/21580557-1515e09b8e0e8190.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>**Deployment Descriptors：**是添加的描述文件web.xml。
**Web Resource Directory：**项目文件所在的目录。
**PathRelativeToDeploymentRoot：**编译后的资源的相对路径。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-40f6abe4e4fc4559.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>URL就是默认打开的页面

![image.png](https://upload-images.jianshu.io/upload_images/21580557-982b669a2ca7ab45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>Application context是项目环境，也是浏览器解析的上下文路径。

**举个例子**
如Application Context是`/cj`，PathRelativeToDeploymentRoot是 `/hhh`；那么访问资源路径就是`localhost:8080/cj/test`；
浏览器解析时，项目路径是/cj/test；
后台解析时，项目路径是编译后的路径;

### 1.2.3 demo
**乱码解决：**
1. setCharacterEncoding("utf-8"); 或 Content-Type:text/html; charset=UTF-8
2. 使用URLDecoder.decode(cookie.getValue(), "UTF-8");
#### 1.2.3.1 html静态文件
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>Title</title>
</head>
<body>
<h1>我是导航栏</h1>
</body>
</html>
```

#### 1.2.3.2 servlet
**依赖**
```
    <!--如下两个依赖都可以，tomcat的lib目录中使用第二个依赖的包-->
<!--    <dependency>-->
<!--      <groupId>javax.servlet</groupId>-->
<!--      <artifactId>javax.servlet-api</artifactId>-->
<!--      <version>4.0.1</version>-->
<!--    </dependency>-->
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>servlet-api</artifactId>
      <version>2.5</version>
    </dependency>
```
**接口**
```
public class HelloWorld extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html");
        resp.setCharacterEncoding("utf-8");
        PrintWriter writer = resp.getWriter();
        writer.write("<html>");
        writer.write("<head>");
        writer.write("<title>Hello Test</title>");
        writer.write("</head>");
        writer.write("<body>");
        writer.write("<h1>HelloWorld 测试</h1>");
        writer.write("</body");
        writer.write("</html>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
```
**web.xml配置映射**
```
<!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >

<web-app>
  <display-name>Archetype Created Web Application</display-name>

  <servlet>
    <servlet-name>helloworld</servlet-name>
    <servlet-class>com.cj.javaweb.HelloWorld</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>/hellotest</url-pattern>
  </servlet-mapping>

</web-app>
```

#### 1.2.3.3 jsp动态文件
**依赖**
```
 <!--如下两个依赖都可以，tomcat的lib目录中使用第二个依赖的包-->
    <!-- jsp依赖 -->
<!--    <dependency>-->
<!--      <groupId>javax.servlet.jsp</groupId>-->
<!--      <artifactId>javax.servlet.jsp-api</artifactId>-->
<!--      <version>2.3.3</version>-->
<!--    </dependency>-->
    <dependency>
      <groupId>javax.servlet.jsp</groupId>
      <artifactId>jsp-api</artifactId>
      <version>2.1</version>
    </dependency>
```
**login.jsp页面**
```
<%@page contentType="text/html; charset=UTF-8"  language="java" %>
<html>
<body>
<h2>Login</h2>
<form action="${pageContext.request.contextPath}/login" method="get">
    账号：<input type="text" name="username"> <br>
    密码：<input type="password" name="password"> <br>
    <input type="submit">
</form>
</body>
</html>
```
**代码**
```
public class LoginServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");

        PrintWriter writer = resp.getWriter();
        writer.println(username + ":" + password);
//        resp.sendRedirect("/cj/success.jsp");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
**web.xml**
```
  <servlet>
    <servlet-name>login</servlet-name>
    <servlet-class>com.cj.response.LoginServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>login</servlet-name>
    <url-pattern>/login</url-pattern>
  </servlet-mapping>
```

<br>
# 二、Servlet
jservlet规范包括三个技术点：servlet ；listener ；filter。
## 2.1 概念
Servlet就是sun公司开发动态web的一门技术，Sun在这些API中提供一个接口叫做：Servlet。把实现了Servlet接口的Java程序叫做Servlet。
可以把Servlet简单理解为运行在服务端的Java小程序，但是Servlet没有main方法，不能独立运行，因此必须把它部署到Servlet容器中，由容器来实例化并调用Servlet。
而Tomcat和Jetty就是一个Servlet容器。为了方便使用，它们也具有HTTP服务器的功能，因此Tomcat或者Jetty就是一个“HTTP服务器 + Servlet容器”，我们也叫它们Web容器。



![image.png](https://upload-images.jianshu.io/upload_images/21580557-736a5743b85d8bcf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Servlet技术是Web开发的原点，几乎所有的Java Web框架（比如Spring）都是基于Servlet的封装，Spring应用本身就是一个Servlet，而Tomcat和Jetty这样的Web容器，负责加载和运行Servlet。你可以通过下面这张图来理解Tomcat和Jetty在Web开发中的位置。


<br>
## 2.2 运行原理
Servlet是由Web服务器调用，web服务器在收到浏览器请求之后，由web容器调用Servlet的service方法，将Request和Response对象作为参数传入，进行处理。

1. client点击一个URL，其URL指向一个servlet；
2. 容器识别出这个请求索要的是一个servlet，所以创建两个对象：httpservletrequest、httpservletresponse；
3. 容器根据请求中的URL找到对应的servlet，为这个请求创建或分配一个线程，并把两个对象request和response传递到servlet线程中；
4. 容器调用servlet的service方法。根据请求的不同类型，service方法会调用doGet或者doPost方法；
5. service方法生成动态页面，然后把这个页面填入到response对象中；
6. 线程结束，容器把response对象转换成http响应，传回client，并销毁response和request对象；
![image.png](https://upload-images.jianshu.io/upload_images/21580557-858bab3f8803fbfc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<br>
## 2.3 映射路径

如果想开发一个Servlet程序，只需要完成两个步骤
- 编写一个类实现Servlet接口(可以继承HttpServlet)
- 把开发好的Java类部署到web服务器中


**1. 一个Servlet可以指定多个映射路径**
```
  <servlet>
    <servlet-name>helloworld</servlet-name>
    <servlet-class>com.cj.javaweb.HelloWorld</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>/hello1</url-pattern>
  </servlet-mapping>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>/hello2</url-pattern>
  </servlet-mapping>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>/hello3</url-pattern>
  </servlet-mapping>
```

**2. 一个Servlet可以指定通用映射路径**
```
  <servlet>
    <servlet-name>helloworld</servlet-name>
    <servlet-class>com.cj.javaweb.HelloWorld</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>/*</url-pattern>
  </servlet-mapping>
  <servlet>
    <servlet-name>error</servlet-name>
    <servlet-class>com.cj.javaweb.Error</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>error</servlet-name>
    <url-pattern>/error</url-pattern>
  </servlet-mapping>
```
>优先级：确定的路径 > 通用路径 > index索引页

**3. 一个Servlet可以指定通用映射路径**
```
  <servlet>
    <servlet-name>helloworld</servlet-name>
    <servlet-class>com.cj.javaweb.HelloWorld</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>/test/*</url-pattern>
  </servlet-mapping>
```

**4. 指定路径后缀**
```
  <servlet>
    <servlet-name>helloworld</servlet-name>
    <servlet-class>com.cj.javaweb.HelloWorld</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>helloworld</servlet-name>
    <url-pattern>*.do</url-pattern>
  </servlet-mapping>
```
>如果指定后缀，<url-pattern>/*.do</url-pattern>或url-pattern>/test/*.do</url-pattern>这种格式是错误的，通配符前不能有路径。

<br>
## 2.4 ServletContext
ServletContext对象是一个应用上下文对象，也是一个域对象。表示Servlet应用程序，每个web应用程序都只有一个ServletContext对象。ApplicationContext对在ServletContext进行了封装。

**ServletContext对象的作用：**
1. 有了ServletContext对象,就可以共享从应用程序中的所有资源访问到的数据信息,并且可以动态注册web对象。
2. 可以获得应用域的全局初始化参数，以及达到Servlet之间的数据共享；
3. 可以作为域对象在整个应用中共享数据；域对象即在一定的作用范围内实现资源共享；
4. 可以用来获取应用中的资源在服务器上的绝对路径；
5. 获取文件的mime类型: 在网络传输中，并不是以扩展名来区分文件的类型，都是以mime类型；如：text/html；表示一个html文件。

生命周期： 应用一加载则创建，应用被停止则销毁
创建时间： 加载web应用时，创建ServletContext对象。

<br>
**获取ServletContext方法**
在HttpServlet类中
- `ServletContext context = this.getServletContext();`

在JSP的代码块中
- `this.getServletConfig().getServletContext()`
- `application.getContext()`

<br>
**ServletContext的属性设置和获取**
设置上下文内容
```
public class SetValue extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        ServletContext context = this.getServletContext();
        context.setAttribute("username","zhangsan");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
获取上下文内容
```
public class Context extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        ServletContext context = this.getServletContext();
        String username = (String) context.getAttribute("username");

        resp.setContentType("text/html");
        resp.setCharacterEncoding("utf-8");
        PrintWriter writer = resp.getWriter();
        writer.println("<h1>" + username + "</h1>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
>注意：启动项目后，如果直接请求context映射的路径，返回值为null；因为只有第一次访问时才会构建servlet，所以需要先请求SetValue映射的路径才能在上下文对象中设置属性。

<br>
**ServletContext的初始属性设置和获取**
```
public class InitParam extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        ServletContext context = this.getServletContext();
        String url = context.getInitParameter("url");

        resp.setContentType("text/html");
        resp.setCharacterEncoding("utf-8");
        PrintWriter writer = resp.getWriter();
        writer.println("<h1>url: " + url + "</h1>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
```
web.xml
```
  <context-param>
    <param-name>url</param-name>
    <param-value>jdbc:mysql://chenjie.aisa:3306/test</param-value>
  </context-param>
  <servlet>
    <servlet-name>initParam</servlet-name>
    <servlet-class>com.cj.javaweb.InitParam</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>initParam</servlet-name>
    <url-pattern>/initParam</url-pattern>
  </servlet-mapping>
```

<br>
**ServletContext的请求转发**
```
public class ReqDispatcher extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        ServletContext context = this.getServletContext();
        RequestDispatcher dispatcher = context.getRequestDispatcher("/error");
        dispatcher.forward(req,resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
```
  <servlet>
    <servlet-name>dispatcher</servlet-name>
    <servlet-class>com.cj.javaweb.ReqDispatcher</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>dispatcher</servlet-name>
    <url-pattern>/disp</url-pattern>
  </servlet-mapping>
```
>注意转发和重定向的区别：转发时访问路径不会跳转，状态码为307，客户端只进行一次访问。重定向时访问路径会跳转，状态码为302，客户端进行两次访问。

<br>
**读取资源文件**
```
public class ReadProp extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        ServletContext context = this.getServletContext();
        InputStream is = context.getResourceAsStream("/WEB-INF/classes/db.properties");

        Properties prop = new Properties();
        prop.load(is);
        String username = prop.getProperty("username");
        String password = prop.getProperty("password");

        resp.setContentType("text/html");
        resp.setCharacterEncoding("utf-8");
        PrintWriter writer = resp.getWriter();
        writer.println(username + ":" + password);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
```
  <servlet>
    <servlet-name>readprop</servlet-name>
    <servlet-class>com.cj.javaweb.ReadProp</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>readprop</servlet-name>
    <url-pattern>/readprop</url-pattern>
  </servlet-mapping>
```
>resources和java都是classpath，这两个文件夹下的配置文件在编译后会被放到/WEB-INF/classes文件夹下，访问时只需要在写上相对路径即可。

<br>
## 2.5 Http响应
### 2.5.1 相关概念
Cache-Control:private   缓存控制
Connection:Keep-Alive  连接
Content-Encoding:gzip  编码
Content-Type:text/html; charset=UTF-8  类型

**响应体**
Accept： 告诉浏览器，它所支持的数据类型
Accept-Encoding： 支持那种编码格式  GBK  UTF-8  GB2312  ISO8859-1
Accept-Language： 告诉浏览器，它的语言环境
Cache-Control： 缓存控制
Connection： 告诉浏览器，请求完成是断开还是保持连接
HOST： 主机
Refresh： 告诉客户端，多久刷新一次
Location： 让网页重新定位

**状态响应码**
200：请求响应成功
3xx：请求重定向
4xx：无法获取资源
5xx：服务器错误   502：网关错误

<br>
### 2.5.2 HttpServletResponse
#### 2.5.2.1 方法
负责向浏览器发送请求头的方法
```java
public void setCharacterEncoding(String charset);
public void setContentLength(int len);
public void setContentLengthLong(long len);
public void setContentType(String type);
```
```

```


<br>
#### 2.5.2.2 功能实现
**向浏览器输出消息**
```
public class HelloWorld extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html");
        resp.setCharacterEncoding("utf-8");
        PrintWriter writer = resp.getWriter();
        writer.write("<h1>HelloWorld 测试</h1>");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
```
**请求下载文件**
```
public class FileServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        // 1. 获取需要下载的文件的输入流
//        String realPath = this.getServletContext().getRealPath("/1.jpg");
        String realPath = "C:\\Users\\Administrator\\Desktop\\UselessProject\\javaweb-demo\\response\\src\\main\\resources";
        String fileName = "1.jpg";
        FileInputStream fis = new FileInputStream(realPath + "\\" + fileName);

        // 2. 设置响应头，让浏览器下载文件(如果不设置，会显示图片而不会下载);中文文件名使用URLEncoder.encode编码，否则有可能乱码
        resp.setHeader("Content-Disposition","attachment; filename=" + fileName + URLEncoder.encode(fileName,"UTF-8"));

        // 3. 获取响应的输出流
        ServletOutputStream os = resp.getOutputStream();

        // 4. 创建缓冲区，将FileOutputStream通过缓冲区写入到响应中
        byte[] buffer = new byte[1024];
        int len = 0;
        while ((len = fis.read(buffer)) > 0) {
            os.write(buffer,0,len);
        }

        fis.close();
        os.close();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
```
  <servlet>
    <servlet-name>down</servlet-name>
    <servlet-class>com.cj.response.FileServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>down</servlet-name>
    <url-pattern>/down</url-pattern>
  </servlet-mapping>
```

**验证码功能**
```
public class ImageServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        BufferedImage image = new BufferedImage(80, 20, BufferedImage.TYPE_INT_RGB);
        Graphics2D graphics = (Graphics2D) image.getGraphics();
        graphics.setColor(Color.WHITE);
        graphics.fillRect(0, 0, 80, 20);
        graphics.setColor(Color.RED);
        graphics.setFont(new Font(null, Font.BOLD, 20));
        graphics.drawString(getRandom(), 0, 20);

        resp.setContentType("image/jpg");
        resp.setHeader("refresh", "5");  // 页面5s刷新一次
        resp.setDateHeader("expires", -1);  // 不过期
        resp.setHeader("Cache-Control", "no-cache");  // 不缓存
        resp.setHeader("Pragma", "no-cache");  // 不缓存

        ImageIO.write(image, "jpg", resp.getOutputStream());
    }

    private String getRandom() {
        Random random = new Random();
        StringBuilder rand = new StringBuilder(random.nextInt(999999) + "");
        System.out.println("rand: " + rand);
        for (int i = 0; i < 7 - rand.length(); i++) {
            rand.append("0");
        }
        return rand.toString();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
```
```
  <servlet>
    <servlet-name>code</servlet-name>
    <servlet-class>com.cj.response.ImageServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>code</servlet-name>
    <url-pattern>/code</url-pattern>
  </servlet-mapping>
```

**实现重定向**
```
public class RedirectServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
//        resp.setHeader("Location","/cj/code");
//        resp.setStatus(302);

        resp.sendRedirect("/cj/code");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
>通过sendRedirect进行重定向。也可以设置请求头Location和状态码302实现重定向。
```
  <servlet>
    <servlet-name>redirect</servlet-name>
    <servlet-class>com.cj.response.RedirectServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>redirect</servlet-name>
    <url-pattern>/redirect</url-pattern>
  </servlet-mapping>
```

<br>
## 2.6 Http请求
### 2.6.1 相关概念
与Http响应相对应。

<br>
## 2.6.2 HttpServletRequest
HttpServletRequest代表客户端的请求，用户通过Http协议访问服务器，Http请求中的所有信息被封装到HttpServletRequest，通过这个HttpServletRequest的方法，获得请求的信息。

**获取前端参数并请求转发**
**login.jsp**文件转发
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>

<div>
    <h2>Login</h2>
    <form action="${pageContext.request.contextPath}/login" method="post">
        账号: <input type="text" name="username"> <br>
        密码: <input type="password" name="password"> <br>

        爱好:
        <input type="checkbox" name="hobby" value="代码">代码
        <input type="checkbox" name="hobby" value="游戏">游戏
        <input type="checkbox" name="hobby" value="运动">运动

        <br>
        <input type="submit">
    </form>
</div>
<body>

</body>
</html>
```
```
public class LoginServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("utf-8");
        resp.setCharacterEncoding("utf-8");

        String username = req.getParameter("username");
        String password = req.getParameter("password");
        String[] hobbies = req.getParameterValues("hobby");

        System.out.println(username);
        System.out.println(password);
        System.out.println(Arrays.toString(hobbies));


        System.out.println(this.getServletContext().getContextPath());
        RequestDispatcher dispatcher = req.getRequestDispatcher("/success.jsp");
        dispatcher.forward(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
```
>需要注意在java代码，jps动态页面及html静态页面中的项目路径。
>- 在java代码中，"/"已经表示了项目路径，即上面这段代码中到的"/success.jsp"已经表示了访问路径"/cj/success.jsp"。
>- 在jps动态页面中，需要使用"\${pageContext.request.contextPath}"来获取项目路径，所以访问"/cj/login.jsp"文件的路径表示"\${pageContext.request.contextPath}/login"。

<br>
# 三、Cookie和Session
**会话：**会话是指从一个浏览器窗口打开到关闭的过程。

**保存会话的两种技术**
- Cookie：客户端行为，将用户信息保存在cookie中，请求时发送给服务器。
- Session：服务器行为，利用这个技术，可以保存用户的会话信息。可以把用户信息和数据放到session中。

## 3.1 Cookie
客户端中存储的Cookies是一个个键值对。
- Cookies是Cookie的数组，一个Cookie只能保存一个信息
- 一个web站点可以给浏览器发送多个cookie，最多存放20个cookie
- Cookie大小限制为4kb
- 300个cookie是浏览器上限
- cookie存储在本地用户目录下的appdata文件夹中

```
public class CookieServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("utf-8");
        resp.setHeader("Content-Type", "text/html; charset=UTF-8");

        // 获取cookies
        Cookie[] cookies = req.getCookies();

        // 遍历请求中携带的cookies
        Long lastVisit = null;
        for (Cookie cookie : cookies) {
            if ("lastVisit".equals(cookie.getName())) {
                lastVisit = Long.parseLong(cookie.getValue());
            }
        }

        // 判断Cookie中的属性是否存在，不存在说明第一次登陆
        PrintWriter out = resp.getWriter();
        if (Objects.isNull(lastVisit)) {
            out.println("第一次访问");
        } else {
            Date date = new Date(lastVisit);
            out.println("上次登陆时间为" + new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date));
        }

        // 将本次登陆时间写入到Cookie中
        long currentTimeMillis = System.currentTimeMillis();
        Cookie cookie = new Cookie("lastVisit", String.valueOf(currentTimeMillis));
        // 过期时间为-1表示cookie永不过期，设置为0表示删除浏览器端的cookie(cookie马上过期)
        cookie.setMaxAge(-1);
        resp.addCookie(cookie);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
```

**如何删除cookie**
- 不设置有效期，关闭浏览器自动失效
- 将cookie的过期时间设置为0，`cookie.setMaxAge(-1);`


<br>
## 3.2 Session
服务器会将客户端信息保存在session中，然后返回给客户端一个cookie记录了sessionId(cookie的name为JSESSIONID)，请求时就可以通过sessionId获取到session。

- 服务器会给每一个客户端创建一个Session；
- 一个Session独占一个客户端，只要客户端没有关闭，这个Session就存在；
- 用户登录之后，下次访问就可以获取session中的数据。

```
public class SessionServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        resp.setCharacterEncoding("UTF-8");

        // 通过request中的JSESSIONID获取session对象
        HttpSession session = req.getSession();
        // 在session中设置属性
        session.setAttribute("name","zhangsan");


        // 从session中获取属性
        String name = session.getAttribute("name").toString();

        // 获取sessionId，判断session是不是这次请求时创建的
        PrintWriter out = resp.getWriter();
        out.println("sessionId:" + session.getId() + " --- isNew:" + session.isNew() + " --- name:" + name);

    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
```
public class Session2Servlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession();
        // 删除session中的属性
        session.removeAttribute("name");
        // 手动注销session
        session.invalidate();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```
Session过期配置，单位为分钟
```
  <session-config>
    <session-timeout>1</session-timeout>
  </session-config>
```

<br>
# 四、Jps
Java Server Pages：Java服务器端页面，也和Servlet一样，用于动态Web技术。Jsp页面中可以嵌入Java代码，为用户提供动态数据。
注意与JS(javascript)区分，JS是一种基于对象的客户端脚本语言，运行在浏览器等前端中。JSP是运行在后端的，实质是java程序。

可以在用户目录下找到Idea的工作目录，然后在tomcat目录下可以找到jps文件已经被编译成了java文件(在第一次访问时进行编译)。我的目录路径如下
`C:\Users\Administrator\AppData\Local\JetBrains\IntelliJIdea2020.1\tomcat\Unnamed_projectname\work\Catalina\localhost\cj\org\apache\jsp`

![image.png](https://upload-images.jianshu.io/upload_images/21580557-979324555c4d519f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 4.1 JSP编译文件
我们打开路径下由jsp文件解析成的java类
如下JSP文件
```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    String name = "zhangsan";
%>
name:<%=name%>
</body>
</html>
```
经过编译后得到
```
public final class form_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

  private static final javax.servlet.jsp.JspFactory _jspxFactory =
          javax.servlet.jsp.JspFactory.getDefaultFactory();

  private static java.util.Map<java.lang.String,java.lang.Long> _jspx_dependants;

  private static final java.util.Set<java.lang.String> _jspx_imports_packages;

  private static final java.util.Set<java.lang.String> _jspx_imports_classes;

  static {
    _jspx_imports_packages = new java.util.HashSet<>();
    _jspx_imports_packages.add("javax.servlet");
    _jspx_imports_packages.add("javax.servlet.http");
    _jspx_imports_packages.add("javax.servlet.jsp");
    _jspx_imports_classes = null;
  }

  private volatile javax.el.ExpressionFactory _el_expressionfactory;
  private volatile org.apache.tomcat.InstanceManager _jsp_instancemanager;

  public java.util.Map<java.lang.String,java.lang.Long> getDependants() {
    return _jspx_dependants;
  }

  public java.util.Set<java.lang.String> getPackageImports() {
    return _jspx_imports_packages;
  }

  public java.util.Set<java.lang.String> getClassImports() {
    return _jspx_imports_classes;
  }

  public javax.el.ExpressionFactory _jsp_getExpressionFactory() {
    if (_el_expressionfactory == null) {
      synchronized (this) {
        if (_el_expressionfactory == null) {
          _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
        }
      }
    }
    return _el_expressionfactory;
  }

  public org.apache.tomcat.InstanceManager _jsp_getInstanceManager() {
    if (_jsp_instancemanager == null) {
      synchronized (this) {
        if (_jsp_instancemanager == null) {
          _jsp_instancemanager = org.apache.jasper.runtime.InstanceManagerFactory.getInstanceManager(getServletConfig());
        }
      }
    }
    return _jsp_instancemanager;
  }

  public void _jspInit() {
  }

  public void _jspDestroy() {
  }

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    if (!javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSP 只允许 GET、POST 或 HEAD。Jasper 还允许 OPTIONS");
        return;
      }
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");

    String name = "zhangsan";

      out.write("\r\n");
      out.write("name:");
      out.print(name);
      out.write("\r\n");
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
```
通过上述源码，可以得到一下几点
- 有多个内置的对象
   ```
   final javax.servlet.jsp.PageContext pageContext;  // 页面上下文
   javax.servlet.http.HttpSession session = null; //session
   final javax.servlet.ServletContext application; //应用上下文
   final javax.servlet.ServletConfig config; //config
   javax.servlet.jsp.JspWriter out = null;  //out
   final java.lang.Object page = this;  //page
   javax.servlet.http.HttpServletRequest request //请求
   javax.servlet.http.HttpServletResponse response //响应
   ```
   在Jsp文件转为java文件时，这些对象都会实例化，所以在Jsp中可以直接使用这些对象。
- Jsp文件转换为Java代码时，对于html代码，通过write方法输出到输出流，对于java代码会原封不懂输出。



<br>
## 4.2 HttpJspBase
发现这个类继承自HttpJspBase类，我们要查看这个类的源码，就需要导包。
在Tomcat的lib目录下有jasper.jar的包，这个包可以将Jsp文件解析为java文件。在maven中引入这个包
```
    <dependency>
      <groupId>org.apache.tomcat</groupId>
      <artifactId>jasper</artifactId>
      <version>6.0.53</version>
    </dependency>
```
查看关键类HttpJspBase源码
```
public abstract class HttpJspBase extends HttpServlet implements HttpJspPage {
    protected HttpJspBase() {
    }

    public final void init(ServletConfig config) throws ServletException {
        super.init(config);
        this.jspInit();
        this._jspInit();
    }

    public String getServletInfo() {
        return Localizer.getMessage("jsp.engine.info");
    }

    public final void destroy() {
        this.jspDestroy();
        this._jspDestroy();
    }

    public final void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this._jspService(request, response);
    }

    public void jspInit() {
    }

    public void _jspInit() {
    }

    public void jspDestroy() {
    }

    protected void _jspDestroy() {
    }

    public abstract void _jspService(HttpServletRequest var1, HttpServletResponse var2) throws ServletException, IOException;

    static {
        if (JspFactory.getDefaultFactory() == null) {
            JspFactoryImpl factory = new JspFactoryImpl();
            if (System.getSecurityManager() != null) {
                String basePackage = "org.apache.jasper.";

                try {
                    factory.getClass().getClassLoader().loadClass(basePackage + "runtime.JspFactoryImpl$PrivilegedGetPageContext");
                    factory.getClass().getClassLoader().loadClass(basePackage + "runtime.JspFactoryImpl$PrivilegedReleasePageContext");
                    factory.getClass().getClassLoader().loadClass(basePackage + "runtime.JspRuntimeLibrary");
                    factory.getClass().getClassLoader().loadClass(basePackage + "runtime.JspRuntimeLibrary$PrivilegedIntrospectHelper");
                    factory.getClass().getClassLoader().loadClass(basePackage + "runtime.ServletResponseWrapperInclude");
                    factory.getClass().getClassLoader().loadClass(basePackage + "servlet.JspServletWrapper");
                } catch (ClassNotFoundException var3) {
                    LogFactory.getLog(HttpJspBase.class).error("Jasper JspRuntimeContext preload of class failed: " + var3.getMessage(), var3);
                }
            }

            JspFactory.setDefaultFactory(factory);
        }

    }
}
```
发现这个类继承自HttpServlet 类，也有类似init、service和destroy的方法，即_jspInit、_jspService和_jspDestroy。

<br>
## 4.3 JSP基础语法
**依赖**
```
    <!-- servlet依赖 -->
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>servlet-api</artifactId>
      <version>2.5</version>
    </dependency>
    <!-- jsp依赖 -->
    <dependency>
      <groupId>javax.servlet.jsp</groupId>
      <artifactId>jsp-api</artifactId>
      <version>2.1</version>
    </dependency>
    <!-- JSTL表达式依赖 -->
    <dependency>
      <groupId>javax.servlet.jsp.jstl</groupId>
      <artifactId>jstl-api</artifactId>
      <version>1.2</version>
    </dependency>
    <!-- standard标签库 -->
    <dependency>
      <groupId>taglibs</groupId>
      <artifactId>standard</artifactId>
      <version>1.1.2</version>
    </dependency>
```

### 4.3.1 Jsp表达式
使用`<%= %>`进行输出
```
<%--JSP表达式作用：用来将程序结果输出到客户端--%>
<%= new java.util.Date()%>
```

### 4.3.2 Jsp脚本片段
使用`<% %>`进行输出
```
<%--JSP脚本片段--%>
<%
    int sum = 0;
    for (int i = 0; i < 100; i++) {
        sum += i;
    }
    out.print(sum);
%>
<%= sum%>
```
不同脚本片段之间的变量是共享的，因为实际解析到Java文件时，它们都是在同一个类的_jspService方法中。

如下脚本片段解析到Java代码是怎样的呢？
```jsp
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    for (int i = 0; i < 5; i++) {
%>
<h1>第 <%=i+1%> 次循环</h1>
<%
    }
%>
</body>
</html>
```
解析得到
```
      out.write("\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");

    for (int i = 0; i < 5; i++) {

      out.write("\r\n");
      out.write("<h1>第 ");
      out.print(i+1);
      out.write(" 次循环</h1>\r\n");

    }

      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
```
>可以发现，jsp文件中的java代码保持不变，html代码通过write方法输出到前端。

### 4.3.3 JSP声明
使用`<%! %>`进行声明
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%!
    static {
        System.out.println("进入static静态代码块");
    }

    private String name;

    public void setName(String name){
        this.name = name;
    }
%>
<%
    setName("zhangsan");
%>
name:<%=name%>
</body>
</html>
```
解析后得到的java部分源码如下
```
public final class test3_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {
    static {
        System.out.println("进入static静态代码块");
    }

    private String name;

    public void setName(String name){
        this.name = name;
    }

   ......

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    if (!javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSP 只允许 GET、POST 或 HEAD。Jasper 还允许 OPTIONS");
        return;
      }
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write('\r');
      out.write('\n');

    setName("zhangsan");

      out.write("\r\n");
      out.write("name:");
      out.print(name);
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
```
>可以发现`<%! %>`中的代码会编译到Java类中；其他的会生成到_jspService方法中！

<br>
## 4.3.4 注释
JSP中可以通过两种方式进行注释
```
<!-- HTML注释 -->
<%-- JSP注释 --%>
```
区别就是，HTML注释可以在网页源码中看到，而JSP注释不会输出到前端。


<br>
## 4.4 JSP指令
### 4.4.1 三个编译指令
#### page指令
**语法结构：<%page %>**
- <%@page language="java"%> ---- 这个属性用于设定jsp的编程语言，目前java是唯一有效的编程语言。
- <%@page extends=""%> ---- 我们知道jsp的底层其实是Servlet，这里的这个属性就是指我们的这个jsp是继承那个Servlet的。这个我们一般不做修改，默认继承的是HttpJspBase.
- <%@page erropage=""%> ---- 发生异常时跳转的资源
- <%@page isErrotpage=""%> ---- 默认为false，即响应的状态码为200；设置成true，响应的状态码为500。
- <%@page contentType="text/html;charset=UTF-8"%> ---- 用于设置文件格式和编码格式。
- <%@page session="true"%> ---- 指的是该页面是否可以用到Session对象，说白了就是设置该页面有没有资格参与http会话。
- <%@page import="java.util.Date"%> ---- 导包
- <%@page buffer=""%> ---- 指定到客户输出流的缓冲模式。如果为none，则不缓冲；如果指定数值，那么输出就用不小于这个值的缓冲区进行缓冲。与autoFlash一起使用。默认不小于8KB，根据不同的服务器可设置。例如，buffer="64kb"。
- <%@page autoFlash=""%> ---- 如果为true缓冲区满时，到客户端输出被刷新；如果为false缓冲区满时，出现运行异常，表示缓冲区溢出。默认为true，例如autoFlash="true"。
- <%@page info=""%> ---- 关于JSP页面的信息，定义一个字符串，可以使用servlet.getServletInfo()获得。 默认省略。例如，info="测试页面"。
- <%@page isThreadSafe=""%> ---- 用来设置JSP文件是否能多线程使用。如果设置为true，那么一个JSP能够同时处理多个用户的请求；相反，如果设置为false，一个JSP只能一次处理一个请求。例如，isThreadSafe="true"。
- <%@page  pageEncoding=""%> ---- JSP页面的字符编码 ，默认值为pageEncoding="iso-8859-1"，例如pageEncoding="gb2312"。

#### include指令
**语法结构：<%include file=" "%>** 

把外部的一个jsp页面加载到当前的jsp页面中，但要注意，jsp页面只能解析静态的外部jsp页面。这样就可以通过标签来实现逻辑处理，如if、forEach等操作。

#### taglib指令
**语法结构：<%@taglib uri="" prefix="">** 
这个指令是引入标签库(jstl)或者自定义标签库的一个指令，以弥补HTML标签库的不足。

**如引入核心库 `<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>`后可以使用如下标签：**
| 标签            | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| \<c:out>        | 用于在JSP中显示数据，就像<%= ... >                           |
| \<c:set\>       | 用于保存数据                                                 |
| \<c:remove\>    | 用于删除数据                                                 |
| \<c:catch>      | 用来处理产生错误的异常状况，并且将错误信息储存起来           |
| \<c:if\>        | 与我们在一般程序中用的if一样                                 |
| \<c:choose\>    | 本身只当做\<c:when\>和\<c:otherwise\>的父标签                |
| \<c:when\>      | \<c:choose\>的子标签，用来判断条件是否成立                   |
| \<c:otherwise\> | \<c:choose\>的子标签，接在\<c:when\>标签后，当\<c:when\>标签判断为false时被执行 |
| \<c:import\>    | 检索一个绝对或相对 URL，然后将其内容暴露给页面               |
| \<c:forEach\>   | 基础迭代标签，接受多种集合类型                               |
| \<c:forTokens\> | 根据指定的分隔符来分隔内容并迭代输出                         |
| \<c:param\>     | 用来给包含或重定向的页面传递参数                             |
| \<c:redirect\>  | 重定向至一个新的URL.                                         |
| \<c:url\>       | 使用可选的查询参数来创造一个URL                              |

**依赖**
```
    <!-- JSTL表达式依赖 -->
    <dependency>
      <groupId>javax.servlet.jsp.jstl</groupId>
      <artifactId>jstl-api</artifactId>
      <version>1.2</version>
    </dependency>
```

**例1**
通过<c:if test=""/>进行if判断
```
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <c:if test="${param.username=='admin'}" var="isAdmin">
        <c:out value="欢迎管理员: ${param.username}"/>
    </c:if>
    <c:out value="${isAdmin}"/>
</body>
</html>
```

**例2**
复制变量，通过<c:choose>和<c:when>标签进行判断
```
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<c:set var="score" value="85"/>

<c:choose>
    <c:when test="${score>90}">
        <c:out value="great"/>
    </c:when>
    <c:when test="${score>=60}">
        <c:out value="good"/>
    </c:when>
    <c:when test="${score<60}">
        <c:out value="bad"/>
    </c:when>
</c:choose>

</body>
</html>
```

**例3**
<c:forEach > 遍历数组，可以指定起止和步长等。
```
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<%@ page import="java.util.ArrayList" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    ArrayList<String> list = new ArrayList<>();
    list.add("zhangsan");
    list.add("lisi");
    list.add("wangwu");
    list.add("zhaoliu");
    list.add("tianqi");
    session.setAttribute("peoples", list);
%>

<c:forEach var="people" items="${peoples}">
    <c:out value="${people}"/> <br>
</c:forEach>
<hr>
<c:forEach var="people" items="${peoples}" begin="1" end="4" step="2">
    <c:out value="${people}"/> <br>
</c:forEach>
</body>
</html>
```

<br>
### 4.4.2 七个动作指令
- jsp:forward ---- 执行页面转向，将请求的处理转发到下一个页面
- jsp:param ---- 用于传递参数，必须与其他支持参数标签一起使用
- jsp:include ---- 用于动态引入一个 JSP 页面
- jsp:plugin ---- 用于下载 JavaBean 或 Applet 到客户端执行
- jsp:useBean ---- 使用 JavaBean
- jsp:setProperty ---- 修改 JavaBean 实例的属性值
- jsp:getProperty ---- 获取 JavaBean 实例的属性值

<br>
### 4.4.3 九大内置对象
- HttpServletRequest request ---- 请求对象：同一次请求有效，包括转发
- HttpServletResponse response ---- 响应
- PageContext pageContext ---- 页面容器：当前页面有效
- HttpSession session ---- 会话对象：同一次会话有效(只要不关闭或者切换浏览器)
- ServletContext application ---- 全局对象：全局有效(整个项目有效，切换浏览器有效，关闭server、其他项目无效)
- ServletConfig config ---- 服务器配置信息，可以取得初始化参数
- JspWriter out ---- 页面输出
- Object page ---- 不使用
- exception

<br>
### 4.4.4 四个作用域
| 名称 | 作用域 |
|---|---|
|application|在所有应用程序中有效|
|session|在当前会话中有效|
|request|在当前请求中有效|
|page|在当前页面中有效|

而pageContext对象的findAttribute方法如下
```
    public Object findAttribute(String name) {
        if (this.mPage.containsKey(name)) {
            return this.mPage.get(name);
        } else if (this.mRequest.containsKey(name)) {
            return this.mRequest.get(name);
        } else if (this.mSession.containsKey(name)) {
            return this.mSession.get(name);
        } else {
            return this.mApp.containsKey(name) ? this.mApp.get(name) : null;
        }
    }
```
>该方法会优先寻找page中的值，如果不存在则向上一作用域寻找，直到找到值或返回null。有点类似双亲委派机制的前半段。

<br>
### 4.4.5 使用示例
#### 异常页面跳转
**全局配置**
通过在web.xml配置全局的异常跳转路径
```
<web-app>
  <display-name>Archetype Created Web Application</display-name>
  <error-page>
    <error-code>404</error-code>
    <location>/404err.jsp</location>
  </error-page>
  <error-page>
    <error-code>500</error-code>
    <location>/500err.jsp</location>
  </error-page>
</web-app>
```

**局部配置**
通过JSP指令在单个JSP文件中配置该文件的异常跳转
```
<%-- 如果发生500错误，跳转到500err.jsp页面--%>
<%@ page errorPage="./500err.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%
    int i = 1/0;
%>
</body>
</html>
```
>**优先级： 局部配置>全局配置**

<br>
发生异常时会跳转到其他jsp页面，该页面向前端返回异常图片或信息，这个页面中需要通过JSP指令`<%@page isErrorPage="true" %>`显示的指定这个页面是错误页面，即响应的状态码是500
```
<%@page isErrorPage="true" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<img src="./img/500.png" alt="">
</body>
</html>
```

<br>
#### 引入其他代码
**①通过<%include file=" "%>引入**
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <%@include file="/common/head.jsp"%>
    <h1>BODY</h1>
    <%@include file="/common/foot.jsp"%>
</body>
</html>
```
**查看源码**
```
public final class test6_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

  static {
    _jspx_dependants = new java.util.HashMap<java.lang.String,java.lang.Long>(2);
    _jspx_dependants.put("/common/head.jsp", Long.valueOf(1626144376000L));
    _jspx_dependants.put("/common/foot.jsp", Long.valueOf(1626144406000L));
  }
  
  ......

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    if (!javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSP 只允许 GET、POST 或 HEAD。Jasper 还允许 OPTIONS");
        return;
      }
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("    ");
      out.write("\r\n");
      out.write("<h1>HEADER</h1>\r\n");
      out.write("\r\n");
      out.write("    <h1>BODY</h1>\r\n");
      out.write("    ");
      out.write("\r\n");
      out.write("<h1>FOOT</h1>\r\n");
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
```
>可以看到<%include file=" "%>引入jps文件时，会通过write将jps的代码直接输出到前端。

<br>
**②通过<jsp:include page=""/>引入**
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <jsp:include page="/common/head.jsp"/>
    <h1>BODY</h1>
    <jsp:include page="/common/foot.jsp"/>
</body>
</html>
```
查看源码
```
public final class test7_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

    ......

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    if (!javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSP 只允许 GET、POST 或 HEAD。Jasper 还允许 OPTIONS");
        return;
      }
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("    ");
      org.apache.jasper.runtime.JspRuntimeLibrary.include(request, response, "/common/head.jsp", out, false);
      out.write("\r\n");
      out.write("    <h1>BODY</h1>\r\n");
      out.write("    ");
      org.apache.jasper.runtime.JspRuntimeLibrary.include(request, response, "/common/foot.jsp", out, false);
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
```
>使用<jsp:include page=""/>引入时，会调用include将代码输出到前端。

<br>
`注意：如果引入的是静态代码，那么两者在前端显示的结果没有区别；但是如果是动态代码，则有很大不同，因为在同一个方法中运行和在不同方法中运行是不同的。`
如引入的文件head.jsp是动态代码
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    int i = 0;
%>
```
创建jsp文件通过<%@include file="/common/head.jsp"%>来应用这个head.jsp文件
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <%@include file="/common/head.jsp"%>
    <%
        int i = 10;
    %>
</body>
</html>
```
节选的部分源码如下
```
      out.write("\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("    ");
      out.write("\r\n");
      out.write("<h1>HEADER</h1>\r\n");
      out.write("\r\n");
      out.write("    ");

        int i = 10;
    
      out.write("\r\n");
      out.write("    ");
      out.write('\r');
      out.write('\n');

    int i = 0;

      out.write('\r');
      out.write('\n');
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
```
可以发现重复定义了变量，servlet运行时会抛出异常。

而创建jsp文件通过<jsp:include page="/common/head.jsp"/>来应用这个head.jsp文件
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <jsp:include page="/common/head.jsp"/>
    <%
        int i = 10;
    %>
</body>
</html>
```
查看源码
```
      out.write("\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("    ");
      org.apache.jasper.runtime.JspRuntimeLibrary.include(request, response, "/common/head.jsp", out, false);
      out.write("\r\n");
      out.write("    ");

        int i = 10;
    
      out.write("\r\n");
      out.write("    ");
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
```
两个定义语句不在一个方法中运行，所以servlet正常运行。这点需要注意。


<br>
## 4.5 EL表达式
如果EL表达式不生效，需要加上`<%@ page isELIgnored="false" %>`
### 4.5.1 获取数据
EL有11个内置对象，除了pageContext以外，其他10个内置对象的类型都是java.util.Map类型
#### 四个域相关内置对象
EL只能从四大域中获取属性：
- pageScope：从page范围域属性空间中查找指定的key
- requestScope：从request范围域属性空间中查找指定的key
- sessionScope：从session范围域属性空间中查找指定的key
- applicationScope：从application范围域属性空间中查找指定的key

**例：**
```
    name=${applicationScope.name }<br>
    name=${pageScope.name }<br>
    name=${sessionScope.name }<br>
    name=${requestScope.name }<br>
    name=${name}
```
>如果没有使用EL的内置对象，则查找数据顺序是依次按照由小到大范围从四大域中查找指定名称的属性值。

#### 四个重要内置对象
- pageContext
- param
- paramValues
- initParam

该pageContext与JSP内置对象pageContext是同一个对象。通过该对象，可以获取到request、response、session、servletContext、servletConfig等对象，注意的是，这些对象在EL里不是内置对象，这些对象只能通过pageContext获取。

**例：**
```
${pageContext.request.contextPath }   <!--代表web应用的根目录-->
name=${param.name }  <!--获取请求中的参数，其底层实际调用request.getParameter()-->
hobby[1]=${paramValues.hobby[1] }  <!--获取参数中的所有值，底层实际调用request.getParameterValues()-->
name=${initParam.name }  <!--获取web.xml的context-param标签中定义的初始化参数，底层调用的是ServletContext.getInitParameter()-->
```

<br>
### 4.5.2 执行运算
如进行比较判断
```
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <c:if test="${param.username=='admin'}" var="isAdmin">
        <c:out value="欢迎管理员: ${param.username}"/>
    </c:if>
    <c:out value="${isAdmin}"/>
</body>
</html>
```

<br>
# 五、JavaBean
即java实体类，实体类要求
- 必须要有一个无参构造
- 属性必须私有化
- 必须有对应的get/set方法

一般用来和数据库的字段做映射，即ORM(对象关系映射)。
- 表 ---> 类
- 字段 ---> 属性
- 行记录 ---> 对象

**通过jsp来操作实体类**
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<!-- 创建对象 -->
<jsp:useBean id="user" class="com.cj.spring.entity.User" scope="page"/>
<!-- 赋值对象属性 -->
<jsp:setProperty name="user" property="id" value="1"/>
<jsp:setProperty name="user" property="name" value="zhangsan"/>
<jsp:setProperty name="user" property="age" value="18"/>
<jsp:setProperty name="user" property="gender" value="boy"/>
</body>
<!-- 打印对象 -->
user: <%= user.getName()%>
<h3>user: ${user}</h3>
</html>
```

<br>
# 六、MVC三层架构
![image.png](https://upload-images.jianshu.io/upload_images/21580557-acd880db8266a1b4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<br>
# 七、过滤器
Servlet过滤器通过拦截请求和响应，以便查看、提取或以某种方式操作客户端和服务器之间交换的数据，实现“过滤”的功能。Filter通常封装了一些功能的web组件，过滤器提供了一种面向对象的模块化机制，将任务封装到一个可插入的组件中， Filter组件通过配置文件来声明，并动态的代理。

## 7.1 通过过滤器设置所有请求的编码
**定义过滤器实现Filter接口**
```
public class CharacterEncodingFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("初始化过滤器");
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");
        response.setContentType("text/html");
        System.out.println("执行过滤器前");
        chain.doFilter(request,response);
        System.out.println("执行过滤器后");
    }

    @Override
    public void destroy() {
        System.gc();
        System.out.println("销毁过滤器");
    }
}
```
>在Tomcat启动和销毁时分别调用init和destroy方法。在doFilter方法前的代码在请求到达接口前执行，doFilter方法后的代码在接口执行完成后执行。

**web.xml配置**
```
  <servlet>
    <servlet-name>msg</servlet-name>
    <servlet-class>com.cj.filter.TestServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>msg</servlet-name>
    <url-pattern>/msg</url-pattern>
  </servlet-mapping>
  <servlet-mapping>
    <servlet-name>msg</servlet-name>
    <url-pattern>/servlet/msg</url-pattern>
  </servlet-mapping>

  <filter>
    <filter-name>filter</filter-name>
    <filter-class>com.cj.filter.CharacterEncodingFilter</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>filter</filter-name>
    <url-pattern>/servlet/*</url-pattern>
  </filter-mapping>
```
>配置过滤器，任何访问路径为/servlet/*的请求都会先经过过滤器。

<br>
## 7.2 实现简单的登陆登出功能
1. 创建一个登陆页面，写死用户名密码。如果登陆成功则跳转到主页，登陆失败跳转到失败页面。
2. 主页上有个注销功能，点击后销毁用户session，跳转到登陆页面。
3. 如果不是登陆页面的路径，则在过滤器中判断该session是否已登陆，未登录则返回401页面，已登陆则放行。

**登陆过滤器**
该过滤器从用户session中取isLogin属性来判断用户是否已登陆，如果已登陆或者是不需要登陆即可访问的资源，则放行；如果未登录访问需要登陆才能访问的资源，则重定向到登陆页面。
```
public class LoginFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {

    }

    @Override
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) resp;

        // 获取session中是否登陆的信息
        String isLogin = (String) request.getSession().getAttribute("isLogin");

        String servletPath = request.getServletPath();
        System.out.println("servletPath: " + servletPath);
        String contextPath = request.getContextPath();
        System.out.println("contextPath: " + contextPath);

        // 如果未登录，则转发到登陆页面
        boolean isAnonyPath = "/sys/login".equals(servletPath) ||
                "/sys/login.jsp".equals(servletPath) || "/sys/error.jsp".equals(servletPath);

        if (!"true".equals(isLogin)) {
            if (!isAnonyPath) {
                response.sendRedirect(request.getContextPath() + "/sys/login.jsp");
            }
        }
        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {

    }
}
```

**登陆页面login.jsp**
访问该登陆页面，提交表单到LoginServlet类中进行账号密码验证
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<h1>登陆</h1>
<form action="${pageContext.request.contextPath}/sys/login" method="get">
    用户名:<input type="text" name="username"> <br>
    密码:<input type="password" name="password"> <br>
    <input type="submit">
</form>
</body>
</html>
```

**LoginServlet**
对登陆页面提交的账号密码进行验证，如果验证通过，则在session中添加属性 ("isLogin", "true") ，用于判断该用户是否已登陆，并重定向到首页success.jsp；如果验证失败，则重定向到失败页面error.jsp。
```
public class LoginServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");

        if ("admin".equals(username) && "abc123".equals(password)) {
            // 通过验证，在session中放上已登陆标记，并转发到主页上
            req.getSession().setAttribute("isLogin","true");
            resp.sendRedirect(req.getContextPath() + "/sys/success.jsp");
        } else {
            // 用户名密码错误，转发到错误页面
            resp.sendRedirect(req.getContextPath() + "/sys/error.jsp");
        }

    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req,resp);
    }
}
```

**success.jsp**
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<h1>主页</h1>
<p><a href="${pageContext.request.contextPath}/sys/loginout">注销</a></p>
</body>
</html>
```

**error.jsp**
```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<h1>账号密码错误</h1>
<p><a href="${pageContext.request.contextPath}/sys/login.jsp">重新登陆</a></p>
</body>
</html>
```

**注销接口**
在首页success.jsp中添加一个注销的链接，发送注销请求。接收到请求后删除session中的isLogin属性。
```
public class LoginOutServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 删除session中的已登陆标记
        req.getSession().removeAttribute("isLogin");
        resp.sendRedirect(req.getContextPath() + "/sys/login.jsp");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }

}
```

**web.xml**
注册过滤器和servlet接口。
```
<!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >

<web-app>
  <display-name>Archetype Created Web Application</display-name>

  <filter>
    <filter-name>loginfilter</filter-name>
    <filter-class>com.cj.javaweb.filter.LoginFilter</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>loginfilter</filter-name>
    <url-pattern>/sys/*</url-pattern>
  </filter-mapping>

  <servlet>
    <servlet-name>login</servlet-name>
    <servlet-class>com.cj.javaweb.login.LoginServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>login</servlet-name>
    <url-pattern>/sys/login</url-pattern>
  </servlet-mapping>

  <servlet>
    <servlet-name>loginout</servlet-name>
    <servlet-class>com.cj.javaweb.login.LoginOutServlet</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>loginout</servlet-name>
    <url-pattern>/sys/loginout</url-pattern>
  </servlet-mapping>

</web-app>
```


<br>
# 八、监听器
监听器就是监听某个对象的的状态变化的组件。
三种监听器：
- ServletContextListener：监听ServletContext域的创建与销毁的监听器。
- HttpSessionListener：监听Httpsession域的创建与销毁的监听器。
- ServletRequestListener：监听ServletRequest域创建与销毁的监听器。

<br>
## 8.1 ServletContextListener
监听ServletContext域的创建与销毁的监听器。
Servlet域的生命周期：在服务器启动创建，服务器关闭时销毁；

<br>
## 8.2 HttpSessionListener
监听Httpsession域的创建与销毁的监听器。
HttpSession对象的生命周期：第一次调用request.getSession时创建；销毁有以下几种情况（服务器关闭、session过期、 手动销毁）

**例：**
使用session监听器，在创建和销毁session是进行计数，这个计数就是session的数量，即在线人数统计。
```
public class OnlineCountListener implements HttpSessionListener {

    @Override
    public void sessionCreated(HttpSessionEvent se) {
        ServletContext context = se.getSession().getServletContext();
        Integer onlineCount = (Integer) context.getAttribute("onlineCount");
        if (Objects.isNull(onlineCount)) {
            Integer count = 1;
            System.out.println("onlineCount为null，设置初始值1");
            context.setAttribute("onlineCount", count);
        } else {
            System.out.println("onlineCount+1");
            context.setAttribute("onlineCount", onlineCount + 1);
        }
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        ServletContext context = se.getSession().getServletContext();
        Integer onlineCount = (Integer) context.getAttribute("onlineCount");
        if (!Objects.isNull(onlineCount) && onlineCount > 0) {
            System.out.println("onlineCount-1");
            context.setAttribute("onlineCount", onlineCount - 1);
        }
    }
}
```
配置监听器
```
  <listener>
    <listener-class>com.cj.listener.OnlineCountListener</listener-class>
  </listener>
```

<br>
## 8.3 ServletRequestListener
监听ServletRequest域创建与销毁的监听器。ServletRequest的生命周期：每一次请求都会创建request，请求结束则销毁。

## 8.4 Java中的窗口监听器示例
运行程序时会打开一个窗口，为该窗口设置窗口监听器，如点击关闭按钮会通过该监听器对象回调windowClosing方法，在该方法中关闭窗口，则可以实现窗口的关闭功能。
```
public class WindowsListener {
    public static void main(String[] args) {
        Frame frame = new Frame("窗口测试");
        Panel panel = new Panel(null);
        frame.setLayout(null);

        frame.setBounds(300,300,500,500);
        frame.setBackground(new Color(0,0,255));

        panel.setBounds(60,60,300,300);
        panel.setBackground(new Color(0,255,0));

        frame.add(panel);
        frame.setVisible(true);

        frame.addWindowListener(new WindowListener() {
            @Override
            public void windowOpened(WindowEvent e) {
                System.out.println("打开");
            }

            @Override
            public void windowClosing(WindowEvent e) {
                System.out.println("关闭ing");
                System.exit(0);
            }

            @Override
            public void windowClosed(WindowEvent e) {
                System.out.println("关闭ed");
            }

            @Override
            public void windowIconified(WindowEvent e) {
            }

            @Override
            public void windowDeiconified(WindowEvent e) {
            }

            @Override
            public void windowActivated(WindowEvent e) {
                System.out.println("窗口激活");
            }

            @Override
            public void windowDeactivated(WindowEvent e) {
                System.out.println("窗口未激活");
            }
        });
    }
}
```

<br>
# 九、JDBC
## 9.1 JDBC基本操作
JDBC（Java Database Connectivity）指Java数据库连接，是Java语言中用来规范客户端程序如何来访问数据库的应用程序接口，提供了诸如查询和更新数据库中数据的方法。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-619659f409eb9125.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**依赖**
引入mysql驱动包
```
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.47</version>
        </dependency>
```

**请求数据库**
分为五步：1. 加载驱动； 2. 获取数据库连接； 3.获取Statement对象用于发送SQL； 4.执行SQL，返回结果； 5.关闭连接
```
public class TestJdbc {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        String username = "root";
        String password = "cj";
        String url = "jdbc:mysql://chenjie.asia:3306/test?useUnicode=true&characterEncoding=utf-8" +
                "&useSSL=true&serverTimezone=UTC&allowMultiQueries=true";
        String driver = "com.mysql.jdbc.Driver";

        // 1.加载驱动(通过反射来加载Driver类，加载类时执行静态代码块将Driver注册到DriverManager中)
        Class.forName(driver);
//        DriverManager.registerDriver(new com.mysql.jdbc.Driver());
        // 2.获取数据库连接
        Connection connection = DriverManager.getConnection(url, username, password);
        // 3.获取Statement对象用于发送SQL
        Statement statement = connection.createStatement();
        // 4.执行SQL，返回结果
        String sql = "select * from t_user";
        ResultSet resultSet = statement.executeQuery(sql);

        while (resultSet.next()) {
            Object id = resultSet.getObject("id");
            Object name = resultSet.getObject("name");
            Object gender = resultSet.getObject("gender");
            Object age = resultSet.getObject("age");
            System.out.println("id:" + id + " -- name:" + name + " -- gender:" + gender + " -- age:" + age);
        }

        // 5.关闭连接
        resultSet.close();
        statement.close();
        connection.close();

    }
}
```
>需要注意的是Statement是不安全的，存在SQL注入的风险；应该使用PreparedStatement，会对SQL进行预编译。

<br>
**PreparedStatement示例如下**
```
public class PreparedStatementTest {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        String username = "root";
        String password = "cj";
        String url = "jdbc:mysql://chenjie.asia:3306/test?useUnicode=true&characterEncoding=utf-8" +
                "&useSSL=true&serverTimezone=UTC&allowMultiQueries=true";
        String driver = "com.mysql.jdbc.Driver";

        // 1.加载驱动
        Class.forName(driver);
        // 2.获取数据库连接
        Connection connection = DriverManager.getConnection(url, username, password);
        // 3.获取PreparedStatement对SQL进行预编译
        String sql = "select * from t_user where id = ?";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        // 查询条件为
        String uid = "1' or '0'='0";
        preparedStatement.setString(1, uid);
        System.out.println(preparedStatement.toString());
        // 4.执行SQL，返回结果
        ResultSet resultSet = preparedStatement.executeQuery();
        while (resultSet.next()) {
            Object id = resultSet.getObject("id");
            Object name = resultSet.getObject("name");
            Object gender = resultSet.getObject("gender");
            Object age = resultSet.getObject("age");
            System.out.println("id:" + id + " -- name:" + name + " -- gender:" + gender + " -- age:" + age);
        }

        // 5.关闭资源
        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
}
```
上例中我们需要通过uid进行查询，但是用户传入的uid为`1' or '0'='0`，试图通过SQL注入查询到所有的记录。如果不采取措施，那么最终的最终执行的sql语句为`select * from t_user where id = '1' or '0'='0'`。
PreparedStatement的setString方法不是简单拼接SQL语句，而是将参数中的单引号都用\进行转义，最终执行的SQL语句为`select * from t_user where id = '1\' or \'0\'=\'0'`，从而达到防止SQL注入的目的。

**PreparedStatement的预编译优点：**
- 1. 提高了sql解析的效率：在使用PreparedStatement执行SQL命令时，命令会带着占位符被数据库进行编译和解析，并放到命令缓冲区。然后，每当执行同一个PreparedStatement语句的时候，由于在缓冲区中可以发现预编译的命令，虽然会被再解析一次，但不会被再次编译。
- 2. 防止SQL注入发生。预编译后，参数传入后作为一个字符串，不会再解析SQL关键词。

执行查询时使用executeQuery方法，返回结果集；执行增删改时使用execute方法，返回受影响的记录数。
```
public class PreparedStatementTest1 {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        String username = "root";
        String password = "cj";
        String url = "jdbc:mysql://chenjie.asia:3306/test?useUnicode=true&characterEncoding=utf-8" +
                "&useSSL=true&serverTimezone=UTC&allowMultiQueries=true";
        String driver = "com.mysql.jdbc.Driver";

        Class.forName(driver);
        Connection connection = DriverManager.getConnection(url, username, password);
        String sql = "insert into t_user values(?,?,?,?,?)";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        preparedStatement.setInt(1, 3);
        preparedStatement.setString(2, "wangwu");
        preparedStatement.setString(3, "nan");
        preparedStatement.setInt(4, 22);
        preparedStatement.setDate(5, new Date(new java.util.Date().getTime()));

        int update = preparedStatement.executeUpdate();
        System.out.println("更新了" + update + "行");

        preparedStatement.close();
        connection.close();
    }
}
```
>java开发手册不推荐使用java.sql.Date类

<br>
## 9.2 事务流程
1. 加载驱动 2. 创建连接 3. 开启事务  4. 获取Statement对象用于发送SQL 5. 执行SQL  6. 出现异常回滚，正常执行提交  7. 关闭连接

```
public class TransactionTest {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        String username = "root";
        String password = "cj";
        String url = "jdbc:mysql://chenjie.asia:3306/test?useUnicode=true&characterEncoding=utf-8" +
                "&useSSL=true&serverTimezone=UTC&allowMultiQueries=true";
        String driver = "com.mysql.jdbc.Driver";

        // 1.注册驱动
        Class.forName(driver);
        // 2.创建链接
        Connection connection = DriverManager.getConnection(url, username, password);
        // 3.开启事务
        connection.setAutoCommit(false);
        // 4.获取Statement对象用于提交SQL
        String sql = "update t_user set balance = balance + ? where id = ?";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        try {
            // 5.执行SQL
            preparedStatement.setInt(1, 100);
            preparedStatement.setInt(2, 1);
            preparedStatement.executeUpdate();

            int i = 1 / 0;

            preparedStatement.setInt(1, -100);
            preparedStatement.setInt(2, 2);
            preparedStatement.executeUpdate();

            // 6.1提交事务
            connection.commit();
        } catch (Exception e) {
            // 6.2回滚事务
            System.out.println(e.getMessage());
            connection.rollback();
        } finally {
            // 7.关闭连接
            preparedStatement.close();
            connection.close();
        }

    }
}
```

<br>
# 十、项目实战 -- SMBMS(超市订单管理系统)
## 10.1 登陆功能
1. 读取配置文件，完成数据库操作的静态方法类
2. 导入前端页面，包括登陆页面，首页，错误页面等。
3. 编写登陆页面提交servlet，验证账号密码，正确则将用户实体类对象作为属性放到session中并重定向到首页，从session中获取对象用户名进行显示；错误则将失败信息作为属性放到session中供登录页面显示错误信息。
4. 首页有退出链接，编写登出的servlet，删除session中的添加的用户属性，跳转到登陆页面
5. 完成编码拦截器和登陆拦截器，登陆时需要经过拦截器判断是否登陆或是否允许匿名访问，决定是否放行或重定向到登录页面。

配置web.xml文件，设置拦截器、欢迎页面，servlet接口，session设置30分钟过期时间等



## 10.2 修改密码
1. 点击首页的修改密码，可以跳转到修改密码页面，需要输入旧密码、新密码和确认密码。
2. 在旧密码框失去焦点时，需要通过ajax访问接口判断旧密码是否正确(从session中获取旧密码进行验证)，在新密码和确认密码框失去焦点时判断格式是否合规范，并在输入框后打印错误信息（通过js实现）。
3. 新建用户操作servlet用于提交修改的密码，从session中获取用户信息，如果有用户信息、旧密码正确且新密码格式正确，则修改数据库密码为新密码。(不同用户操作可以通过在前端传标志位来复用同一个servlet)
4. 还有就是对用户和角色的一些增删改查。通过用户名和角色名进行查询。
