![过滤器链](https://upload-images.jianshu.io/upload_images/21580557-7f8ceff6108e1d7f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**流程图如下：**
![1622701717884.png](https://upload-images.jianshu.io/upload_images/21580557-271600d65568eb12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

WebSecurityConfigurerAdapter 的三个重载方法的参数
- HttpSecurity ：认证方式和资源权限设置（包括csrf、cors、自动登录RemeberMe、登出、设置token认证过滤器、设置session、资源访问权限、）；
- AuthenticationManagerBuilder ：设置角色和权限信息（账号密码及其角色权限存储到内存，或将角色信息存储在数据库中,从数据库中动态加载用户账号密码及其权限），设置UserDetailsService和BCryptPasswordEncoder；
- WebSecurity ：设置不需要鉴权静态资源访问路径。

基本原理：
通过SecurityContextHolder.getContext().setAuthentication(authenticationToken)将token设置到上下文中，
在UsernamePasswordAuthenticationFilter过滤器中会通过AuthenticationManager的authenticate方法对Security上下文中的token进行校验（实现UserDetailsService和UserDetails）。

###HttpBasic认证方式
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
   
   @Override
   protected void configure(HttpSecurity http) throws Exception {
      http.httpBasic()//开启httpbasic认证
      .and()
      .authorizeRequests()
      .anyRequest()
      .authenticated();//所有请求都需要登录认证才能访问
   }

}
```
访问服务器中的资源需要进行认证，默认用户名为user，密码为启动服务器时产生的密码。

当然我们也可以通过application.yml指定配置用户名密码:
```xml
spring:
    security:
      user:
        name: admin
        password: admin
```

***原理***
![image](https://upload-images.jianshu.io/upload_images/21580557-0e9776340427cabf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
*   首先，HttpBasic模式要求传输的用户名密码使用Base64模式进行加密。如果用户名是 `"admin"`  ，密码是“ admin”，则将字符串`"admin:admin"`使用Base64编码算法加密。加密结果可能是：YWtaW46YWRtaW4=。
*   然后，在Http请求中使用Authorization作为一个Header，“Basic YWtaW46YWRtaW4=“作为Header的值，发送给服务端。（注意这里使用Basic+空格+加密串）
*   服务器在收到这样的请求时，到达BasicAuthenticationFilter过滤器，将提取“ Authorization”的Header值，并使用用于验证用户身份的相同算法Base64进行解码。
*   解码结果与登录验证的用户名密码匹配，匹配成功则可以继续过滤器后续的访问。


###formLogin认证模式
Spring Security支持我们自己定制登录页面，即formLogin模式登录认证模式。
***依赖***
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
</dependency>

***代码***
![认证方式](https://upload-images.jianshu.io/upload_images/21580557-8d9d29464140639e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    /**
     * 采用formLogin方式进行认证
     *
     * @param http
     * @throws Exception
     */
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable() //禁用csrf攻击防御
                //1.formLogin配置段
                .formLogin()
                .loginPage("/login.html")//用户访问资源时先跳转到该登录页面
                .loginProcessingUrl("/login")//登录表单中的action的地址，在该接口中进行认证
                .usernameParameter("username")//登录表单form中的用户名输入框input的name名，缺省是username
                .passwordParameter("password")//登录表单form中的密码输入框input的name名，缺省是password
                .defaultSuccessUrl("/index")//登录成功后默认跳转的路径
                .failureUrl("/login.html") //登录失败后返回登录页
                .and()
                //2.authorizeRequests配置端
                .authorizeRequests()
                .antMatchers("/login.html","/login").permitAll() //不需要验证即可访问
                .antMatchers("/biz1","/biz2").hasAnyAuthority("ROLE_user","ROLE_admin")//user和admin权限可以访问的路径，等同于hasAnyRole("user","admin")
//                .antMatchers("/syslog","/sysuser").hasAnyRole("admin")//admin角色可以访问的路径
                .antMatchers("/syslog").hasAuthority("sys:log")//权限id，有该id的用户可以访问
                .antMatchers("/sysuser").hasAuthority("sys:user")
                .anyRequest().authenticated();
    }

    /**
     * 将角色信息存储在内存中
     * @param auth
     * @throws Exception
     */
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.inMemoryAuthentication()
                .withUser("user")
                .password(bCryptPasswordEncoder().encode("abc123"))
                .roles("user")
                .and()
                .withUser("admin")
                .password(bCryptPasswordEncoder().encode("abc123"))
//                .authorities("sys:log","sys:user")
                .roles("admin")
                .and()
                .passwordEncoder(bCryptPasswordEncoder());//配置BCrypt加密
    }

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder(){
        return new BCryptPasswordEncoder();
    }

    /**
     * 静态资源访问不需要鉴权
     * @param web
     * @throws Exception
     */
    @Override
    public void configure(WebSecurity web) throws Exception {
        web.ignoring().antMatchers("/css/**", "/fonts/**", "img/**", "js/**");
    }
}
```

#####自定义的登陆处理逻辑
***登陆成功后的处理逻辑***
```java
@Component
public class MyAuthenticationSuccessHandler extends SavedRequestAwareAuthenticationSuccessHandler {

    @Value("${spring.security.loginType}")
    private String loginType;

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws ServletException, IOException {
        if ("JSON".equalsIgnoreCase(loginType)) {
            //登录成功后返回登录成功信息
            response.setContentType("application/json;charset=UTF-8");
            response.getWriter().write(new ObjectMapper().writeValueAsString(CommonResult.success().setData("/index.html")));
        } else {
            //登录成功后跳转到拦截发生时访问的路径
            super.onAuthenticationSuccess(request,response,authentication);
        }
    }

}
```
将.defaultSuccessUrl()方法替换为successHandler()方法。


***登陆失败后的处理逻辑***
```java
@Component
public class MyAuthenticationFailureHandler extends SimpleUrlAuthenticationFailureHandler {

    @Value("${spring.security.loginType}")
    private String loginType;

    @Override
    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException, ServletException {
        if ("JSON".equalsIgnoreCase(loginType)) {
            response.setContentType("application/json;charset=UTF-8");
            response.getWriter().write(new ObjectMapper().writeValueAsString(CommonResult.error().setMessage("用户名或密码错误")));
        } else {
            super.onAuthenticationFailure(request,response,exception);
        }
    }

}
```
将failureUrl()方法替换为failureHandler()方法。


#####自定义登陆页面和跳转
```java
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>首页</title>
</head>
<body>
    <h1>业务系统登录</h1>
    <form action="/login" method="post">
        <span>用户</span><input type="text" name="username" id="username"/> <br>
        <span>密码</span><input type="password" name="password" id="password"/> <br>
        <input type="button" onclick="login()" value="登录">
    </form>

    <script src="https://cdn.staticfile.org/jquery/1.12.3/jquery.min.js"></script>
    <script>
        function login(){
            var username = $("#username").val();
            var password = $("#password").val();
            // var username = document.getElementById("username").valueOf();
            // var password = document.getElementById("password").valueOf();
            if (username === "" || password === "") {
                alert("用户名或密码不能为空");
                return;
            }
            $.ajax({
                type: "POST",
                url: "/login",
                data: {
                    "username": username,
                    "password": password
                },
                success: function(json){
                    if (json.code === 200) {
                        location.href = json.data;
                    }else{
                        alert(json.message);
                    }
                },
                error: function(error){
                    console.log(e.responseText)
                }
            })
        }
    </script>

</body>
</html>
```
***逻辑***
- 如果登陆密码错误，则弹框提示用户名密码错误
- 如果登录成功，则跳转到index.html


###Spring Security与session的创建使用
***四种模式***
- always：如果当前请求没有session存在，Spring Security创建一个session。
- never：不主动创建session，如果session存在，会使用该session。
- ifRequired(默认)：在需要时才创建session
- stateless：不会创建或使用任何session。适用于接口型的无状态应用，该方式节省资源。


***会话超时配置***
- server.servlet.session.timeout=15m
- spring.session.timeout=15m
```xml
#springboot限制session最少过期时间为1min，所以此时session过期时间为1min
server:
  servlet:
    session
      timeout: 10s
```


***session保护***
- 默认情况下，Security启用了migrationSession保护方式，对同一个cookies的session用户，每次登录都会创建一个新的http会话，就http会话失效且属性会复制到新会话中。
- 设置为none，原始会话不会失效
- 设置为newSession，将创建一个干净的会话，不复制旧会话中的任何属性。

***cookie保护***
session存储在cookie中，通过如下配置保证cookie的安全。
```xml
server:
  servlet:
    session:
      cookie:
        http-only: true #浏览器脚本无法访问cookie
        secure: true #仅通过https连接发送cookie，http无法携带cookie
```

***限制最大登录用户数量***
同一账号允许同时登陆的最大数量
```java
http.sessionManagement()
        .maximumSessions(1) //最大登录数为1
        .maxSessionsPreventsLogin(false) //false表示允许再次登录但会踢出之前的登陆；true表示不允许再次登录
        .expiredSessionStrategy(new MyExpiredSessionStrategy());//会话过期后进行的自定义操作
```

自定义会话超时处理
```java
@Component
public class MyExpiredSessionStrategy implements SessionInformationExpiredStrategy {

    /**
     * session超时后该方法会被回调
     * @param event
     * @throws IOException
     * @throws ServletException
     */
    @Override
    public void onExpiredSessionDetected(SessionInformationExpiredEvent event) throws IOException, ServletException {
        CommonResult commonResult = CommonResult.error().setMessage("其他设别登录，当前设备已下线");
        event.getResponse().setContentType("application/json;charset=UTF-8");
        event.getResponse().getWriter().write(new ObjectMapper().writeValueAsString(commonResult));
    }
}
```



***总结代码配置***
配置session模式和过期跳转路径：
```java
 http.sessionManagement()
        .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED) //设置session创建模式
        .invalidSessionUrl("/login.html") //sessin失效后跳转路径
        .sessionFixation().migrateSession() //重新登录后创建新session并复制属性
        .maximumSessions(1) //最大登录数为1
        .maxSessionsPreventsLogin(false)//false表示允许再次登录但会踢出之前的登陆；true表示不允许再次登录
        .expiredSessionStrategy(new MyExpiredSessionStrategy());//会话过期后进行的自定义操作
```

完整SecurityConfig类代码
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    /**
     * 采用httpbasic方式进行认证
     * @param http
     * @throws Exception
     */
//    @Override
//    protected void configure(HttpSecurity http) throws Exception {
//        http.httpBasic()//开启httpbasic认证
//        .and()
//                .authorizeRequests()
//                .anyRequest()
//                .authenticated();//所有请求都需要登录认证
//    }

    @Resource
    private MyAuthenticationSuccessHandler mySuthenticationSuccessHandler;

    @Resource
    private MyAuthenticationFailureHandler myAuthenticationFailureHandler;

    @Resource
    private CaptchaCodeFilter captchaCodeFilter;

    /**
     * 采用formLogin方式进行认证
     *
     * @param http
     * @throws Exception
     */
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                //设置过滤器
                .addFilterBefore(captchaCodeFilter,UsernamePasswordAuthenticationFilter.class) //将验证码过滤器放到账号密码前面执行
                //退出登录
                .logout()
                .logoutUrl("/logout") //退出登录的请求接口
                .logoutSuccessUrl("/login.html") //退出登录后跳转的路径
                .deleteCookies("JSESSIONID") //退出时删除浏览器中的cookie
                .and()
                //禁用csrf攻击防御
                .csrf().disable()
                //1.formLogin配置段
                .formLogin()
                .loginPage("/login.html")//用户访问资源时先跳转到该登录页面
                .loginProcessingUrl("/login")//登录表单中的action的地址，在该接口中进行认证
                .usernameParameter("username")//登录表单form中的用户名输入框input的name名，缺省是username
                .passwordParameter("password")//登录表单form中的密码输入框input的name名，缺省是username
//                .defaultSuccessUrl("/index")//登录成功后默认跳转的路径
                .successHandler(mySuthenticationSuccessHandler)//使用自定义的成功后的逻辑
//                .failureUrl("/login.html") //登录失败后返回登录页
                .failureHandler(myAuthenticationFailureHandler) //使用自定义的失败后的逻辑
                .and()
                //2.authorizeRequests配置端
                .authorizeRequests()
                .antMatchers("/login.html", "/login","/kaptcha").permitAll() //不需要验证即可访问
                .antMatchers("/biz1", "/biz2").hasAnyAuthority("ROLE_user", "ROLE_admin")//user和admin权限可以访问的路径，等同于hasAnyRole("user","admin")
//                .antMatchers("/syslog","/sysuser").hasAnyRole("admin")//admin角色可以访问的路径
                .antMatchers("/syslog").hasAuthority("sys:log")//权限id，有该id的用户可以访问
                .antMatchers("/sysuser").hasAuthority("sys:user")
                .anyRequest().authenticated()
                .and()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
                .invalidSessionUrl("/login.html")
                .sessionFixation().migrateSession()
                .maximumSessions(1) //最大登录数为1
                .maxSessionsPreventsLogin(false)//false表示允许再次登录但会踢出之前的登陆；true表示不允许再次登录
                .expiredSessionStrategy(new MyExpiredSessionStrategy());//会话过期后进行的自定义操作
    }

    /**
     * 将角色信息存储在内存中
     * @param auth
     * @throws Exception
     */
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.inMemoryAuthentication()
                .withUser("user")
                .password(bCryptPasswordEncoder().encode("abc123"))
                .roles("user")
                .and()
                .withUser("admin")
                .password(bCryptPasswordEncoder().encode("abc123"))
