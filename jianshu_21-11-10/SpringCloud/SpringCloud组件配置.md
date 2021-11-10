# 一、组件更替图：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-a37fc3fab2108ff9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 二、Springcloud各组件简单使用
## 2.1 springcloud依赖的最新版本
```
<dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>2.2.2.RELEASE</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-dependencies</artifactId>
        <version>Hoxton.SR1</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-alibaba-dependencies</artifactId>
        <version>2.1.0.RELEASE</version>
      </dependency>
```

## 2.2 actuator端点配置
**依赖**
```
 <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```
如果要访问`info`接口想获取`maven`中的属性内容请记得添加如下内容:
```
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <executions>
                <execution>
                    <goals>
                        <goal>build-info</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**配置**
`Spring Boot2.x`中，默认只开放了`info、health`两个端点，剩余的需要自己通过设置如下配置来加载（也有`exclude`属性）。
```
management:
  endpoints:
    web:
      exposure:
        include: refresh,health,info,env
```
如果想单独操作某个端点可以使用`management.endpoint.端点.enabled`属性进行启用或禁用。
```yml
# 描述信息
info:
  blog-url: http://www.jianshu.com
  author: CJ
  version: @project.version@

# 加载所有的端点，默认只加载了 info / health
management:
  endpoints:
    web:
      exposure:
        include: refresh,health,info,env
  endpoint:
    health:
      show-details: always

# 可以关闭制定的端点
management:
  endpoint:
    shutdown:
      enabled: false

# 路径映射，将 health 路径映射成 rest_health 那么在访问 health 路径将为404，因为原路径已经变成 rest_health 了，一般情况下不建议使用
# management.endpoints.web.path-mapping.health=rest_health
```



| id                 | desc                                                         | Sensitive |
| ------------------ | ------------------------------------------------------------ | --------- |
| **auditevents**    | 显示当前应用程序的审计事件信息                               | Yes       |
| **beans**          | 显示应用Spring Beans的完整列表                               | Yes       |
| **caches**         | 显示可用缓存信息                                             | Yes       |
| **conditions**     | 显示自动装配类的状态及及应用信息                             | Yes       |
| **configprops**    | 显示所有 @ConfigurationProperties 列表                       | Yes       |
| **env**            | 显示 ConfigurableEnvironment 中的属性                        | Yes       |
| **flyway**         | 显示 Flyway 数据库迁移信息                                   | Yes       |
| **health**         | 显示应用的健康信息（未认证只显示`status`，认证显示全部信息详情） | No        |
| **info**           | 显示任意的应用信息（在资源文件写info.xxx即可）               | No        |
| **liquibase**      | 展示Liquibase 数据库迁移                                     | Yes       |
| **metrics**        | 展示当前应用的 metrics 信息                                  | Yes       |
| **mappings**       | 显示所有 @RequestMapping 路径集列表                          | Yes       |
| **scheduledtasks** | 显示应用程序中的计划任务                                     | Yes       |
| **sessions**       | 允许从Spring会话支持的会话存储中检索和删除用户会话。         | Yes       |
| **shutdown**       | 允许应用以优雅的方式关闭（默认情况下不启用）                 | Yes       |
| **threaddump**     | 执行一个线程dump                                             | Yes       |
| **httptrace**      | 显示HTTP跟踪信息（默认显示最后100个HTTP请求 - 响应交换）     | Yes       |

>**简单测试**
>启动项目，访问 [http://localhost:8080/actuator/info](http://localhost:8080/actuator/info) 看到如下内容代表配置成功
>```
>{
>  "blog-url": "http://www.jianshu.com",
>  "author": "CJ",
>  "version": "0.0.1-SNAPSHOT"
>}
>```

参考文章：[http://blog.battcn.com/2018/05/24/springboot/v2-actuator-introduce/](http://blog.battcn.com/2018/05/24/springboot/v2-actuator-introduce/)



<br>
## 2.3 注册中心
### 2.3.1 eureka配置
####服务端
**依赖**
```
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

**配置文件**
```
server:
  port: 7001
eureka:
  server:
    enable-self-preservation: false #是否启用自动保护机制，默认为true
    eviction-interval-timer-in-ms: 2000 #清理间隔(单位毫秒,默认是60*1000ms) 
  client:
    register-with-eureka: false #false表示不向注册中心注册自己
    fetch-registry: false #false表示不需要去检索服务
    service-url:
      defaultZone:   http://eureka2.com:7002/eureka/,http://eureka3.com:7003/eureka/  #服务查询地址和注册地址
  instance:
    instance-id: eureka7001
    prefer-ip-address: true
    lease-expiration-duration-in-seconds: 15
    lease-renewal-interval-in-seconds: 5
    health-check-url-path: /actuator/health
```

**注解**
主启动类上加注解`@EnableEurekaServer`

