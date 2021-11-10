# 一、Seata介绍
全局的跨数据库的多数据源的统一调度。
微服务环境下，原来的多个模块被拆分为多个独立的应用，分别使用多个独立的数据源。因此每个服务内部的数据一致性由本地事务来保证，但是全局的数据一致性问题需要分布式事务来保证。
Seata在微服务架构下提供高性能的分布式事务服务。

## 1.1 Seata AT原理
### 1.1.1 概念梳理
**本地锁：**本地事务进行操作时添加的排它锁。
**全局锁：**本地提交需要先获取全局锁，提交之后释放全局锁。数据的修改将被互斥开来。也就不会造成写入脏数据。全局锁可以让分布式修改中的写数据隔离。

### 1.1.2 分布式事务的一ID+三组件模型
1. 全局唯一的事务ID：TransactionID XID
2. 三组件概念
- TC(Transaction Coordinator)：事务协调者，维护全局和分支事务的状态，驱动全局事务提交和回滚。
- TM(Transaction Manager)：事务管理器，定义全局事务的范围，开始全局事务、提交或回滚全局事务。
- RM(Resource Manager)：资源管理器，管理分支事务处理的资源，与TC交谈以注册分支事务和报告分支事务的状态，并驱动分支事务提交或回滚。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-bdcaa8e98bd5b7b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####步骤：
1. TM向TC申请开启一个全局事务，全局事务创建成功并生成一个全局唯一的XID；
2. XID在微服务调用链路的上下文中传播；
3. RM向TC注册分支事务，将其纳入XID对应的全局事务的管辖；
4. TM向TC发起针对XID的全局提交或回滚决议；
5. TC调度XID下管辖的全部分支事务完成提交或回滚请求。
- 全局事务提交：TM向TC发起全局事务提交请求，TC收到后，向各个分支事务发起提交请求，分支事务接收到请求，只需要删除全局事务的undo_log记录即可
- 全局事务回滚：TM向TC发起全局事务回滚请求，TC收到后，向各个分支事务发起回滚请求，分支事务接收到请求，只需要根据XID对应的undo_log表记录进行回滚即可。