//                .authorities("sys:log","sys:user")
                .roles("admin")
                .and()
                .passwordEncoder(bCryptPasswordEncoder());//配置BCrypt加密
    }

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder(){
        return new BCryptPasswordEncoder();
    }

    /**
     * 静态资源访问不需要鉴权
     * @param web
     * @throws Exception
     */
    @Override
    public void configure(WebSecurity web) throws Exception {
        web.ignoring().antMatchers("/css/**", "/fonts/**", "img/**", "js/**");
    }

}
```



###方法级别过滤的注解
**四个方法级别的过滤注解：**
@EnableGlobalMethodSecurity(prePostEnabled
 = true)使用表达式时间方法级别的安全性 4个注解可用（hasRole hasAnyRole hasAuthority hasAnyAuthority）。
- @PreAuthorize
例：@PreAuthorize("hasRole('admin')") 在方法执行前进行判断，如果当前用户不是admin角色，则拒绝访问，抛出异常。
- @PreFilter
例：@PreFilter(filterTarget="ids",value="filterObject%2==0") 在方法执行前对参数数组ids进行过滤，对数组中的值filterObject进行判断，不满足条件的参数剔除。
- @PostAuthorize
例：@PostAuthorize("returnObject.name == authentication.name")  在方法执行后进行判断，如果不满足条件，则拒绝访问，抛出异常。
- @PostFilter
例：@PostFilter("filterObject.name == authentication.name") 在方法执行之后对返回值数组进行过滤，将不满足条件的返回值剔除。


###记住密码RememberMe
通过创建并验证remember-me session，可以不输入账号密码进行登录。

#####memory模式实现记住密码
后台配置：http.rememberMe()
前端配置：<label><input type="checkbox" name="remember-me"/>记住密码</label>
如果前端采用的是ajax方式进行请求
```js
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>首页</title>
</head>
<body>
    <h1>业务系统登录</h1>
    <form action="/login" method="post">
        <span>用户</span><input type="text" name="username" id="username"/> <br>
        <span>密码</span><input type="password" name="password" id="password"/> <br>
        <input type="button" onclick="login()" value="登录">
        <label><input type="checkbox" name="remember-me" id="remember-me" />记住密码</label>
    </form>

    <script src="https://cdn.staticfile.org/jquery/1.12.3/jquery.min.js"></script>
    <script>
        function login(){
            var username = $("#username").val();
            var password = $("#password").val();
            var rememberMe = $("#remember-me").is(":checked");
            if (username === "" || password === "") {
                alert("用户名或密码不能为空");
                return;
            }
            $.ajax({
                type: "POST",
                url: "/login",
                data: {
                    "username": username,
                    "password": password,
                    "remember-me-new": rememberMe
                },
                success: function(json){
                    if (json.code === 200) {
                        location.href = json.data;
                    }else{
                        alert(json.message);
                    }
                },
                error: function(error){
                    console.log(e.responseText)
                }
            })
        }
    </script>

