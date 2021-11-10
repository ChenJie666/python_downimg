## 进程命令
#### 对hadoop集群的操作
start-dfs.sh  stop-dfs.sh   打开和关闭dfs
start-yarn.sh  stop-yarn.sh   打开和关闭yarn

#### hadoop单进程操作
**旧版本命令**
hadoop-daemon.sh  start/stop  namenode/datanode/secondarynamenode  
yarn-daemon.sh  start/stop  resourcemanager/nodemanager  
mr-jobhistory-daemon.sh start/stop historyserver 
>**注：**修改hadoop-daemon.sh和yarn-daemon.sh的启动文件，可以修改pid和log的存储位置。

<br>
**新版本命令**
hdfs --daemon start/stop namenode/datanode/secondarynamenode
yarn --daemon start/stop nodemanger/resourcemanager
mapred --daemon start/stop historyserver

<br>
## 基础命令
hadoop  fs  -help  rm   输出rm指令的详细信息
hadoop  fs  -usage  rm   输出rm的标准格式

hadoop  fs  -setrep  10  /input.txt  设置HDFS中文件的replication(副本)数量（setrep指令记录在NameNode中，实际副本数还是看最大节点数。）
hadoop fs -checksum /a/b/c/xsync   每次写入读出都会自动进行一次校验判断文件的完整性；checksum是手动判断文件的完整型命令，如果和crc文件比对不同，则抛出错误。

| 选项名称 | 使用格式 | 含义 |
| --- | --- | --- |
| -ls | -ls <路径> | 查看指定路径的当前目录结构 |
| -lsr | -lsr <路径> | 递归查看指定路径的目录结构 |
| -du | -du <路径> | 统计目录下个文件大小 |
| -dus | -dus <路径> | 汇总统计目录下文件(夹)大小 |
| -count | -count [-q] <路径> | 统计文件(夹)数量 |
| -mv | -mv <源路径> <目的路径> | 移动 |
| -cp | -cp <源路径> <目的路径> | 复制 |
| -rm | -rm [-skipTrash] <路径> | 删除文件/空白文件夹 |
| -rmr | -rmr [-skipTrash] <路径> | 递归删除 |
| -put | -put <多个linux上的文件> <hdfs路径> | 上传文件 |
| -copyFromLocal | -copyFromLocal <多个linux上的文件> <hdfs路径> | 从本地复制 |
| -moveFromLocal | -moveFromLocal <多个linux上的文件> <hdfs路径> | 从本地移动 |
| -getmerge | -getmerge <源路径> <linux路径> | 合并到本地 |
| -cat | -cat <hdfs路径> | 查看文件内容 |
| -text | -text <hdfs路径> | 查看文件内容 |
| -copyToLocal | -copyToLocal [-ignoreCrc] [-crc] [hdfs源路径] [linux目的路径] | 从本地复制 |
| -moveToLocal | -moveToLocal [-crc] <hdfs源路径> <linux目的路径> | 从本地移动 |
| -mkdir | -mkdir <hdfs路径> | 创建空白文件夹 |
| -setrep | -setrep [-R] [-w] <副本数> <路径> | 修改副本数量 |
| -touchz | -touchz <文件路径> | 创建空白文件 |
| -stat | -stat [format] <路径> | 显示文件统计信息 |
| -tail | -tail [-f] <文件> | 查看文件尾部信息 |
| -chmod | -chmod [-R] <权限模式> [路径] | 修改权限 |
| -chown | -chown [-R] [属主](#)] 路径 | 修改属主 |
| -chgrp | -chgrp [-R] 属组名称 路径 | 修改属组 |
| -help | -help [命令选项] | 帮助 |

<br>
## 管理命令
hadoop dfsadmin -report  查看各个datenode节点的状态
hadoop dfsadmin -safemode get   命令是用来查看当前hadoop安全模式的开关状态
hadoop dfsadmin -safemode enter  命令是打开安全模式
hadoop dfsadmin -safemode leave 命令是离开安全模式

hdfs dfsadmin -fetchImage /data 获取fsimage信息并存储到目标地址

<br>
## 节点间数据均衡
开启数据均衡命令：
start-balancer.sh -threshold 10
>对于参数10，代表的是集群中各个节点的磁盘空间利用率相差不超过10%，可根据实际情况进行调整。

停止数据均衡命令：
stop-balancer.sh
>注意：于HDFS需要启动单独的Rebalance Server来执行Rebalance操作，[所以尽量不要在NameNode上执行start-balancer.sh，而是找一台比较空闲的机器。

## 磁盘间数据均衡
（1）生成均衡计划（我们只有一块磁盘，不会生成计划）
hdfs diskbalancer -plan hadoop103
（2）执行均衡计划
hdfs diskbalancer -execute hadoop103.plan.json
（3）查看当前均衡任务的执行情况
hdfs diskbalancer -query hadoop103
（4）取消均衡任务
hdfs diskbalancer -cancel hadoop103.plan.json