####客户端
**依赖：**该依赖已集成ribbon，自动实现负载均衡
```
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```
**配置文件**
```yml
spring:
  application:
    name: REGISTER-CENTER
eureka:
  #server:
  #  enable-self-preservation: false  #自我保护机制禁用
  client: #将eureka注册进eureka服务中
    register-with-eureka: true #是否将自己注册进EurekaServer，默认为true
    fetch-registry: true #是否抓取注册信息，默认为true;配合ribbon使用负载均衡
    service-url:
    #单机
    #  defaultZone: http://localhost:7001/eureka/
    #集群
      defaultZone: http://eureka1.com:7001/eureka/,http://eureka2.com:7002/eureka,http://eureka3.com:7003/eureka/
  instance:
    instance-id: microservicecloud-dept8001-hystrix #自定义hystrix相关服务名称信息
    prefer-ip-address: true #访问路径可以显示IP地址
    health-check-url-path: /actuator/health
    eureka.instance.lease-renewal-interval-in-seconds=30 #Eureka客户端发送心跳间隔，默认为30秒;
    eureka.instance.lease-expiration-duration-in-seconds=90  #Eureka客户端发送心跳后指定时间内未收到心跳，则剔除服务。默认为90秒;
    # ip-address: xxxxxxxx    # 指定向eureka注册时的项目地址
```
**注解**
主启动类上加注解`@EnableEurekaClient`


# 消费者
#### 配置类
```
@Configuration
public class ApplicationContextConfig {

    @Bean
    @LoadBalanced    //需要添加负载均衡的注解，默认策略为轮询
    public RestTemplate getRestTemplate(){
        return new RestTemplate();
    }
}
```
#### 通过服务名访问
public static final String PAYMENT_URL = "http://CLOUD-PAYMENT-SERVICE";



#Discovery服务发现
#####获取DiscoveryClient对象
```
@Resource
private DiscoveryClient discoveryClient;

@GetMapping(value = "/payment/discovery")
    public Object discovery(){
        List<String> services = discoveryClient.getServices();
        for (String service : services) {
            log.info("***element:"+service);
        }

        List<ServiceInstance> instances = discoveryClient.getInstances("CLOUD-PAYMENT-SERVICE");
        for (ServiceInstance instance : instances) {
            log.info("***instance:" + instance.getServiceId() + "\t" + instance.getHost() + "\t" + instance.getPort() + "\t" + instance.getUri());
        }

        return discoveryClient;
    }
```
#####添加主启动类上的注解
@EnableDiscoveryClient



#Zookeeper配置（使用不多）：
//服务端
需要安装zookeeper组件作为服务端，可以用docker安装。可以进入zk客户端查看微服务的注册信息，生成的节点是临时节点，一旦心跳发送超时，就会断开连接，删除节点。

//客户端依赖
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-zookeeper-discovery</artifactId>
</dependency>

//客户端application配置文件
server:
  port: 8004
spring:
  application:
    name: cloud-provider-payment
  cloud:
    zookeeper:
      connect-string: 192.168.32.225:2181

//客户端注解
主启动类添加注解@EnableDiscoveryClient，该注解用于向使用consul或者zookeeper作为注册中心时注册服务