</body>
</html>
```
```java
http.rememberMe()
    .rememberMeParameter("remember-me-new") //前端传入的参数名需要对应
    .rememberMeCookieName("remember-me-cookie") //生成的cookie的名称
    .tokenValiditySeconds(60*60*24*2) //该session的有效期
```
*新增一个remember-me session*
![image.png](https://upload-images.jianshu.io/upload_images/21580557-6bcf8f564e33457f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***原理***
通过创建remember-me session，存储了remember-me token，令牌记录了用户名、过期时间和signatureValue。signatureValue是用户名、过期时间、密码和预定义key的MD5加密后的签名。

进行登录时，通过RememberMeAuthenticationFilter过滤器进行过滤。

#####数据库模式实现记住密码
![image.png](https://upload-images.jianshu.io/upload_images/21580557-9dad5e5a788c8464.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***依赖***
```
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
<dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
</dependency>
```
***配置***
```yml
spring:
  datasource:
    url: jdbc:mysql://116.62.148.11:3306/xxx?useUnicode=true&characterEncoding=utf-8
    driver-class-name: com.mysql.jdbc.Driver
    username: root
    password: abc123
```

***数据库表创建***
```sql
CREATE TABLE persistent_logins (
    username varchar(64) NOT NULL,
    series varchar(64) NOT NULL,
    token varchar(64) NOT NULL,
    last_used timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (series)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
***java代码***
```java
    http.rememberMe()
      .rememberMeParameter("remember-me-new") //前端传入的参数名需要对应
      .rememberMeCookieName("remember-me-cookie") //生成的cookie的名称
      .tokenValiditySeconds(60*60*24*2) //该session的有效期
      .tokenRepository(persistentTokenRepository()) //配置remember-me的token存储在指定的数据库中，缺省为存储在内存中。

    /**
     * 注入dataSource对象
     */
    @Resource
    private DataSource dataSource;

    /**
     * 将数据库连接封装到框架中
     *
     * @return
     */
    @Bean
    public PersistentTokenRepository persistentTokenRepository() {
        JdbcTokenRepositoryImpl tokenRepository = new JdbcTokenRepositoryImpl();
        tokenRepository.setDataSource(dataSource);

        return tokenRepository;
    }
```

![数据库存储的token](https://upload-images.jianshu.io/upload_images/21580557-a86821878c67123b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###退出登录功能
logout功能默认的四个行为：
- 当前用户session失效
- 删除当前用户的remember-me功能信息
- 清除当前的SecurityContext上下文
- 重定向到登录页面，loginPage()配置项指定的页面

***最简实现***
后端代码：http.logout();
前端代码：<a href="/logout">退出</a>

***个性化配置***
```java
http.logout()
                .logoutUrl("/logout") //退出登录的请求接口
//                .logoutSuccessUrl("/login.html") //退出登录后重定向的路径
                .deleteCookies("JSESSIONID") //退出时删除浏览器中的cookie，默认会删除session和remember-me session。
                .logoutSuccessHandler(myLogoutSuccessHandler) //;自定义登出成功的方法,不能和logoutSuccessUrl方法同时使用
```
注意：重定向的资源需要有访问权限，否则默认跳转到登录页面。
```java
@Component
public class MyLogoutSuccessHandler implements LogoutSuccessHandler {
    @Override
    public void onLogoutSuccess(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Authentication authentication) throws IOException, ServletException {
        httpServletResponse.sendRedirect("/login.html");
    }
}
```
可以自定义个性化退出功能，如统计用户登录时间。


###图片验证码
***基于session的验证***
客户端请求验证图片；服务端生成session并保存验证图片的文字，并返回验证图片；客户端携带验证的文字发起登录请求，服务端取出文字与session中的验证码进行验证，如果正确，则进行登录操作，不正确，则返回失败信息。

***共享session***
如果服务端是分布式的，那么需要redis作为共享session，存储验证码并在验证时读取验证码到服务器进行验证。

***基于对称算法的验证***
不需要在服务端生成session存储验证码信息的无状态应用。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-0fd90b69411300a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
1.生成验证码文字，对验证码文字进行对称加密，生成验证码图片。将验证码密文和图片发送给客户端。
2.客户端发送登录请求时会携带用户识别的验证文字和验证码密文，服务端将两个验证码文字进行比对，如果正确，进行登录操作。


***验证码工具类库***
1.生成验证码文字或其他用于校验的数据形式（即谜底）
2.生成验证码前端显示图片或拼图等（即谜面）
3.用于校验用户输入与谜底的校验方法（如果是基于物理图形拖拽、旋转等方式，需要专用的校验方式）

*依赖*
```
<dependency>
    <groupId>com.github.penggle</groupId>
    <artifactId>kaptcha</artifactId>
    <version>2.3.2</version>
    <excludes>
      <exclude>
        <groupId>javax.servlet-api</groupId>
        <artifactId>javax.servlet</artifactId>
      </exclude>
    </excludes>
</dependency>
```
*配置*
新建配置类kaptcha.properties
```properties
kaptcha.border=no
kaptcha.border.color=105,179,90 
kaptcha.image.width=100 #图片宽度
kaptcha.image.height=45 #图片高度
kaptcha.session.key=code 
kaptcha.textproducer.font.color=blue #字体颜色
kaptcha.textproducer.font.size=35 #字体大小
kaptcha.textproducer.char.length=4 #验证码长度
kaptcha.textproducer.font.names=宋体,楷体,微软雅黑
```
*配置加载类*
```java
@Component
@PropertySource(value = {"classpath:kaptcha.properties"})
public class CaptchaConfig {

    @Value("${kaptcha.border}")
    private String border;
    @Value("${kaptcha.border.color}")
    private String borderColor;
    @Value("${kaptcha.image.width}")
    private String imageWidth;
    @Value("${kaptcha.image.height}")
    private String imageHeight;
    @Value("${kaptcha.session.key}")
    private String sessionKey;
    @Value("${kaptcha.textproducer.font.color}")
    private String fontColor;
    @Value("${kaptcha.textproducer.font.size}")
    private String fontSize;
    @Value("${kaptcha.textproducer.font.names}")
    private String fontNames;
    @Value("${kaptcha.textproducer.char.length}")
    private String charLength;

    @Bean(name = "captchaProducer")
    public DefaultKaptcha getKaptchaBean(){
        DefaultKaptcha defaultKaptcha = new DefaultKaptcha();

        Properties properties = new Properties();
        properties.setProperty("kaptcha.border", border);
        properties.setProperty("kaptcha.border.color", borderColor);
        properties.setProperty("kaptcha.image.width", imageWidth);
        properties.setProperty("kaptcha.image.height", imageHeight);
        properties.setProperty("kaptcha.session.key", sessionKey);
        properties.setProperty("kaptcha.textproducer.font.color", fontColor);
        properties.setProperty("kaptcha.textproducer.font.size", fontSize);
        properties.setProperty("kaptcha.textproducer.font.names", fontNames);
        properties.setProperty("kaptcha.textproducer.char.length", charLength);

        defaultKaptcha.setConfig(new Config(properties));

        return defaultKaptcha;
    }

}
```
接口类
```java
@RestController
public class CaptchaController {

    @Resource
    private DefaultKaptcha captchaProducer;

    @GetMapping("/kaptcha")
    public void kaptcha(HttpSession session, HttpServletResponse response) {
        response.setDateHeader("Expires",0);
        response.setHeader("Cache-Control", "no-store,no-cache,must-revalidate");//不能使用缓存
        response.addHeader("Cache-Control","post-check=0,pre-check=0");
        response.setHeader("Pragma","no-cache");
        response.setContentType("image/jpeg");

        //生成验证码
        String text = captchaProducer.createText();
        //将验证码和过期时间封装为对象保存到session中
        session.setAttribute("captcha_key",new CaptchaImageVO(text,60));
        //写出到输出流中
        ServletOutputStream outputStream = null;
        try {
            outputStream = response.getOutputStream();
            BufferedImage image = captchaProducer.createImage(text);
            ImageIO.write(image, "jpg", outputStream);
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            if(outputStream != null) {
                try {
                    outputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```
实体类
```java
@Data
public class CaptchaImageVO {

    private String code;
    private LocalDateTime expireTime;

    public CaptchaImageVO(String code,int expireAfterSeconds){
        this.code = code;
        this.expireTime = LocalDateTime.now().plusSeconds(expireAfterSeconds);
    }
    //判断是否过期
    public boolean isExpired(){
        return LocalDateTime.now().isAfter(expireTime);
    }

}
```
前端代码
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>首页</title>
</head>
<body>
    <h1>业务系统登录</h1>
    <form action="/login" method="post">
        <span>用户</span><input type="text" name="username" id="username"/> <br>
        <span>密码</span><input type="password" name="password" id="password"/> <br>
        <span>验证码</span><input type="text" name="captchaCode" id="captchaCode"/> <br>
        <img src="/kaptcha" id="kaptcha" width="110px" height="40px"/> <br>
        <input type="button" onclick="login()" value="登录">
        <label><input type="checkbox" name="remember-me"/>记住密码</label>
    </form>

    <script src="https://cdn.staticfile.org/jquery/1.12.3/jquery.min.js"></script>
    <script>
        window.onload = function(){
            var kaptchaImg = document.getElementById("kaptcha");

            kaptchaImg.onclick = function(event){
                kaptchaImg.src = "/kaptcha?" + Math.floor(Math.random() * 100)
            }
        }
        function login(){
            var username = $("#username").val();
            var password = $("#password").val();
            var captchaCode = $("#captchaCode").val();
            var rememberMe = $("#remember-me").is(":checked");
            if (username === "" || password === "") {
                alert("用户名或密码不能为空");
                return;
            }
            $.ajax({
                type: "POST",
                url: "/login",
                data: {
                    "username": username,
                    "password": password,
                    "captchaCode": captchaCode,
                    "remember-me": rememberMe
                },
                success: function(json){
                    if (json.code === 200) {
                        location.href = json.data;
                    }else{
                        alert(json.message);
                    }
                },
                error: function(error){
                    console.log(e.responseText)
                }
            })
        }
    </script>

</body>
</html>
```

后端需要对返回的验证码进行校验
自定义拦截器
```java
@Component
public class CaptchaCodeFilter extends OncePerRequestFilter {

    @Resource
    MyAuthenticationFailureHandler myAuthenticationFailureHandler;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        if (StringUtils.equals("/login", request.getRequestURI()) && StringUtils.equalsIgnoreCase("post", request.getMethod())) {
            try {
                validate(new ServletWebRequest(request));
            } catch (AuthenticationException e) {
                myAuthenticationFailureHandler.onAuthenticationFailure(request,response,e);
                return;
            }
        }
        System.out.println("filterChain.doFilter(request,response)");
        filterChain.doFilter(request,response);
    }

    private void validate(ServletWebRequest request) throws ServletRequestBindingException {

        HttpSession session = request.getRequest().getSession();

        String codeInRequest = ServletRequestUtils.getStringParameter(request.getRequest(), "captchaCode");


        if (StringUtils.isEmpty(codeInRequest)) {
            throw new SessionAuthenticationException("验证码不能为空");
        }

        CaptchaImageVO codeInSession = (CaptchaImageVO)session.getAttribute(MyConstants.CAPTCHA_SESSION_KEY);
        if (Objects.isNull(codeInSession)) {
            throw new SessionAuthenticationException("验证码不存在");
        }

        if (codeInSession.isExpired()) {
            session.removeAttribute(MyConstants.CAPTCHA_SESSION_KEY);
            throw new SessionAuthenticationException("验证码已过期");
        }

        if (!codeInRequest.equals(codeInSession.getCode())) {
            throw new SessionAuthenticationException("验证码不匹配");
        }
    }
}
```
设置过滤器
```java
http.addFilterBefore(captchaCodeFilter,UsernamePasswordAuthenticationFilter.class) //将验证码过滤器放到账号密码前面执行
```
验证失败处理类
```java
@Component
public class MyAuthenticationFailureHandler extends SimpleUrlAuthenticationFailureHandler {

    @Value("${spring.security.loginType}")
    private String loginType;

    @Override
    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException, ServletException {
        String errorMsg = "用户名或密码错误";
        //首先处理校验码部分抛出的异常
        if (exception instanceof SessionAuthenticationException) {
            errorMsg = exception.getMessage();
        }
        //再处理账号密码抛出的异常
        if ("JSON".equalsIgnoreCase(loginType)) {
            response.setContentType("application/json;charset=UTF-8");
            response.getWriter().write(new ObjectMapper().writeValueAsString(CommonResult.error().setMessage(errorMsg)));
        } else {
            super.onAuthenticationFailure(request,response,exception);
        }
    }
}
```


###短信验证码登录功能
TODO


###外部数据库校验账号密码
#####RBAC 基于角色的访问权限控制
![image.png](https://upload-images.jianshu.io/upload_images/21580557-0cb5dbe4f520ff7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***关键类***
- UserDetails :UserDetail包含了用户信息，用户名、密码和该用户所有的权限，将用户信息封装到认证对象中去，最终交给Spring Security，Spring Security 会根据 UserDetails中的 password 和客户端传递过来的 password 进行比较。如果相同则表示认证通过,如果不相同表示认证失败。
![UserDetails](https://upload-images.jianshu.io/upload_images/21580557-f9e7b8f106228527.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
注意一下getAuthorities方法，这个方法返回的是权限，但是我们返回的权限必须带有“ROLE_”开头才可以，spring会自己截取ROLE_后边的字符串

- UserDetailsService：接口需要实现loadUserByUsername方法，通过用户名从数据存储系统中查询用户信息(账号密码和权限信息)并封装为UserDetails对象返回。

- UserDetailsServiceAutoConfiguration

- UserDetailsManager：

- BCryptPasswordEncoder：BCryptPasswordEncoder 是 Spring Security 官方推荐的密码解析器，BCryptPasswordEncoder 是对 bcrypt 强散列方法的具体实现。是基于 Hash 算法实现的单向加密.可以通过 strength 控制加密强度,默认 10，每次加密的结果都不一样。

***代码***
数据库查询
```java
@Component
public interface MyUserDetailsServerMapper {

    /**
     * 根据用户名查询
     * @param username
     * @return
     */
    @Select("SELECT username,password " +
            "FROM tb_user " +
            "WHERE username=#{username}")
    MyUserDetails findByUsername(@Param("username") String username);

    /**
     * 根据用户名查询角色列表
     * @param username
     * @return
     */
    @Select("SELECT r.enname " +
            "FROM tb_role r " +
            "LEFT JOIN tb_user_role ur ON ur.role_id=r.id " +
            "LEFT JOIN tb_user u ON u.id=ur.user_id " +
            "WHERE u.username=#{username}")
    List<String> findRoleByUsername(@Param(value = "username") String username);

    /**
     * 根据用户角色查询权限
     * @param roleCodes
     * @return
     */
    @Select("<script> " +
            "SELECT url " +
            "FROM tb_permission p " +
            "LEFT JOIN tb_role_permission rp ON rp.permission_id=p.id " +
            "LEFT JOIN tb_role r ON r.id=rp.role_id " +
            "WHERE r.enname IN " +
            "<foreach collection='roleCodes' item='roleCode' open='(' separator=',' close=')'> " +
            "#{roleCode} " +
            "</foreach> " +
            "</script>")
    List<String> findAuthorityByRoleCodes(@Param(value = "roleCodes") List<String> roleCodes);

}
```
自定义MyUserDetails类继承UserDetails
```java
@Component
@Data
public class MyUserDetails implements UserDetails {

    private String username;
    private String password;
    boolean accountNonExpired = true; // 账号是否过期
    boolean accountNonLocked = true; //用户是否被锁定
    boolean credentialsNonExpired = true; //凭证是否过期
    boolean enabled = true; //账号是否可用
    Collection<? extends GrantedAuthority> authorities; //用户权限集合

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return accountNonExpired;
    }

    @Override
    public boolean isAccountNonLocked() {
        return accountNonLocked;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return credentialsNonExpired;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }
}
```
自定义MyUserDetailsServer类继承UserDetailsService ，为框架提供UserDetails对象
```java
@Service
@Slf4j
public class MyUserDetailsServer implements UserDetailsService {