####数据库表：
- **global_table表：**
TM 向 TC 请求发起（Begin）、提交（Commit）、回滚（Rollback）全局事务，注册并获取xid。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-af5d1d3396a17cd1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- **branch_table表：**
TM 把代表全局事务的 XID 绑定到分支事务上，本地事务提交前，RM 向 TC 注册分支事务，把分支事务关联到 XID 代表的全局事务中。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-bb3eb611075aa78a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- **lock_table表：**
为了防止脏读等情况的发生，需要为表记录添加全局锁。本地事务提交前向TC申请全局锁。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-ff026b6750f5c3b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- **undo_log表：**
rollback_info中记录了beforeImage和afterImage的信息，用于脏数据校验和回滚数据。
![image.png](https://upload-images.jianshu.io/upload_images/21580557-e4e6f564bc9f2b10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**roll_back信息如下：**记录了beforeImage和afterImage
```
{
	"@class": "io.seata.rm.datasource.undo.BranchUndoLog",
	"xid": "192.168.32.128:8091:3954260645732352",
	"branchId": 3954261379735553,
	"sqlUndoLogs": ["java.util.ArrayList", [{
		"@class": "io.seata.rm.datasource.undo.SQLUndoLog",
		"sqlType": "UPDATE",
		"tableName": "t_account",
		"beforeImage": {
			"@class": "io.seata.rm.datasource.sql.struct.TableRecords",
			"tableName": "t_account",
			"rows": ["java.util.ArrayList", [{
				"@class": "io.seata.rm.datasource.sql.struct.Row",
				"fields": ["java.util.ArrayList", [{
					"@class": "io.seata.rm.datasource.sql.struct.Field",
					"name": "id",
					"keyType": "PRIMARY_KEY",
					"type": -5,
					"value": ["java.lang.Long", 1]
				}, {
					"@class": "io.seata.rm.datasource.sql.struct.Field",
					"name": "residue",
					"keyType": "NULL",
					"type": 3,
					"value": ["java.math.BigDecimal", 1000]
				}, {
					"@class": "io.seata.rm.datasource.sql.struct.Field",
					"name": "used",
					"keyType": "NULL",
					"type": 3,
					"value": ["java.math.BigDecimal", 0]
				}]]
			}]]
		},
		"afterImage": {
			"@class": "io.seata.rm.datasource.sql.struct.TableRecords",
			"tableName": "t_account",
			"rows": ["java.util.ArrayList", [{
				"@class": "io.seata.rm.datasource.sql.struct.Row",
				"fields": ["java.util.ArrayList", [{
					"@class": "io.seata.rm.datasource.sql.struct.Field",
					"name": "id",
					"keyType": "PRIMARY_KEY",
					"type": -5,
					"value": ["java.lang.Long", 1]
				}, {
					"@class": "io.seata.rm.datasource.sql.struct.Field",
					"name": "residue",
					"keyType": "NULL",
					"type": 3,
					"value": ["java.math.BigDecimal", 900]
				}, {
					"@class": "io.seata.rm.datasource.sql.struct.Field",
					"name": "used",
					"keyType": "NULL",
					"type": 3,
					"value": ["java.math.BigDecimal", 100]
				}]]
			}]]
		}
	}]]
}
```

<br>
### 1.1.3 整体流程
#### 1.1.3.1 机制
**两阶段提交协议的演变：**
- 一阶段：业务数据和回滚日志记录在同一个本地事务中提交，释放本地锁和连接资源。
- 二阶段：
提交异步化，非常快速地完成。
回滚通过一阶段的回滚日志进行反向补偿。

**详细执行步骤：**
- 一阶段
1. 先解析sql语句,得到表名,条件,sql类型,等信息；
2. 得到前镜像：根据解析得到的条件信息，生成查询语句，定位数据；
3. 执行业务 SQL；
4. 查询后镜像：根据前镜像的结果，通过 主键 定位数据；
5. 插入回滚日志：把前后镜像数据以及业务 SQL 相关的信息组成一条回滚日志，插入到 UNDO_LOG 表中；
6. **提交前，RM 向 TC 注册分支：申请一个主键等于目标数据主键值的全局锁**；
7. 本地事务提交：业务数据的更新和前面步骤中生成的 UNDO LOG 一并提交；
8. 将本地事务提交的结果上报给 TC。TM清除内存中XID，RM清除内存中的XID、branchId。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-3d634dc629c0f850.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 二阶段-提交
9. 收到 TC 的分支提交请求，把请求放入一个异步任务的队列中，马上返回提交成功的结果给 TC。
10. 异步任务阶段的分支提交请求将异步和批量地删除相应 UNDO LOG 记录。（提交全局事务时，RM将删除undo log。先将删除操作封装为任务放入AsyncWorker中的阻塞队列中，并返回TC成功消息。AsyncWorker中的定时器每隔1s执行删除任务。）

- 二阶段-回滚
9. 当 TC 接收到全局事务回滚的指令时，会向每个 RM 发送分支事务回滚的请求。收到 TC 的分支回滚请求，开启一个本地事务，执行如下操作；
10. 通过 XID 和 Branch ID 查找到相应的 UNDO LOG 记录。
11. 数据校验：拿 UNDO LOG 中的后镜与当前数据进行比较，如果有不同，说明数据被当前全局事务之外的动作做了修改。这种情况，需要根据配置策略来做处理。
12. 根据 UNDO LOG 中的前镜像和业务 SQL 的相关信息生成并执行回滚的语句。
13. 提交本地事务。并把本地事务的执行结果（即分支事务回滚的结果）上报给 TC。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-87fdd4fb09b65b47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

全局事务提交或者回滚操作处理完成之后（异常会封装异常信息），会把处理结果发送给 TC(服务端) `sender.sendResponse(msgId, serverAddress, resultMessage)`。服务端那边会有超时检测和重试机制，来保证分布式事务运行结果的正确性。

#### 1.1.3.2 写隔离
**即避免脏写。**
>**脏写：**当两个事务同时尝试去更新某一条数据记录时，就肯定会存在一个先一个后。而当事务A更新时，事务A还没提交，事务B就也过来进行更新，覆盖了事务A提交的更新数据，这就是脏写。
在4种隔离级别下，都不存在脏写情况，因为写时会添加排它锁。
脏写会带来什么问题呢？当多个事务并发写同一数据时，先执行的事务所写的数据会被后写的覆盖，这也就是更新丢失。Seata中会导致回滚时afterImage与实际记录对不上，发生异常。
##### 1.1.3.2.1 要点
- 一阶段本地事务提交前，需要确保先拿到 **全局锁** 。
- 拿不到 **全局锁** ，不能提交本地事务。
- 拿 **全局锁** 的尝试被限制在一定范围内，超出范围将放弃，并回滚本地事务，释放本地锁。

##### 1.1.3.2.2 示例说明
两个全局事务 tx1 和 tx2，分别对 a 表的 m 字段进行更新操作，m 的初始值 1000。

#####①正常情况
**tx1执行流程如下：**
- 1. tx1获取本地锁；
- 2. tx1执行`UPDATE a SET m = m - 100 WHERE  id = 1;` 但是还未commit；
- 3. tx1获取全局锁；
- 4. tx1提交本地事务；
- 5. tx1释放本地锁；
- 6. tx1提交全局事务；
- 7. tx1释放全局锁；

**tx2执行流程如下：**
- 1. tx1释放本地锁后，tx2获取本地锁
- 2. tx2执行`UPDATE a SET m = m - 100 WHERE  id = 1;` 但是还未commit；
- 3. tx2自旋尝试获取全局锁，直到tx1释放全局锁；
- 4. tx2获取全局锁并提交本地事务；
- 5. tx2释放本地锁；
- 6. tx2提交全局事务；
- 7. tx2释放全局锁；

**如下图：**
![image](https://upload-images.jianshu.io/upload_images/21580557-67bac890072d5409.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
tx1 二阶段全局提交，释放 全局锁 。tx2 拿到 全局锁 提交本地事务。

<br>
#####②异常情况
**tx1执行流程如下：**
- 1. tx1获取本地锁；
- 2. tx1执行`UPDATE a SET m = m - 100 WHERE  id = 1;` 但是还未commit；
- 3. tx1获取全局锁；
- 4. tx1提交本地事务；
- 5. tx1释放本地锁；
此时全局事务中的其他事务异常发生了全局回滚。
- 7. tx1自旋尝试获取本地锁；

**tx2执行流程如下：**
- 1. tx1释放本地锁后，tx2获取本地锁
- 2. tx2执行`UPDATE a SET m = m - 100 WHERE  id = 1;` 但是还未commit；
- 3. tx2自旋尝试获取全局锁，直到tx1释放全局锁；
因为tx1一直在等待tx2释放本地锁，而tx2一直在等待tx1释放全局锁，导致了死锁的产生。

**如下图：**
![image](https://upload-images.jianshu.io/upload_images/21580557-3c7d5c2df706961b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果 tx1 的二阶段全局回滚，则 tx1 需要重新获取该数据的本地锁，进行反向补偿的更新操作，实现分支的回滚。

此时，如果 tx2 仍在等待该数据的 全局锁，同时持有本地锁，则 tx1 的分支回滚会失败。分支的回滚会一直重试，直到 tx2 的 全局锁 等锁超时，放弃 全局锁 并回滚本地事务释放本地锁，tx1 的分支回滚最终成功。

tx1由于拿不到本地锁，会回滚失败，然后不断的进行重试，而tx2获取全局锁，是有超时时间限制的，一旦获取全局锁超时，tx2会放弃全局锁并回滚本地事务，然后释放本地锁，此时tx1拿到了本地锁，然后回滚成功。

**在这个整个过程中，这条数据的全局锁，始终被tx1持有直到全局事务提交，所以是不会出现脏写的。**

>如果一个不是Seata管理的事务对记录进行修改，为了避免脏写，需要在该事务方法上添加@GlobalLock+@Transactional，并且在查询语句上加 for update。这样事务被Seata代理，只有获取全局锁的情况下才能提交，避免脏写。


#### 1.1.3.3 读隔离
**在数据库本地事务隔离级别 读已提交（Read Committed） 或以上的基础上，Seata（AT 模式）的默认全局隔离级别是 读未提交（Read Uncommitted） 。**

**如果应用在特定场景下，必需要求全局的 读已提交 ，目前 Seata 的方式是通过 SELECT FOR UPDATE 语句的代理。**

![image](https://upload-images.jianshu.io/upload_images/21580557-4e52f5a9a46f1d7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**SELECT FOR UPDATE 语句的执行会申请 全局锁，同时获取记录的排它锁 ，如果 全局锁 被其他事务持有，则释放本地锁（回滚 SELECT FOR UPDATE 语句的本地执行）并重试。这个过程中，查询是被 block 住的，直到 全局锁 拿到，即读取的相关数据是 已提交 的才返回。**

出于总体性能上的考虑，Seata 目前的方案并没有对所有 SELECT 语句都进行代理，仅针对 FOR UPDATE 的 SELECT 语句。


[见官网解释：https://seata.io/zh-cn/docs/dev/mode/at-mode.html](https://seata.io/zh-cn/docs/dev/mode/at-mode.html)

[参考 https://www.jianshu.com/p/de4b65019cc5](https://www.jianshu.com/p/de4b65019cc5)


<br>
### 1.1.5 Seata AT优缺点
#### 1.1.5.1 优点
- 应用层基于SQL解析实现了自动补偿，从而最大程度的降低业务侵入性；
- 速度更快:二阶段是异步提交,无需再像XA协议那样需要等所有的操作都执行完才进行提交.所谓分支事务的二阶段异步提交，其实就是异步删除undoLog。因为一阶段的时候已经提交了本地事务，所以二阶段就非常地快速。
- 将分布式事务中TC（事务协调者）可以集群部署，避免单点问题；
- 通过全局锁实现了写隔离与读隔离。

#### 1.1.5.2 缺点
#####开销
我们看看Seata增加了哪些开销（纯内存运算类的忽略不计）：
一条Update的SQL，则需要全局事务xid获取（与TC通讯）、before image（解析SQL，查询一次数据库）、after image（查询一次数据库）、insert undo log（写一次数据库）、before commit（与TC通讯，判断锁冲突），这些操作都需要一次远程通讯RPC，而且是同步的。另外undo log写入时blob字段的插入性能也是不高的。每条写SQL都会增加这么多开销,粗略估计会增加5倍响应时间（二阶段虽然是异步的，但其实也会占用系统资源，网络、线程、数据库）。

#####性价比
为了进行自动补偿，需要对所有交易生成前后镜像并持久化，可是在实际业务场景下，这个是成功率有多高，或者说分布式事务失败需要回滚的有多少比率？这个比例在不同场景下是不一样的，考虑到执行事务编排前，很多都会校验业务的正确性，所以发生回滚的概率其实相对较低。按照二八原则预估，即为了20%的交易回滚，需要将80%的成功交易的响应时间增加5倍，这样的代价相比于让应用开发一个补偿交易是否是值得？值得我们深思。

优化思路：通过数据库binlog恢复SQL执行前后镜像，这样省去了同步undo log生成记录，减少了性能损耗，同时对业务零侵入。

#####全局锁
- **热点数据**
Seata在每个分支事务中会携带对应的锁信息，在before commit阶段会依次获取锁(因为需要将所有SQL执行完才能拿到所有锁信息，所以放在commit前判断)。相比XA，Seata 虽然在一阶段成功后会释放数据库锁，但一阶段在commit前全局锁的判定也拉长了对数据锁的占有时间，这个开销比XA的prepare低多少需要根据实际业务场景进行测试。全局锁的引入实现了隔离性，但带来的问题就是阻塞，降低并发性，尤其是热点数据，这个问题会更加严重。

- **回滚锁释放时间**
Seata在回滚时，需要先删除各节点的undo log，然后才能释放TC内存中的锁，所以如果第二阶段是回滚，释放锁的时间会更长。

- **死锁问题**
Seata的引入全局锁会额外增加死锁的风险，如果出现死锁，会不断进行重试，最后靠等待全局锁超时，这种方式并不优雅，也延长了对数据库锁的占有时间。

- **保证隔离级别**
为了保证隔离级别，需要所有操作该记录的事务在获取全局锁的情况下才能进行操作，即引入Seata提供的@GlobalLock的注解。


<br>
#  二、部署
## 2.1 单机部署
### 2.1.1 启动
**docker-compose up -d    启动seata：**
```yml
version: "3"
services:
    seata:
        container_name: seata-server
        image: seataio/seata-server:1.2.0
        hostname: seata-server
        ports:
            - "8091:8091"
        environment:
            - SEATA_IP=192.168.32.225
            - SEATA_PORT=8091
        volumes:
            - /root/seata/resources:/seata-server/resources
            - /root/seata/logs:/root/logs/seata
        # network_mode: "host"
```
**或命令启动：**
```
docker run -d --net=host --name seata-server -p 8091:8091 -e SEATA_IP=192.168.32.128 -v /root/seata/resources:/seata-server/resources -v /root/seata/logs:/root/logs/seata seataio/seata-server:latest
```

### 2.1.2 配置文件
**register.conf**
```
registry {
  # file 、nacos 、eureka、redis、zk、consul、etcd3、sofa
  type = "eureka"

  eureka {
    serviceUrl = "http://192.168.32.230:8761/eureka"
    application = "default"
    weight = "1"
  }
}

config {
  # file、nacos 、apollo、zk、consul、etcd3
  type = "file"

  file {
    name = "file.conf"
  }
}
```
**file.conf**
1. 修改模式为db模式
2. 指定数据库的信息，和三张表的名字。
```
## transaction log store, only used in seata-server
store {
  ## store mode: file、db
  mode = "db"

  ## file store property
  file {
    ## store location dir
    dir = "sessionStore"
    # branch session size , if exceeded first try compress lockkey, still exceeded throws exceptions
    maxBranchSessionSize = 16384
    # globe session size , if exceeded throws exceptions
    maxGlobalSessionSize = 512
    # file buffer size , if exceeded allocate new buffer
    fileWriteBufferCacheSize = 16384
    # when recover batch read size
    sessionReloadReadSize = 100
    # async, sync
    flushDiskMode = async
  }

  ## database store property
  db {
    ## the implement of javax.sql.DataSource, such as DruidDataSource(druid)/BasicDataSource(dbcp) etc.
    datasource = "druid"
    ## mysql/oracle/postgresql/h2/oceanbase etc.
    dbType = "mysql"
    driverClassName = "com.mysql.jdbc.Driver"
    url = "jdbc:mysql://192.168.32.225:3306/seata"
    user = "root"
    password = "hxr"
    minConn = 5
    maxConn = 30
    globalTable = "global_table"
    branchTable = "branch_table"
    lockTable = "lock_table"
    queryLimit = 100
    maxWait = 5000
  }
}
```

## 2.2 集群部署
即部署多个Seata服务。
1. 注册到同一个eureka中，注册时的application服务名需要相同。如果注册中心是eureka，最好使用默认的DEFAULT作为应用名。
2. file.conf中需要使用同一个db存储公共资源（即global_table、branch_table、lock_table）。

<br>
## 2.3 数据库配置
创建数据库seata，通过以下命令创建三张表
```sql
-- -------------------------------- The script used when storeMode is 'db' --------------------------------
-- the table to store GlobalSession data
CREATE TABLE IF NOT EXISTS `global_table`
(
    `xid`                       VARCHAR(128) NOT NULL,
    `transaction_id`            BIGINT,
    `status`                    TINYINT      NOT NULL,
    `application_id`            VARCHAR(32),
    `transaction_service_group` VARCHAR(32),
    `transaction_name`          VARCHAR(128),
    `timeout`                   INT,
    `begin_time`                BIGINT,
    `application_data`          VARCHAR(2000),
    `gmt_create`                DATETIME,
    `gmt_modified`              DATETIME,
    PRIMARY KEY (`xid`),
    KEY `idx_gmt_modified_status` (`gmt_modified`, `status`),
    KEY `idx_transaction_id` (`transaction_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- the table to store BranchSession data
CREATE TABLE IF NOT EXISTS `branch_table`
(
    `branch_id`         BIGINT       NOT NULL,
    `xid`               VARCHAR(128) NOT NULL,
    `transaction_id`    BIGINT,
    `resource_group_id` VARCHAR(32),
    `resource_id`       VARCHAR(256),
    `branch_type`       VARCHAR(8),
    `status`            TINYINT,
    `client_id`         VARCHAR(64),
    `application_data`  VARCHAR(2000),
    `gmt_create`        DATETIME(6),
    `gmt_modified`      DATETIME(6),
    PRIMARY KEY (`branch_id`),
    KEY `idx_xid` (`xid`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- the table to store lock data
CREATE TABLE IF NOT EXISTS `lock_table`
(
    `row_key`        VARCHAR(128) NOT NULL,
    `xid`            VARCHAR(96),
    `transaction_id` BIGINT,
    `branch_id`      BIGINT       NOT NULL,
    `resource_id`    VARCHAR(256),
    `table_name`     VARCHAR(32),
    `pk`             VARCHAR(36),
    `gmt_create`     DATETIME,
    `gmt_modified`   DATETIME,
    PRIMARY KEY (`row_key`),
    KEY `idx_branch_id` (`branch_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
```
在每个业务数据库下创建回滚日志表
```sql
CREATE TABLE `undo_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `branch_id` bigint(20) NOT NULL,
  `xid` varchar(100) NOT NULL,
  `context` varchar(128) NOT NULL,
  `rollback_info` longblob NOT NULL,
  `log_status` int(11) NOT NULL,
  `log_created` datetime NOT NULL,
  `log_modified` datetime NOT NULL,
  `ext` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ux_undo_log` (`xid`,`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```


<br>
# 三、项目配置
## 3.1 依赖
```
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
    <exclusions>
        <exclusion>
            <artifactId>io.seata</artifactId>
            <groupId>seata-all</groupId>
        </exclusion>
    </exclusions>
</dependency>
<!-- https://mvnrepository.com/artifact/io.seata/seata-all -->
<dependency>
    <groupId>io.seata</groupId>
    <artifactId>seata-all</artifactId>
    <version>1.2.0</version>
</dependency>
```

## 3.2 代理数据源配置
```
@Configuration
public class DataSourceProxyConfiguration {

    @Bean
    @ConfigurationProperties(prefix = "spring.datasource.hikari")
    HikariDataSource dataSource(DataSourceProperties properties) {
        HikariDataSource dataSource = properties.initializeDataSourceBuilder().type(HikariDataSource.class).build();
        if (StringUtils.hasText(properties.getName())) {
            dataSource.setPoolName(properties.getName());
        }
        return dataSource;
    }

    @Primary
    @Bean
    public DataSourceProxy dataSourceProxy(DataSource dataSource){
        return new DataSourceProxy(dataSource);
    }

}
```

## 3.3 配置文件
Seata有两个配置文件： registry.conf 和 file.conf
registry.conf用于指定注册中心的类型，地址
### 3.3.1 Eureka作为注册中心
将registry.conf和file.conf文件放在resources下(与bootstrap.yml同级)，用于指定自定义事务组名称和注册的seata服务名+事务日志存储模式为db+数据库连接信息。
- **bootstrap.yml**
1. 指定eureka地址
2. 指定事务组名称，与file.conf中的vgroupMapping.my_test_tx_group = "default"对应
```
server:
  port: 10030

spring:
  profiles:
    active: dev
  application:
    name: commodity
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.32.225:3306/commodity_demo?characterEncoding=utf8&useUnicode=true&useSSL=false&serverTimezone=UTC&allowMultiQueries=true
    username: root
    password: hxr
  cloud:
    alibaba:
      seata:
        tx-service-group: my_test_tx_group

eureka:
  client:
    fetch-registry: true
    register-with-eureka: true
    service-url:
      defaultZone: http://192.168.32.230:8761/eureka/
  instance:
    instance-id: ${spring.application.name}
    prefer-ip-address: true
    lease-expiration-duration-in-seconds: 15
    lease-renewal-interval-in-seconds: 5
    health-check-url-path: /actuator/health
```

- **①registry.conf**
1. 修改type 为eureka
2. 修改serviceUrl为eureka地址。
```
registry {
  # file 、nacos 、eureka、redis、zk、consul、etcd3、sofa
  type = "eureka"
  
  eureka {
    serviceUrl = "http://192.168.32.230:8761/eureka"
    weight = "1"
  }

}

config {
  # file、nacos 、apollo、zk、consul、etcd3、springCloudConfig
  type = "file"

  file {
    name = "file.conf"
  }
}
```
<br>
- **②file.conf**
1. 修改vgroupMapping.my_test_tx_group为seata-server节点注册的应用名default(不修改Seata注册到eureka应用名，否则找不到seata服务)，my_test_tx_group需要与配置文件中的spring.cloud.alibaba.seata.tx-service-group对应。
```
transport {
  # tcp udt unix-domain-socket
  type = "TCP"
  #NIO NATIVE
  server = "NIO"
  #enable heartbeat
  heartbeat = true
  # the client batch send request enable
  enableClientBatchSendRequest = true
  #thread factory for netty
  threadFactory {
    bossThreadPrefix = "NettyBoss"
    workerThreadPrefix = "NettyServerNIOWorker"
    serverExecutorThread-prefix = "NettyServerBizHandler"
    shareBossWorker = false
    clientSelectorThreadPrefix = "NettyClientSelector"
    clientSelectorThreadSize = 1
    clientWorkerThreadPrefix = "NettyClientWorkerThread"
    # netty boss thread size,will not be used for UDT
    bossThreadSize = 1
    #auto default pin or 8
    workerThreadSize = "default"
  }
  shutdown {
    # when destroy server, wait seconds
    wait = 3
  }
  serialization = "seata"
  compressor = "none"
}
service {
  #transaction service group mapping
  vgroupMapping.my_test_tx_group = "default"
  #only support when registry.type=file, please don't set multiple addresses
  default.grouplist = "192.168.32.225:8091"
  #degrade, current not support
  enableDegrade = false
  #disable seata
  disableGlobalTransaction = false
}

client {
  rm {
    asyncCommitBufferLimit = 10000
    lock {
      retryInterval = 10
      retryTimes = 30
      retryPolicyBranchRollbackOnConflict = true
    }
    reportRetryCount = 5
    tableMetaCheckEnable = false
    reportSuccessEnable = false
  }
  tm {
    commitRetryCount = 5
    rollbackRetryCount = 5
  }
  undo {
    dataValidation = true
    logSerialization = "jackson"
    logTable = "undo_log"
  }
  log {
    exceptionRate = 100
  }
}
```




<br>
### 3.3.2 Nacos作为注册中心
1. 将registry.conf文件放在resources下(与bootstrap.yml同级)，用于指定自定义事务组名称+事务日志存储模式为db+数据库连接信息。
2. 此处注册到nacos中，同时指定配置文件file.conf的地址，此处将配置文件放到nacos中。
3. file.conf用于指定Seata框架所需表数据库的信息
 
[Seata的配置文件官网](https://github.com/seata/seata/blob/develop/script/config-center/nacos/nacos-config.sh)

- bootstrap.yml中配置
```yml
spring:
  application:
    name: seata-storage-service
  cloud:
    nacos:
      discovery:
        server-addr: http://192.168.32.128:8848/
    alibaba:
      seata:
        tx-service-group: my_test_tx_group  #指定config.txt文件中的配置service.vgroupMapping.my_test_tx_group事务分组名。
```

- registry.conf配置文件
```
registry {
  # file 、nacos 、eureka、redis、zk、consul、etcd3、sofa
  type = "nacos"

  nacos {
    application = "seata-server"
    serverAddr = "192.168.32.128:8848"
    namespace = ""
    cluster = "default"
    username = "nacos"
    password = "nacos"
  }
}

config {
  # file、nacos 、apollo、zk、consul、etcd3
  type = "nacos"

  nacos {
    serverAddr = "192.168.32.128:8848"
    namespace = ""
    group = "SEATA_GROUP"
    username = "nacos"
    password = "nacos"
  }
}
```

- 将Seata的配置信息config上传到Nacos集群中
对于大批量的修改，可以使用以下脚本进行上传。

**创建脚本nacos-config.sh**
```sh
#!/usr/bin/env bash
# Copyright 1999-2019 Seata.io Group.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at、
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

while getopts ":h:p:g:t:u:w:" opt
do
  case $opt in
  h)
    host=$OPTARG
    ;;
  p)
    port=$OPTARG
    ;;
  g)
    group=$OPTARG
    ;;
  t)
    tenant=$OPTARG
    ;;
  u)
    username=$OPTARG
    ;;
  w)
    password=$OPTARG
    ;;
  ?)
    echo " USAGE OPTION: $0 [-h host] [-p port] [-g group] [-t tenant] [-u username] [-w password] "
    exit 1
    ;;
  esac
done

if [[ -z ${host} ]]; then
    host=localhost
fi
if [[ -z ${port} ]]; then
    port=8848
fi
if [[ -z ${group} ]]; then
    group="SEATA_GROUP"
fi
if [[ -z ${tenant} ]]; then
    tenant=""
fi
if [[ -z ${username} ]]; then
    username=""
fi
if [[ -z ${password} ]]; then
    password=""
fi

nacosAddr=$host:$port
contentType="content-type:application/json;charset=UTF-8"

echo "set nacosAddr=$nacosAddr"
echo "set group=$group"

failCount=0
tempLog=$(mktemp -u)
function addConfig() {
  curl -X POST -H "${contentType}" "http://$nacosAddr/nacos/v1/cs/configs?dataId=$1&group=$group&content=$2&tenant=$tenant&username=$username&password=$password" >"${tempLog}" 2>/dev/null
  if [[ -z $(cat "${tempLog}") ]]; then
    echo " Please check the cluster status. "
    exit 1
  fi
  if [[ $(cat "${tempLog}") =~ "true" ]]; then
    echo "Set $1=$2 successfully "
  else
    echo "Set $1=$2 failure "
    (( failCount++ ))
  fi
}

count=0
for line in $(cat $(dirname "$PWD")/config.txt | sed s/[[:space:]]//g); do
  (( count++ ))
	key=${line%%=*}
    value=${line#*=}
	addConfig "${key}" "${value}"
done

echo "========================================================================="
echo " Complete initialization parameters,  total-count:$count ,  failure-count:$failCount "
echo "========================================================================="

if [[ ${failCount} -eq 0 ]]; then
	echo " Init nacos config finished, please start seata-server. "
else
	echo " init nacos config fail. "
fi
```

将config.txt文件放在脚本的前一级路径下  （  \$(dirname "$PWD")/config.txt  ）
```
service.vgroupMapping.my_test_tx_group=default
store.mode=db
store.db.datasource=druid
store.db.dbType=mysql
store.db.driverClassName=com.mysql.jdbc.Driver
store.db.url=jdbc:mysql://116.62.148.11:3306/seata?useUnicode=true&characterEncoding=UTF-8
store.db.user=root
store.db.password=abc123
store.db.minConn=5
store.db.maxConn=30
store.db.globalTable=global_table
store.db.branchTable=branch_table
store.db.queryLimit=100
store.db.lockTable=lock_table
store.db.maxWait=5000
```

运行命令./nacos-config.sh -h 192.168.32.128 -p 8848 -g SEATA_GROUP，
在WINDOW系统上可以用Git Bash命令窗口运行命令，将配置文件的信息保存到Nacos中。

## 3.4 注解
启动类注解`@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)` //取消数据源的自动创建，使用自定义的数据源配置
添加`@GlobalTransactional(name="my_test_tx_group",rollbackFor=Exception.class)`注解在业务方法上,name属性随便取名字但不能冲突，rollbackFor属性表示指定类型异常发生时进行回滚。

## 3.5 业务代码
**调用创建订单接口后执行流程：**
1. 订单数据库中创建订单，订单状态为0；
2. 通过openfeign调用库存微服务，将库存数据库中的商品库存数减少；
3. 通过openfeign调用账户微服务，将账户数据库中的用户余额减少；
```java
@Service
@Slf4j
public class OrderServiceImpl extends ServiceImpl<OrderMapper, TbOrder> implements OrderService {

    @Resource
    private UserFeign userFeign;

    @Resource
    private CommodityFeign commodityFeign;

    @Override
    @GlobalTransactional(name = "my_seata_group", rollbackFor = Exception.class)
    @Transactional(rollbackFor = Exception.class)
    public String order(TbOrder tbOrder) {
        // TODO 创建订单并发送消息
        // 1. 存储订单
        log.info("----->开始创建订单");
        save(tbOrder);
        log.info("----->开始创建订单END");

        log.info("----->订单微服务开始调用账户，做扣减");
        userFeign.points(tbOrder.getUserId(),tbOrder.getPoints());
        log.info("----->订单微服务开始调用账户，做扣减END");

        log.info("----->订单微服务开始调用库存，做扣减");
        commodityFeign.stock(tbOrder.getCommodityId(),tbOrder.getNum());
        log.info("----->订单微服务开始调用库存，做扣减END");

        return "ok";
    }
}
```

## 3.6 手动解绑和手动提交回滚
RootContext.getXID() 可以直接获取到XID，我们可以在中途控制排除不需要在事务内的服务。
```
String xid = RootContext.getXID();
RootContext.unbind();//解绑
//中途做一些与事务无关的事。比如日志服务等等 排除掉，然后
RootContext.bind(xid);//再绑回来
```
我们还可以自定义事务整个流程，下面只写了begin commit rollback,其中还有suspend和resume等方法，用来暂停和恢复事务，suspend的参数是表示是否解绑xid
```
GlobalTransaction tx = GlobalTransactionContext.getCurrentOrCreate();
// 超时时间 , 所在服务
tx.begin(30000, "user-service"); //30秒
//第二个参数transactionName 会在global_table中体现，可有可无，默认为default

try{
 //todo something
 //可以手动进行提交
 tx.commit();
}catch (Exception ignored){
 //如果捕获异常 可以手动进行回滚
 tx.rollback();
}
```
上面的例子就是我们自己来控制事务流程，如果有需要可以用AOP自己实现，一般情况下@GlobalTransaction已经够用。


<br>
#四、附
## 4.1 踩坑
1. Eureka作为注册中心，seata-server节点注册的名字只能是DEFAULT，其他名字会导致找不到服务。
2. 拉取的Seata 1.2.0中，file.conf配置文件没有vgroupMapping.my_test_tx_group = "default"等配置，最好参照官方GitHub实例。
3. 参考官网docker-compose.yaml脚本时，一定不要指定- STORE_MODE=file，否则不管file.conf怎么配，都会使用file存储资源。结果就是seata单机时正常，集群时有概率找不到xid。

## 4.2 问题 
####Q: 1. undo_log表log_status=1的记录是做什么用的？
**场景 ：** 分支事务a注册TC后，a的本地事务提交前发生了全局事务回滚
**后果 ：** 全局事务回滚成功，a资源被占用掉，产生了资源悬挂问题
防悬挂措施： a回滚时发现回滚undo还未插入，则插入一条log_status=1的undo记录，a本地事务（业务写操作sql和对应undo为一个本地事务）提交时会因为undo表唯一索引冲突而提交失败。
**说明：** log_status=1的是防御性的，是收到全局回滚请求，但是不确定某个事务分支的本地事务是否已经执行完成了，这时事先插入一条branchid相同的数据，①插入的假数据成功了，本地事务继续执行就会报主键冲突并自动回滚本地事务。 ②假如插入不成功说明表里有数据这个本地事务已经执行完成了，那么取出这条undolog数据做反向回滚操作。
**结果 ：** 全局事务回滚成功后，确保 a资源不会Commit成功。如果本地未提交，阻止提交；如本地已提交，回滚提交。

####Q: 2. 怎么使用Seata框架，来保证事务的隔离性？
A: 因seata一阶段本地事务已提交，为防止其他事务脏读脏写需要加强隔离。

- ①. 脏读 select语句加for update，代理方法增加`@GlobalLock`+@Transactional或@GlobalTransaction
- ②. 脏写 必须使用@GlobalTransaction
注：如果你查询的业务的接口没有GlobalTransactional 包裹，也就是这个方法上压根没有分布式事务的需求，这时你可以在方法上标注@GlobalLock+@Transactional 注解，并且在查询语句上加 for update。 如果你查询的接口在事务链路上外层有GlobalTransactional注解，那么你查询的语句只要加for update就行。设计这个注解的原因是在没有这个注解之前，需要查询分布式事务读已提交的数据，但业务本身不需要分布式事务。 若使用GlobalTransactional注解就会增加一些没用的额外的rpc开销比如begin 返回xid，提交事务等。GlobalLock简化了rpc过程，使其做到更高的性能。

####Q: 3.脏数据回滚失败如何处理?
A:
- 脏数据需手动处理，根据日志提示修正数据或者将对应undo删除（可自定义实现FailureHandler做邮件通知或其他）
- 关闭回滚时undo镜像校验，不推荐该方案。

####Q: 4.为什么分支事务注册时, 全局事务状态不是begin?
A:
- 异常：Could not register branch into global session xid = status = Rollbacked（还有Rollbacking、AsyncCommitting等等二阶段状态） while expecting Begin
- 描述：分支事务注册时，全局事务状态需是一阶段状态begin，非begin不允许注册。属于seata框架层面正常的处理，用户可以从自身业务层面解决。
- 出现场景（可继续补充）
① 分支事务是异步，全局事务无法感知它的执行进度，全局事务已进入二阶段，该异步分支才来注册
② 服务a rpc 服务b超时（dubbo、feign等默认1秒超时），a上抛异常给tm，tm通知tc回滚，但是b还是收到了请求（网络延迟或rpc框架重试），然后去tc注册时发现全局事务已在回滚
③ tc感知全局事务超时(@GlobalTransactional(timeoutMills = 默认60秒))，主动变更状态并通知各分支事务回滚，此时有新的分支事务来注册


## 4.3 异常
####1. 出现异常`RmTransactionException: Response[ TransactionException[Could not found global transaction xid = 192.168.32.225:8091:2009683400, may be has finished.]`

- 原因一：Seata未使用db进行资源的持久化，导致Seata集群没有共享资源而找不到xid。
- 原因二：服务重试及超时有关。比如A->B此时A调B超时，Feign如果进行重试，B等于被调了2遍；第二次被调用的B进行了响应，A发起者接收到结果后进行了提交/回滚，这次超时的B因为网络问题现在才被调用，他也收到了一样的全局事务id，进行业务处理，直到注册分支，此时全局事务已经被提交/回滚，导致当前超时的分支事务B无法注册上。
**这种问题一般保证你的业务不会去超时重试,如果你需要,请确认全局事务状态,做好幂等,防止已经做过的处理重复操作。**

>**参考其他文章：**Seata AT模式下针对同一个数据在并发情况下，如果先是下游服务成功，上游服务失败会出现异常io.seata.core.exception.GlobalTransactionException:Could not found global transaction xid = 192.168.0.2:8091:2011766308, may be has finished.
需要一段时间后lock_table和global_table才会被清理干净，虽然事务会回滚，但是中途会造成很长时间的检查事务是否已被提交等等。
几种思路：
>- 注意对用户的限流(这里所说的限流不是sentinel或hystrix的熔断降级那的限流，sentinel是针对服务本身的限流只用来防止服务超载挂掉而引发的服务雪崩，我们要做的是针对用户IP+URL的限流)
>- 在下游服务先进行扣金额扣库存等操作，这样可以尽可能保证不会出问题。
>- 加入csrf_token 用来防止重放攻击，毕竟csrf_token除了防御csrf攻击还可以用来干这事。
>- 检查http头referer是否来自正确的请求。
>- 可以适当减少client.rm.lock.retryTimes 的重试次数，默认为30次
client.rm.lock.retryInterval为重试间隔 默认10毫秒，看情况修改。从上面2个参数我们可以得出恶意请求在事务中一次最坏的情况是300ms，这还不算服务retry的时间。
一般这种分布式事务肯定不是用在对着一个商品不停的减库存这样的地方，这种秒杀肯定是redis+消息中间件，所以主要是为了防止某些恶意请求，比如黑客并发请求某服务，造成一直去判断全局事务之前的事务完成了没。


`......待续`

<br>
# 五、资料
[官方网站   https://seata.io/zh-cn/](https://seata.io/zh-cn/)
[官方GitHub   https://github.com/seata/seata-samples](https://github.com/seata/seata-samples)
[官方问题解答   https://seata.io/zh-cn/docs/overview/faq.html](https://seata.io/zh-cn/docs/overview/faq.html)



