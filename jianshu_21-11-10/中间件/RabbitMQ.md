#一、概念
## 2.1 架构图
![image.png](https://upload-images.jianshu.io/upload_images/21580557-92f1c3a96682e8b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Broker：消息队列服务进程，包括Exchange和Queue。
Exchange：消息队列交换机，按一定的规则将消息路由转发到某个队列，对消息进行过滤。
Queue：消息队列，存储消息的队列，消息达到队列并转发给指定的消费方。

**核心概念**
Server：又称broker，接收客户端的连接，实现AMQP实体服务。安装rabbitmq-server。
Connection：连接，应用程序与Broker的网络连接TCP/IP 三次握手和四次挥手。
Channel：网络信道，几乎所有的操作都在Channel中进行，Channel是进行消息读写的通道，客户端可以建立多个Channel，每个Channel代表一个会话任务。
Message消息：服务与应用程序之间传送的数据，由Properties和body组成，Properties可以对消息进行修饰，比如消息的优先级，延迟等高级特性，Body则就是消息体的内容。
Virtual Host：虚拟地址，用于逻辑隔离，最上层的消息路由，一个虚拟主机可以有若干个Exchange和Queue，同一个虚拟主机里面不能有相同名字的Exchange。

**面试题：**
RabbitMQ为什么需要信道，为什么不是TCP直接通信：
1. TCP的创建和销毁开销大，创建要三次握手，销毁要四次分手。每个线程都开一个TCP连接，造成底层操作系统处理繁忙；
2. 信道的原理是一条线程一个信道，多条线程多条信道同用一条TCP连接，一条TCP连接可以容纳无限的信道，即使每秒成千上万的请求也不会成为性能瓶颈。


<br>
## 2.2 流程
---发送消息---
1. 生产者和Broker建立TCP连接；
2. 生产者和Broker建立通道；
3. 生产者通过通道将消息发送到Broker，由Exchange将消息进行转发；
4. Exchange将消息转发到指定的Queue（队列）。

---接受消息---
1. 消费者和Broker建立TCP连接；
2. 消费者和Broker建立通道；
3. 消费者监听指定的Queue；
4. 当有消息到达Queue时Broker默认将消息推送给消费者；
5. 消费者收到消息


## 2.3 6种工作模式
首先介绍交换机类型
- 1. 默认模式：对应工作队列模式，使用默认的交换机。
- 2. fanout：对应的Publish/Subscribe工作模式
- 3. direct：对应的Routing工作模式
- 4. topic：对应的Topic工作模式
- 5. headers：对应的headers工作模式

`不同的工作模式主要是exchange模式不同的来实现的。`

### 2.3.6.1 Work queues 工作队列模式
![工作队列模式](https://upload-images.jianshu.io/upload_images/21580557-584457470b03101f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**工作原理：**一个生产者将消息发送给一个队列（会有一个默认的交换机），多个消费者共同监听一个队列消息。消息不能重复消费，采用轮询方式进行消费。
**作用：**用于一个消费者出来不过来的情况，负载均衡。

### 2.3.6.2. Publish/subscribe 发布订阅模式
![发布订阅模式](https://upload-images.jianshu.io/upload_images/21580557-2bcb64b0a66ee724.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**工作原理：**一个生产者将消息发送给交换机，与交换机绑定的多个队列，每个消费者监听自己的队列。生产者将消息发送给交换机，由交换机将消息发送到绑定此交换机的每个队列，每个绑定的交换机队列都将接受到消息。
**作用：**多个消费者都需要接收到同一条消息。同时可以让多个消费者监听同一个队列，实现负载均衡。
```java
// 定义交换机，模式为FANOUT
channel.exchangeDeclare(EXCHANGE_NAME,BuiltinExchangeType.FANOUT);
// 交换机绑定队列，发布订阅模式将路由键设为空串。
channel.queueBind(QUEUE_NAME1,EXCHANGE_NAME,"");
channel.queueBind(QUEUE_NAME2,EXCHANGE_NAME,"");
// 将路由键设为空串，会发送到所有的绑定队列
channel.basicPublish(EXCHANGE_NAME,"",NULL,message.getBytes());
```

### 2.3.6.3. Routing  路由模式
![路由模式](https://upload-images.jianshu.io/upload_images/21580557-1732cfd27e3c45af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**工作原理：**一个交换机绑定多个队列，每个队列设置routingkey，并且一个队列可以设置多个routingKey。
每个消费者监听自己的队列。
生产者将消息发送给交换机，发送消息时需要指定routingKey的值，交换机来判断该routingKey的值和哪个队列的routingKey相等，如果相等则将消息转发给该队列。
**作用：**将消息根据路由发送到指定的队列中。可以发送到多个队列中，因此可以实现发布订阅模式功能。
```java
// 定义交换机，模式为DIRECT
channel.exchangeDeclare(EXCHANGE_NAME,BuiltinExchangeType.DIRECT);
// 交换机绑定队列，路由模式定义路由键。此处为一个队列设置了两个路由键
channel.queueBind(QUEUE_NAME1,EXCHANGE_NAME,"info");
channel.queueBind(QUEUE_NAME2,EXCHANGE_NAME,"info");
channel.queueBind(QUEUE_NAME2,EXCHANGE_NAME,"info");
// 设置消息的路由键，消息会发送到相同路由的队列
channel.basicPublish(EXCHANGE_NAME,"info",null,message.getBytes());
```

### 2.3.6.4. Topics  通配符模式
![通配符模式](https://upload-images.jianshu.io/upload_images/21580557-c3fc9202ebb25d61.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**工作原理**：一个交换机可以绑定多个队列，每个队列可以设置一个或多个带通配符的routingKey。根据路由键进行匹配发送到队列。
与路由模式不同的时路由的匹配方式，路由模式时相等匹配，topics模式是通配符匹配。
>符号#：匹配任意个词，如inform.#可以匹配inform、inform.sms和inform.email.sms；
符号*：只能匹配一个词，如inform.#可以匹配inform.sms。

### 2.3.6.5. Header  Header转发器
**工作原理**：header模式与路由模式不同的是，header模式取消routingkey，使用header中的key/value匹配队列。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-e33d77670b2c4324.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 2.3.6.6. RPC  远程过程调用
![image.png](https://upload-images.jianshu.io/upload_images/21580557-b8a91c772590038f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

RPC即客户端调用服务端的方法，使用MQ可以实现RPC的异步调用，基于Direct交换机实现。
1. 客户端即是生产者又是消费者，向RPC请求队列发送RPC调用消息，同时监听RPC响应队列；
2. 服务端监听RPC请求队列的消息，收到消息后执行服务端的方法，得到方法返回的结果；
3. 服务端将RPC方法的结果发送到RPC相应队列。


<br>
#二、代码
## 2.1 使用原生
**依赖**
```
        <dependency>
            <groupId>com.rabbitmq</groupId>
            <artifactId>amqp-client</artifactId>
            <version>5.9.0</version>
        </dependency>
```
**Provider**
```java
public class Provider {

    private static final String QUEUE = "mcook.bigdata.mac_iotid";
    private static final String EXCHANGE = "";

    public static void main(String[] args) {
        // 添加到mq中，存储到数据库
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.32.244");
        connectionFactory.setPort(5672);
        connectionFactory.setUsername("guest");
        connectionFactory.setPassword("guest");

        Connection connection = null;
        Channel channel = null;
        try {
            connection = connectionFactory.newConnection();
            // 创建会话通道，生产者和mq服务所有通信都在channel通道中完成
            channel = connection.createChannel();
            /**
             * 定义队列，参数说明
             * 1. queue 队列名称
             * 2. durable 是否持久化，如果持久化，mq重启后队列还在
             * 3. exclusive 是否独占连接，队列只允许在该连接中访问，如果连接关闭队列自动删除（如果将此参数设置true可用于临时队列的创建）
             * 4. autoDelete 自动删除，队列不再使用时是否自动删除此队列，如果将此参数和exclusive参数设置为true就可以实现临时队列（队列不用了就自动删除）
             * 5. arguments 参数，可以设置一个队列的扩展参数，比如设置存活时间
             */
            channel.queueDeclare(QUEUE, true, false, false, null);
            /**
             * 发送消息，参数说明
             * 1. exchange，交换机，如果不指定将使用mq的默认交换机
             * 2. routingKey，路由key，交换机根据路由key来将消息转发到指定的队列，如果使用默认交换机，routingKey设置为队列名称
             * 3. props，消息的属性
             * 4. body，消息内容
             */
            channel.basicPublish(EXCHANGE, QUEUE, null, "hello_world".getBytes());
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (channel != null) {
                try {
                    channel.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            if(connection != null){
                try {
                    connection.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

}
```

**Consumer**
```java
public class Consumer {

    private static final String QUEUE = "mcook.bigdata.mac_iotid";
    private static final String EXCHANGE = "";

    public static void main(String[] args) {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("192.168.32.244");
        connectionFactory.setPort(5672);
        connectionFactory.setUsername("guest");
        connectionFactory.setPassword("guest");

        Connection connection = null;

        try {
            connection = connectionFactory.newConnection();
            Channel channel = connection.createChannel();

            channel.queueDeclare(QUEUE, true, false, false, null);

            DefaultConsumer defaultConsumer = new DefaultConsumer(channel){
                /**
                 * 当接受到消息后此方法被调用
                 * @param consumerTag  消费者标签，用来标识消费者，在监听队列时设置channel，basicCosume
                 * @param envelope  信封，通过envelope可以获取消息的id，用于确认消息已接收
                 * @param properties  参数，可以设置一个队列的扩展参数
                 * @param body
                 * @throws IOException
                 */
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                    // 交换机
                    String exchange = envelope.getExchange();
                    // 消息id，mq在channel中用来标识消息的id，可用于确认消息已接受
                    long deliveryTag = envelope.getDeliveryTag();
                    // 消息内容
                    String message = new String(body, "utf-8");
                    System.out.println(message);
                }
            };

            /**
             * 监听队列，参数说明String queue，boolean autoAck，Consumer callback
             * 1. queue 队列名称
             * 2. autoAck 自动回复，设置为true，发送后就删除消息；如果设置为false，需要编程手动确认删除，否则会一直存在
             * 3. callback 消费方法，当消费者收到消息后需要执行的方法
             */
            channel.basicConsume(QUEUE, true, defaultConsumer);
        } catch (Exception e) {
            if (connection != null) {
                try {
                    connection.close();
                } catch (IOException ioException) {
                    ioException.printStackTrace();
                }
            }
        }
        
    }
}
```

## 2.2 整合springboot
### 2.2.1 部分源码
1. 在spring-boot-autoconfigure中的spring.factories文件中包含RabbitAutoConfiguration类，引入amqp依赖后就会将RabbitAutoConfiguration类加载到容器中。
2. 在该类中会以RabbitProperties作为参数创建并注入工厂类CachingConnectionFactory的对象，我们在配置文件中的自定义配置会被封装到RabbitProperties对象中；
同时也会以RabbitProperties作为参数创建并注入RabbitTemplate对象，该对象用于发送消息；
还会以注入的RabbitAutoConfiguration对象作为参数创建并注入AmqpAdmin对象；
以注入的RabbitTemplate对象作为参数创建并注入RabbitMessagingTemplate对象。
3. 在创建RabbitTemplate对象时，会将容器中的MessageConverter对象作为参数，如果容器中的MessageConverter为空，即用户没有注入，就会使用初始赋值的SimpleMessageConverter转换器，源码如下。
```
// 解析：即如果是bytes数组，会直接传输bytes数组。如果是String会转换为bytes数组传输，如果是Serializable实现类会序列化后传输。
if (object instanceof byte[]) {
            bytes = (byte[])((byte[])object);
            messageProperties.setContentType("application/octet-stream");
        } else if (object instanceof String) {
            try {
                bytes = ((String)object).getBytes(this.defaultCharset);
            } catch (UnsupportedEncodingException var6) {
                throw new MessageConversionException("failed to convert to Message content", var6);
            }

            messageProperties.setContentType("text/plain");
            messageProperties.setContentEncoding(this.defaultCharset);
        } else if (object instanceof Serializable) {
            try {
                bytes = SerializationUtils.serialize(object);
            } catch (IllegalArgumentException var5) {
                throw new MessageConversionException("failed to convert to serialized Message content", var5);
            }

            messageProperties.setContentType("application/x-java-serialized-object");
        }
```
4. 在接收参数时可以直接使用传输对象类来接收。

### 2.2.2 实现
**注解**
@EnableRabbit   用于
@RabbitListener(queues = "updateBookmark")   用于监听队列
@RabbitHandler   用于监听方法的重载

**依赖**
```
<dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

**配置文件**
```yml
spring:
  rabbitmq:
    host: 192.168.32.207
    port: 5672
    username: guest
    password: guest
    virtual-host: /
    # 发送确认
    publisher-confirms: true
    # 发送回调
    publisher-returns: true
    # 消费手动确认
    listener:
      simple:
        acknowledge-mode: manual
```

**配置类**
```java
@Configuration
@EnableRabbit
public class RabbitMQConfig {

    /**
     * 交换器
     *
     * @return
     */
    @Bean
    TopicExchange exchange() {
        return new TopicExchange("smartcookExchange");
    }

    /**
     * 搜索历史队列
     */
    @Bean
    public Queue findSearchHistoryQueue() {
        return new Queue("findSearchHistory");
    }

    @Bean
    Binding bindingFindSearchHistory() {
        return BindingBuilder.bind(findSearchHistoryQueue()).to(exchange()).with("searchhistory.findSearchHistory");
    }

    @Bean
    public Queue addSearchHistoryQueue() {
        return new Queue("addSearchHistory");
    }   //添加到redis中

    @Bean
    Binding bindingAddSearchHistory() {
        return BindingBuilder.bind(addSearchHistoryQueue()).to(exchange()).with("searchhistory.addSearchHistory");
    }

    /**
     * elasticsearch队列
     */
    @Bean
    TopicExchange maxwellExchange(){
        return new TopicExchange("maxwell",false,false);
    }

    @Bean
    public Queue getFromMaxwell(){
        return new Queue("getFromMaxwell");
    }

    @Bean
    Binding bindingGetFromMaxwell(){
        return BindingBuilder.bind(getFromMaxwell()).to(maxwellExchange()).with("dev_smartcook.menu");
    }

}
```

**工具类**
用于对象和字节码的互转。
```java
public class BytesUtil {

    public static byte[] getBytesFromObject(Serializable obj) throws Exception {
        if (obj == null) {
            return null;
        }
        ByteArrayOutputStream bo = new ByteArrayOutputStream();
        ObjectOutputStream oo = new ObjectOutputStream(bo);
        oo.writeObject(obj);
        return bo.toByteArray();
    }

    public static Object getObjectFromBytes(byte[] objBytes) throws Exception {
        if (objBytes == null || objBytes.length == 0) {
            return null;
        }
        ByteArrayInputStream bi = new ByteArrayInputStream(objBytes);
        ObjectInputStream oi = new ObjectInputStream(bi);
        return oi.readObject();
    }

}
```
<br>
**逻辑代码**
```java
@Autowired
private RabbitTemplate rabbitTemplate;

@Override
public Result updateBookmark(String userId, Integer 
groupId, String name, Boolean deletable) {
    //业务代码 ......
    //发送消息到MQ
    byte[] bytesFromObject;
    try {
        bytesFromObject = BytesUtil.getBytesFromObject(bookmark);
    } catch (Exception e) {
        e.printStackTrace();
        throw new IllegalArgumentException("反序列化Bookmark对象失败");
    }
    rabbitTemplate.convertAndSend("smartcookExchange", "bookmark.updateBookmark", bytesFromObject);
    return new Result().ok();
}

@RabbitListener(queues = "updateBookmark")
public void updateBookmark2Redis(byte[] bytesFromObject, Channel channel, Message message) throws IOException {
    log.info("进入updateBookmark2Redis方法");
    Bookmark bookmark;
    try {
        bookmark = (Bookmark) BytesUtil.getObjectFromBytes(bytesFromObject);
    } catch (Exception e) {
        e.printStackTrace();
        throw new IllegalArgumentException("反序列化Bookmark对象失败");
    }
    String userId = bookmark.getUserId();
    Integer groupId = bookmark.getId();
    log.info("更新redis中的数据:" + bookmark);
//        redisTemplate.opsForHash().delete("bookmark:" + userId, groupId);
    redisTemplate.opsForHash().put("bookmark:" + userId, groupId, bookmark);

    channel.basicAck(message.getMessageProperties().getDeliveryTag(), false);
}
```

```
@RabbitListener(queues = "updateBookmark")
public class RabbitTest{
  
  @Autowired
  private RabbitTemplate rabbitTemplate;
  
  @Override
  public Result updateBookmark(String userId, Integer 
  groupId, String name, Boolean deletable) {
      //业务代码 ......
      //发送消息到MQ
      Teacher teacher = new Teacher(1,"zs",28);
      Student student = new Student(1,"ls",15);
      rabbitTemplate.convertAndSend("smartcookExchange", "bookmark.updateBookmark", teacher);
      rabbitTemplate.convertAndSend("smartcookExchange", "bookmark.updateBookmark", student);
      return new Result().ok();
  }
  
  @RabbitHandler
  public void updateBookmark2Redis(Message message, Student student, Channel channel) throws IOException {

      log.info("收到重载的Student对象:" + student);
      channel.basicAck(message.getMessageProperties().getDeliveryTag(), false);
  }

  @RabbitHandler
  public void updateBookmark2Redis(Message message, Teacher teacher, Channel channel) throws IOException {
      log.info("收到重载的Teacher 对象:" + teacher);
  
      channel.basicAck(message.getMessageProperties().getDeliveryTag(), false);
  }

}
```


## 注意点
1. 反序列化需要有无参构造器。