    @Resource
    private MyUserDetailsServerMapper myUserDetailsServerMapper;

    /**
     * 将账号密码和权限信息封装到UserDetails对象中返回
     * @param username
     * @return
     * @throws UsernameNotFoundException
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        //通过查询数据库获取用户的账号密码
        MyUserDetails myUserDetails = myUserDetailsServerMapper.findByUsername(username);

        List<String> roleCodes = myUserDetailsServerMapper.findRoleByUsername(username);
        List<String> authorities = myUserDetailsServerMapper.findAuthorityByRoleCodes(roleCodes);

        //将用户角色添加到用户权限中
        authorities.addAll(roleCodes);

        //设置UserDetails中的authorities属性，需要将String类型转换为GrantedAuthority
        myUserDetails.setAuthorities(AuthorityUtils.commaSeparatedStringToAuthorityList(String.join(",",authorities)));

        log.info("UserDetail:" + myUserDetails);
        return myUserDetails;
    }

}
```
![常用权限表达式](https://upload-images.jianshu.io/upload_images/21580557-a3beece328ebce35.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
***WebSecurityConfigurerAdapter实现类***
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Resource
    private MyAuthenticationSuccessHandler mySuthenticationSuccessHandler;

    @Resource
    private MyAuthenticationFailureHandler myAuthenticationFailureHandler;

    @Resource
    private CaptchaCodeFilter captchaCodeFilter;

    /**
     * 采用formLogin方式进行认证
     *
     * @param http
     * @throws Exception
     */
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                //设置过滤器
                .addFilterBefore(captchaCodeFilter, UsernamePasswordAuthenticationFilter.class) //将验证码过滤器放到账号密码前面执行
                //退出登录
                .logout()
                .logoutUrl("/logout") //退出登录的请求接口
                .logoutSuccessUrl("/login.html") //退出登录后跳转的路径
                .deleteCookies("JSESSIONID") //退出时删除浏览器中的cookie
                .and()
                //自动登录
                .rememberMe()
                .rememberMeParameter("remember-me-new")
                .rememberMeCookieName("remember-me-cookie")
                .tokenValiditySeconds(60 * 60 * 24 * 2)
                .tokenRepository(persistentTokenRepository())
                .and()
                //禁用csrf攻击防御
                .csrf().disable()
                //1.formLogin配置段
                .formLogin()
                .loginPage("/login.html")//用户访问资源时先跳转到该登录页面
                .loginProcessingUrl("/login")//登录表单中的action的地址，在该接口中进行认证
                .usernameParameter("username")//登录表单form中的用户名输入框input的name名，缺省是username
                .passwordParameter("password")//登录表单form中的密码输入框input的name名，缺省是username
//                .defaultSuccessUrl("/index")//登录成功后默认跳转的路径
                .successHandler(mySuthenticationSuccessHandler)//使用自定义的成功后的逻辑
//                .failureUrl("/login.html") //登录失败后返回登录页
                .failureHandler(myAuthenticationFailureHandler) //使用自定义的失败后的逻辑
                .and()
                //2.authorizeRequests配置端
                .authorizeRequests()
                .antMatchers("/login.html", "/login", "/kaptcha").permitAll() //不需要验证即可访问
                .antMatchers("/index.html").authenticated() //通过认证即可访问
                .anyRequest().access("@rbacService.hasPermission(request,authentication)")
//                .antMatchers("/contents/view/biz1", "/contents/view/biz2").hasAnyAuthority("ROLE_operator", "ROLE_admin")//user和admin权限可以访问的路径，等同于hasAnyRole("user","admin")
////                .antMatchers("/syslog","/sysuser").hasAnyRole("admin")//admin角色可以访问的路径
//                .antMatchers("/users/view/syslog","/syslog.html").hasAuthority("/users/view/**")//权限id，有该id的用户可以访问
//                .antMatchers("/users/view/sysuser").hasAuthority("/users/view/**")
//                .anyRequest().authenticated()
                .and()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
                .invalidSessionUrl("/login.html")
                .sessionFixation().migrateSession()
                .maximumSessions(1) //最大登录数为1
                .maxSessionsPreventsLogin(false)//false表示允许再次登录但会踢出之前的登陆；true表示不允许再次登录
                .expiredSessionStrategy(new MyExpiredSessionStrategy());//会话过期后进行的自定义操作
    }

    @Resource
    private MyUserDetailsServer myUserDetailsServer;

    /**
     * 将角色信息存储在内存中
     *
     * @param auth
     * @throws Exception
     */
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(myUserDetailsServer).passwordEncoder(bCryptPasswordEncoder());
    }

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /**
     * 静态资源访问不需要鉴权
     *
     * @param web
     * @throws Exception
     */
    @Override
    public void configure(WebSecurity web) throws Exception {
        web.ignoring().antMatchers("/css/**", "/fonts/**", "img/**", "js/**");
    }

    /**
     * 注入dataSource对象
     */
    @Resource
    private DataSource dataSource;

    /**
     * 将数据库连接封装到框架中
     *
     * @return
     */
    @Bean
    public PersistentTokenRepository persistentTokenRepository() {
        JdbcTokenRepositoryImpl tokenRepository = new JdbcTokenRepositoryImpl();
        tokenRepository.setDataSource(dataSource);

        return tokenRepository;
    }

}
```
***验证权限类***
```java
@Component(value = "rbacService")
public class MyRBACServer {

