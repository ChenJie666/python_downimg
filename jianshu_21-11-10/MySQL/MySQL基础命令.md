# mysql：

## 新建用户
方式一：直接将用户信息插入mysql.user表
mysql> insert into mysql.user(Host,User,Password) values("%","root",password("abc123"));

方式二：创建默认权限的用户
CREATE USER 'rangerdba'@'localhost' IDENTIFIED BY 'rangerdba';

方式三：创建用户并赋予用户root所有数据库的所有表的权限
mysql> grant all privileges on *.* to 'root'@'%' identified by 'abc123';

注意：需要执行flush privileges使得修改生效。

**查看用户权限**
1. 执行`select * from mysql.user where user='ranger'\G;` 获取用户的信息
2. 执行`show grants for ranger` 获取执行的授权语句


创建数据库时指定字符集和排序规则
create database hive DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

远程链接数据库（指定地址和端口）
mysql -P3308 -h 192.168.32.244 -uroot -proot

## sql
执行顺序
![image.png](https://upload-images.jianshu.io/upload_images/21580557-583481530e2517a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/21580557-442bcefe01beefec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



## 创建表时指定默认值，主键，数据库引擎和编码

```sql
DROP TABLE IF EXISTS `app_user`;
CREATE TABLE `app_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(60) NOT NULL COMMENT '密码',
  `nickname` varchar(255) DEFAULT NULL COMMENT '昵称',
  `headImgUrl` varchar(1024) DEFAULT NULL COMMENT '头像url',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机号',
  `sex` tinyint(1) DEFAULT NULL COMMENT '性别',
  `enabled` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态（1有效,0无效）',
  `type` varchar(16) NOT NULL COMMENT '类型（暂未用）',
  `createTime` datetime NOT NULL COMMENT '创建时间',
  `updateTime` datetime NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY(`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```
```sql
CREATE TABLE order_record(
    id INT(11) PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    item_id INT(11) NOT NULL COMMENT '商品',
    total INT(11) NOT NULL COMMENT '数量',
    custmer_name VARCHAR(255) DEFAULT NULL  COMMENT '客户姓名',
    order_time DATETIME DEFAULT NULL  COMMENT '下单时间',
    is_active INT(11) DEFAULT '1'  COMMENT '是否有效(1=是;0=否)',
    update_time TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' ) #初始为null值，默认为null值，更新时记录update_time为当前时间  
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;
```
```sql
CREATE TABLE IF NOT EXISTS ads_uv_count(
dt varchar(255) NOT NULL,
day_count bigint(255) NULL DEFAULT NULL,
wk_count bigint(255) NULL DEFAULT NULL,
mn_count bigint(255) NULL DEFAULT NULL, 
is_weekend varchar(3) NULL DEFAULT NULL,
is_monthend varchar(3) NULL DEFAULT NULL,
PRIMARY KEY (dt) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;
```


CREATE TABLE `offset_manager` (
  `groupid` varchar(50) DEFAULT NULL,
  `topic` varchar(50) DEFAULT NULL,
  `partition` int(11) DEFAULT NULL,
  `untiloffset` mediumtext,
  UNIQUE KEY `offset_unique` (`groupid`,`topic`,`partition`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'


//修改字段注释字符集
alter table COLUMNS_V2 modify column COMMENT varchar(256) character set utf8;
//修改表注释字符集
alter table TABLE_PARAMS modify column PARAM_VALUE varchar(4000) character set utf8;
//修改分区注释字符集
alter table PARTITION_KEYS modify column PKEY_COMMENT varchar(4000) character set utf8;


## mysql类型和java类型对照表
| 类型名称  | 显示长度 | 数据库类型            | JAVA类型             | JDBC类型索引(int) | 描述 |
| --------- | -------- | --------------------- | -------------------- | ----------------- | ---- |
|           |          |                       |                      |                   |      |
| VARCHAR   | L+N      | VARCHAR               | java.lang.String     | 12                |      |
| CHAR      | N        | CHAR                  | java.lang.String     | 1                 |      |
| BLOB      | L+N      | BLOB                  | java.lang.byte[]     | -4                |      |
| TEXT      | 65535    | VARCHAR               | java.lang.String     | -1                |      |
|           |          |                       |                      |                   |      |
| INTEGER   | 4        | INTEGER UNSIGNED      | java.lang.Long       | 4                 |      |
| TINYINT   | 3        | TINYINT UNSIGNED      | java.lang.Integer    | -6                |      |
| SMALLINT  | 5        | SMALLINT UNSIGNED     | java.lang.Integer    | 5                 |      |
| MEDIUMINT | 8        | MEDIUMINT UNSIGNED    | java.lang.Integer    | 4                 |      |
| BIT       | 1        | BIT                   | java.lang.Boolean    | -7                |      |
| BIGINT    | 20       | BIGINT UNSIGNED       | java.math.BigInteger | -5                |      |
| FLOAT     | 4+8      | FLOAT                 | java.lang.Float      | 7                 |      |
| DOUBLE    | 22       | DOUBLE                | java.lang.Double     | 8                 |      |
| DECIMAL   | 11       | DECIMAL               | java.math.BigDecimal | 3                 |      |
| BOOLEAN   | 1        | 同TINYINT             |                      |                   |      |
|           |          |                       |                      |                   |      |
| ID        | 11       | PK (INTEGER UNSIGNED) | java.lang.Long       | 4                 |      |
|           |          |                       |                      |                   |      |
| DATE      | 10       | DATE                  | java.sql.Date        | 91                |      |
| TIME      | 8        | TIME                  | java.sql.Time        | 92                |      |
| DATETIME  | 19       | DATETIME              | java.sql.Timestamp   | 93                |      |
| TIMESTAMP | 19       | TIMESTAMP             | java.sql.Timestamp   | 93                |      |
| YEAR      | 4        | YEAR                  | java.sql.Date        | 91                |      |


## 函数
| 函数 | 说明 |
| --- | --- |
| date(current_date) | 将时间转换为yyyy-DD-MM格式 |
| date_sub(current_date,INTERVAL 1 DAY) | 将日期减一天 |
| group_concat(distinct xxx) | 聚合并去重 |
| GREATEST(xx,yy) | 取两列最大值，注意与max不同，max是同一列groupby时取最大值 |

##mysql中的函数
concat(id,name,email) : 将多个元素进行拼接
concat_ws("|",id,name,email) :将多个元素进行拼接并指定分隔符
group_concat(id order by id desc separator '_') :通常和group by配合使用，将同一分组的元素拼接为字符串，并指定分隔符。


## 中文乱码问题
**首先查看mysql编码**
show variables like 'char%';
```
mysql> show variables like 'char%';
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8mb4                    |
| character_set_connection | utf8mb4                    |
| character_set_database   | utf8                       |
| character_set_filesystem | binary                     |
| character_set_results    | utf8mb4                    |
| character_set_server     | latin1                     |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
```
如果不是utf8编码，则设置编码
set character_set_client=utf8;

**查看url的地址上是否加上了编码集**
```url
jdbc:mysql://chenjie.asia:3306/test?characterEncoding=utf8&useUnicode=true&useSSL=false&serverTimezone=UTC&allowMultiQueries=true
```

**大数据量批量写入**
需要加rewriteBatchedStatements参数，并保证5.1.13以上版本的驱动，才能实现高性能的批量插入。
MySQL JDBC驱动在默认情况下会无视executeBatch()语句，把我们期望批量执行的一组sql语句拆散，一条一条地发给MySQL数据库，批量插入实际上是单条插入，直接造成较低的性能。
只有把rewriteBatchedStatements参数置为true, 驱动才会帮你批量执行SQL
另外这个选项对INSERT/UPDATE/DELETE都有效

## 查询当前MySQL使用的时区
SHOW VARIABLES LIKE "%time_zone%";
高版本的MySQL要求在连接url中配置本次连接时，MySQL所使用的时区(serverTimezone=UTC)，根据该时区进行时区转换并保存。

## 修改mysql密码策略，可以使用比较简单的密码
```
mysql> set global validate_password_length=4;
mysql> set global validate_password_policy=0;
```

## MySQL中的函数
**from_unixtime() 函数将十位时间戳转为日期**
select from_unixtime(1111111111);

**unix_timestamp()获取十位时间戳**
select unix_timestamp('2009-08-06');

两者结合使用可以改变日期格式 结合使用from_unixtime(unix_timestamp(date_created),'yyyy-MM-dd HH:mm:ss')来规范时间的格式。

## 索引：

	索引本身也是表，因此会占用存储空间，一般来说，索引表占用的空间的数据表的1.5倍；索引表的维护和创建需要时间成本，这个成本随着数据量增大而增大；构建索引会降低数据表的修改操作（删除，添加，修改）的效率，因为在修改数据表的同时还需要修改索引表；

### 索引的增删改查：

在创建表的时候添加索引：

```sql
CREATE TABLE mytable(  
    ID INT NOT NULL,   
    username VARCHAR(16) NOT NULL, 
    INDEX [indexName] (username(length)
)  
或
CREATE TABLE `offset_manager` (
  `groupid` varchar(50) DEFAULT NULL,
  `topic` varchar(50) DEFAULT NULL,
  `partition` int(11) DEFAULT NULL,
  `untiloffset` mediumtext,
  UNIQUE KEY `offset_unique` (`groupid`,`topic`,`partition`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

在建表后添加索引：

```sql
ALTER TABLE my_table ADD [UNIQUE] INDEX index_name(column_name);
或者
CREATE INDEX index_name ON my_table(column_name)
```

删除索引

```sql
DROP INDEX my_index ON tablename；
或者
ALTER TABLE table_name DROP INDEX index_name
```

**查看表中的索引**

```
SHOW INDEX FROM tablename
```

**查看查询语句使用索引的情况**

```
//explain 加查询语句
explain SELECT * FROM table_name WHERE column_1='123'
```



### 索引分类：

1、主键索引：即主索引，根据主键pk_clolum（length）建立索引，不允许重复，不允许空值；

ALTER TABLE 'table_name' ADD PRIMARY KEY pk_index('col')；

2、唯一索引：用来建立索引的列的值必须是唯一的，允许空值

ALTER TABLE 'table_name' ADD UNIQUE index_name('col')；

3、普通索引：用表中的普通列构建的索引，没有任何限制

ALTER TABLE 'table_name' ADD INDEX index_name('col')；

4、全文索引：用大文本对象的列构建的索引

ALTER TABLE 'table_name' ADD FULLTEXT INDEX ft_index('col')；

5、组合索引：用多个列组合构建的索引，这多个列中的值不允许有空值

ALTER TABLE 'table_name' ADD INDEX index_name('col1','col2','col3')；
**相当于建立了col1,col1col2,col1col2col3三个索引**



	在使用组合索引的时候可能因为列名长度过长而导致索引的key太大，导致效率降低，在允许的情况下，可以只取col1和col2的前几个字符作为索引。

ALTER TABLE 'table_name' ADD INDEX index_name(col1(4),col2（3))；



```
索引分类
1.普通索引index :加速查找
2.唯一索引
    主键索引：primary key ：加速查找+约束（不为空且唯一）
    唯一索引：unique：加速查找+约束 （唯一）
3.联合索引
    -primary key(id,name):联合主键索引
    -unique(id,name):联合唯一索引
    -index(id,name):联合普通索引
4.全文索引fulltext :用于搜索很长一篇文章的时候，效果最好。
5.空间索引spatial :了解就好，几乎不用
```



# hive：

drop database gmall cascade;

select get_json_object(line,'$.mid') mid_id；	解析json对象

show create table ads_uv_count;	查看建表语句



# hadoop：
show create table gmall.ods_start_log;

	datax导入到mysql中时，如果使用writeMode为insert模式，会产生警告，影响效率；可以使用insert ignore模式。
