
#二、自动配置
###06集
@AutoConfigurtionPackage  自动配置包
@Import(AutoConfigurationPackages.Register.class)：Spring的底层注解@Import(AutoConfigurationImportSelector.class)导入自动配置类，给容器汇总导入自动配置类，就是给容器中导入的这个场景需要的所有组件，并配置好这些组件。
`将主配置类（@SpringBootApplication标注的类）的所在包及下面所有子包里面的所有组件扫描到Spring容器中。`

###12.13集
@PropertySource(value = {"classpath:person.yml"})   加载指定的yml/properties文件中的内容并绑定到类对象中。这样可以将配置信息放在另一个文件中而非Springboot的配置文件。

@ImportResource(locations = {"classpath:beans.xml"})   标注在配置类上，可以导入Spring的xml配置文件，让配置文件中的内容生效。
通过xml文件想容器中注入helloService对象
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans .....>
  <bean id="helloService" class="com.atguigu.service.HelloService"></bean>
</beans>
```
```java
// 判断容器中是否有helloSrevice
@Autowired
ApplicationContext  ioc;   // 获取容器

@Test
public void testHelloService(){
  ioc.containsBean("helloService");
}
```

###14
**yml中的占位符：**
获取随机值
\${random.uuid}  
\${random.int}  
获取之前配置的值，可以指定缺省值
\${server.port}   获取前面定义的属性，如果不存在则不进行占位，值为该表达式
\${server.port:9999}   可以指定默认值，如果不存在，则值为默认值


###多profile文件 
application.yml
application-{profile}.yml
默认使用application.yml文件。可以在application.yml文件中添加spring.profiles.active=dev来激活对应环境下的配置文件，激活的配置参数会覆盖原参数形成互补。

**多文档块**
可以使用 --- 将一个配置文件分成多个文档块，添加spring.profiles: dev 指定该文档块的环境。
如下配置文件，分为了三个文档块，默认读取第一个文档块。可以为每个文档块设置环境然后在第一个文档块中进行激活。
```yml
server:
  port: 8080
spring:
  profiles:
    active: dev

---
server:
  port: 8081
spring:
  profile: dev

---
server:
  port: 8082
spring:
  profile: prod

```

可以在启动时添加启动命令，在VM options中添加-Dspring.profiles.active=dev或program arguments参数框中添加 --spring.profiles.active=dev来激活dev环境。会使配置文件中的激活配置失效。

**springboot配置文件的加载位置**
springboot启动会扫描一下位置 的application.properties或者application.yml文件作为Springboot的默认配置文件。优先级由高到低，高优先级会覆盖低优先级形成互补配置。
- file:./config/
- file:./
- classpath:/config/
- classpath:/

配置项目的访问路径：
server.context-path=/path

也可以指定配置文件的位置，该配置文件优先级高于默认配置，会与默认的访问路径中的配置文件形成互补。
spring.config.location=G:/application.properties


###自动配置原理@@@
1.springboot启动时加载主配置类，开启了@SpringBootApplication的@EnableAutoConfiguration注解中的自动配置功能。在@EnableAutoConfiguration注解的作用是导入了选择器@Import(AutoConfigurationImportSelector.class)，利用AutoConfigurationImportSelector的selectImports()方法给容器中导入一些组件。
```java
	@Override
	public String[] selectImports(AnnotationMetadata annotationMetadata) {
		if (!isEnabled(annotationMetadata)) {
			return NO_IMPORTS;
		}
		// 通过
		AutoConfigurationMetadata autoConfigurationMetadata = AutoConfigurationMetadataLoader
				.loadMetadata(this.beanClassLoader);
		AutoConfigurationEntry autoConfigurationEntry = getAutoConfigurationEntry(autoConfigurationMetadata,
				annotationMetadata);
		return StringUtils.toStringArray(autoConfigurationEntry.getConfigurations());
	}
```
```java
	protected static final String PATH = "META-INF/spring-autoconfigure-metadata.properties";
	//扫描该路径下的所有的资源
	static AutoConfigurationMetadata loadMetadata(ClassLoader classLoader) {
		return loadMetadata(classLoader, PATH);
	}

	static AutoConfigurationMetadata loadMetadata(ClassLoader classLoader, String path) {
		try {
			Enumeration<URL> urls = (classLoader != null) ? classLoader.getResources(path)
					: ClassLoader.getSystemResources(path);
			Properties properties = new Properties();
			while (urls.hasMoreElements()) {
				properties.putAll(PropertiesLoaderUtils.loadProperties(new UrlResource(urls.nextElement())));
			}
			return loadMetadata(properties);
		}
		catch (IOException ex) {
			throw new IllegalArgumentException("Unable to load @ConditionalOnClass location [" + path + "]", ex);
		}
	}