    @Resource
    private MyRBACServerMapper myRBACServerMapper;

    public boolean hasPermission(HttpServletRequest request, Authentication authentication) {

        Object principal = authentication.getPrincipal();

        if (principal instanceof UserDetails) {
            UserDetails userDetails = (UserDetails) principal;
            String username = userDetails.getUsername();

            List<String> authorities = myRBACServerMapper.findAuthorityByUsername(username);

            return authorities.stream().anyMatch(uri -> new AntPathMatcher().match(uri,request.getRequestURI()));
        }

        return false;
    }

}
```
***权限查询类***
```java
@Component
public interface MyRBACServerMapper {

    @Select("SELECT url\n" +
            "FROM tb_permission p\n" +
            "LEFT JOIN tb_role_permission rp ON rp.permission_id=p.id\n" +
            "LEFT JOIN tb_role r ON r.id=rp.role_id\n" +
            "LEFT JOIN tb_user_role ur ON ur.user_id=r.id\n" +
            "LEFT JOIN tb_user u ON u.id=ur.user_id\n" +
            "WHERE username=#{username};")
    List<String> findAuthorityByUsername(@Param("username") String username);
}
```

<br>

###JWT
**Session缺点**
- 非浏览器的客户端、手机移动端等不会自动维护cookie；
- 集群应用，session在不同服务器上状态不统一。

**JWT优点：**
- jwt基于json，非常方便使用；
- 可以在令牌中自定义丰富的内容，易扩展；
- 通过非对称加密算法和数字签名技术，JWT防止篡改，安全性高；
- 资源服务使用JWT可不依赖认证服务器即可完成授权。


***JWT令牌使用方式***
![image.png](https://upload-images.jianshu.io/upload_images/21580557-fcbfce47a60a96b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***JWT令牌结构***
![image.png](https://upload-images.jianshu.io/upload_images/21580557-c512e514d75f5d34.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
JWT令牌结构分为三部分：
- Header：包括令牌的类型（即JWT）及使用的哈希算法（如HMAC、SHA256或RSA）
- Payload：存放有效信息，如iss（签发者）、exp（过期时间）、sub（授权用户）和创建时间等，也可以自定义字段方便扩展。
- Signature：是对前两部分的数字签名，防止被篡改。

***JWT安全加强***
- 避免网络劫持，HTTP协议使用header传递JWT容易泄露，使用HTTPS协议传输更安全。
- 私钥存放在服务器端，保证服务器不被攻破。
- JWT可以被暴力破解，所以需要保证秘钥复杂度，定期更换秘钥。

***JWT鉴权流程***
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d838977c26327c22.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
 ***依赖***
```
<dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt</artifactId>
            <version>0.9.0</version>
