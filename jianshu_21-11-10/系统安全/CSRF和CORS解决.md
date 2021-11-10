![image.png](https://upload-images.jianshu.io/upload_images/21580557-80e3f1f04ba42d41.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#CSRF跨站请求伪造
流程：在请求开放的 /authentication 接口时，会返回X-XSRF-TOKEN令牌，在请求头或请求体中携带该令牌进行请求时才不会被CSRF攻击防御拦截(CSRF不防御GET请求)。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-d0b1e4028ef3253d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-822dc7833d8b9cd6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#CORS跨站资源共享
![image.png](https://upload-images.jianshu.io/upload_images/21580557-c6e647d6d5189c14.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###常用的跨域访问后端配置
![方案一](https://upload-images.jianshu.io/upload_images/21580557-e9320381bd82d946.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![方案二](https://upload-images.jianshu.io/upload_images/21580557-cea47b70119d88c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![方案三](https://upload-images.jianshu.io/upload_images/21580557-d85bddfbd93fc8e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/21580557-cff1dafe6073c027.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-92ee30d70f723108.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-a19d1109bf624242.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![不常用，直接手写头信息](https://upload-images.jianshu.io/upload_images/21580557-cadc108d3821bb8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
/**
 * 跨域配置<br>
 * 页面访问域名和后端接口地址的域名不一致时，会先发起一个OPTIONS的试探请求<br>
 * 如果不设置跨域的话，js将无法正确访问接口，域名一致的话，不存在这个问题
 */
@Configuration
public class CrossDomainConfig {

    /**
     * 跨域支持
     *
     * @return
     */
    @Bean
    public CorsWebFilter corsFilter() {
        final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource(new PathPatternParser());
        final CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true); // 允许cookies跨域
        config.addAllowedOrigin("*");// #允许向该服务器提交请求的URI，*表示全部允许
        config.addAllowedHeader("*");// #允许访问的头信息,*表示全部
        config.setMaxAge(18000L);// 预检请求的缓存时间（秒），即在这个时间段里，对于相同的跨域请求不会再预检了
        config.addAllowedMethod("*");// 允许提交请求的方法，*表示全部允许
        source.registerCorsConfiguration("/**", config);
        return new CorsWebFilter(source);
    }

    //方式二
//    @Bean
//    public WebMvcConfigurer corsConfigurer() {
//        return new WebMvcConfigurer() {
//            @Override
//            public void addCorsMappings(CorsRegistry registry) {
//                registry.addMapping("/**") // 拦截所有权请求
//                        .allowCredentials(true) // 允许cookies跨域
//                        .allowedOrigins("*") // #允许向该服务器提交请求的URI，*表示全部允许
//                        .allowedHeaders("*") // #允许访问的头信息,*表示全部
//                        .maxAge(18000L); // 预检请求的缓存时间（秒），即在这个时间段里，对于相同的跨域请求不会再预检了
//                        .allowedMethods("*") // 允许提交请求的方法，*表示全部允许
//            }
//        };
//    }

    //方式三：通过配置文件配置
    /**
     *     spring:
     *     cloud:
     *     gateway:
     *     globalcors:
     *     corsConfigurations:
     *             '[/**]':
     *     allowedOrigins: "*"
     *     allowedMethods: "*"
     */

}
```


###以上方式在Spring Security环境下以上四种方式全部失效

http.cors();  //开启同源策略
```java
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
```
