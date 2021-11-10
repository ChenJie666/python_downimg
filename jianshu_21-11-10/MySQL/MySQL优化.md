# 1. 性能下降原因
- 查询语句效率低
- 索引失效（会导致行锁变表锁，很严重！！！）
- 关联查询太多
- 服务器调优及各个参数设置（缓冲、线程数等）
- 锁的效率（可能间隙锁导致并发下降，主键需要自增） 
- 数据量过大，使用缓存，进行读写分离，分库分表等

# 2. 性能分析
## 2.1 优化器(MySQL Query Optimizer)
专门负责优化SELECT语句的优化器模型。通过计算分析系统中收集到的统计信息，为客户端请求的Query提供它认为最优的执行计划（不一定是DBA认为最优的计划，这部分最耗时间）

## 2.2 MySQL常见瓶颈
- 1.CPU饱和的时候一般发生在数据装入内存或从磁盘上读取数据的时候；
- 2.IO：磁盘I/O瓶颈发生在装入数据远大于内存容量的时候；
- 3.服务器硬件性能瓶颈：top、free、iostat和vmstat查看系统性能。

<br>
## 2.3 效率分析
### 2.3.1 开启慢查询日志，设置阈值，比如超过5秒钟的就是慢SQL，并将它抓取出来；
```
**设置开启**
SHOW VARIABLES LIKE '%slow_query_log%';
set global show_query_log=1;
set slow_query_log_file=/var/lib/mysql/slow-query.log;
**设置慢查询时间**
SHOW VARIABLES LIKE 'long_query_time%';
set long_query_time = 3;
会将慢查询的信息存储到指定文件中。
```
**在生产环境中，可以使用MySQL提供的日志分析工具mysqldumpslow进行分析。**![image.png](https://upload-images.jianshu.io/upload_images/21580557-498fdab035ad7ff1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**还可以开启全局查询日志，将所有的sql都保存到一张表中。**
```
set global general_log=1;
set global log_output='TABLE';
记录到mysql库的general_log表中
select * from mysql.general_log;
```

### 2.3.2 Explain+索引分析
| id   | select_type | table   | type | possible_keys | key       | key_len | ref   | rows | Extra |
| ---- | ----------- | ------- | ---- | ------------- | --------- | ------- | ----- | ---- | ----- |
| 1    | SIMPLE      | student | ref  | score_nor     | score_nor | 5       | const | 1    | NULL  |

- **id**：id值越大越先被执行，如果相同则顺序执行；
- select_type：SIMPLE(简单查询)，PRIMARY(子查询语句中主体)，SUBQUERY(子查询语句中的子查询)，DERIVED(查询另一个表产生的衍生虚表)，UNION(出现在UNION后的查询)，UNION RESULT(从UNION表获取结果的SELECT)；
- **type**：system(只有一行记录) > const(索引一次找到，常见主键索引) > eq_ref(唯一性索引扫描，通过主键关联两表) > - **ref**(非唯一性索引扫描，返回匹配单个值的数据) > **range**(非唯一性索引扫描，返回匹配范围的数据) > index(遍历索引树) > ALL(遍历磁盘中的全表)；
- possible_keys：显示可能应用在表中的索引，一个或多个。不一定被实际使用；
- **key**：实际使用的索引，为null表示没有使用索引；查询中若使用了覆盖索引，则该索引仅出现在key列表中；
- key_len：表示索引中使用的字节数；
- ref：被该行的索引检索的数据的类型；
- **rows**：mysql认为执行查询时必须检索的行数；
- **Extra**：
**Using index(使用了索引)：**select操作中使用了覆盖索引，避免访问表数据行，效率不错。同时出现using where，表明索引被用来执行索引键值查找；
**Using filesort(文件内排序)：**无法利用索引完成的排序；
**Using temporary(使用了临时表)：**使用了临时表保存中间结果，常见order by和group by；
Using join buffer：使用了连接缓存；
Impossible where：where子句的值总是false，不能用来获取任何元素；
Select tables optimized away：没有groupby情况下，基于索引优化Min/Max操作。
distinct：优化distinct操作，再找到第一匹配的远足后即停止找相同的值的动作；
![image.png](https://upload-images.jianshu.io/upload_images/21580557-92491d48c4320234.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 2.3.3 查看执行细节
show profile是mysql提供可以用来分析当前会话中语句执行的资源消耗情况，查询会话SQL的执行细节和生命周期情况；
```
打开profile
show variables like 'profiling';
set profiling=on;
查询命令
show profiles;   #最近15次的运行结果
show profile cpu,block io for query 3;  #查看第三条sql的生命周期
```

**需要注意**
- converting HEAP to MyISAM：查询结果太大，内存不够用写出到磁盘；
- Creating tmp table：创建临时表
- Copying to tmp table on disk：把内存中临时表复制到磁盘，危险！！！
- locked

### 2.3.4 硬件调优
运维经理 or DBA，进行SQL数据库服务器的参数调优。

### 2.3.5 锁效率
查看锁信息：show status like 'innodb_row_lock%';
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d4b4e208390c377b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<br>
# 3. 优化
## 3.1 索引创建
**需要建索引的情况：**
1. 主键自动建立主键索引；
2. 频繁作为查询条件的字段；
3. 查询中与其他表关联的字段，外键关系建立索引；
4. 单值/组合索引的选择（高并发下倾向组合索引）；
5. 查询中排序的字段，排序字段若通过索引去访问将大大提高排序速度；
6. 查询中统计或者分组字段（分组需要排序）；

**不建索引的情况：**
1. 表记录太少（300万以下）；
2. 经常增删改的表；
3. 数据重复且分布平均的表字段。选择性指索引列中不同值的数目与表中记录数的比，选择性越接近1，索引效率越高。

**语法**
创建：CREATE [UNIQUE] INDEX indexName ON mytable(columnname(length));
ALTER mytable ADD [UNIQUE] INDEX [indexName] ON (columnname(length));
删除：DROP INDEX [indexName] ON table;
查看：SHOW INDEX FROM table_name\G

## 3.2 索引优化
1. 复合索引需要满足最左匹配原则；
2. left join等操作，因为主表需要全表扫描，所以索引建在从表上；同时使用小表作为主表，大表作为从表。无法避免join buffer，调大JoinBuffer的设置；
3. 不要对索引列做任何操作，如计算操作；
4. 复合索引中，范围插叙之后索引失效，如a=1 and b>2 and c=3，c=3不会使用索引，但是a=1 and b like 'k%k%' and c=3，c=3会使用索引；
5. 使用覆盖索引(using index)，避免回表二次查询；
6. 不使用 != 或 <> ，避免索引失效；
7. is null 和 is not null 索引效率不高，避免使用；
8. like 不要以通配符开头('%abc...')，会使索引失效。但是可以使用覆盖索引来使用type为index级别的索引，效率不高（使用覆盖索引可能是出于效率，如果先遍历索引树再回表，还不如扫描聚簇索引）；
9. varchar型的搜索时一定要加引号，例 name=2000，如果name是varchar型的就会转换类型导致索引失效；
10. 少用or，用它来连接时会导致索引失效；

## 3.3 IN、Exists优化
小表驱动大表，小的数据集驱动大的数据集。如子查询用小表，小表join大表。

**使用in、exists的场景如下:**
```
**当B表的数据集小于A表数据集时，用in优于exists：**
select * from A where id in (select id from B);
等价于：
for select id from B
for select * from A where A.id = B.id;

**当A表的数据集小于B表数据集时，用exists优于in：**
select * from A where exists (select 1 from B where A.id = B.id);
等价于
for select * from
for select * from B where B.id = A.id;
```
>**in的场景：**IN后面的查询会先进行，结果存入内存作为查询主表的条件，所以主表是大表，从表是小表的情况下用IN好；
**exists的场景：**exists中，会遍历主表，放到子查询中做条件验证，根据返回的True或False决定主查询的数据结果是否保留，所以主表是小表，从表是大表的情况下用Exists好；

## 3.4 Order by优化
### 3.4.1 利用索引进行排序
复合索引存储在索引树中，是按创建索引时的字段顺序进行排列的，所以order by时要注意不能使索引失效要满足最左匹配原则。
当使用Using filesort时需要进行优化。

### 3.4.2 FileSort排序
如果不在索引列上，filesort有两种算法：
- 双路排序：双路排序会先取出记录的主键和待排字段，进行排序后再根据主键拿到所有的字段。会经历两次IO，时间消耗大。
- 单路排序：4.1之后开始使用单路排序，会取出所有字段存入内存中进行排序，内存消耗大。但是容易导致sort_buffer容量溢出，需要进行多次局部排序导致大量IO，得不偿失。

**优化：**
1. Order by时select * 时大忌，只query需要的字段；
2. 提高sort_buffer_size的值；
3. 提高max_length_for_sort_data的值，增加使用单路排序的概率。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-8efe2177254429db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 3.5 Group by优化
1. group by实质是先排序后分组；
2. 无法使用索引时，提高sort_buffer_size和max_length_for_sort_data的值；
3. where 高于 having，能写在where限定的条件就不要写在having里。