</dependency>
```


***步骤***
`通过账号密码获取JWT令牌token`
1.在登录接口中，先通过AuthenticationManager类提供的校验方法对账号密码进行校验，会调用UserDetailsService方法查询UserDetails。
2.1如果校验不通过，抛出异常。
2.2如果校验通过，查询数据库得到该用户的UserDetails，调用生成token方法返回token。
所以会对数据库进行两次插叙，效率问题是否可以改进。
`通过JWT令牌token进行身份验证`
需要将token转换为Security框架识别的Authentication对象。
1.通过秘钥解析token，获取用户信息，校验用户是否合法
2.1不合法则直接发往下一个拦截器
2.2合法，则通过UserDetailsService获取UserDetails，通过UserDetails和UserDetails中的权限信息生成Authentication对象设置到上下文中，认证完成，后续拦截器放行。
3.将该token认证拦截器放到账号密码认证拦截器前执行。

`请求流程 `
1.通过账号密码认证后返回token令牌，将token放到header中发起请求。
2.后台接受请求先验证token有效性
3.如果认证有效，再通过access方法验证权限有效性，通过自定义的MyRBACServer类获取数据库中的用户权限和请求路径，如果路径匹配(支持/users/**格式匹配)，则有权限访问，返回资源。
4.刷新token并返回。

***关键类***
- authenticationManager：在 UsernamePasswordAuthenticationFilter 源码分析 中，最后在类UsernamePasswordAuthenticationFilter 的验证方法 attemptAuthentication() 会将用户表单提交过来的用户名和密码封装成对象委托类 AuthenticationManager 的验证方法 authenticate() 进行身份验证。

- Authentication：SecurityContextHolder.getContext().getAuthentication(); 从上下文中获取当前线程中的验证信息。                    UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
生成Authentication对象。Security上下文中已经设置过Authentication对象，那么认证过程已完成，后续拦截器会放行。

获得的token为
```
{
    "code": 200,
    "message": "success",
    "data": "eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE1OTc3Mjk1NjIsInN1YiI6ImFkbWluIiwiY3JlYXRlZCI6MTU5NzcyNTk2MjQxNX0.qwyZ2-2rgVfNbQ3lPYfXDepy88FA77C0QCBjWb1gk-x_YvsnQukAh-DMHNhAOJ2T7tOrRkdLT5NHt7O3FayYPw"
}
```
>第一段为加密算法，第二段为


***代码***
JWT工具类(提供token生成，token解析，token合法验证等功能)
```java
@Data
@ConfigurationProperties(prefix = "jwt")
@Component
public class JwtTokenUtil {