```

2.将类路径下的META-INF的spring-autoconfigure-metadata.properties中的所有的url加载到容器中。每一个这样的xxxAutoConfiguration类都是容器中的一个组件，都加入到容器中，用他们来做自动配置。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-3d181f34045580ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3.每一个自动配置类进行自动配置功能，以HttpEncodingAutoConfiguration为例解释自动配置原理
```java
@Configuration  
@EnableConfigurationProperties(HttpProperties.class) // 启用指定类的ConfigurationProperties功能，将配置文件中对应的值和HttpProperties绑定起来
@ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET) //Spring底层@Conditional注解，根据不同的条件，如果满足指定的条件，整个配置类里面的配置就会生效。 判断当前应用是否是web应用，如果是，当前配置生效。
@ConditionalOnClass(CharacterEncodingFilter.class) //判断当前项目有没有CharacterEncodingFilter这个类(这个类是SpringMVC中进行乱码解决的过滤器)
@ConditionalOnProperty(prefix = "spring.http.encoding", value = "enabled", matchIfMissing = true) //判断配置文件中是否存在某个配置 spring.http.encoding.enabled；如果不存在，判断也是成立的
public class HttpEncodingAutoConfiguration {...}
```
根据当前不同的条件判断，决定这个配置类是否生效？如上述的@ConditionalOnClass判断容器中是否存储在CharacterEncodingFilter类，如果存在则该配置类生效。我们可以通过debug: true 属性来让控制台打印自动配置报告。


4.所有在配置文件中能配置的属性都是在xxxProperties类中封装着，配置文件能配置什么就可以参照某个功能对应的这个属性类。
```java
@ConfigurationProperties(prefix = "spring.http")
public class HttpProperties {
```

<br>
#三、日志
###1. 日志原理
日志
![蓝色的是接口层，墨绿的是适配层，蓝色的是实现层](https://upload-images.jianshu.io/upload_images/21580557-0ada0f4a95fe29c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/21580557-93db5ea8f8324810.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Springboot框架中的Spring-boot-starter-logging会自动引入各个框架（jul、jcl、log4j）的slf4j的适配层，最终用logback实现，所以如果其他框架有引入不同的日志框架，需要进行排除，否则会有冲突。

###2. 其他日志框架的适配
每个日志的实现框架都有自己的配置文件，使用SLF4j之后，配置文件还是做成日志实现框架自己本身的配置文件。
如何使其他日志框架也能统一使用SLF4j+logback的日志框架？
![日志框架诗配图](https://upload-images.jianshu.io/upload_images/21580557-f66b0993de311795.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
1. 可以先**排除框架中的原日志接口层**的包
2.然后使用SLF4j提供的对应的**替换包来替换原有的包**。这样原接口没有消失，但是会调用SLF4j的方法进行统一的输出。（spring-boot-starter中默认已经导入）
3. 再导入SLF4j其他的实现。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-8fee8bc9afbf51e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**总结**
1. Springboot底层也是使用SLF4j+logback的方式进行日志记录。
2. Springboot也把其他日志都替换成了SLF4j
3. 如果我们引入其他框架，需要将这个框架的默认的日志依赖移除掉。如Springboot依赖了spring-core框架，但是将spirng-core框架中的common-logging日志框架直接移除掉。

**也可以将springboot的默认的spring-boot-starter-logging包替换为spring-boot-starter-log4j2包，来实现对log4j2的支持。**

###3. slf4j的使用
**日志的级别**
从低到高分别为
logger.trace();
logger.debug();
logger.info();
logger.warn();
logger.error();
可以进行设置后让控制台打印指定级别的高级别的日志（Springboot默认使用的是info级别）。

**调整指定包下的类的打印级别**
logging.level.com.hxr: warn

**将日志输出到指定的目录中**
指定日志输出的目录，生成的文件名为默认的spring.log
logging.path: /spring/log

**将日志输出到指定目录的指定文件中**
不指定目录在当前文件夹下生成，指定路径则生成到对应路径下。会覆盖logging.path设置。
logging.file: G:/springboot.log

**在控制台输出的日志的格式**
logging.pattern.console: %d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n

**在文件中输出的日志的格式**
logging.pattern.console: %d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n

注：
%d表示日期时间
%thread表示线程名
%-5level  级别从左显示5个字符宽度
%logger{50} 表示logger名字最长50个字符，否则按照句点分割
%msg  日志消息
%n 换行符

![logback的默认配置文件](https://upload-images.jianshu.io/upload_images/21580557-84ad9da9ba1bbe60.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<br>
**如何覆盖框架默认的配置文件**
![image.png](https://upload-images.jianshu.io/upload_images/21580557-b5da5f9cc04f09bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对于Logback框架，只需要在路径中创建logback-spring.xml或logback.xml
logback.xml直接就被日志框架识别了
logback-spring.xml日志框架就不直接加载日志的配置项，由springboot解析日志配置，可以使用Springboot的高级profile功能。

>**logback-spring.xml的springProfile 可以指定某段配置只在某个环境下生效：**
>```xml
><layout class="ch.qos.logback.classic.PatternLayout>
>  <springProfile name="dev">
>    <pattern>......</pattern>
>  </springProfile>
>  <springProfile name="!dev">
>    <pattern>......</pattern>
>  </springProfile>
></layout>
>```

<br>
#四、SpringBoot与Web开发

###4.1SpringBoot对静态资源的映射规则
在启动时自动注入了WebMvcAutoConfiguration配置类，该配置类中的addResourceHandlers方法中添加了静态资源映射规则。
```
		// 映射/webjars/**和"/**"
		@Override
		public void addResourceHandlers(ResourceHandlerRegistry registry) {
			if (!this.resourceProperties.isAddMappings()) {
				logger.debug("Default resource handling disabled");
				return;
			}
			// 此处从配置文件中读取了缓存时间，可以通过spring.resources进行设置
			Duration cachePeriod = this.resourceProperties.getCache().getPeriod();
			CacheControl cacheControl = this.resourceProperties.getCache().getCachecontrol().toHttpCacheControl();
			if (!registry.hasMappingForPattern("/webjars/**")) {
				customizeResourceHandlerRegistration(registry.addResourceHandler("/webjars/**")
						.addResourceLocations("classpath:/META-INF/resources/webjars/")
						.setCachePeriod(getSeconds(cachePeriod)).setCacheControl(cacheControl));
			}
			String staticPathPattern = this.mvcProperties.getStaticPathPattern();
			if (!registry.hasMappingForPattern(staticPathPattern)) {
				customizeResourceHandlerRegistration(registry.addResourceHandler(staticPathPattern)
						.addResourceLocations(getResourceLocations(this.resourceProperties.getStaticLocations()))
						.setCachePeriod(getSeconds(cachePeriod)).setCacheControl(cacheControl));
			}
		}

