# 一、消息确认机制
## 1.1 概念
**保证消息不丢失，可靠抵达，可以使用的方式如下**
- 使用事务消息：通过事务保证消息不丢失，但是性能下降250倍
- **确认机制：**①`publisher： confirmCallback 确认模式  `②`publisher： returnCallback 为投递到queue退回模式 `③`consumer： ack机制`![image.png](https://upload-images.jianshu.io/upload_images/21580557-a8c63c5d4b8dbeb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<br>
## 1.2. 具体实现
### 2.1 从publisher到exchange
**原理：**消息只要被broker接受就会执行confirmCallback，如果是cluster模式，需要所有的broker接受到才会调用confirmCallback。

**yml配置**
```yml
spring.rabbitmq.publisher-confirm-type=correlated
```

**收信后回调操作：**
```
    /**
     * 设置消息接受的回调方法
     */
    @PostConstruct
    public void initRabbitTemplate() {

        rabbitTemplate.setConfirmCallback(new RabbitTemplate.ConfirmCallback() {
            /**
             * 设置消息抵达exchange的回调方法
             * @param correlationData 当前消息的唯一关联数据(消息的唯一id)
             * @param ack 消息是否成功收到
             * @param cause 失败的原因
             */
            @Override
            public void confirm(CorrelationData correlationData, boolean ack, String cause) {
                System.out.println("confirm...correlationData[" + correlationData + "]==>ack[" + ack + "]");
            }
        });

    }
```
>CorrelationData：用来表示当前消息的唯一性，可以在发送消息时进行设置 `rabbitTemplate.convertAndSend("test-exchange", "test.java", car, new CorrelationData(UUID.randomUUID().toString()));`

### 2.2 从exchange到queue
**原理：**我们要保证exchange中的消息要投递到目标queue中，需要开启return退回模式。

**yml配置**
```yml
spring.rabbitmq.publisher-returns=true
spring.rabbitmq.template.mandatory=true
```

**exchange发送到queue失败后回调操作：**
```
    /**
     * 设置消息接受的回调方法
     */
    @PostConstruct
    public void initRabbitTemplate() {

        rabbitTemplate.setReturnCallback(new RabbitTemplate.ReturnCallback() {
            /**
             * 只要消息没有投递给指定的队列，就触发这个失败回调
             * @param message 投递失败的消息
             * @param replyCode 回复的状态码
             * @param replyText 回复的文本内容
             * @param exchange 这个消息发送给那个交换机
             * @param routingKey 消息使用的是哪个路由键
             */
            @Override
            public void returnedMessage(Message message, int replyCode, String replyText, String exchange, String routingKey) {
                System.out.println("Fail Message[" + message + "]-->replyCode[" + replyCode + "]-->replyText[" + replyText + "]-->exchange[" + exchange + "]-->routingKey[" + routingKey + "]");
            }
        });

    }
```
- 可以在回调方法中将发送失败的信息存储到MySQL中

### 2.3 从queue到consumer
**原理：**
消费者获取到消息，成功处理，可以回复Ack给Broker
- basic.ack用于肯定回复；broker将移除此消息
- basic.nack用于否定回复；可以指定broker是否丢弃消息，可以批量
- basic.reject用于否定回复；同上，但不能批量

默认情况下Broker的消息发送给queue后会自动Ack，删除该消息。但是如果无法确定此消息是否被处理完成或成功处理。我们可以手动开启ack模式：
- 消息处理成功，ack()，接受下一个消息，broker删除该消息
- 消息处理失败，nack()/reject()，重新发送给其他人进行处理，或者容错后ack
- 消息一直没有调用ack/nack方法，broker认为此消息被其他consumer处理，不会投递给别人，此时consumer断开，消息不会被broker删除，会投递给别人。

**配置**
```yml
spring.rabbitmq.listener.simple.acknowledge-mode=manual
```

<br>
# 二、延时队列和死信队列
## 2.1 延时队列
**消息的TTL(Time To Live)**
消息的TTL就是消息的存活时间。RabbitMQ可以对队列和消息分别设置TTL。
- 对队列设置TTL：队列没有消费者连接的过期时间。
- 对消息设置TTL：超时后该消息就是死信。

如果队列和消息都设置了TTL，那么会取最小的。通过设置消息的`expiration`字段或者`x-message-ttl`属性来设置时间，两者效果相同。


<br>
## 2.2 死信队列
**死信情况包括如下三种：**
- 消息被consumer拒收(unack或reject)且requeue是false；
- 消息TTL超时未消费；
- 队列长度满了，排在前面的消息会被丢弃或发送到死信exchange中。
- 超过最大重试次数

**DLE(Dead Letter Exchange)**
死信exchange是一种普通的exchange，只是所有的死信都会自动从队列中发送到该exchange中。

<br>
## 2.3 应用场景
**场景：**比如未支付订单，超时一定时间后，系统自动取消订单并释放占有的物品。

**解决方案：**
- Spring的schedule定时或xxl中间件定时任务：消耗系统内存、增加数据库压力、存在较大的时间误差；
- RabbitMQ的`消息TTL和死信Exchange`结合

如果订单超时时间为1小时，即为消息设置1小时的TTL时间且为队列设置DLE和死信路由键，消息超时过期后发送到DLE，根据死信路由键路由到死信队列中，从死信队列中获得的消息就是超时订单。

**实现一：**
给队列中的所有消息设定TTL时间，到达队列的时间时开始计时。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-2562794805919995.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
```
        // 创建信息过期时间为1m的队列
        HashMap<String, Object> arguments = new HashMap<>();
        arguments.put("x-dead-letter-exchange", "order-event-exchange"); // 指定死信交换机的名字
        arguments.put("x-dead-letter-routing-key", "order.release.order"); // 指定死信的路由键
        arguments.put("x-message-ttl", 10000); // TTL时间设为1m
        Queue delayQueue = new Queue("order.delay.queue", true, false, false, arguments);
        amqpAdmin.declareQueue(delayQueue);
```

**实现二：**
给发布者发送的每条消息设施TTL时间，缺点是前一个过期处理之后才会处理后续的过期数据，存在过期数据处理不及时的情况。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-8b96f18eedc3f489.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
```
    @Test
    public void sendOrderCreate() {
        MessagePostProcessor messagePostProcessor = new MessagePostProcessor() {
            @Override
            public Message postProcessMessage(Message message) throws AmqpException {
                message.getMessageProperties().setExpiration("60000");
                message.getMessageProperties().setContentEncoding("UTF-8");
                return message;
            }
        };
        Order book = new Order(1, "book");
        rabbitTemplate.convertAndSend("order-event-exchange", "order.create.order", book, messagePostProcessor, new CorrelationData(UUID.randomUUID().toString()));
    }
```

注意点：如果创建队列成功后，代码中修改队列的属性，是不会覆盖原有属性的，需要删除后再次创建队列。

## 2.4 实现
### 2.4.1 流程
①定义交换机(普通信息和死信共用)、延时队列(参数指定死信交换器、死信路由和延时时间)和死信队列。
②绑定交换器和延时队列与死信队列。
③发送消息到交换机，路由到延时队列。
④不消费延时队列信息，信息过期后发送到死信交换器，交换器通过死信路由发送到死信队列。
⑤消费死信队列获得死信信息。

### 2.4.2 代码
**依赖**
```
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-amqp</artifactId>
        </dependency>
```
**配置类**
```
@Configuration
public class RabbitMqConfig {

    @Resource
    private AmqpAdmin amqpAdmin;

    @Resource
    private RabbitTemplate rabbitTemplate;

    /**
     * 注入并使用指定的消息转换器(将序列化传输转变为json传输)
     *
     * @return
     */
//    @Bean
//    public Jackson2JsonMessageConverter converter(){
//        return new Jackson2JsonMessageConverter();
//    }

    /**
     * 设置消息接受的回调方法
     */
    @PostConstruct
    public void initRabbitTemplate() {
        rabbitTemplate.setConfirmCallback(new RabbitTemplate.ConfirmCallback() {
            /**
             * 设置消息抵达exchange的回调方法
             * @param correlationData 当前消息的唯一关联数据(消息的唯一id)
             * @param ack 消息是否成功收到
             * @param cause 失败的原因
             */
            @Override
            public void confirm(CorrelationData correlationData, boolean ack, String cause) {
                System.out.println("confirm...correlationData[" + correlationData + "]==>ack[" + ack + "]");
            }
        });

        rabbitTemplate.setReturnCallback(new RabbitTemplate.ReturnCallback() {
            /**
             * 只要消息没有投递给指定的队列，就触发这个失败回调
             * @param message 投递失败的消息
             * @param replyCode 回复的状态码
             * @param replyText 回复的文本内容
             * @param exchange 这个消息发送给那个交换机
             * @param routingKey 消息使用的是哪个路由键
             */
            @Override
            public void returnedMessage(Message message, int replyCode, String replyText, String exchange, String routingKey) {
                System.out.println("Fail Message[" + message + "]-->replyCode[" + replyCode + "]-->replyText[" + replyText + "]-->exchange[" + exchange + "]-->routingKey[" + routingKey + "]");
            }
        });
    }


    /**
     * 定义交换机，参数说明
     * 1. name 交换机名称
     * 2. durable 是否持久化，如果持久化，mq重启后交换机还在
     * 3. autoDelete 自动删除，交换机没有绑定队列则删除，如果将此参数和exclusive参数设置为true就可以实现临时队列（队列不用了就自动删除）
     * 4. arguments 参数，可以设置一个队列的扩展参数，比如设置存活时间
     */
    @PostConstruct
    public void createExchange() {
        // 创建交换机(同时作为订单信息交换机和死信交换机)
        DirectExchange directExchange = new DirectExchange("order-event-exchange", true, false);
        amqpAdmin.declareExchange(directExchange);
    }

    /**
     * 定义队列，参数说明
     * 1. queue 队列名称
     * 2. durable 是否持久化，如果持久化，mq重启后队列还在
     * 3. exclusive 是否独占连接，队列只允许在该连接中访问，如果连接关闭队列自动删除（如果将此参数设置true可用于临时队列的创建）
     * 4. autoDelete 自动删除，队列不再使用时是否自动删除此队列，如果将此参数和exclusive参数设置为true就可以实现临时队列（队列不用了就自动删除）
     * 5. arguments 参数，可以设置一个队列的扩展参数，比如设置存活时间
     */
    @PostConstruct
    public void createQueue() {
        // 创建信息过期时间为1m的队列
        HashMap<String, Object> arguments = new HashMap<>();
        arguments.put("x-dead-letter-exchange", "order-event-exchange"); // 指定死信交换机的名字
        arguments.put("x-dead-letter-routing-key", "order.release.order"); // 指定死信的路由键
        arguments.put("x-message-ttl", 10000); // TTL时间设为1m
        Queue delayQueue = new Queue("order.delay.queue", true, false, false, arguments);
        amqpAdmin.declareQueue(delayQueue);

        // 创建死信队列
        Queue releaseQueue = new Queue("order.release.order.queue", true, false, false);
        amqpAdmin.declareQueue(releaseQueue);
    }

    /**
     * 定义队列，参数说明
     * 1. destination 绑定的队列或者交换机的名字
     * 2. destinationType 需要绑定的类型
     * 3. exchange 交换机的名字
     * 4. routingKey 路由键
     * 5. arguments 参数，可以设置一个队列的扩展参数
     */
    @PostConstruct
    public void createBinding() {
        // 交换机order-event-exchange与订单创建队列order.delay.queue绑定，路由键为order.create.order
        Binding createBinding = new Binding("order.delay.queue", Binding.DestinationType.QUEUE, "order-event-exchange", "order.create.order", null);
        amqpAdmin.declareBinding(createBinding);

        // 交换机order-event-exchange与死信队列order.release.order.queue绑定，路由键为order.release.order
        Binding releaseBinding = new Binding("order.release.order.queue", Binding.DestinationType.QUEUE, "order-event-exchange", "order.release.order", null);
        amqpAdmin.declareBinding(releaseBinding);
    }

}
```
**监听死信队列**
```
@Service
public class RabbitListenerService {

    @RabbitListener(queues = "order.release.order.queue")
    public void consumer1(Message message, Order order, Channel channel) throws IOException {
        System.out.println(order);

        long deliveryTag = message.getMessageProperties().getDeliveryTag();
        channel.basicAck(deliveryTag,false);
    }

}
```
**发送信息**
```
    @Test
    public void sendOrderCreate() {
        Order book = new Order(1, "book");
        rabbitTemplate.convertAndSend("order-event-exchange", "order.create.order",book, new CorrelationData(UUID.randomUUID().toString()));
    }
```

<br>
# 三、 硬件
![image.png](https://upload-images.jianshu.io/upload_images/21580557-c2545bf4e71220a6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 3.1 内存
默认如果rabbitmq使用超过物理内存的40%，会报警并阻塞所有队列。
可以通过配置文件或输入命令来改变默认的配置
命令方式：
1. 如果使用内存超过90MB则报警：rabbitmqctl set_vm_memory_high_watermark absolute 90MB
2. 如果使用内存超过物理内存的40%则报警：rabbitmqctl set_vm_memory_high_watermark 0.4

## 3.2 磁盘
磁盘剩余空间低于阈值时，同样会阻塞生产者，避免因非持久化的消息持续换页导致服务器磁盘耗尽而崩溃。
1. 如果磁盘空间剩余小于100GB则报警：`rabbitmqctl set_disk_free_limit 100GB`
2. 如果磁盘空间剩余小于内存的1.5倍，则报警：`rabbitmqctl set_disk_free_limit memory_limit 1.5`

## 3.3 内存换页
在某个broker节点及内存阻塞生产者之前，它会尝试将队列中的消息换页到磁盘以释放内存空间，持久化和非持久化的消息都会写入到磁盘中，其中持久化的消息本身就在磁盘胡中有一个副本，所以在转移过程中持久化的消息会先从内存中清除掉。
>默认情况下，内存到达的阈值是50%时进行换页，即在默认情况下物理内存使用超过0.4*0.5=0.2时，进行换页。
可以通过设置`vm_memory_high_watermark_paging_ratio`进行调整。


[官网配置](https://www.rabbitmq.com/configure.html)

<br>
# 四、附
####常用配置
```yml
spring:
  rabbitmq:
    host: 192.168.32.207
    port: 5672
    # addresses: 192.168.32.207:5672,... # 配置集群的地址
    username: guest
    password: guest
    virtual-host: /transaction_demo
    publisher-confirm-type: correlated
    publisher-returns: true
    template:
      mandatory: true
    listener:
      simple:
        acknowledge-mode: manual
        #retry:
          #enabled: true # 开启重试
          #max-attempts: 10 # 最大重试次数
          #initial-interval: 2000m # 重试间隔时间
```
消费者retry重试消费消息后要放入死信队列，就不能将acknowledge-mode设为manual，否则消息一直是unack状态。

####完整配置
```yml
spring:
  rabbitmq:
    host: 192.168.32.207
    # addresses: # 配置集群的地址
    port: 5672
    username: guest
    password: guest
    virtual-host: /transaction_demo
    publisher-confirm-type: correlated
    publisher-returns: true
    requested-heartbeat: # 指定心态超时，单位秒，0为不指定：默认60s
    connection-timeout: # 连接超时，单位毫秒，0表示无穷大，不超时
    cache:
      channel:
        size: # 缓存中保存的channel数量
        checkout-timeout: # 当缓存数量被设置时，从缓存中获取一个channel的超时时间，单位毫秒；如果为0，则总是创新一个新channel
      connection:
        size: # 缓存的链接数，只有是CONNECTION模式时生效
        mode: # 连接工厂缓存模式：CHANNEL和CONNECTION
    template:
      mandatory: true
      receive-timeout: # receive()操作的超时时间
      reply-timeout: # sendAndReceive()操作的超时时间
      retry:
        enabled: # 发送重试是否可用
        max-attempts: #最大重试次数
        initial-interval: # 第一次和第二次尝试发布或传递消息之间的间隔
        multiplier: # 应用于上一重试间隔的乘数
        max-interval: # 最大重试时间间隔
    listener:
      simple:
        acknowledge-mode: manual
        retry:
          enabled: true # 开启重试
          max-attempts: 10 # 最大重试次数
          initial-interval: 2000ms # 重试间隔时间
          multiplier: # 应用于上一重试间隔的乘数
          max-interval: # 最大重试时间间隔
          stateless: # 重试是有状态or无状态
        auto-startup: # 是否启动时自动启动容器
        concurrency: # 最小的消费者数量
        max-concurrency: # 最大的消费者数量
        prefetch: # 指定一个请求能处理多少个消息，如果有事务的话，必须大于等于transaction数量
        transaction-size: # 指定一个事务处理的消息数量，最好小于等于prefetch的数量
        default-requeue-rejected: # 决定被拒绝的消息是否重新入队，默认是true(与参数acknowledge-mode有关系)
        idle-event-interval: # 多少长时间发布空闲容器时间，单位毫秒
```

<br>
#### 面试题
RabbitMQ为什么需要信道，为什么不是TCP直接通信：
1. TCP的创建和销毁开销大，创建要三次握手，销毁要四次分手。每个线程都开一个TCP连接，造成底层操作系统处理繁忙；
2. 信道的原理是一条线程一个信道，多条线程多条信道同用一条TCP连接，一条TCP连接可以容纳无限的信道，即使每秒成千上万的请求也不会成为性能瓶颈。

<br>
# 五、RabbitMQ集群搭建

`......待续`