    private String secret;
    private Long expiration;
    private String header;

    /**
     * 生成jwt令牌
     * @param userDetails
     * @return
     */
    public String generateToken(UserDetails userDetails) {
        HashMap<String, Object> claims = new HashMap<>(2);
        claims.put("sub", userDetails.getUsername());
        claims.put("created", new Date());
        return generateToken(claims);
    }

    /**
     * 令牌的过期时间，加密算法和秘钥
     * @param claims
     * @return
     */
    private String generateToken(Map<String, Object> claims) {
        Date date = new Date(System.currentTimeMillis() + expiration);
        return Jwts.builder().setClaims(claims)
                .setExpiration(date)
                .signWith(SignatureAlgorithm.HS512,secret)
                .compact();
    }

    /**
     * 获取token中的用户名
     * @param token
     * @return
     */
    public String getUsernameFromToken(String token) {
        String username = null;
        try {
            Claims claims = getClaimsFromToken(token);
            username = claims.getSubject();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return username;
    }

    /**
     * 获取token中的claims
     * @param token
     * @return
     */
    private Claims getClaimsFromToken(String token) {
        Claims claims = null;
        try {
            //获取claims的过程就是对token合法性检验的过程，将token解析为Claims对象
            claims = Jwts.parser().setSigningKey(secret).parseClaimsJws(token).getBody();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return claims;
    }

    /**
     * 判断token是否过期
     * @param token
     * @return
     */
    public Boolean isTokenExpired(String token) {
        Claims claims = getClaimsFromToken(token);
        Date expiration = claims.getExpiration();
        return expiration.before(new Date());
    }

    /**
     * 刷新token令牌，将新的生成时间放入claims覆盖原时间并和从新生成token
     * @param token
     * @return
     */
    public String refreshToken(String token) {
        String refreshedToken = null;
        try {
            Claims claims = getClaimsFromToken(token);
            claims.put("created", new Date());
            refreshedToken = generateToken(claims);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return refreshedToken;
    }

    /**
     * 校验token是否合法和过期
     * @param token
     * @param userDetails
     * @return
     */
    public Boolean validateToken(String token, UserDetails userDetails) {
        String username = getUsernameFromToken(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }

}
```

token认证过滤器
```java
@Component
@Slf4j
public class JwtAuthenticationTokenFilter extends OncePerRequestFilter {

    @Resource
    private JwtTokenUtil jwtTokenUtil;

    @Resource
    private MyUserDetailsServer myUserDetailsServer;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        String token = request.getHeader(jwtTokenUtil.getHeader());
        if (!StringUtils.isEmpty(token)) {
            String username = jwtTokenUtil.getUsernameFromToken(token);
            log.info(username);
            //用户名非空且token没有进行过校验
            if(!Objects.isNull(username) && SecurityContextHolder.getContext().getAuthentication() == null) {
                UserDetails userDetails = myUserDetailsServer.loadUserByUsername(username);
                if (jwtTokenUtil.validateToken(token, userDetails)) {
                    //通过用户和权限生成Authentication对象
                    UsernamePasswordAuthenticationToken authenticationToken = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                    log.info("验证通过");
                    //将Authentication对象设置到上下文中，验证完成，后续拦截器放行
                    SecurityContextHolder.getContext().setAuthentication(authenticationToken);
                }
            }
        }
        log.info("交给后续拦截器");
        //交给后续拦截器验证，如果已设置Authentication对象到上下文中，验证完成，后续拦截器放行
        filterChain.doFilter(request,response);
    }

}
```

JWT接口层
```java
@RestController
@Slf4j
public class JwtAuthController {

    @Resource
    JwtAuthService jwtAuthService;

    @RequestMapping(value = "/authentication")
    public CommonResult login(@RequestBody Map<String,String> map){
        String username = map.get("username");
        String password = map.get("password");

        if (StringUtils.isEmpty(username) || StringUtils.isEmpty(password)) {
            throw new IllegalArgumentException("账号或密码不能为空");
        }

        String token = jwtAuthService.login(username, password);

        log.info("token:"+token);
        return CommonResult.success().setData(token);
    }

    /**
     * 刷新请求头中的token令牌
     * @param token
     * @return
     */
    @RequestMapping(value = "/refreshToken")
    public CommonResult refresh(@RequestHeader("${jwt.header}") String token) {
        String newToken = jwtAuthService.refreshToken(token);
        return CommonResult.success().setData(newToken);
    }

}
```

JWT服务层
```java
@Service
public class JwtAuthService {

    //UsernamePasswordAuthenticationFilter最终会将用户名密码通过AuthenticationManager的authenticate方法进行验证
    @Resource
    AuthenticationManager authenticationManager;

    @Resource
    UserDetailsService userDetailsService;

    @Resource
    JwtTokenUtil jwtTokenUtil;

    /**
     * 登录认证换取JWT令牌
     * @return
     */
    public String login(String username,String password){
        try {
            //根据账号密码构造token
            UsernamePasswordAuthenticationToken upToken = new UsernamePasswordAuthenticationToken(username, password);
            //通过该方法对账号密码进行认证，认证不通过则抛出异常
            Authentication authenticate = authenticationManager.authenticate(upToken);
            //认证通过则将认证结果放入上下文
            SecurityContextHolder.getContext().setAuthentication(authenticate);
        } catch (AuthenticationException e) {
            throw new IllegalArgumentException("账号密码认证不通过");
        }

        //验证通过后，根据username查询数据库中的该用户的详细信息，生成token返回
        UserDetails userDetails = userDetailsService.loadUserByUsername(username);
        return jwtTokenUtil.generateToken(userDetails);
    }

    /**
     * 刷新请求头中的token令牌
     *
     * @param oldToken
     * @return
     */
    public String refreshToken(String oldToken) {
        if (!jwtTokenUtil.isTokenExpired(oldToken)) {
            return jwtTokenUtil.refreshToken(oldToken);
        }

        return null;
    }

}
```
SecurityConfig
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Resource
    private JwtAuthenticationTokenFilter jwtAuthenticationTokenFilter;

    /**
     * 采用JWT方式进行认证
     *
     * @param http
     * @throws Exception
     */
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                //设置token认证过滤器
                .addFilterBefore(jwtAuthenticationTokenFilter, UsernamePasswordAuthenticationFilter.class)
                //开启csrf攻击防御,通过cookie存储csrf令牌
                .csrf()
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
                .ignoringAntMatchers("/authentication")
                .and()
                //开启跨站资源共享
                .cors()
                .and()
                //authorizeRequests配置端
                .authorizeRequests()
                .antMatchers("/login.html", "/login", "/kaptcha", "/authentication", "/refreshToken").permitAll() //不需要验证即可访问
                .antMatchers("/index.html").authenticated()
                .anyRequest().access("@rbacService.hasPermission(request,authentication)")
//                .antMatchers("/biz1", "/biz2").hasAnyAuthority("ROLE_user", "ROLE_admin")//user和admin权限可以访问的路径，等同于hasAnyRole("user","admin")
////                .antMatchers("/syslog","/sysuser").hasAnyRole("admin")//admin角色可以访问的路径
//                .antMatchers("/syslog").hasAuthority("sys:log")//权限id，有该id的用户可以访问
//                .antMatchers("/sysuser").hasAuthority("sys:user")
                .and()
                //将session类型改为无状态，不创建也不使用session
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    }


    /**
     * 注入自定义用户信息加载对象
     */
    @Resource
    private UserDetailsService userDetailsService;

    /**
     * 将角色信息存储在数据库中,从数据库中动态加载用户账号密码及其权限
     *
     * @param auth
     * @throws Exception
     */
    @Override
    public void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService)
                .passwordEncoder(bCryptPasswordEncoder());
    }

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder(){
        return new BCryptPasswordEncoder();
    }

    /**
     * 静态资源访问不需要鉴权
     * @param web
     * @throws Exception
     */
    @Override
    public void configure(WebSecurity web) throws Exception {
        web.ignoring().antMatchers("/css/**", "/fonts/**", "img/**", "js/**");
    }

    /**
     * 注入认证管理器，在JwtAuthService类中使用
     * @return
     * @throws Exception
     */
    @Bean(name = BeanIds.AUTHENTICATION_MANAGER)
    @Override
    public AuthenticationManager authenticationManager() throws Exception {
        return super.authenticationManager();
    }

    /**
     * 添加security框架的同源策略
     * @return
     */
    @Bean
    CorsConfigurationSource corsConfigurationSource(){
        CorsConfiguration corsConfiguration = new CorsConfiguration();
        corsConfiguration.setAllowedOrigins(Arrays.asList("http://localhost:8080"));
        corsConfiguration.setAllowedMethods(Arrays.asList("GET","POST"));
        corsConfiguration.applyPermitDefaultValues();
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**",corsConfiguration);
        return source;
    }

}
```

>**如何使用Jwt和redis实现自动刷新token思路：**
可以将jwt保存在redis中，设置的key过期时间需要大于jwt的过期时间。key过期时间 - jwt过期时间 = 刷新token时间。
当请求进入后分为三种情况：
1. token无效或不携带token，返回无法访问资源；
2. token有效，允许访问资源；
3. token过期，则查询redis中是否有该token；如果存在，则刷新token，将新jwt存入redis中并返回给前端。如果不存在，则需要重新登录。


<br>
**附：**
![Database权限验证整合图片管理](https://upload-images.jianshu.io/upload_images/21580557-a8379669f570d56e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![JWT权限验证](https://upload-images.jianshu.io/upload_images/21580557-14a4249f8a104524.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**源码：**
https://github.com/ChenJie666/security.git
