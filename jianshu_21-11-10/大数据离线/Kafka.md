# 一、Kafka命令
## 1.1 启动命令
启动和关闭节点上的kafka服务，-daemon表示在后台启动
```
bin/kafka-server-start.sh -daemon config/server.properties
```
```
bin/kafka-server-stop.sh
```
>指定zookeeper，因为需要先在zk上创建节点，kafka controller监控目录下有新文件，会创建新的topic，进行分区和副本均衡，选举leader然后将信息发送到zk中，同时每个broker都会缓存在metadatacache文件中，即zk和每台服务器上都有topic元数据。

<br>
## 1.2 常用命令
- 查看所有的topic
  ```
  bin/kafka-topics.sh  --zookeeper bigdata1:2181  --list   
  ```

- 创建一个名为first，分区数为3，副本数为2的topic
  ```
  bin/kafka-topics.sh  --zookeeper bigdata1:2181  --create --topic first  --partitions 3  --replication-factor 2 
  ```

- 查看名为first的topic的具体参数
  ```
  bin/kafka-topics.sh  --zookeeper bigdata1:2181  --describe  --topic first 
  ```
  分别表示topic名、分区号、该分区leader所在的brokerid、副本号、副本所在brokerid、可以同步的副本所在的brokerid
  ![image.png](https://upload-images.jianshu.io/upload_images/21580557-a2a6a18a68f3e599.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 修改分区数或副本数（分区数只能增不能减，副本数可增可减）
  ```
  bin/kafka-topics.sh  --zookeeper bigdata1:2181  --alter  --topic first  --partitions 5
  ```
  在bigdata1的logs文件夹中可以查看该节点存储的副本文件first-n（n表示分区号）。分区0存储在broker0、1上，分区2存储在broker2、0上，分区3存储在broker0、2上、分区4存储在broker1、0上。综上，bigdata1存储了分区0、2、3、4的副本，与logs中的first副本文件对应。

  ![image.png](https://upload-images.jianshu.io/upload_images/21580557-983c29ad3b3f3b05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  ![image.png](https://upload-images.jianshu.io/upload_images/21580557-c702f58faa4f989c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 删除topic
  ```
  bin/kafka-topics.sh  --zookeeper bigdata1:2181  --delete  --topic first
  ```
  > 如果在server.properties中将 delete.topic.enable=true，那么删除时就会将原数据删除。否则只会删除zk上的节点，原数据不会删除。

- 生产数据到topic中
  ```
  bin/kafka-console-producer.sh --broker-list bigdata2:9092,bigdata3:9092  --topic first
  ```

- 从topic中读取数据
  ```
  bin/kafka-console-consumer.sh --bootstrap-server bigdata1:9092 --topic first [from-beginning]
  ```
  > 可以指定消费组的offset，默认是latest

- 展示当前正在消费的消费者组的信息
  ```
  bin/kafka-consumer-groups.sh  --bootstrap-server  bigdata1:9092   --list
  ```

  ![image.png](https://upload-images.jianshu.io/upload_images/21580557-39ac0df5c5c42d65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 监控某一消费者消费了哪些topic（一个消费者组可以消费多个topic）
  ```
  bin/kafka-consumer-groups.sh  --bootstrap-server hadoop102:9092  --describe  --group id
  ```
  ![image.png](https://upload-images.jianshu.io/upload_images/21580557-81f5eae33ccbb740.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  > 这两个脚本直接从服务器上获取元数据，得到leader的信息；底层也是调用生产者和消费者的api。


<br>
## 1.3 不常用命令
- 如新增了节点，需要重新分配分区，将数据均衡。资源消耗很大。
  ```
  reassign-partitions.sh  
  ```

- 每一个partition的leader的重新选举。
  ```
  preferred-replica-election.sh
  ```
  > 将leader分布在不同节点上，缓解压力。一台leader挂了，其他副本会成为leader，可能会在同一个broker有多个leader，原leader上线后变成follower，需要重新选举，将leader的分别变为均匀状态（这两个指令需要json格式的文件指定分配计划）。

<br>
## 1.4 压测
**压测写入**
```
./kafka-producer-perf-test.sh --topic test --num-records 1000000 --record-size 1000 --throughput -1 --producer-props bootstrap.servers=bigdata1:9092
```
>--num-records 总共需要发送的消息数，本例为1000000  
--record-size 每个记录的字节数，本例为1000  
--throughput 每秒钟发送的记录数，如果为-1，表示不限流。

**压测消费**
```
./kafka-consumer-perf-test.sh --zookeeper bigdata1:2181 --topic test --fetch-size 1048576 --messages 1000000 --threads 1
```
>--fetch-size 指定每次fetch的数据的大小，本例为1048576，也就是1M  
--messages 总共要消费的消息个数，本例为1000000，100w
