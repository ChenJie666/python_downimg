***日志级别***
七个日志级别：OFF FATAL ERROR WARN INFO DEBUG ALL

***依赖***
```
<dependency>
	<groupId>ch.qos.logback</groupId>
	<artifactId>logback-classic</artifactId>
	<version>1.2.1</version>
</dependency>
<dependency>
	<groupId>ch.qos.logback</groupId>
	<artifactId>logback-core</artifactId>
	<version>1.2.1</version>
</dependency>
```

#####方式一：
***在.yml文件中添加配置***
```java
#修改日志级别和日志输出位置
logging:
  level:
    # root日志以INFO级别输出
    root: INFO
    # 此包下所有class以DEBUG级别输出
    com.example.log_demo.log1: DEBUG
  file: logs/${spring.application.name}.log
```


#####方式二：
resources中创建logback-spring.xml文件，logback-spring.xml文件相比较logback.xml文件，可以使用<springProfile>这个标签。
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration scan="true" scanPeriod="10 seconds">
    <!-- scan:当scan为true时，配置文件如果发生变化，会被重新加载，默认为true -->
    <!-- scanPeriod:监测配置文件是否修改的时间间隔，单位默认ms，默认间隔为1分钟 -->
    <!-- debug:当debug为true时，会打印logback内部日志，默认为false -->

    <!-- 工程名字 -->
    <contextName>${SERVICE_NAME}</contextName>

    <!-- property用于定义变量，通过${}来调用已定义的变量 -->
    <!-- 日志在工程中的输出位置 -->
    <property name="log.path" value="C:/Users/Administrator/Desktop/log"/>
    <!-- 彩色日志 -->
    <!-- 配置格式变量：CONSOLE_LOG_PATTERN 彩色日志格式 -->
    <!-- magenta:洋红 -->
    <!-- boldMagenta:粗红-->
    <!-- cyan:青色 -->
    <!-- white:白色 -->
    <!-- magenta:洋红 -->
    <!-- 定义日志输出样式 -->
    <property name="CONSOLE_LOG_PATTERN" value="%yellow(%date{yyyy-MM-dd HH:mm:ss}) |%highlight(%-5level) |%blue(%thread) |%blue(%file:%line) |%green(%logger) |%cyan(%msg%n)"/>


    <!-- 控制台输出 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <!-- 此处设置了INFO级别，其他位置的配置不会生效 -->
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>INFO</level>
        </filter>
        <!-- 日志输出样式和编码 -->
        <encoder>
            <pattern>${CONSOLE_LOG_PATTERN}</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>


    <!-- 时间滚动输出日志，level为DEBUG -->
    <appender name="DEBUG_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${log.path}/log_debug.log</file>　　　　　　　　　　　
        　　
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg %n</pattern>
            <charset>UTF-8</charset>
        </encoder>

        <!-- 日志滚动策略，按日期和大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">　　　　　　　　　　　　　
            <!-- 每天日志归档路径及格式 -->
            <fileNamePattern>${log.path}/debug/log-debug-%d{yyyy-MM-dd}.%i.log</fileNamePattern>　　　　　　　　　　　　
            <!-- 文件查过100M回滚为新文件 -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <!-- 日志保留天数 -->
            <maxHistory>30</maxHistory>　
        </rollingPolicy>

        <!-- 日志记录的级别 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>DEBUG</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!-- 时间滚动输出日志，level为INFO -->
    <appender name="INFO_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${log.path}/log_info.log</file>　　　　　　　　　　　
        　　
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg %n</pattern>
            <charset>UTF-8</charset>
        </encoder>

        <!-- 日志滚动策略，按日期和大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">　　　　　　　　　　　　　
            <!-- 每天日志归档路径及格式 -->
            <fileNamePattern>${log.path}/info/log-info-%d{yyyy-MM-dd}.%i.log</fileNamePattern>　　　　　　　　　　　　
            <!-- 文件查过100M回滚为新文件 -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <!-- 日志保留天数 -->
            <maxHistory>30</maxHistory>　
        </rollingPolicy>

        <!-- 日志记录的级别 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>INFO</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!-- 时间滚动输出日志，level为WARN -->
    <appender name="WARN_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${log.path}/log_warn.log</file>　　　　　　　　　　　
        　　
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg %n</pattern>
            <charset>UTF-8</charset>
        </encoder>

        <!-- 日志滚动策略，按日期和大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">　　　　　　　　　　　　　
            <!-- 每天日志归档路径及格式 -->
            <fileNamePattern>${log.path}/warn/log-warn-%d{yyyy-MM-dd}.%i.log</fileNamePattern>　　　　　　　　　　　　
            <!-- 文件查过100M回滚为新文件 -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <!-- 日志保留天数 -->
            <maxHistory>30</maxHistory>　
        </rollingPolicy>

        <!-- 日志记录的级别 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>WARN</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!-- 时间滚动输出日志，level为ERROR -->
    <appender name="ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${log.path}/log_error.log</file>　　　　　　　　　　　
        　　
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg %n</pattern>
            <charset>UTF-8</charset>
        </encoder>

        <!-- 日志滚动策略，按日期和大小记录 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">　　　　　　　　　　　　　
            <!-- 每天日志归档路径及格式 -->
            <fileNamePattern>${log.path}/error/log-error-%d{yyyy-MM-dd}.%i.log</fileNamePattern>　　　　　　　　　　　　
            <!-- 文件查过100M回滚为新文件 -->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <!-- 日志保留天数 -->
            <maxHistory>30</maxHistory>　
        </rollingPolicy>

        <!-- 日志记录的级别 -->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>ERROR</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
    </appender>

    <!--
        使用mybatis时，sql语句是debug下才打印，而此处只配置了INFO级别，所以想查看sql语句，有以下两种操作：
        第一种把<root level="INFO">改为<root level="DEBUG">就会打印sql，不过会造成日志记录过大
        第二种就是单独给mapper下目录配置DEBUG模式，代码如下，这样配置sql语句会打印，其他还是正常的INFO级别；
     -->

    <!-- 对应spring.profiles.active属性，如果是dev环境，则生效 -->
    <springProfile name="dev">
        <!--
            logger用来设置某个包或某个类的日志打印级别。
            name：来指定包或者类
            level：用来设置打印级别，如果未设置，logger会继承上级的级别
            可以输出项目中的debug日志，包括mybatis的sql日志
        -->
        <logger name="com.cj" level="DEBUG"></logger>

        <!-- root节点用来指定最基础的日志输出级别，只有一个level属性；level用来设置打印级别，默认是DEBUG，可以包含零个或多个appender元素 -->
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
            <appender-ref ref="DEBUG_FILE"/>
            <appender-ref ref="INFO_FILE"/>
            <appender-ref ref="WARN_FILE"/>
            <appender-ref ref="ERROR_FILE"/>
        </root>
    </springProfile>

    <!-- 对应spring.profiles.active属性，如果是pro环境，则生效 -->
    <springProfile name="pro">

        <!-- root节点用来指定最基础的日志输出级别，只有一个level属性；level用来设置打印级别，默认是DEBUG，可以包含零个或多个appender元素 -->
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
            <appender-ref ref="DEBUG_FILE"/>
            <appender-ref ref="INFO_FILE"/>
            <appender-ref ref="WARN_FILE"/>
            <appender-ref ref="ERROR_FILE"/>
        </root>
    </springProfile>

</configuration>
```

可以通过@SLF4J注解，log.info/warn/error（）方法输出信息到日志文件中。

#####方式三：
在reousrces文件夹下创建log4j.properties
```
log4j.rootLogger=info,stdout
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss}  %5p --- [%50t]  %-80c(line:%5L)  :  %m%n
```
