#### 优化器
与关系型数据库类似，Hive会在真正执行计算之前，生成和优化逻辑执行计划与物理执行计划。Hive有两种优化器：Vectorize(向量化优化器) 与 Cost-BasedOptimization (CBO 成本优化器)。

**矢量化优化器**
矢量化查询(要求执行引擎为Tez)执行通过一次批量执行1024行而不是每行一行来提高扫描，聚合，过滤器和连接等操作的性能，这个功能一显着缩短查询执行时间。

set hive.vectorized.execution.enabled = true; -- 默认 false
 
set hive.vectorized.execution.reduce.enabled = true; -- 默认 false
备注：要使用矢量化查询执行，必须用ORC格式存储数据

**成本优化器**
Hive的CBO是基于apache Calcite的，Hive的CBO通过查询成本(有analyze收集的统计信息)会生成有效率的执行计划，最终会减少执行的时间和资源的利用，使用CBO的配置如下：

SET hive.cbo.enable=true; -- 从 v0.14.0默认true
 
SET hive.compute.query.using.stats=true; -- 默认false
 
SET hive.stats.fetch.column.stats=true; -- 默认false
 
SET hive.stats.fetch.partition.stats=true; -- 默认true
定期执行表（analyze）的分析，分析后的数据放在元数据库中。

<br>
# 一、基础


<br>
# 二、优化
## 2.1 数据倾斜
方式①：表A与表B进行Join，在明知Id=1的数据明显的存在数据倾斜，可以将语句select A.id from A join B on A.id = B.id拆分为以下两条：
```
select A.id from A join B on A.id = B.id where A.id <> 1;
select A.id from A join B on A.id = B.id where  A.id = 1 and B.id = 1;
```
优点：
针对只有少量的Key会产生数据倾斜的场景下非常的有用。
缺点：
表A和表B需要被读和处理两次。处理的结果也需要读和写两次。
需要人为的去找出这些产生数据倾斜的Key,并手动拆分处理。

方式②：加盐


方式③：如果进行JOIN的两张表中有一张表是小表(默认25M)，那么默认会启用Mapjoin，将小表发送到每个节点上在map阶段即完成了join，没有reduce阶段，从而避免了数据倾斜。
>需要注意的是，如果是left join且小表在左，那么不会使用map join。因为left join需要保留左表的所有数据，但是每个分片中，不知道其他分片是否有匹配的数据，导致每个分片无法确定是否将未匹配到的左表数据写出。所以干脆不使用mapjoin操作。


<br>
# 三、源码
## 3.1 框架概念
### 3.1.1 核心组成
![image.png](https://upload-images.jianshu.io/upload_images/21580557-9369f3856b1e5195.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 1）用户接口：Client
CLI（command-line interface）、JDBC/ODBC(jdbc 访问 hive)、WEBUI（浏览器访问 hive） 
- 2）元数据：Metastore
元数据包括：表名、表所属的数据库（默认是 default）、表的拥有者、列/分区字段、表的类型（是否是外部表）、表的数据所在目录等；
默认存储在自带的 derby 数据库中，推荐使用 MySQL 存储 Metastore
- 3）Hadoop
使用 HDFS 进行存储，使用 MapReduce 进行计算。
- 4）驱动器：Driver
- 5）解析器（SQL Parser） 将 SQL 字符串转换成抽象语法树 AST，这一步一般都用第三方工具库完成，比如 antlr； 对 AST 进行语法分析，比如表是否存在、字段是否存在、SQL 语义是否有误。
- 6）编译器（Physical Plan） 将 AST 编译生成逻辑执行计划。
- 7）优化器（Query Optimizer）
对逻辑执行计划进行优化。
- 8）执行器（Execution）
把逻辑执行计划转换成可以运行的物理计划。对于 Hive 来说，就是 MR/Spark。

## 3.1.2 HQL 转换为 MR 任务流程说明
1. 进入程序，利用Antlr框架定义HQL的语法规则，对HQL完成词法语法解析，将HQL转换为为AST（抽象语法树）；
2. 遍历AST，抽象出查询的基本组成单元QueryBlock（查询块），可以理解为最小的查询执行单元；
3. 遍历QueryBlock，将其转换为OperatorTree（操作树，也就是逻辑执行计划），可以理解为不可拆分的一个逻辑执行单元；
4. 使用逻辑优化器对OperatorTree（操作树）进行逻辑优化。例如合并不必要的ReduceSinkOperator，减少Shuffle数据量；
5. 遍历OperatorTree，转换为TaskTree。也就是翻译为MR任务的流程，将逻辑执行计划转换为物理执行计划；
6. 使用物理优化器对TaskTree进行物理优化；
7. 生成最终的执行计划，提交任务到Hadoop集群运行。

## 3.2 HQL 转换为 MR 源码详细解读
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d7eb8bef68aabede.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 3.2.1 程序入口 — CliDriver
众所周知，我们执行一个 HQL 语句通常有以下几种方式：
1）/bin/hive 进入客户端，然后执行 HQL； 
2）/bin/hive -e "hql"； 
3）/bin/hive -f hive.sql；
4）先开启 hivesever2 服务端，然后通过 JDBC 方式连接远程提交 HQL。

可 以 知 道 我 们 执 行 HQL 主 要 依 赖 于 \$HIVE_HOME/bin/hive 和 \$HIVE_HOME/bin/hivesever2 两种脚本来实现提交 HQL，而在这两个脚本中，最终启动的 JAVA 程序的主类为`org.apache.hadoop.hive.cli.CliDriver`，所以其实 Hive 程序的入口就是“CliDriver”这个类。

找到“CliDriver”这个类的“main”方法如下
```
  public static void main(String[] args) throws Exception {
    int ret = new CliDriver().run(args);
    System.exit(ret);
  }
```
进入run方法
```

```

<br>
# 四、面试