#Consul（用Go语言开发）
[https://www.springcloud.cc/spring-cloud-consul.html](https://www.springcloud.cc/spring-cloud-consul.html)
需要安装consul组件作为服务端，可以用docker安装
docker run -d --name consul consul agent -server -ui -bootstrap-expect=1 -client=0.0.0.0;
通过8500端口访问consul的前端网页，可以看到注册的服务（/actuator/health请求不到，service checks会显示红叉）。

//客户端依赖
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-consul-discovery</artifactId>
</dependency>

//客户端application配置文件
server:
  port: 8006
spring:
  application:
    name: cloud-provider-payment
  cloud:
    consul:
      host: 192.168.32.225
      port: 8500
      discovery:
        service-name: ${spring.application.name}

//客户端注解
主启动类添加注解@EnableDiscoveryClient，该注解用于向使用consul或者zookeeper作为注册中心时注册服务

CAP原则：Consistency(一致性) 、Availability(可用性) 、Partition tolerance(分区容错性)
![image.png](https://upload-images.jianshu.io/upload_images/21580557-382362e6ab06f712.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




## 2.Ribbon：
#####依赖
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-ribbon</artifactId>
</dependency>

#####在消费者中填写配置类
@Configuration
public class ConfigBean {   //TODO 词类等同于applicationContext.xml

    //TODO 配置了RestTemplate类的自动注入（@Autowired）
    @Bean
    @LoadBalanced   //TODO Ribbon负载均衡只需要加这个标签
    public RestTemplate getRestTemplate(){  //TODO 提供了多种便捷访问Http服务的方法，是一种简单便捷的访问restful服务模板类，是Spring提供的用于访问Rest服务的客户端模板工具类
        return new RestTemplate();
    }

    @Bean
    public IRule myRule(){
//        return new RoundRobinRule();  //TODO 默认的轮询算法
//        return new RandomRule();    //TODO 用随机算法替换轮训算法
        return new RetryRule(); //TODO retry算法，如果有个服务宕机了，会尝试几次后自动跳过
    }

}

通过eureka中的微服务名访问生产者，即可实现负载均衡。


还可以通过注解@RibbonClient(name="menu-center",configuration=MyRibbonRule.class)
@Configuration
public class ConfigBean {   //TODO 词类等同于applicationContext.xml

    //TODO 配置了RestTemplate类的自动注入（@Autowired）
    @Bean
    @LoadBalanced   //TODO Ribbon负载均衡只需要加这个标签
    public RestTemplate getRestTemplate(){  //TODO 提供了多种便捷访问Http服务的方法，是一种简单便捷的访问restful服务模板类，是Spring提供的用于访问Rest服务的客户端模板工具类
        return new RestTemplate();
    }

    @Bean
    public IRule myRule(){
//        return new RoundRobinRule();  //TODO 默认的轮询算法
//        return new RandomRule();    //TODO 用随机算法替换轮训算法
        return new RetryRule(); //TODO retry算法，如果有个服务宕机了，会尝试几次后自动跳过
    }

}
来指定使用的负载均衡算法,在MyRibbonRule类中指定使用的算法。
![七种自带负载均衡算法.png](https://upload-images.jianshu.io/upload_images/21580557-04b440ff7403a1ae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以自定义类继承AbstractLoadBalanceRuler类来自定义负载均衡算法。
这个自定义配置类不能放在@ComponentScan所扫描的当前包下以及子包下，否则我们自定义的这个配置类就会被所有的Ribbon客户端所共享，达不到特殊化定制的目的了。而@SpringApplication注解中的@ComponentScan注解会扫描当前包及其子包。
```java
@Configuration
public class MySelfRule{
  @Bean
  public IRule myRule(){
    return new RandomRule(); //定义为随机算法
  }
}
```
主启动类上添加注解@RibbonClient(name = "CLOUD-PAYMENT-SERVICE",configuration = MySelfRule.class)


#OpenFeign
[https://github.com/spring-cloud/spring-cloud-openfeign](https://github.com/spring-cloud/spring-cloud-openfeign)
OpenFeign在feign的基础上支持了SpringMVC的注解，如@RequestMapping等。OpenFeign的@FeignClient可以解析SpringMVC的@RequestMapping直接下的接口，并通过动态代理的方式产生实现类，实现类中做负载均衡并调用其他服务。OpenFeign已集成ribbon，默认启动负载均衡；
OpenFeign的访问超时功能：OpenFeign访问接口的默认超时时间为1s，超过1s会报错SocketTimeoutException；
```yml
\#设置feign客户端超时时间(OpenFeign默认支持ribbon)
ribbon:
  \#建立连接所用的时间
  ConnectTimeout: 1000
  \#建立连接后服务器响应时间
  ReadTimeout: 5000
```
```yml
feign:
  hystrix:
    enabled: true #开启feign的hystrix支持,默认是false 
  compression:
    request:
      enabled: true #为Feign请求启用GZIP压缩
      mime-types: text/xml,application/xml,application/json #压缩介质类型
      min-request-size: 2048 #最小请求阈值长度
    response:
      enabled: true #为Feign响应启用GZIP压缩
```
OpenFeign的增强日志打印功能：NONE(默认不显示任何日志)、BASIC(仅记录请求方法、URL、响应状态码及执行时间)、HEADERS(在BASIC基础上增加请求和响应的头信息)、FULL(在HEADERS基础上增加请求和响应的正文及元数据)
```java
@Configuration
public class FeignConfig {

    @Bean
    Logger.Level feignLoggerLevel(){
        return Logger.Level.FULL;
    }

}
```
```yml
logging:
  level:
    com.cj.springcloud.config.service.PaymentFeignService: debug
```

#####依赖：
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>

#####配置文件


#####注解：
在主启动类上添加注解@EnableFeignClients
创建服务类，添加@FeignClient注解，属性为需要调用的服务名
```java
@Service
public class PaymentService {

    public String paymentInfo_OK(Integer id) {
        return "线程池： " + Thread.currentThread().getName()+"   paymentInfo_OK,id  " + id;
    }

    @HystrixCommand(fallbackMethod = "paymentInfo_TimeOutHandler",commandProperties = {
            @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds",value = "2000")
    })
    public String paymentInfo_TimeOut(Integer id) {
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "线程池： " + Thread.currentThread().getName()+"   paymentInfo_timeout,id  " + id;
    }

    public String paymentInfo_TimeOutHandler(Integer id) {
        return "线程池： " + Thread.currentThread().getName()+"   paymentInfo_timeoutHandler,id  " + id;
    }

}
```


#Hystrix
#####依赖
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
Hystrix是处理分布式系统的延迟和容错的开源库。保证一个依赖出问题的情况下，不会导致整体服务失败，避免级联故障，提高分布式系统的弹性。
#####问题：
1. 超时导致服务器响应变慢 -> 超时不再等待
2. 出错(宕机或程序运行出错) -> 出错要有兜底措施
#####解决：
1. 对方服务超时，调用者不能一直等待，需要有降级服务
2. 对方服务宕机，调用者不能一直等待，需要有降级服务
3. 对方服务ok，调用者自己出故障或有自我要求，需要自己处理降级
#####hystrix功能：
1. 服务降级
- 介绍：服务器忙请稍后再试，不让客户端等待并立刻返回一个友好的提示；
- 产生原因：程序运行异常、超时、服务熔断触发、线程池/信号量打满也会导致服务降级；
① 生产端进行服务降级
***注解***
在主启动类上添加注解@EnableCircuitBreaker
***对接口进行降级***
```java
@Service
public class PaymentService {

    public String paymentInfo_OK(Integer id) {
        return "线程池： " + Thread.currentThread().getName()+"   paymentInfo_OK,id  " + id;
    }

    @HystrixCommand(fallbackMethod = "paymentInfo_TimeOutHandler",commandProperties = {
            @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds",value = "2000") //响应时间超过2s，则终止响应并调用备用方法。
    })
    public String paymentInfo_TimeOut(Integer id) {
        //异常或超时都可以触发服务降级
        int i = 1/0;
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return "线程池： " + Thread.currentThread().getName()+"   paymentInfo_timeout,id  " + id;
    }

    public String paymentInfo_TimeOutHandler(Integer id) {
        return "线程池： " + Thread.currentThread().getName()+"   系统繁忙或出现异常,id  " + id;
    }

}
```

② 消费端进行服务降级
***feign整合hystrix配置***
```yml
feign:
  hystrix:
    enabled: true #开启feign的hystrix支持,默认是false 
  compression:
    request:
      enabled: true
      mime-types[0]: text/xml
      mime-types[1]: application/xml
      mime-types[3]: application/json
      min-request-size: 2048
    response:
      enabled: true
```
***注解***
在主启动类上添加@EnableHystrix （包含@EnableCircuitBreaker）
***代码***
```java
@RestController
@DefaultProperties(defaultFallback = "payment_Global_Handler")
public class OrderFeignHystrixController {

    @Resource
    private PaymentFeignHystrixService paymentFeignHystrixService;

    @GetMapping(value = "/consumer/payment/hystrix/ok/{id}")
    public String paymentInfo_OK(@PathVariable("id") Integer id) {
        return paymentFeignHystrixService.paymentInfo_OK(id);
    }

//    @HystrixCommand(fallbackMethod = "paymentInfo_TimeOutHandler", commandProperties = {
//                    @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "2000")
//            })
    @HystrixCommand
    @GetMapping(value = "/consumer/payment/hystrix/timeout/{id}")
    public String paymentInfo_TimeOut(@PathVariable("id") Integer id) {
        return paymentFeignHystrixService.paymentInfo_TimeOut(id);
    }

//    public String paymentInfo_TimeOutHandler() {
//        return "线程池： " + Thread.currentThread().getName() + "  消费者端进行降级";
//    }

    public String payment_Global_Handler() {
        return "线程池： " + Thread.currentThread().getName() + "  消费者端统一降级处理方法";
    }

}
```

2. 服务熔断：
- 介绍：类似保险丝，达到最大服务访问后，直接拒绝访问；然后调用服务降级的方法返回友好提示。
- 流程：服务降级->进而熔断 ->恢复调用链路
- 机制：熔断机制是为了应对雪崩效应的一种微服务链路保护机制。当微服务不可用或响应时间过长，会进行服务降级，进而熔断该节点微服务的调用，快速返回错误的响应信息。当检测到该节点微服务调用响应正常后，恢复调用链路。SpringCloud框架中，默认5秒内失败20次调用失败，就会启动熔断机制，停止访问该服务。在指定时间窗口后熔断器状态变为半熔断，接受一个服务，如果成功访问，熔断器关闭；如果访问失败，熔断器开启。
![熔断参数解析](https://upload-images.jianshu.io/upload_images/21580557-273fedf38d81017e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***注解***
@HystrixCommand
***代码***
```java
@Service
public class PaymentService {

    // 服务熔断
    @HystrixCommand(fallbackMethod = "paymentCircuitBreaker_fallback", commandProperties = {
            //查看HystrixCommandProperties查看可以设置的属性
            @HystrixProperty(name = "circuitBreaker.enabled", value = "true"), //是否开启断路器
            @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "10"),//打开熔断器的最少请求次数
            @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "10000"),//时间窗口期后断路器状态置为半开放接收一条请求
            @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "60")//请求次数中失败次数达到百分之60后熔断
    })
    public String paymentCircuitBreaker(@PathVariable("id") Integer id) {
        if (id < 0) {
            throw new RuntimeException("******id 不能为负数");
        }
        String serialNumber = IdUtil.simpleUUID();  //返回不带"-"号的UUID

        return Thread.currentThread().getName() + "\t" + "调用成功，流水号：" + serialNumber;
    }

    public String paymentCircuitBreaker_fallback(Integer id){
        return "线程池： " + Thread.currentThread().getName()+"  配置熔断器的服务繁忙或出现异常,id  " + id;
    }

}
```


3. 服务限流：秒杀等高并发操作时使请求排队，每秒钟N个请求进入。

4. 近实时监控HystrixDashboard
***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix-dashboard</artifactId>
</dependency>
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
***注解***
主启动类上添加@EnableHystrixDashboard
***监控端配置***
server:
  port: 9001
***被监控服务需要添加配置***
```java
@SpringBootApplication
@EnableEurekaClient
@EnableCircuitBreaker
public class PaymentHystrixMain8001 {

    public static void main(String[] args) {
        SpringApplication.run(PaymentHystrixMain8001.class, args);
    }

    /**
     * 此配置是为了服务监控而配置，与服务容错本身无关，springcloud升级后的坑
     * ServletRegistrationBean因为springboot的默认路径不是"/hystrix.stream",
     * 只要在自己的项目里配置上下面的servlet就可以了
     */
    @Bean
    public ServletRegistrationBean getServlet(){
        HystrixMetricsStreamServlet streamServlet = new HystrixMetricsStreamServlet();
        ServletRegistrationBean servletRegistrationBean = new ServletRegistrationBean(streamServlet);
        servletRegistrationBean.setLoadOnStartup(1);
        servletRegistrationBean.addUrlMappings("/hystrix.stream");
        servletRegistrationBean.setName("HystrixMetricsStreamServlet");
        return servletRegistrationBean;
    }

}
```

启动服务后访问ip:9001/hystrix路径查看仪表盘界面。在仪表盘中输入需要监控的服务路径
![image.png](https://upload-images.jianshu.io/upload_images/21580557-38eac651e2100511.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
圆圈的大小表示流量大小，圆圈的颜色表示实例的健康程度。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7bab9bc1b2543926.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/21580557-bea10881add66ce9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#Zuul配置：
zuul1.x是基于阻塞I/O的API Gateway，基于Servlet2.5使用阻塞架构不支持任何长链接。
//服务端依赖：
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-zuul</artifactId>
</dependency>

//application配置文件(zuul注册到eureka)
```yml
eureka:
  client:
    service-url:
      defaultZone: http://eureka1.com:7001/eureka/,http://eureka2.com:7002/eureka/,http://eureka3.com:7003/eureka/
  instance:
    instance-id: gateway-9527.com  #实例名称
    prefer-ip-address: true  #实例显示地址

spring:
  mvc:
    servlet:
      load-on-startup: 1
  zipkin:
    base-url: http://192.168.32.128:9411
    enabled: true
    sender:
      type: web
  #接口默认全部采样
  sleuth:
    sampler:
      probability: 1.0
logging:
  level:
    root: info
    com.cloud: debug
#  file: logs/${spring.application.name}.log
zuul:
  prefix: /v1   # 前缀，可以用来做版本控制
  ignored-services: "*"   # 禁用默认路由，执行配置的路由
  routes:
    # 配置menu接口微服务
    menu:
      path: /api-menu/**
      serviceId: menu-center
      stripPrefix: false   #默认为true，转发的路径不会带上api-menu；设为false，会带上api-menu进行转发
    oauth:
      path: /api-oauth/**
      serviceId: oauth-center
    user:
      path: /api-user/**
      serviceId: user-center
    log:
      path: /api-log/**
      serviceId: log-center
    file:
      path: /api-file/**
      serviceId: file-center
  host:  #设置超时时间
    connect-timeout-millis: 10000
    socket-timeout-millis: 60000
  add-proxy-headers: true  #将请求转发时会携带原有的请求头
  ribbon:
    eager-load:
      enabled: true  

hystrix:  #熔断降级
  common:
    default:
      execution:
        isolation:
          thread:
            timeoutInMilliseconds: 5000
```
//注解
主启动类添加注解@EnableZuulProxy

就可以通过Zuul访问的注册在eureka上的服务了


额外：
![目录结构](https://upload-images.jianshu.io/upload_images/21580557-90ab92b9c7eaf2fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![配置类config](https://upload-images.jianshu.io/upload_images/21580557-18c3df5785a25501.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![接口类controller](https://upload-images.jianshu.io/upload_images/21580557-6ae62eb9d6ed5248.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![服务调用类feign](https://upload-images.jianshu.io/upload_images/21580557-e5267a2c436a4240.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![过滤器filter](https://upload-images.jianshu.io/upload_images/21580557-a588188cdf5d93c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

参考文章：[https://blog.csdn.net/liuchuanhong1/article/details/62236793](https://blog.csdn.net/liuchuanhong1/article/details/62236793)


#Gateway
基于WebFlux框架实现，框架底层使用高性能的Reator模式通讯框架Netty（非阻塞式响应框架）。
网关功能：
1.Route(路由)：路由是构建网关的基本模块，它由ID,目标URI,一系列的断言和过滤器组成，如果断言为true则匹配该路由
2.Predicate(断言)：开发人员可以匹配HTTP请求中的所有内容(例如请求头或请求参数)，如果请求与断言匹配则进行路由
3.Filter(过滤)：Spring框架中GatewayFilter的实例，使用过滤器，可以在请求被路由前后队请求进行修改。

在网关中 (1)可以区分请求类型，集成负载均衡，将请求发送到不同的服务中；(2)集成hystrix进行熔断降级；(3)可以在网关中通过对认证中心的调用，完成权限认证，登录退出等操作。

***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
Spring Cloud Gateway 是使用 netty+webflux 实现因此不需要再引入 web 模块，添加spring-boot-starter-web依赖会报错。
***配置***
通过配置文件配置
```
server:
  port: 8100

spring:
  application:
    name: gateway-server
  zipkin:
    base-url: http://192.168.32.128:9411
    enabled: true
    sender:
      type: web
  sleuth:
    sampler:
      #采样率介于0到1之间，1表示全部采集
      probability: 1
  cloud:
#    config:
#      discovery:
#        enabled: true
#        serviceId: config-center
#      profile: dev
#      fail-fast: true
    gateway:
      default-filters:  #全局过滤器
        - name: Hystrix
          args:
            name: fallbackcmd  #使用HystrixCommand打包剩余的过滤器，并命名为fallbackcmd
            fallbackUri: forward:/fallback  #配置fallbackUri，降级逻辑被调用
      discovery:
        locator:
          enabled: true
      routes:
        - id: MENU-CENTER
          uri: lb://MENU-CENTER
          filters:
            - SetPath=/menu-anon/{path}
          predicates:
            - Path=/v1/api-menu/menu-anon/{path}  #直接访问菜谱接口
        - id: MENU-CENTER
          uri: lb://MENU-CENTER
          filters:
            - SetPath=/menu/{path}
          predicates:
            - Path=/v1/api-menu/menu/{path}   #需要权限验证
#      globalcors: #跨域配置
#        corsConfigurations:
#          '[/**]':
#            allowedOrigins: "*"
#            allowedMethods: "*"

eureka:
  client:
    fetch-registry: true
    register-with-eureka: true
    service-url:
      defaultZone: http://localhost:7001/eureka/ #http://hxr:hxr123@192.168.32.128:8761/eureka/
  instance:
    instance-id: ${spring.application.name}:${server.port}
    prefer-ip-address: true

#设置feign客户端负载均衡和超时时间(OpenFeign默认支持ribbon)
ribbon:
  #开启ribbon负载均衡
  eureka:
      enabled: true
  #建立连接所用的时间
  ConnectTimeout: 100
  #建立连接后服务器响应时间
  ReadTimeout: 500


hystrix:
  command:
    default:
      execution:
        isolation:
          thread:
            timeoutInMilliseconds: 5000 # 设置hystrix的超时时间为5000ms

management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always

cron:
  black-ip: 0 0/5 * * * ?
```
过滤器改变请求地址：
 filters:
        # 访问localhost:8080/test, 请求会转发到localhost:8001/app/test
        - RewritePath=/test, /app/test
过滤器设置熔断器：
spring:
  cloud:
    gateway:
      default-filters:  #全局过滤器
        - name: Hystrix
          args:
            name: fallbackcmd  #使用HystrixCommand打包剩余的过滤器，并命名为fallbackcmd
            fallbackUri: forward:/fallback  #配置fallbackUri，降级逻辑被调用

断言：
①时间级别的断言- Before、- After、- Between
②cookie的断言- cookie=username,abc  (可以使用正则表达式);则请求需要带上对应的cookie，如curl   http://localhost:9527/payment/hystrix/circuit/1  --cookie  "username=abc" 。
③Header的断言- Header=X-Request-Id,\d+  (使用正则表达式) ;则请求需要带上指定的请求头并且值为整数，如curl http://localhost:9527/payment/hystrix/circuit/1 -H "X-Request-Id:1234" 。
④Host的断言- Host=**.cj.com  ;则请求需要符合断言，如curl http://localhost:9527/payment/hystrix/circuit/1 -H "Host:www.cj.com" 。
⑤Method的断言- Method=GET ;则请求方法为GET才允许访问。
⑥Query的断言- Query=username,\d+ ;要有参数名username并且值还要是整数才能路由
通过配置类配置
```java
@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        RouteLocatorBuilder.Builder routes = builder.routes();
        routes.route("path_route_cj",r -> r.path("/guonei").uri("http://news.baidu.com/guonei")).build();  //将访问ip:port/guonei路径的请求通过网关转到http://news.baidu.com/guonei网站

        return routes.build();
    }

}
```
***注解***
暂不需要
***自定义过滤器***
```java
@Component
@Slf4j
public class MyLogGateWayFilter implements GlobalFilter,Ordered {


    //TODO 过滤请求
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        log.info("*********come in MyLogGateWayFilter:"+new Date());
        //TODO 获取请求参数并获取uname参数的值
        String uname = exchange.getRequest().getQueryParams().getFirst("uname");
        if (uname == null) {
            log.info("*******用户名为null，非法用户");
            //TODO 设置响应码为406
            exchange.getResponse().setStatusCode(HttpStatus.NOT_ACCEPTABLE);
            //TODO 返回拒绝的响应
            return exchange.getResponse().setComplete();
        }
        //TODO 进入下一个过滤器
        return chain.filter(exchange).then(
                Mono.fromRunnable(() -> {
                    log.info("POST过滤器");
                    }
                })
        );
    }

    //TODO 加载过滤器的顺序，越小优先级越高
    @Override
    public int getOrder() {
        return 0;
    }
}
```
自定义过滤器需要继承两个接口GlobalFilter和Ordered，重写filter和getOrder方法，分别用于过滤请求和设置该过滤器的优先级。
filter(exchange,chain)方法，此处是一个“pre”类型的过滤器，然后再chain.filter的内部类中的run()方法中相当于"post"过滤器。
如上自定义的过滤器，会拒绝请求http://localhost:9527/payment/hystrix/ok/1，会响应请求http://localhost:9527/payment/hystrix/ok/1?uname=a


Spring Cloud Gateway根据作用范围划分为GatewayFilter和GlobalFilter，二者区别如下：
GatewayFilter : 需要通过spring.cloud.routes.filters 配置在具体路由下，只作用在当前路由上或通过spring.cloud.default-filters配置在全局，作用在所有路由上
GlobalFilter : 全局过滤器，不需要在配置文件中配置，作用在所有的路由上，最终通过GatewayFilterAdapter包装成GatewayFilterChain可识别的过滤器，它为请求业务以及路由的URI转换为真实业务服务的请求地址的核心过滤器，不需要配置，系统初始化时加载，并作用在每个路由上。




#Config-Center
###服务端
***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
</dependency>
***配置***
```
spring:
  application:
    name: cloud-config-center
  cloud:
    config:
      server:
        git:
          #uri: git@github.com:ChenJie666/springcloud-config-file.git #GitHub上的仓库名字
          uri: https://github.com/ChenJie666/springcloud-config-file.git
          username: chenjie666
          password: 88596532xx
          search-paths:
            - springcloud-config  #搜索目录
      label: master #读取分支
```
***注解***
@EnableConfigServer
***将配置文件推到github上***
注:文件名需要符合{application}-{profile}.yml格式
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/ChenJie666/springcloud-config-file.git
git push -u origin master

访问http://localhost:3344/master/config-dev.yml得到配置得到配置文件的内容。


###客户端
***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config</artifactId>
</dependency>
***配置***
```
spring:
  application:
    name: config-client
  cloud:
    config:
      # http://localhost:3344/master/config-dev.yml
      label: master #分支名称
      name: config  #GitHub上的配置文件名为config-dev.yml，对应{name}-{profile}.yml
      profile: dev
      # uri: http://localhost:3344  #配置中心的地址
      discovery:
        enabled: true
        service-id: config-center #通过eureka获取配置中心地址
```
***注解***
暂不需要

######问题：
客户端只会在启动时读取配置文件，如果配置文件发生变化，客户端无法及时更新。
#####解决措施-动态刷新
监控配置中心的变化，动态改变
***依赖***
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
***配置***
```
# 暴露监控端点
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always
```
***注解***
在controller类上添加@RefreshScope注解
***刷新请求***
需要发送POST请求curl -X POST "http://192.168.32.151:3355/actuator/refresh"刷新服务，则微服务配置会重新加载，无需重启服务。


#Bus消息总线
什么是总线：Bus能管理和传播分布式系统间的消息，可用于广播状态更改、时间推送等，也可以作为微服务间的消息通道。
基本原理：ConfigClient实例都监听MQ中同一个topic(默认是springCloudBus)。当一个服务刷新数据的时候，它会把这个信息放入到Topic中，这样其他监听同一个服务就能得到通知，然后去更新自己的配置。
Bus支持两种消息代理：Kafka和RabbitMQ

有两种设计思想：①通知服务端，由服务端通知客户端②通知某一客户端，由客户端在通知其他客户端。
一般选择方式①

###配置中心
***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
***配置***
```
## rabbitmq相关配置
spring:
  rabbitmq:
    host: 116.62.148.11
    port: 5672
    username: guest
    password: guest

## 暴露bus刷新配置的端点
management:
  endpoints:
    web:
      exposure:
        include: 'bus-refresh'
```
***注解***
@

###配置客户端（同服务端）
***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
***配置***
```
## rabbitmq相关配置
spring:
  rabbitmq:
    host: 116.62.148.11
    port: 5672
    username: guest
    password: guest

## 暴露bus刷新配置的端点
management:
  endpoints:
    web:
      exposure:
        include: '*'
```
***发送命令到服务端刷新客户端***
- 全局更新：通过请求 curl -X POST "http://192.168.32.151:3344/actuator/bus-refresh" 刷新服务端的数据
- 局部更新：通过请求 curl -X POST "http://192.168.32.151:3344/actuator/bus-refresh/config-client:3355" 刷新服务端的数据，即需要指定微服务名和端口号，微服务名区分大小写。

![原理图](https://upload-images.jianshu.io/upload_images/21580557-3e5253306132dac5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#SpringCloud Stream消息驱动
通过绑定器作为中间层，实现了应用程序与消息中间件细节之间的隔离。通过向应用程序暴露统一的Channel通道，是应用程序不需要在考虑各种不同的消息中间件实现。
INPUT对用于消费者，OUTPUT对应于生产者
![image.png](https://upload-images.jianshu.io/upload_images/21580557-8c7c9e6dcd50faef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/21580557-02c6a8e8fe8d5309.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
***组件***
- Binder：连接中间件，屏蔽差异
- Channel：通道，是队列Queue的一种抽象，在消息通讯系统中就是实现存储和转发的媒介，通过Channel对队列进行配置。
- Source和Sink：可理解为参照对象是SpringCLoudStream自身，从Stream发布消息就是输出，接收消息就是输入。
- Middleware：中间件，目前只支持RabbitMQ和Kafka


***依赖***
rabbitqm的依赖
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-stream-rabbit</artifactId>
</dependency>
***配置***
生产者:
```
spring:
  application:
    name: cloud-stream-provider
  cloud:
    stream:
      binders: #在此处配置要绑定的rabbitmq的服务信息
        defaultRabbit:  #表示定义的名称，用于binding整合
          type: rabbit  #消息组件类型
          environment:  #设置rabbitmq的相关的环境配置
            spring:
              rabbitmq:
                host: 116.62.148.11
                port: 5672
                username: guest
                password: guest
      bindings: #服务的整合处理
        output: #这个名字是一个通道的名称
          destination: studyExchange  #表示要使用的Exchange名称
          content-type: application/json  #设置消息类型，本次为json，文本则设置“text/plain"
          binder: defaultRabbit #设置要绑定的消息服务的具体设置
          group: cloud-stream-consumer #创建监听队列接受交换机信息
```
消费者:
```
spring:
  application:
    name: cloud-stream-consumer
  cloud:
    stream:
      binders:  #设置需要绑定的rabbitmq的服务信息
       defaultRabbit: #表示定义的名称，用于bingding集合
        type: rabbit  #消息组件类型是RabbitMQ
        environment:  #设置RabbitMQ的环境变量
          spring:
            rabbitmq:
              host: 116.62.148.11
              port: 5672
              username: guest
              password: guest
      bindings:  #服务的整合处理
        input:  #这个名字是一个通道的名称
          destination: studyExchange  #表示要使用的Exchange名称
          content-type: application/json  #设置消息类型，本次为json，文本则设置“text/plain"
          binder: defaultRabbit #设置要绑定的消息服务的具体设置
          group: cloud-stream-consumer #创建监听队列接受交换机信息
```
***注解***
@Input：标识输入通道
@Output：标识输出通道
@StreamListener：监听队列，用于消费者的队列的消息接收
@EnableBinding：指信道channel和exchange绑定在一起
***代码***
生产者：
```
@EnableBinding(Source.class)    //定义消息的推送管道
public class MessageProviderImpl implements MessageProvider {

    @Resource
    private MessageChannel output;  //消息发送管道

    @Override
    public String send() {
        String serial = UUID.randomUUID().toString();
        output.send(MessageBuilder.withPayload(serial).build());
        System.out.println("*********serial:" + serial);
        return null;
    }

}
```
消费者：
```
@RestController
@EnableBinding(Sink.class)
public class ReceiveMessageListenerController {

    @Value("${server.port}")
    private String serverPort;

    @StreamListener(Sink.INPUT)
    public void input(Message<String> message) {
        System.out.println("消费者1号接收到消息：" + message.getPayload() + "\t port: " + serverPort);
    }

}
```
两个问题：重复消费和消息持久化问题
- 重复消费：默认每个实例都会生成一个队列，所以即使是同一个微服务中的实例，每个实例都会收到生产者发送的信息，所以需要将同一个微服务的实例都分到一个队列中，避免重复消费。配置文件需要加上group: cloud-stream-consumer。
- 消息持久化：如果未设置group，会创建临时的队列，该队列不会将消息持久化，导致未被消费者消费的消息丢失。


#Sleuth分布式请求链路跟踪（包含zipkin）
微服务中，客户端发起的请求在后端系统中会经过多个不同的服务节点调用来协调产生最后的请求结果，每一格前端请求都会形成一条复杂的分布式服务调用链路。Zipkin类似大数据中的血缘分析。
每一条请求链路都会通过Trace Id唯一标识，Span标识发起的请求信息，各span通过parent id关联起来。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-a2e73356d8bae9ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


SpringCloud从F版起就不需要自己构建Zipkin Server了，只需要调用jar包即可。下载地址[https://dl.bintray.com/openzipkin/maven/io/zipkin/java/zipkin-server/2.12.9/](https://dl.bintray.com/openzipkin/maven/io/zipkin/java/zipkin-server/2.12.9/)
访问Zipkin的UI界面：[http://116.62.148.11:9411/zipkin/](http://116.62.148.11:9411/zipkin/)


***依赖***
<dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-zipkin</artifactId>
</dependency>
***配置***
```
spring:
  zipkin:
        base-url: http://116.62.148.11:9411
        enabled: true
        sender:
          type: web
  sleuth:
    sampler:
      #采样率介于0到1之间，1表示全部采集
      probability: 1
```
***注解***
暂不需要

刷新zipkin的UI之后会得到服务名及服务的链路信息。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d21348f6e338dda2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


将业务切分为微服务，方便调用：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-5a8014054d4ca01b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

整体结构：
![image.png](https://upload-images.jianshu.io/upload_images/21580557-9d574feac2af8874.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![fd74d95c2ad4abc29f.jpg](https://upload-images.jianshu.io/upload_images/21580557-1fccafefe7fab384.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