		// 映射欢迎页面
		@Bean
		public WelcomePageHandlerMapping welcomePageHandlerMapping(ApplicationContext applicationContext,
				FormattingConversionService mvcConversionService, ResourceUrlProvider mvcResourceUrlProvider) {
			WelcomePageHandlerMapping welcomePageHandlerMapping = new WelcomePageHandlerMapping(
					new TemplateAvailabilityProviders(applicationContext), applicationContext, getWelcomePage(),
					this.mvcProperties.getStaticPathPattern());
			welcomePageHandlerMapping.setInterceptors(getInterceptors(mvcConversionService, mvcResourceUrlProvider));
			return welcomePageHandlerMapping;
		}

		private Optional<Resource> getWelcomePage() {
			String[] locations = getResourceLocations(this.resourceProperties.getStaticLocations());
			return Arrays.stream(locations).map(this::getIndexHtml).filter(this::isReadable).findFirst();
		}
```

**映射规则：**
1. 所有`/webjars/**`，都去`classpath:/META-INF/resources/webjars/`找资源；
webjars：以jar包方式引入静态资源，在Springboot中可以直接通过依赖jar包的方式引入webjars静态资源。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-7a00a8040b70b90e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

localhost:8080/webjars/jquery/3.3.1/jquery.js
```
<!-- 引入jquery-webjar -->
<dependency>
  <groupId>org.webjars</groupId>
  <artifactId>jquery</artifactId>
  <version>3.3.1</version>
</dependency>
```

2. "/**" 访问将会映射到的路径如下
`"classpath:/META-INF/resources/",
			"classpath:/resources/", "classpath:/static/", "classpath:/public/"`

3.  欢迎页，静态资源文件夹下的所有的index.html页面；被"/**"映射

4. 显示网站图标，将favicon.ico图标放在静态资源文件下。(2.2.x已删除)

<br>
**修改默认配置**
在该自动配置类中的属性都是从ResourceProperties类中进行查找的，该配置类从配置文件中获取属性值，我们只需要在配置类中的添加属性即可改变默认的配置。
```java
@ConfigurationProperties(prefix = "spring.resources", ignoreUnknownFields = false)
public class ResourceProperties {

	private static final String[] CLASSPATH_RESOURCE_LOCATIONS = { "classpath:/META-INF/resources/",
			"classpath:/resources/", "classpath:/static/", "classpath:/public/" };

	private String[] staticLocations = CLASSPATH_RESOURCE_LOCATIONS;

	......
}
```
如修改映射的默认文件夹：
spring.resources.static-locations: classpath:/myresource/,classpath:/myfile/


###2. 模板引擎
JSP、Velocity、Freemarker、Thymeleaf；

导入Thymeleaf
```
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
```
会自动配置Thymeleaf自动配置类，该配置类会读取并解析"classpath:/templates/"路径下的文件。
```java
@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(ThymeleafProperties.class)
@ConditionalOnClass({ TemplateMode.class, SpringTemplateEngine.class })
@AutoConfigureAfter({ WebMvcAutoConfiguration.class, WebFluxAutoConfiguration.class })
public class ThymeleafAutoConfiguration {
		......

		@Bean
		SpringResourceTemplateResolver defaultTemplateResolver() {
			SpringResourceTemplateResolver resolver = new SpringResourceTemplateResolver();
			resolver.setApplicationContext(this.applicationContext);
			resolver.setPrefix(this.properties.getPrefix());  // "classpath:/templates/"
			resolver.setSuffix(this.properties.getSuffix()); //".html"
			resolver.setTemplateMode(this.properties.getMode());
			if (this.properties.getEncoding() != null) {
				resolver.setCharacterEncoding(this.properties.getEncoding().name());
			}
			resolver.setCacheable(this.properties.isCache());
			Integer order = this.properties.getTemplateResolverOrder();
			if (order != null) {
				resolver.setOrder(order);
			}
			resolver.setCheckExistence(this.properties.isCheckTemplate());
			return resolver;
		}

		......
}
```


###3. SpringMVC自动配置
Springboot自动配置好了SpringMVC
以下是SpringBoot对SpringMVC的默认：

***1. 自动配置了ContentNegotiatingViewResolver视图解析器和BeanNameViewResolver解析器。***
- 视图解析器：根据方法的返回值得到试图对象，试图对象决定如何渲染（转发？重定向？）
- ContentNegotiatingViewResolver：组合了所有的视图解析器
- 如何定制：我们可以自己给容器中添加一个视图解析器，ContentNegotiatingViewResolver会自动将其组合为视图解析器。

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnWebApplication(type = Type.SERVLET)
@ConditionalOnClass({ Servlet.class, DispatcherServlet.class, WebMvcConfigurer.class })
@ConditionalOnMissingBean(WebMvcConfigurationSupport.class)
@AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE + 10)
@AutoConfigureAfter({ DispatcherServletAutoConfiguration.class, TaskExecutionAutoConfiguration.class,
		ValidationAutoConfiguration.class })
public class WebMvcAutoConfiguration {
		......

		@Bean
		@ConditionalOnBean(ViewResolver.class)
		@ConditionalOnMissingBean(name = "viewResolver", value = ContentNegotiatingViewResolver.class)
		public ContentNegotiatingViewResolver viewResolver(BeanFactory beanFactory) {
			ContentNegotiatingViewResolver resolver = new ContentNegotiatingViewResolver();
			resolver.setContentNegotiationManager(beanFactory.getBean(ContentNegotiationManager.class));
			// ContentNegotiatingViewResolver uses all the other view resolvers to locate
			// a view so it should have a high precedence
			resolver.setOrder(Ordered.HIGHEST_PRECEDENCE);
			return resolver;
		}

		......
}
```
在ContentNegotiatingViewResolver类中的initServletContext方法中会将容器中所有的ViewResolver的实现类组合为视图解析器。
```java
public class ContentNegotiatingViewResolver extends WebApplicationObjectSupport
		implements ViewResolver, Ordered, InitializingBean {	
	......
	@Override
	protected void initServletContext(ServletContext servletContext) {
		Collection<ViewResolver> matchingBeans =
				BeanFactoryUtils.beansOfTypeIncludingAncestors(obtainApplicationContext(), ViewResolver.class).values();
		if (this.viewResolvers == null) {
			this.viewResolvers = new ArrayList<>(matchingBeans.size());
			for (ViewResolver viewResolver : matchingBeans) {
				if (this != viewResolver) {
					this.viewResolvers.add(viewResolver);
				}
			}
		}
		else {
			for (int i = 0; i < this.viewResolvers.size(); i++) {
				ViewResolver vr = this.viewResolvers.get(i);
				if (matchingBeans.contains(vr)) {
					continue;
				}
				String name = vr.getClass().getName() + i;
				obtainApplicationContext().getAutowireCapableBeanFactory().initializeBean(vr, name);
			}

		}
		AnnotationAwareOrderComparator.sort(this.viewResolvers);
		this.cnmFactoryBean.setServletContext(servletContext);
	}
	......
}
```
向容器中注入一个ViewResolver实现类MyViewResolver后，会自动添加到视图解析器中。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-e54c105976be6607.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***2.支持静态资源，首页访问***
如前所述

***3. 自动注册了Converter，GenericConverter，Formatter  beans***
Converter 转换器：如public String hello(User user)，将提交的表单转换为User对象，需要将文本转换为对应的数据类型。
Formatter 格式化器： 如将文本2020-10-24 转换为Date对象。
```java
		@Bean
		@Override
		public FormattingConversionService mvcConversionService() {
			WebConversionService conversionService = new WebConversionService(this.mvcProperties.getDateFormat());
			addFormatters(conversionService);
			return conversionService;
		}
```
可以通过在配置文件中添加属性`spring.mvc.dateFormat`来指定日期格式。

如果需要用到自定义的Converter，只需要实现Converter并注入到容器中，框架会自动将Converter的实现类进行注册。
```java
    public static void addBeans(FormatterRegistry registry, ListableBeanFactory beanFactory) {
        Set<Object> beans = new LinkedHashSet();
        beans.addAll(beanFactory.getBeansOfType(GenericConverter.class).values());
        beans.addAll(beanFactory.getBeansOfType(Converter.class).values());
        beans.addAll(beanFactory.getBeansOfType(Printer.class).values());
        beans.addAll(beanFactory.getBeansOfType(Parser.class).values());
        Iterator var3 = beans.iterator();

        while(var3.hasNext()) {
            Object bean = var3.next();
            if (bean instanceof GenericConverter) {
                registry.addConverter((GenericConverter)bean);
            } else if (bean instanceof Converter) {
                registry.addConverter((Converter)bean);
            } else if (bean instanceof Formatter) {
                registry.addFormatter((Formatter)bean);
            } else if (bean instanceof Printer) {
                registry.addPrinter((Printer)bean);
            } else if (bean instanceof Parser) {
                registry.addParser((Parser)bean);
            }
        }

    }
```

***3. 支持HttpMessageConverters***
- HttpMessageConverter：SpringMVC用来转换Http请求和响应；User---json
- HttpMessageConverters是从容器中确定；获取所有的HttpMessageConvcerter；
自己给容器中添加HttpMessageConverter，只需要将自己的组价注册到容器中

***4. 自动注册MessageCodesResolver***
定义错误代码生成规则

***5. 自动使用ConfigurableWebBindingInitializer***
初始化WebDataBinder：将请求数据绑定到javabean中。在其中会进行数据转化和日期格式化又会用到前面注入的Converter和Formatter。
我们可以配置一个ConfigurableWebBindingInitializer类替换默认的类。

<br>
###五、如何修改SpringBoot的默认配置
***1. 模式***
要修改容器中的某些自定义配置，就需要注入该类接口的实现类到容器中的，容器对该类的处理分为几种情况：
1. 处理类会读取容器中所有的该接口的实现类，包括用户自定义的和容器默认的类，同时生效。
2. 容器会首先注入用户自定义的类，当注入默认的实现类时会通过注解@ConditionMissingBear()来判断该类是否已注入，如已注入用户自定义的类，那么默认的类不注入。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-9eae8e4174399d2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 会通过BeanFactory.getBean()方法从容器中获取对象，如果获取不到，则自己创建一个默认的对象返回。即如果用户已注入自定义的类，就采用用户自定义的类。如ConfigurableWebBindingInitializer。

***2. 扩展SpringMVC***
```xml
<mvc:view-controller path="/hello" view-name="success"/>
<mvc:inerceptors>
  <mvc:interceptor>
    <mvc:mapping path="/hello"/>
    <bean></bean>
  </mvc:interceptor>
</mvc:interceptor>
```
编写一个配置类（@Configuration），是WebMvcConfigurerAdapter的实现类。
```java
@Configuration
public class WebMvcConfigurerAdapter implements WebMvcConfigurer {
    // 添加资源映射，浏览器发送/hello，请求，返回资源success.html
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/hello").setViewName("success");
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/uaa/public/**").addResourceLocations("classpath:public/");
    }
}
```
原理：
1. WebMvcAutoConfiguration是SpringMVC的自动配置类,SpringBoot项目启动时会将所有的WebMvcAutoConfiguration加入到容器中生效。
2. 在做其他自动配置时会导入SpringMVC相关的自动配置类@Import(EnableWebMvcConfiguration.class)
3. 容器中所有的WebMvcConfigurer都会一起起作用，包括我们自己注入的配置类


***3.全面接管SpringMVC***
在配置类中添加@EnableWebMvc注解
SpringBoot对SpringMVC的自动配置不需要了，所有SpringMVC配置失效，所有都需要我们自己进行配置。
1).
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
@Import(DelegatingWebMvcConfiguration.class)
public @interface EnableWebMvc {
}
```
2).
```java
@Configuration(proxyBeanMethods = false)
public class DelegatingWebMvcConfiguration extends WebMvcConfigurationSupport {
}
```
3).`失效原因：WebMvcAutoConfiguration有注解@ConditionalOnMissingBean，容器中没有WebMvcConfigurationSupport时该自动配置类才会生效。但是@EnableWebMvc会导入WebMvcConfigurationSupport导致该自动配置类失效。`
```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnWebApplication(type = Type.SERVLET)
@ConditionalOnClass({ Servlet.class, DispatcherServlet.class, WebMvcConfigurer.class })
@ConditionalOnMissingBean(WebMvcConfigurationSupport.class)
@AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE + 10)
@AutoConfigureAfter({ DispatcherServletAutoConfiguration.class, TaskExecutionAutoConfiguration.class,
		ValidationAutoConfiguration.class })
public class WebMvcAutoConfiguration {
}
```

<br>
###六、RestfulCRUD
#####1）、默认访问首页
......


<br>
#####2）、国际化
1. 编写国际化配置文件
2. 使用ResourceBundleMessageSource管理国际化资源文件
3. 在页面使用fmt:message取出国际化内容

**步骤：**
***1. 编写国际化配置文件，抽取页面了需要显示的国际化消息***
![image.png](https://upload-images.jianshu.io/upload_images/21580557-fc192beacd829cc2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***2. SpringBoot自动配置好了管理国际化资源文件的组件，默认为基础名为message（即直接写配置文件message.properties即可被国际化组件识别），可以在配置文件中配置该基础名spring.messages.basename=i18n.login。***
```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnMissingBean(name = AbstractApplicationContext.MESSAGE_SOURCE_BEAN_NAME, search = SearchStrategy.CURRENT)
@AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE)
@Conditional(ResourceBundleCondition.class)
@EnableConfigurationProperties
public class MessageSourceAutoConfiguration {

	@Bean
	@ConfigurationProperties(prefix = "spring.messages")
	public MessageSourceProperties messageSourceProperties() {
		return new MessageSourceProperties();

	@Bean
	public MessageSource messageSource(MessageSourceProperties properties) {
		ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
		if (StringUtils.hasText(properties.getBasename())) {  //private String basename = "messages";
			//设置国际化资源文件的基础名（去掉语言国家代码的）
			messageSource.setBasenames(StringUtils
					.commaDelimitedListToStringArray(StringUtils.trimAllWhitespace(properties.getBasename())));
		}
		if (properties.getEncoding() != null) {
			messageSource.setDefaultEncoding(properties.getEncoding().name());
		}
		messageSource.setFallbackToSystemLocale(properties.isFallbackToSystemLocale());
		Duration cacheDuration = properties.getCacheDuration();
		if (cacheDuration != null) {
			messageSource.setCacheMillis(cacheDuration.toMillis());
		}
		messageSource.setAlwaysUseMessageFormat(properties.isAlwaysUseMessageFormat());
		messageSource.setUseCodeAsDefaultMessage(properties.isUseCodeAsDefaultMessage());
		return messageSource;
	}
	......
}
```

***3. 去页面获取国际化的值***
需要将前端页面放在"classpath:/templates/"路径下，使得thymeleaf对其进行解析。
将前端页面的原值通过th: 标签进行修改，将国际化的值导入
![image.png](https://upload-images.jianshu.io/upload_images/21580557-ef9db301acf2a11e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

默认国际化是根据浏览器语言设置的信息切换国际化，如下WebMvcAutoConfiguration中的方法所示。
```java
		@Bean
		@ConditionalOnMissingBean
		@ConditionalOnProperty(prefix = "spring.mvc", name = "locale")
		public LocaleResolver localeResolver() {
			if (this.mvcProperties.getLocaleResolver() == WebMvcProperties.LocaleResolver.FIXED) {
				return new FixedLocaleResolver(this.mvcProperties.getLocale());
			}
			AcceptHeaderLocaleResolver localeResolver = new AcceptHeaderLocaleResolver();
			localeResolver.setDefaultLocale(this.mvcProperties.getLocale());
			return localeResolver;
		}
```
如果需要自定义国际化区域解析器，只需要在框架中注入LocaleResolver方法，那么默认的配置会失效（因为@ConditionalOnMissingBean注解存在）。
以下是自定义的区域解析器，通过在前端请求中添加区域信息，在区域解析器中获取区域信息，返回国际化后的页面
```java
@Component
public class MyLocaleResolver {

    @Bean
    public LocaleResolver localeResolver(){
        return new LocaleResolver() {
            @Override
            public Locale resolveLocale(HttpServletRequest request) {
                // 从请求参数中获取区域信息，如果没有携带，那么获取系统默认的区域信息
                String l = request.getParameter("l");
                Locale locale = Locale.getDefault();
                if (!StringUtils.isEmpty(l)) {
                    String[] split = l.split("_");
                    locale = new Locale(split[0], split[1]);
                }
                return locale;
            }

            @Override
            public void setLocale(HttpServletRequest request, HttpServletResponse response, Locale locale) {
            }
        };
    }
}
```
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7d3b9ca1bef208be.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>Thymeleaf的页面修改后，如何生效：
>1. 禁用缓存spring.thymeleaf.cache=false
>2. ctrl+f9后可以进行重新编译

<br>
#####3)添加拦截器
在登录页面成功登录后跳转到首页，可以返回重定向后的页面`return "redirect:/main.html";`来重定向到首页。
`return "forward:/main.html";`来转发到首页。

**为了防止用户在未登录的情况下直接访问首页，需要添加拦截器判断该用户是否登录，需要自定义拦截器并将该拦截器注册到框架中。**
1. 自定义类实现HandlerInterceptor接口。
```java
@Component
public class MyLoginHandlerInterceptor {

    @Bean
    public HandlerInterceptor handlerInterceptor() {
        return new HandlerInterceptor() {
            @Override
            public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
                Object user = request.getSession().getAttribute("loginUser");
                if (user == null) {
                    // 未登录，返回登录页面
                    request.setAttribute("msg","未登录，请先登录！");
                    request.getRequestDispatcher("/index.html").forward(request,response);  // 获取转发器，转发到指定路径
                    return false;
                } else {
                    // 已登录，放行请求
                    return true;
                }
            }

            @Override
            public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
            }

            @Override
            public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
            }
        };
    }

}
```
2. 注册到自动配置类中
```java
@Configuration
public class WebMvcConfigurerAdapter implements WebMvcConfigurer {

    @Resource
    private HandlerInterceptor handlerInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry){
        registry.addInterceptor(handlerInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns("/","/login.html","/user/login");
    }
}
```

<br>
#####4）错误处理机制
***1. 现象***

- 如果是网页访问返回一个默认的错误页面

![网页访问错误](https://upload-images.jianshu.io/upload_images/21580557-54a56565d061d8bf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 如果是其他客户端，默认响应一个json数据

![postman访问错误](https://upload-images.jianshu.io/upload_images/21580557-c529457ebd592d45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***2. 原理***
在@Import(AutoConfigurationImportSelector.class)中会自动导入spring.factories中的类，其中包括自动配置类ErrorMvcAutoConfiguration。
给容器中添加了以下组件
- DefaultErrorAttributes :
- BasicErrorController ：处理默认的/error请求，浏览器发送的请求头如果是text/html，则会返回html格式的响应，如果是其他，返回json格式的响应。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-c3ab924641e7774b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- ErrorPageCustomizer ：	@Value("${error.path:/error}")系统出现错误后来到error进行处理
- DefaultErrorViewResolver ：在BasicErrorController中遍历所有的异常视图解析器得到ModelAndView，然后交由DefaultErrorViewResolver 处理

步骤：一旦系统出现4xx或者5xx之类的错误；ErrorPageCustomizer就会生效（定制错误的响应规则），来到/error请求。就会被BasicErrorController提供的/error接口处理，通过判断

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnWebApplication(type = Type.SERVLET)
@ConditionalOnClass({ Servlet.class, DispatcherServlet.class })
// Load before the main WebMvcAutoConfiguration so that the error View is available
@AutoConfigureBefore(WebMvcAutoConfiguration.class)
@EnableConfigurationProperties({ ServerProperties.class, ResourceProperties.class, WebMvcProperties.class })
public class ErrorMvcAutoConfiguration {

	@Bean
	@ConditionalOnMissingBean(value = ErrorAttributes.class, search = SearchStrategy.CURRENT)
	public DefaultErrorAttributes errorAttributes() {
		return new DefaultErrorAttributes(this.serverProperties.getError().isIncludeException());
	}

	@Bean
	@ConditionalOnMissingBean(value = ErrorController.class, search = SearchStrategy.CURRENT)
	public BasicErrorController basicErrorController(ErrorAttributes errorAttributes,
			ObjectProvider<ErrorViewResolver> errorViewResolvers) {
		return new BasicErrorController(errorAttributes, this.serverProperties.getError(),
				errorViewResolvers.orderedStream().collect(Collectors.toList()));
	}

	@Bean
	public ErrorPageCustomizer errorPageCustomizer(DispatcherServletPath dispatcherServletPath) {
		return new ErrorPageCustomizer(this.serverProperties, dispatcherServletPath);
	}

	@Configuration(proxyBeanMethods = false)
	static class DefaultErrorViewResolverConfiguration {
		......
		@Bean
		@ConditionalOnBean(DispatcherServlet.class)
		@ConditionalOnMissingBean(ErrorViewResolver.class)
		DefaultErrorViewResolver conventionErrorViewResolver() {
			return new DefaultErrorViewResolver(this.applicationContext, this.resourceProperties);
		}
	}
	......
}
```

<br>
***3. 如何定制错误响应***

**3.1 如何定制错误的页面：**
- 有模板引擎的情况下，error/404.html（将错误页面命名为 错误状态码.html 放在模板引擎文件夹里面的error文件夹下），发生此状态码的错误就会来到对应的页面；可以使用4xx和5xx作为错误页面的文件名来匹配这种类型的所有错误，精确优先（优先寻找精确的状态码.html）；页面能获取的信息：timestamp、status、error、exception、message、errors
- 没有模板引擎（模板引擎templates/error找不到这个错误），也会到静态资源文件夹static/error下找
- 以上都没有错误页面，就是默认来到SpringBoot默认的错误提示页面
```java
// 在BasicErrorController类中，如果找不到视图，那么创建error视图并进行跳转
return (modelAndView != null) ? modelAndView : new ModelAndView("error", model);
```
```java
// 上述创建的error视图，跳转到在ErrorMvcAutoConfiguration中创建的视图对象，并返回默认的html错误页面
		@Bean(name = "error")
		@ConditionalOnMissingBean(name = "error")
		public View defaultErrorView() {
			return this.defaultErrorView;
		}
```

**3.2 如何定制错误json串**
通过注解@ControllerAdvice注解类来处理所有的异常信息。
但是这样会导致所有的异常都会返回json格式的信息。

**如何做到自适应，即网页返回自定义的错误页面、其他客户端返回json数据**
可以通过返回重定向到/error接口进行自适应。即`return "forward:/error";` 

>但是有个问题，就是这样重定向之后的状态码是200，导致无法匹配到自定义的异常页面。代码如下：
>```java
>	@RequestMapping(produces = MediaType.TEXT_HTML_VALUE)
>	public ModelAndView errorHtml(HttpServletRequest request, >HttpServletResponse response) {
>		HttpStatus status = getStatus(request);   //这个方法会获取请>求中的javax.servlet.error.status_code属性的值作为状态码
>		Map<String, Object> model = Collections
>				.unmodifiableMap(getErrorAttributes(request, >isIncludeStackTrace(request, MediaType.TEXT_HTML)));
>		response.setStatus(status.value());
>		ModelAndView modelAndView = resolveErrorView(request, >response, status, model);
>		return (modelAndView != null) ? modelAndView : new >ModelAndView("error", model);
>	}
>```

`因此需要在请求中添加javax.servlet.error.status_code属性并将值设置为对应的错误码.`如下代码所示。
```java
    @ExceptionHandler
    @ResponseStatus(HttpStatus.OK)
    public CommonResult<String> exception(Exception e, HttpServletRequest request) {
        String message = e.getMessage();
        e.printStackTrace();
        request.setAttribute("javax.servlet.error.status_code",500);

        return CommonResult.error(message);
    }
```

**3.3**将我们的定制数据携带出去
出现错误后
