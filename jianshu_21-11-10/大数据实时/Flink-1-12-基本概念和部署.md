#一、简介
Flink是一个框架和分布式处理引擎，用于对无界和有界数据流进行状态计算。实现处理的低延迟、高吞吐、准确性和容错性。

**需要解决的问题：**
1.如何保证处理结果准确性
2.如何保证数据的时序性
3.如何保证容灾

**那些行业需要处理流数据：**
1.电商和市场营销：数据报表、广告投放、业务流程需要
2.物联网：传感器实时数据采集和显示、实时报警，交通运输业
3.电信业：基站流量调配
4.实时结算和通知推送，实时检测异常行为

#二、处理架构对比
##2.1 离线处理架构
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7b2b3a97918b5944.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
存储与处理是分离的。


<br>
##2.2 流式处理框架
- ![image.png](https://upload-images.jianshu.io/upload_images/21580557-330f4548aa99dfce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###2.2.1 第一代流式处理框架（Storm）
- ![image.png](https://upload-images.jianshu.io/upload_images/21580557-5b949853788bf65e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
为了解决内存中数据的可靠性，引入了远程存储的概念，即有状态的流式处理。

与第三代流式处理框架
| 对比点          | Storm                            | Spark Streaming                                           |
| --------------- | -------------------------------- | --------------------------------------------------------- |
| 实时计算模型    | 纯实时，来一条数据，处理一条数据 | 准实时，对一个时间段内的数据收集起来，作为一个RDD，再处理 |
| 实时计算延迟度  | 毫秒级                           | 秒级                                                      |
| 吞吐量          | 低                               | 高                                                        |
| 事务机制        | 支持完善                         | 支持，但不够完善                                          |
| 健壮性 / 容错性 | ZooKeeper，Acker，非常强         | Checkpoint，WAL，一般                                     |
| 动态调整并行度  | 支持                             | 不支持                                                    |

storm保证了低延迟，但是没有保证数据的吞吐量、时序性和准确性

<br>
###2.2.2 第二代流式处理架构（lambda架构）
- ![image.png](https://upload-images.jianshu.io/upload_images/21580557-f66f10d59d3b2b9d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
使用两套系统，流处理系统保证低延迟，批处理系统来校准结果准确性。

<br>
###2.2.3 第三代流式处理架构 （Flink/Spark Streaming）
Flink的主要特点：
- 事件驱动（Event-driven）：一个事件记录进行一次处理，区别于顺序和流程驱动。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-0d92f520bc321888.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 基于流的世界观：离线数据是有界的流；实时数据是一个没有界限的流，这就是所谓的有界流和无界流。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-0585014dfe54cf12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 分层API：越顶层越抽象，表达含义越简明，使用越方便；越底层越具体，表达能力越丰富，使用越灵活。如果顶层API不够用，可以通过底层API进行实现。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-b47bf831da9092d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**SQL/Table API：**如果业务逻辑比较简单，可以使用顶层的API进行实现；
**DataStream API：**可以对流进行自定义转换和操作，如开窗；也可以使用DataSet进行批处理操作。是最为常用的API层级。
**ProcessFunction（events，state，time）：**对于非常复杂的业务场景，DataStream API都不能实现，那么可以使用这个最底层的API，可以自定义任何功能。可以获取当前所有的`时间`(state)和`状态`(time)，可以定义`定时器`。

- 其他特点：支持事件时间和处理时间；`精确一次`的状态一致性保证；低延迟，每秒处理百万个事件，`毫秒级延迟`；与众多常用的存储系统的连接；`高可用`，`动态扩展`，实现7*24小时全天候运行。

- ![image.png](https://upload-images.jianshu.io/upload_images/21580557-12bc05d9e878b95e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Spark和Flink的主要差别就在于计算模型不同。Spark采用了微批处理模型，而Flink采用了基于操作符的连续流模型。因此，对Apache Spark和Apache Flink的选择实际上变成了计算模型的选择，而这种选择需要在延迟、吞吐量和可靠性等多个方面进行权衡。
	如果对流数据进行处理，推荐使用Flink，主（显而）要（易见）的原因为：
- Flink灵活的窗口
- Exactly Once语义保证


<br>
# 三、Flink的简单使用
**依赖**
```xml
    <properties>
        <flink.version>1.12.0</flink.version>
        <scala.binary.version>2.11</scala.binary.version>
        <slf4j.version>1.7.30</slf4j.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-streaming-scala_${scala.binary.version}</artifactId>
            <version>${flink.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-clients_${scala.binary.version}</artifactId>
            <version>${flink.version}</version>
        </dependency>

        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>${slf4j.version}</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
            <version>${slf4j.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.logging.log4j</groupId>
            <artifactId>log4j-to-slf4j</artifactId>
            <version>2.14.0</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- 该插件用于将scala代码编译为class字节码文件 -->
            <plugin>
                <groupId>net.alchim31.maven</groupId>
                <artifactId>scala-maven-plugin</artifactId>
                <version>4.4.0</version>
                <executions>
                    <execution>
                        <!-- 声明编译到maven的compile阶段 -->
                        <goals>
                            <goal>compile</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                </configuration>
                <executions>
                    <execution>
                        <id>make-assembly</id>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
```

## getExecutionEnvironment
创建一个执行环境，表示当前执行程序的上下文。 如果程序是独立调用的，则此方法返回本地执行环境；如果从命令行客户端调用程序以提交到集群，则此方法返回此集群的执行环境，也就是说，getExecutionEnvironment会根据查询运行的方式决定返回什么样的运行环境，是最常用的一种创建执行环境的方式。
```
val env: ExecutionEnvironment = ExecutionEnvironment.getExecutionEnvironment
```
如果没有设置并行度，会以flink-conf.yaml中的配置为准，默认是1。
```yaml
parallelism.default: 1
```

## createLocalEnvironment
返回本地执行环境，需要在调用时指定默认的并行度。
```
val env = StreamExecutionEnvironment.createLocalEnvironment(1)
```

## createRemoteEnvironment
返回集群执行环境，将Jar提交到远程服务器。需要在调用时指定JobManager的IP和端口号，并指定要在集群中运行的Jar包。
```
val env = ExecutionEnvironment.createRemoteEnvironment("jobmanage-hostname", 6123,"YOURPATH//wordcount.jar")
```


## 3.1 Source输入
word_count功能代码
**①批处理**
需要导入隐式转换：`import org.apache.flink.api.scala._`
```scala
import org.apache.flink.api.scala.DataSet
import org.apache.flink.api.scala._

object WordCount {
  //  **_  的用法：①包中所有类②系统默认初始化③将函数不执行返回④参数占位符⑤隐藏导入的类⑥标识符⑦绝对路径**⑧case _ 不管什么值都匹配⑨case _:BigInt =>...  当后面不用该变量，不关心变量时，可以用 _ 代替。
  def main(args: Array[String]):Unit = {
    // 创建一个批处理的执行环境
    val env: ExecutionEnvironment = ExecutionEnvironment.getExecutionEnvironment

    // 从文件中读取数据
    val inputPath: String = "C:\\Users\\Administrator\\Desktop\\不常用的项目\\flink_demo\\src\\main\\resources\\test.txt"
    val inputDataSet: DataSet[String] = env.readTextFile(inputPath)

    // 对数据进行转换处理统计，先分词，再按照word进行分组，最后进行聚合统计
    val resultDataSet: DataSet[(String,Int)] = inputDataSet
      .flatMap(_.split(" "))
      .map((_, 1))
      .groupBy(0)  // 以第一个元素作为key进行分组
      .sum(1)

    resultDataSet.print()
  }
}
```
**②流处理**
如在192.168.32.242节点上启动命令`nc -lk 7777`向端口7777发送数据包
配置程序的参数`--host 192.168.32.242 --port 7777`来监听该端口获取流数据。
```scala
import org.apache.flink.api.java.utils.ParameterTool
import org.apache.flink.streaming.api.scala.{DataStream, StreamExecutionEnvironment}
import org.apache.flink.api.scala._

object StreamWordCount {
  def main(args: Array[String]): Unit = {
    // 创建一个流处理的执行环境  DataStreamApi
    val env: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment

    env.setParallelism(8) // 设置最大并行度，默认是本机核心数

    // 接收一个socket文本流
    val paramTool: ParameterTool = ParameterTool.fromArgs(args)
    val host: String = paramTool.get("host")
    val port: Int = paramTool.getInt("port")
    val inputDataStream: DataStream[String] = env.socketTextStream(host, port)

    // 进行转化处理统计
    val resultDataStream: DataStream[(String, Int)] = inputDataStream
      .flatMap(_.split(" "))
      .filter(_.nonEmpty)
      .map((_, 1))
      .keyBy(0) // 流处理没有groupBy，使用keyBy进行聚合
      .sum(1)

    resultDataStream.print() //分布式处理会导致输出是乱序的
    resultDataStream.print().setParallelism(1) //打印的并行度是1，不会输出进程号。

    // 定义任务后，开始执行
    env.execute("stream word count")
  }
}
```
结果如下，最开始的数字表示运行在哪个线程下，线程号是根据key的hash值来决定的
```
6> (word,1)
3> (hello,1)
3> (hello,2)
5> (world,1)
```
原理：会将key计算得到哈希后发送到对应的线程中，这样相同key的数据发送到同一个线程中进行计算，保证了数据的准确性和吞吐量。
问题：分布式会导致时序错乱，如print()算子在不同节点上执行导致输出结果时间错乱。

**③从kafka中读取流数据**
添加kafka连接依赖
```
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-connector-kafka_${scala.binary.version}</artifactId>
            <version>${flink.version}</version>
        </dependency>
```
代码
```scala
import java.util.Properties

import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.streaming.api.scala.{DataStream, StreamExecutionEnvironment}
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer
import org.apache.flink.api.scala._

object StreamKafka {
  def main(args: Array[String]): Unit = {
    val env: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment

    // 1.从集合中读取数据
    val readProperties = new Properties()
    readProperties.setProperty("bootstrap.servers", "192.168.32.242:9092")
    readProperties.setProperty("group.id", "consumer-group")
    readProperties.setProperty("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    readProperties.setProperty("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    val myConsumer = new FlinkKafkaConsumer[String]("kafka_test", new SimpleStringSchema(), readProperties)
    //    myConsumer.setStartFromEarliest()
    myConsumer.setStartFromLatest()

    val inputStream = env.addSource(myConsumer)

    val resultDataStream: DataStream[(String, Int)] = inputStream
      .flatMap(_.split(" "))
      .filter(_.nonEmpty)
      .map((_, 1))
      .keyBy(0) // 流处理没有groupBy，使用keyBy进行聚合
      .sum(1)

    resultDataStream.print() //分布式处理会导致输出是乱序的
    resultDataStream.print().setParallelism(1) //打印的并行度是1，不会输出进程号。

    env.execute("kafka_source_test")
  }
}
```
在kafka中创建topic：`bin/kafka-topics.sh --zookeeper bigdata1:2181 --create --topic kafka_test --partitions 3 --replication-factor 1`
启动程序，然后向创建的topic中添加数据`bin/kafka-console-producer.sh --broker-list bigdata1:9092 --topic kafka_test`进行测试。


④读取自定义数据源的流式数据
```scala
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment
import org.apache.flink.streaming.api.functions.source.SourceFunction

import scala.util.Random

object SourceTest {
  // 自定义数据源读取流数据
  def main(args: Array[String]): Unit = {
    val env: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment

    val stream2 = env.addSource(new MySensorSource())

    stream2.print()

    env.execute("diy_source_test")

  }

}

// 自定义函数实现run和cancel方法
class MySensorSource() extends SourceFunction[SensorReading] {
  // 定义一个标志位表示数据源是否正常发出数据
  var running: Boolean = true

  override def cancel(): Unit = running = false

  override def run(sourceContext: SourceFunction.SourceContext[SensorReading]): Unit = {
    // 定义一个循环，不停生产数据，除非被cancel
    val curTemp = 1.to(10).map(i => ("sensor_" + i, Random.nextDouble() * 100))

    while (running) {

      curTemp.map(
        data => (data._1, data._2 + Random.nextGaussian())
      )
      val curTime = System.currentTimeMillis()
      curTemp.foreach(
        data => sourceContext.collect(SensorReading(data._1, data._2, curTime))
      )

      Thread.sleep(1000)
    }
  }

}

case class SensorReading(name: String, temp: Double, timestamp: Long)
```

<br>
## 3.2  Transform转换算子
### map
```
val streamMap = stream.map { x => x * 2 }
```

### flatMap
flatMap(List(1,2,3))(i ⇒ List(i,i))
结果是List(1,1,2,2,3,3), 
List("a b", "c d").flatMap(line ⇒ line.split(" "))
结果是List(a, b, c, d)。
```
val streamFlatMap = stream.flatMap{
    x => x.split(" ")
}
```

### Filter
过滤不符合条件的元素
```
val streamFilter = stream.filter{
    x => x == 1
}
```

### KeyBy
DataStream → KeyedStream：逻辑地将一个流拆分成不相交的分区，每个分区包含具有相同key的元素，在内部以hash的形式实现的。

### 滚动聚合算子(Rolling Aggregation)
这些算子可以针对KeyedStream的每一个支流做聚合。
- sum()
- min()
- max()
- minBy()
- maxBy()

### Reduce
KeyedStream → DataStream：一个分组数据流的聚合操作，合并当前的元素和上次聚合的结果，产生一个新的值，返回的流中包含每一次聚合的结果，而不是只返回最后一次聚合的最终结果。
```
    val stream2 = env.readTextFile("input/sensor.txt")
      .map( data => {
        val dataArray = data.split(",")
        SensorReading1(dataArray(0).trim, dataArray(1).trim.toLong, dataArray(2).trim.toDouble)
      })
      .keyBy("id")
      .reduce( (x, y) => SensorReading1(x.id, y.timestamp, y.temperature.min(x.temperature)) )
```

### Split 和 Select

### Connect 和 CoMap

### Union

<br>
## 3.3 支持的数据类型

<br>
## 3.4 实现UDF函数

<br>
## 3.5 Sink输出
输出包括文件、Kafka、ES、MySQL等

<br>
###3.4 窗口API
窗口包括滚动窗口（TumblingWindow）、滑动窗口（SlidingWindow）、会话窗口（SessionWindow）和全局窗口（GlobalWindow）。

KeyedStream有window方法调用窗口函数，
DataStream有windowAll方法调用窗口函数（因为并行度是1，性能不高，所以先进行聚合），
调用窗口函数之后，得到的是WindowedStream，无界流变成了有界流。
调用聚合函数后得到的还是DataStream。

窗口函数分为增量聚合函数（数据来一条计算一次）和全窗口函数（收集后统一计算）。ReduceFunction、AggregateFunction等就是增量聚合函数，ProcessWindowFunction就是全窗口函数。

<br>
###3.5 其他API
trigger() 触发器：定义window什么时候关闭，触发计算并输出结果
evictor() 移除器：定义删除某些数据逻辑
allowedLateness()：允许处理迟到的数据
sideOutputLateData()：将迟到的数据放入到侧输出流
getSideOuntput()：获取侧输出流

![image.png](https://upload-images.jianshu.io/upload_images/21580557-20e161f91f978ad3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



<br>
#四、服务器中运行程序
## 4.1单机模式
4.1.1 启动单机模式
下载地址：[https://www.apache.org/dyn/closer.lua/flink/flink-1.12.0/flink-1.12.0-bin-scala_2.12.tgz](https://www.apache.org/dyn/closer.lua/flink/flink-1.12.0/flink-1.12.0-bin-scala_2.12.tgz)
启动命令
```shell
/bin/start-cluster.sh
```
启动单节点模式。
可以访问UI界面[http://192.168.32.242:8081](http://192.168.32.242:8081/)
![基础配置](https://upload-images.jianshu.io/upload_images/21580557-2d6a1c4a4b069e1f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##4.1.2 提交任务
**设置并行度的优先级(由高到低)**
- 算子设置
- 全局设置
- 提交时UI界面输入设置
- 配置文件设置

**4.1.3 上传文件设置参数**
![配置参数](https://upload-images.jianshu.io/upload_images/21580557-2fd23a5209b5ab60.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**4.1.4 查看执行计划**
![任务计划图JobGraph](https://upload-images.jianshu.io/upload_images/21580557-6ebf3caa50194c01.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**4.1.5 启动任务**
可以通过UI界面提交任务，也可以通过命令行提交任务：
```shell
bin/flink run -c com.iotmars.wecook.StreamWordCount -p 2 /opt/jar/flink-demo-0.0.1-SNAPSHOT-jar-with-dependencies.jar --host localhost --port 6666
```
>- -c 表示类路径
>- -p 表示并行度
>- 然后加上启动jar路径
>- 最后添加参数
>`注意：如果slot不够，会导致卡死在分配资源阶段导致最后超时失败。`

**4.1.6 查看任务**
```shell
bin/flink list [-a]
```
![image.png](https://upload-images.jianshu.io/upload_images/21580557-a163f2a575c2d85a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**4.1.7 取消任务**
可以通过UI界面取消任务，也可以通过命令行取消任务：
```shell
bin/flink cancel 4198899a1a47f496309fe2da2e31c1f5
```

**4.1.8 停止flink集群**
```shell
/bin/stop-cluster.sh
```

<br>
## 4.2 Yarn模式
###4.2.1 Session-cluster
**概念：**Session-Cluster模式需要先启动集群，然后再提交作业，接着会向yarn申请一块空间后，**资源永远保持不变**。如果资源满了，下一个作业无法提交，只能等到yarn中的一个作业执行完成之后释放了资源，才能进行下一个作业任务。
所有作业共享Dispatcher和ResourceManager，共享资源，适合规模小执行时间短的作业。

`在yarn中初始化一个flink集群，开辟指定的资源，以后提交任务都向这里提交。这个flink集群会常驻在yarn集群中，除非手工停止。`

**启动：**
①启动yarn-session：
```
// 添加环境变量
export HADOOP_CLASSPATH=`hadoop classpath`
// 启动yarn-session
yarn-session.sh -n 2 -s 2 -jm 1024 -nm test -d
// 或调度器中创建了多个队列，需要指定队列
nohup ./yarn-session.sh -s 2 -jm 1024 -tm 2048 -nm flink-on-yarn -qu flink -d 1>/opt/module/flink-1.12.0/yarn-session.log 2>/opt/module/flink-1.12.0/yarn-session.err &
```
>**参数说明：** 
>**-n（--container）：**TaskManager的数量（建议不指定，会动态添加，且flink1.10中已经不再支持）；
>**-s（--slots）：**每个TaskManager的slot数量，默认一个slot一个sore，默认每个taskmanager的slot个数为1，有时可以多一些taskmanager，做冗余；
>**-jm：**JobManager的内存（MB）；
>**-tm：**每个taskmanager的内存（MB）；
>**-nm：**yarn的appName（yarn的ui上的名字）；
>**-d：**后台执行；
>**-qu：**指定使用的yarn队列

关闭yarn-session：
```
# 找到flink集群任务的id，然后kill
yarn application -kill application_1616059084025_0002
```

②提交任务(和standalone模式一样)：
```shell
bin/flink run -c com.iotmars.wecook.StreamWordCount -p 2 /opt/jar/flink-demo-0.0.1-SNAPSHOT-jar-with-dependencies.jar --host localhost --port 6666
```
>- -c 表示类路径
>- -p 表示并行度
>- 然后加上启动jar路径
>- 最后添加参数
>`注意：如果slot不够，会导致卡死在分配资源阶段导致最后超时失败。`

③查看任务状态：去yarn控制台查看任务状态
④取消yarn-session：
```shell
yarn application --kill job_id
```

可以通过[http://192.168.32.243:37807](http://192.168.32.243:37807/)访问Web页面（会在某台服务器上部署一个Web页面）


###4.2.2 Per-Job-Cluster
**概念：**一个Job会对应一个集群，每提交一个作业会根据自身的情况，都会单独向yarn申请资源，直到作业执行完成，一个作业失败与否不会影响下一个作业的正常提交和运行。独享Dispatcher和ResourceManager，按需接受资源申请，适合大规模长时间运行的作业。
`每次提交都会创建一个新的flink集群，任务之间互相独立，互不影响，方便管理。任务执行完成后创建的集群也会消失。`
**操作：**
①不启动yarn-session，直接执行job
```shell
flink run -m yarn-cluster -c com.iotmars.wecook.StreamWordCount  /opt/jar/flink-demo-0.0.1-SNAPSHOT-jar-with-dependencies.jar --host localhost --port 7777
```

<br>
## 4.3 Kubernetes部署
Flink在最近的版本中也支持了k8s部署模式，部署如下
- ①搭建k8s集群
- ②配置各组件的yaml文件
在k8s上构建Flink Session Cluster，需要将Flink集群的组件对应的docker镜像分别在k8s上启动，包括JobManager、JobManager、JobManagerService三个镜像服务。每个镜像服务都可以从中央镜像仓库中获取。
- ③启动Flink Session Cluster
```
// 启动jobmanager-service服务
kubectl create -f jobmanager-service.yaml
// 启动jobmanager-deployment服务
kubectl create -f jobmanager-deployment.yaml
// 启动taskmanager-deployment服务
kubectl create -f taskmanager-deployment.yaml
```
- ④访问Flink UI页面
集群启动后，就可以通过JobManagerServices中配置的WebUI端口进行访问
http://{JobManagerHost:Port}/api/v1/namespaces/default/services/flink-jobmanager:ui/proxy

<br>
#五、 Flink运行架构
link运行时架构主要包括四个不同的组件，它们会在运行流处理应用程序时协同工作：**作业管理器（JobManager）**、**资源管理器（ResourceManager）**、**任务管理器（TaskManager）**，以及**分发器（Dispatcher）**。因为Flink是用Java和Scala实现的，所以所有组件都会运行在Java虚拟机上。每个组件的职责如下：
- 作业管理器（JobManager）：控制一个应用程序执行的主进程，也就是说，每个应用程序都会被一个不同的JobManager所控制执行。**①**JobManager会先接收到要执行的应用程序，这个应用程序会包括：作业图（JobGraph）、逻辑数据流图（logical dataflow graph）和打包了所有的类、库和其它资源的JAR包。JobManager会把JobGraph转换成一个物理层面的数据流图，这个图被叫做“执行图”（ExecutionGraph），包含了所有可以并发执行的任务。**②**JobManager会向资源管理器（ResourceManager）请求执行任务必要的资源，也就是任务管理器（TaskManager）上的插槽（slot）。**③**一旦它获取到了足够的资源，就会将执行图分发到真正运行它们的TaskManager上。**④**而在运行过程中，JobManager会负责所有需要中央协调的操作，比如说检查点（checkpoints）的协调。
- 资源管理器（ResourceManager）：主要负责管理任务管理器（TaskManager）的插槽（slot），TaskManger插槽是Flink中定义的处理资源单元。Flink为不同的环境和资源管理工具提供了不同资源管理器，比如YARN、Mesos、K8s，以及standalone部署。**①**当JobManager申请插槽资源时，ResourceManager会将有空闲插槽的TaskManager分配给JobManager。**②**如果ResourceManager没有足够的插槽来满足JobManager的请求，它还可以向资源提供平台发起会话，以提供启动TaskManager进程的容器。**③**另外，ResourceManager还负责终止空闲的TaskManager，释放计算资源。
- 任务管理器（TaskManager）：Flink中的工作进程。通常在Flink中会有多个TaskManager运行，每一个TaskManager都包含了一定数量的插槽（slots）。插槽的数量限制了TaskManager能够执行的任务数量。**①**启动之后，TaskManager会向资源管理器注册它的插槽；**②**收到资源管理器的指令后，TaskManager就会将一个或者多个插槽提供给JobManager调用。JobManager就可以向插槽分配任务（tasks）来执行了。**③**在执行过程中，一个TaskManager可以跟其它运行同一应用程序的TaskManager以流的形式进行数据的传输。
- 分发器（Dispatcher）：**①**可以跨作业运行，它为应用提交提供了REST接口。当一个应用被提交执行时，分发器就会启动并将应用移交给一个JobManager。由于是REST接口，所以Dispatcher可以作为集群的一个HTTP接入点，这样就能够不受防火墙阻挡。**②**Dispatcher也会启动一个Web UI，用来方便地展示和监控作业执行的信息。Dispatcher在架构中可能并不是必需的，这取决于应用提交运行的方式。


##5.1 任务提交流程
### 5.1.1 Flink的单机模式任务提交流程
![image.png](https://upload-images.jianshu.io/upload_images/21580557-dc864e0a97120a92.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
1. Dispatcher提供了restful风格的接口用于提交任务；
2. JobManager分析任务生成执行图，然后向ResourceManager申请slot资源；
3. ResourceManager启动TaskManager，TaskManager在启动会向ResourceManager进行注册slot；
4. JobManager提交要在slot中执行的任务。

##5.1.2 Yarn的Per-Job-Cluster模式下的任务提交流程
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7f4a7f129fbe38ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**流程概述：**
提交Job请求后由Yarn启动所需资源数量的容器，容器中启动的TaskManager节点向ResourceManager进行slots的注册，然后JobManager向slots分发任务执行。
`相当于每次提交Job后都启动一个Flink的TaskManager集群进行处理。`

**流程详情：**
1. 提交JOB后，将JAR包和配置上传到HDFS，之后向YARN的ResourceManager提交任务；
2. RM通知NodeManager启动AM，AM启动后加载Flink的Jar包和配置构建环境，然后启动JobManager和Flink的ResourceManager；
3. 在JobManager中进行任务切分，然后向Flink的ResourceManager进行任务请求，再向Yarn的ResourceManager进行资源申请；
4. Yarn的ResourceManager根据请求的资源数启动NodeManager，然后在容器中启动TaskManager；
5. TaskManager向Flink的ResourceManager进行slots资源注册(发送心跳)，然后由Flink的JobManager进行任务分配。


###5.2 TaskManager和Slot
**两者关系**
- 一个TaskManager至少有一个Slot，有多少个slot可以接收多少个任务。
- Slot拥有独立的内存，而不是独立的cpu。可以理解为Flink中每一个TaskManager都是一个JVM进程，它会在独立的线程上执行一个或多个子任务。
- Task Slot是静态的概念，是指TaskManager具有的并发执行能力，可以通过参数`taskmanager.numberOfTaskSlots`进行配置；而并行度parallelism是动态概念，即TaskManager运行程序时实际使用的并发能力，可以通过参数`parallelism.default`进行配置。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-8c7d510071d8a094.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**任务分配**
- 并不是每个算子的任务都会放到不同的Slot中，而是同一个任务会根据并发分配到不同的Slot中，而不同任务会分配到同一个Slot中，所以可能会有slot会保存一个pipeline(即包含了所有的算子任务)。好处是如果算子工作量不同，不会导致某些Slot闲置，可以动态分配任务量，可以充分利用多核CPU并发）。
- 因此所需Slot的最大数量就是任务最大并行度的值。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-b9102c31d88bb44d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 5.3 程序与数据流
&ensp;&ensp;所有的Flink程序都是由三部分组成的：  Source 、Transformation和Sink。
- Source负责读取数据源
- Transformation利用各种算子进行处理加工
- Sink负责输出。

&ensp;&ensp;&ensp;&ensp;在运行时，Flink上运行的程序会被映射成“逻辑数据流”（dataflows），它包含了这三部分。每一个dataflow以一个或多个sources开始以一个或多个sinks结束。dataflow类似于任意的有向无环图（DAG）。在大部分情况下，程序中的转换运算（transformations）跟dataflow中的算子（operator）是一一对应的关系，但有时候，一个transformation可能对应多个operator。

## 5.4 执行图
由Flink程序直接映射成的数据流图是StreamGraph，也被称为逻辑流图，因为它们表示的是计算逻辑的高级视图。为了执行一个流处理程序，Flink需要将逻辑流图转换为物理数据流图（也叫执行图），详细说明程序的执行方式。
Flink 中的执行图可以分成四层：StreamGraph -> JobGraph -> ExecutionGraph -> 物理执行图
- **StreamGraph：**是根据用户通过 Stream API 编写的代码生成的最初的图。用来表示程序的拓扑结构。
- **JobGraph：**StreamGraph经过优化后生成了 JobGraph，提交给 JobManager 的数据结构。主要的优化为，将多个符合条件的节点 chain 在一起作为一个节点，这样可以减少数据在节点之间流动所需要的序列化/反序列化/传输消耗。
- **ExecutionGraph：**JobManager 根据 JobGraph 生成ExecutionGraph。ExecutionGraph是JobGraph的并行化版本，是调度层最核心的数据结构。
- **物理执行图：**JobManager 根据 ExecutionGraph 对 Job 进行调度后，在各个TaskManager 上部署 Task 后形成的“图”，并不是一个具体的数据结构。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-27bd099dc3034eac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 5.5 并行度
在执行过程中，一个流（stream）包含一个或多个分区（stream partition），而每一个算子（operator）可以包含一个或多个子任务（operator subtask），这些子任务在不同的线程、不同的物理机或不同的容器中彼此互不依赖地执行。
**一个特定算子的子任务（subtask）的个数被称之为其并行度（parallelism）。**

**数据传输形式**
- one-to-one：map、filter、flatMap等算子符合one-to-one对应关系。这些算子的子任务得到的元素的个数和顺序跟source算子的子任务生产的元素的个数、顺序相同(类似于spark中的窄依赖);
- redistributing：如果前后任务并行度不同，会采用round-robin重新分区；如果是keyBy等类似shuffle的宽依赖操作算子，会进行hashCode重分区；而broadcast和rebalance会随机重分区(类似于spark中的宽依赖);
- local forward(本地转发)：flink采用了任务链优化技术，采用**one-to-one操作**且设置算子的**并行度相同**，可以实现本地转发进行任务连接。这样数据在本地进行流转，减少了序列化和网络传输的花销。

## 5.6 任务链拆分和Slot独占
**相同并行度的one to one操作，**flink会自动优化任务链合并多个任务为一个任务。将算子链接成task是非常有效的优化：它能减少线程之间的切换和基于缓存区的数据交换，在减少时延的同时提升吞吐量。
- 如果某个算子任务特别复杂需要单独拆出来，可以在算子后面设置`.disableChaining()`，这样这个任务就不会被合并；
- 如果想把合并的任务拆分为两个任务，可以在需要拆分的算子后添加`.startNewChain()`。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-ab3f5266b8ca6b54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 5.7 共享组
可以将不同的任务分配到指定的共享组内。只有在同一组的算子任务会共享Slot，不同组的任务不会存在同一个Slot中。这样需要重新计算需要的Slot的数量。
- 如拆分出来的算子任务如果想独占一个Slot，可以在算子后面添加`.slotSharingGroup("a")`。



<br>
#六、时间语义和水位线
##6.1 时间概念
Event Time：事件创建时间
Ingestion Time：数据进入Flink的时间
Processing Time：执行操作算子的本地系统时间，与机器相关

##6.2 设置时间语义
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
如果不设置，默认是Processing Time语义。

##6.3 水位线
###6.3.1 概念
水位线用于标记当前任务的时间，被水位线没过的时间窗口才会触发执行。当前水位线是到达的最大事件时间戳减去设置的延迟时间。
###6.3.2 水位线上下游传递
任务会记录所有上游任务传递的水位线，并取最低的水位线传递给下游的任务。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-f91adaa3ac5cd253.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当前事件时间-水位线延迟时间=水位线
水位线-窗口允许延迟时间=窗口关闭时间
**注意点：**
- 1.如果水位线没过窗口，那么会对窗口进行计算但不关闭，延迟数据进入后会重复触发窗口的计算，直到到达窗口关闭时间。
- 2.如果迟到数据属于多个窗口，每个窗口都会进行计算。
- 3.只有当迟到数据不属于任何一个窗口时，才会进入侧输出流。


**水位线生成逻辑：**
①
new BoundedOutOfOrdernessTimestampExtractor[ModelLogQ6](Time.seconds(5)) {
        override def extractTimestamp(element: ModelLogQ6): Long = element.timestamp
}
如上对象为周期性生成watermark逻辑，默认为每隔200ms生成一个。
```
// 手动设置时间间隔为1s
env.getConfig().setAutoWatermarkInterval(1000);
```
②
new AssignerWithPunctuatedWatermarks[ModelLogQ6] {
        override def checkAndGetNextWatermark(lastElement: ModelLogQ6, extractedTimestamp: Long): Watermark = ???

        override def extractTimestamp(element: ModelLogQ6, recordTimestamp: Long): Long = ???
}
每条数据到达都可以生成一个watermark。


<br>
#七、Flink中的状态
![image.png](https://upload-images.jianshu.io/upload_images/21580557-11724610a4219b13.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

算子状态（Operator state）

键控状态（keyed state）

##7.2 状态后端
MemoryStateBackend：将键控状态存储在taskManager的JVM堆上，checkpoint存储在JobManager的内存中。一般测试时使用。
FsStateBackend：键控状态存储在TaskManager的JVM堆上，而将checkPoint存储在dfs上。Flink默认的配置。
RocksDBStateBackend：所有状态序列化后存储到本地RocksDB中。

##7.3 一致性检查点checkpoint
![image.png](https://upload-images.jianshu.io/upload_images/21580557-5d5ab9fc6625bc3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**checkpoint策略配置**
env.enableCheckpointing(1000L) // 设置checkpoint的间隔时间
env.getCheckpointConfig.setCheckpointingMode(CheckpointingMode.AT_LEAST_ONCE) //设置checkpoint的模式
env.getCheckpointConfig.setCheckpointTimeout(60000L) //设置checkpoint的超时时间
env.getCheckpointConfig.setMaxConcurrentCheckpoints(2) //允许最多两个checkpoint同时执行
env.getCheckpointconfig.setMinPauseBetweenCheckpoints(500L) //保证两次checkpoint之间至少有500ms的间隔时间
env.getCheckpointconfig.setPreferCheckpointForRecovery(true) //是否直接使用checkpoint进行故障恢复。默认是false，表示如果savepoint更近，则会使用savepoint进行恢复
env.getCheckpointconfig.setTolerableCheckpointFailureNumber(0) // 能容忍多少次的checkpoint失败。如果是0，则checkpoint失败会导致任务失败，进行重启。

**重启策略配置**
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(3,10000L)) // 固定时间间隔尝试的重启次数。
env.setRestartStrategy(RestartStrategies.failureRateRestart(3,Time.of(5,TimeUnit.MINUTES)，Time.of(10,TimeUnit.SECONDS))) // 在固定时间内间隔多少时间重启多少次


##7.4 保存点savepoints
原理同checkpoint，但是需要手动触发savepoint操作。
可以用于手动备份、更新应用程序、版本迁移、暂停和重启应用。
最好在程序中定义这个任务的uid(.uid("1"))，这样可以清楚找到任务对应的savepoint。

##7.5 状态一致性
AT-MOST-ONCE 最多一次
AT-LEASE-ONCE 至少一次
EXACTLY-ONCE 精确一次

- 内部保证 —— checkpoint
- source端 —— 可重设数据的读取位置
- sink端 —— 从故障恢复时，数据不会重复写入外部系统

##7.6 端到端一致性
###7.6.1幂等写入**


###7.6.2事务写入
**概念：**
- 预写日志WAL：将结果先进行保存，收到checkpoint完成通知后一次性写入到sink中。优点是简单；缺点是延迟变大而且可能会丢数据。

- 两阶段提交2PC：每个checkpoint，sink任务会启动一个事务，将接下来所有接收的数据添加到事务中。然后将数据写入到外部sink系统，但不提交（预提交），当收到checkpoint完成通知后才正式提交事务。**Flink提供了TwoPhaseCommitSinkFunction接口**。优点：实现exactly-once；缺点：需要提供事务支持的外部sink系统，而且可以在进程失败后恢复事务。如果sink超时关闭也会导致预提交的数据丢失。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-a2290161e0364dc5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**Kafka中的两阶段提交**
source消费Kafka数据，在checkpoint点插入barrier并记录offset到状态后端，sink会开启事务对到达的数据进行预提交。当barrier到达sink时，会开启一个新的事务对后续的数据进行预提交，直到barrier到达所有的sink，完成checkpoint后JobManager会通知Kafka进行正式提交关闭事务。
注意：1.Kafka隔离级别设置为read-commit；2.Kafka超时时间默认为15m，flink默认的checkpoint超时时间为1h。设置checkpoint超时间小于Kafka。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-22921057ee118e15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#八、Table API 和 FLink SQL
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7b049269115c4a30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/21580557-0834650b30e8f3d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-ab2be78f74813b38.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**依赖**
```xml
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-table-planner-blink_2.12</artifactId>
            <version>1.10.1</version>
        </dependency>
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-table-api-scala-bridge_2.12</artifactId>
            <version>1.10.1</version>
        </dependency>
        <!-- 引入格式描述器FormatDescriptor，适配Kafka -->
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-csv</artifactId>
            <version>1.10.1</version>
        </dependency>
```

**简单使用**
```scala
object TableApiTest {
  def main(args: Array[String]): Unit = {
    // 1. 创建环境
    val env: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)

    val tableEnv = StreamTableEnvironment.create(env)

    // 1.1 基于老版本planner的流处理
    val oldStreamSettings = EnvironmentSettings.newInstance()
      .useOldPlanner()
      .inStreamingMode()
      .build()
    val oldStreamTableEnv = StreamTableEnvironment.create(env, oldStreamSettings)

    // 1.2 基于老版本planner的批处理
    val batchEnv = ExecutionEnvironment.getExecutionEnvironment
    val oldBatchTableEnv = BatchTableEnvironment.create(batchEnv)

    // 1.3 基于blink planner的流处理
    val blinkStreamSettings = EnvironmentSettings.newInstance()
      .useBlinkPlanner()
      .inStreamingMode()
      .build()
    val blinkStreamEnv = StreamTableEnvironment.create(env, blinkStreamSettings)

    // 1.4 基于blink planner的批处理
    val blinkBatchSettings = EnvironmentSettings.newInstance()
      .useBlinkPlanner()
      .inBatchMode()
      .build()
    val blinkBatchEnv = TableEnvironment.create(blinkBatchSettings)


    // 2. 连接外部系统，读取数据，注册表
    // 2.1 读取文件,进行表注册并读取数据
    val path = "C:\\Users\\Administrator\\Desktop\\不常用的项目\\flink_demo\\src\\main\\resources\\test.txt";

    tableEnv.connect(new FileSystem().path(path))
      .withFormat(new Csv())
      .withSchema(new Schema()
        .field("name", DataTypes.STRING())
        .field("age", DataTypes.INT())
      )
      .createTemporaryTable("fileInputTable")

    val fileInputTable: Table = tableEnv.from("fileInputTable")
    fileInputTable.toAppendStream[(String,Int)].print()


    // 2.2 从Kafka读取数据，进行表注册并读取数据
    tableEnv
      .connect(new Kafka()
        .version("0.11")
        .topic("sensor")
        .property("zookeeper.connect", "192.168.32.242:2181")
        .property("bootstrap.servers", "192.168.32.242:9092")
      )
      .withFormat(new Csv())
      .withSchema(new Schema()
        .field("name", DataTypes.STRING())
        .field("age", DataTypes.INT())
      )
      .createTemporaryTable("kafkaInputTable")

    val kafkaInputTable = tableEnv.from("kafkaInputTable")
    kafkaInputTable.toAppendStream[(String,Int)].print()

    env.execute("table api test")
  }
}
```

表是由一个“标识符”来指定，由3部分组成：Catalog名、数据库（database）名和表名。
表包括常规表和视图View。

**两种连接外部数据库的方式**

![通过sql语句](https://upload-images.jianshu.io/upload_images/21580557-2894d9f5691d16ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![通过API](https://upload-images.jianshu.io/upload_images/21580557-bd84f58a97bf9927.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
