# 一、目录结构

| 目录        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| /bin        | Binary的缩写，这个目录存放最经常使用的命令；                 |
| /sbin       | s就是Super User的意思，这里存放的时系统管理员使用的系统管理程序； |
| /home       | 存放普通用户的主目录，在Linux中每个用户都有一个自己的目录，一般该目录名是以用户的账号命名的； |
| /root       | 该目录为系统管理员，也称作超级权限者的用户主目录；           |
| /lib        | 系统开机所需要最基本的动态连接共享库，起作用类似与Windows里的DLL文件。几乎所有的应用程序都需要用到这些共享库； |
| /lost+found | 这个目录一般情况下是空的，当系统非法关机后，这里就存放了一些文件； |
| /etc        | 所有的系统管理所需要的配置文件和子目录；                     |
| /usr        | 这是一个非常重要的目录，用户的很多应用程序和文件都放在这个目录下，累细雨windows下的program files目录； |
| /boot       | 这里存放的是启动Linux是使用的一些核心文件，包括一些连接文件以及镜像文件，自己安装的别放在这里； |
| /proc       | 这个目录是一个虚拟的目录，他是系统内存的映射，我们可以通过直接访问这个目录来获取系统信息； |
| /srv        | service缩写，该目录存放一些服务启动之后需要提取的数据；      |
| /sys        | 这是linux2.6内核的一个很大的变化。该目录下安装了2.6内核中新出现的一个文件系统sysfs； |
| /tmp        | 用于存放一些临时文件；                                       |
| /dev        | 类似于windows的设备管理器，把所有的硬件用文件的形式存储；    |
| /media      | linux系统会自动识别一些设备，例如U盘、光驱等待，当识别后linux会把识别的设备挂载到这个目录下； |
| /mnt        | 系统提供该目录是为了让用户临时挂载别的文件系统，我们可以将外部的存储挂载在/mnt/上，然后进入该目录就可以查看里面的内容了； |
| /opt        | 这是给主机额外安装软件所摆放的位置。默认时空的；             |
| /var        | 这个目录中存放着不断扩充着的东西，我们习惯将那些经常被修改的目录放在这个目录下。包括各种日志文件； |
| /selinux    | SELinux是一种安全子系统，它能控制程序只能访问特定文件；      |


快照功能：记录当前的硬盘的状态。刚建快照时快照占用内存为0，标记了当前硬盘的存储状态。当虚拟机对快照标记的内容改写时，会将改写的内容存储进快照，与未改写的部分整合得到完整的快照。当快照标记的部分被完全改写，那么快照存储空间完整记录了当时拍摄时的内存状态。


# 二、常用命令

**参数形式**

第一种：参数用一横的说明后面的参数是字符形式。

第二种：参数用两横的说明后面的参数是单词形式。

第三种：参数前有横的是 System V风格。

第四种：参数前没有横的是 BSD风格。

|      | 常用的参数                                                   |
| ---- | ------------------------------------------------------------ |
| -a   | 全部文件  ps中所有进程                                       |
| -d   | unzip指定解压路径                                            |
| -e   | 支持反斜线控制字符转换  rpm中表示卸载                        |
| -f   | 强制执行（force）  tail中不断刷新内容（flush）               |
| -g   | group用户组                                                  |
| -h   | df命令中以较易阅读的 GBytes, MBytes, KBytes 等格式显示       |
| -l   | 长串数据  fdisk中显示所有硬盘分区列表                        |
| -n   | 显示行号   head和tail中指定显示行数   groupmod中修改组名（groupmod  -n 新组名 老组名） |
| -p   | 多层目录                                                     |
| -r   | 递归整个文件夹   用户和用户的相关文件夹  zip中指定压缩目录   |
| -R   | 与权限相关的操作chmod、chown，也是整个文件夹递归操作         |
| -v   | 显示指令的详细过程                                           |
| -y   | 执行yum命令时所有问题都是yes                                 |
| -9   | kill指令中强迫进程立即停止                                   |



## 概述

| 命令                        | 说明                                          |
| --------------------------- | --------------------------------------------- |
| man                         | 获得帮助信息                                  |
| help 命令                   | 获得shell内置命令的帮助信息                   |
| pwd:print working directory | 打印工作目录                                  |
| vim                         | 查看文件（不存在则创建）                      |
| ls                          | 查看目录下的文件                              |
| cd                          | 跳转路径                                      |
| mkdir [-p] 目录             | 创建目录（-p 是否递归创建）                   |
| rmdir                       | 删除空目录                                    |
| touch                       | 需要创建的空文件名称                          |
| cp                          | 复制                                          |
| rm                          | 删除                                          |
| cat                         | 查看小文件                                    |
| more                        | 要查看的文件（查看大文件）                    |
| less                        | less 要查看的文件（查看大文件，效率比more高） |
| head                        | 查看文件头10行内容                            |
| tail                        | 查看文件后10行内容                            |
| ln                          | 链接                                          |
| \>    \>>                   | 覆盖和追加                                    |
| echo                        | 输出内容到控制台                              |
| read                        | 从标准输入读取数值                            |



## 2.1 文本操作

**cat、more、less、head、tail命令的比较：**

cat命令可以一次显示整个文件，如果文件比较大，使用不是很方便；

more命令可以让屏幕在显示满一屏幕时暂停，按空格往前翻页，按b往后翻页。

less命令也可以分页显示文件，和more命令的区别就在于： 支持上下键卷动屏幕、查找；不需要在一开始就读取整个文件，打开大文件时比more、vim更快。

head命令用于查看文件的前n行。

tail命令用于查看文件的后n行，加上-f命令，查看在线日志非常方便，可以打印最新增加的日志。



### vim/vi

**一般模式：**

| yy                          | **复制**光标当前一行                |
| --------------------------- | ----------------------------------- |
| p                           | 箭头移动到目的行**粘贴**            |
| u                           | **撤销上一步**                      |
| dd                          | **删除**光标当前行                  |
| x                           | 删除一个字母，相当于del，**向后删** |
| ^                           | **移动到行头**                      |
| \$                           | **移动到行尾**                      |
| gg或者1+G                   | **移动到页头**                      |
| G                           | **移动到页尾**                      |
| 数字+G（先输入数字，在按G） | **移动到目标行**                    |

**编辑模式：**

| i    | **当前光标前**         |
| ---- | ---------------------- |
| a    | 当前光标后             |
| o    | **当前光标行的下一行** |
| I    | 光标所在行最前         |
| A    | 光标所在行最后         |
| O    | 当前光标行的上一行     |

**命令模式：**

| :w             | **保存**                                           |
| -------------- | -------------------------------------------------- |
| :q             | **退出**                                           |
| :!             | **强制执行**                                       |
| / 要查找的词   | n 查找下一个，N 往上查找                           |
| ZZ（shift+zz） | **没有修改文件直接退出，如果修改了文件保存后退出** |
| :set nu        | 显示行号                                           |
| :set nonu      | 关闭行号                                           |
| :nohl          | 删除高亮                                           |
| \G             | 查询sql中以列的形式显示                            |

**编码**
- set ff  （查看编码）
- set ff=unix  （修改编码为unix）

### vimdiff

-  vimdiff [文件a]  [文件b]	（同时打开两个文件进行比较，左右分布）
- vimdiff -o2 [文件a]  [文件b]	（同时打开两个文件进行比较，上下分布）

### diff
- diff [文件a]  [文件b]   (展示两个文件的不同行)


### head/tail

**①head：显示文件头部内容**

- head [文件]	      （功能描述：查看文件头10行内容）

- head -n 5 [文件]      （功能描述：查看文件头5行内容，5可以是任意行数）

| 选项      | 功能                   |
| --------- | ---------------------- |
| -n <行数> | 指定显示头部内容的行数 |

 

**②tail：输出文件尾部内容**

- tail  [文件] 		（功能描述：查看文件后10行内容）

- tail  -n  5  [文件] 	（功能描述：查看文件后5行内容，5可以是任意行数）

- tail  -f  [文件]		（功能描述：实时追踪该文档的所有更新）

| 选项     | 功能                                 |
| -------- | ------------------------------------ |
| -n<行数> | 输出文件尾部n行内容                  |
| -f       | 显示文件最新追加的内容，监视文件变化 |

注意：用vim和vi修改内容会删除源文件并生成新文件，所以tail -f会失效。需要用到

追加和覆盖语句（>或>>），才能被tail -f监视到。



### cat

一般用于查看小文件

- cat  [选项] [文件]

| 选项 | 功能描述                     |
| ---- | ---------------------------- |
| -n   | 显示所有行的行号，包括空行。 |

 

### more/less

**①more：文件内容分屏查看器**

- more [文件]

| 操作           | 功能说明                                 |
| -------------- | ---------------------------------------- |
| 空白键 (space) | 代表向下翻一页；                         |
| Enter          | 代表向下翻『一行』；                     |
| q              | 代表立刻离开 more ，不再显示该文件内容。 |
| Ctrl+F         | 向下滚动一屏                             |
| Ctrl+B         | 返回上一屏                               |
| =              | 输出当前行的行号                         |
| :f             | 输出文件名和当前行的行号                 |

 

**②less：分屏显示文件内容，效率比more高**

- less [文件]

| 操作       | 功能说明                                           |
| ---------- | -------------------------------------------------- |
| 空白键     | 向下翻动一页；                                     |
| [pagedown] | 向下翻动一页                                       |
| [pageup]   | 向上翻动一页；                                     |
| /字串      | 向下搜寻『字串』的功能；n：向下查找；N：向上查找； |
| ?字串      | 向上搜寻『字串』的功能；n：向上查找；N：向下查找； |
| q          | 离开 less 这个程序；                               |

 

### read

 **1、简单读取**

运行脚本如下

```
#!/bin/bash

#这里默认会换行  
echo "输入网站名: "  
#读取从键盘的输入  
read website  
echo "你输入的网站名是 $website"  
exit 0  #退出
```

测试结果为：

```
输入网站名: 
www.runoob.com
你输入的网站名是 www.runoob.com
```

**2、-p 参数，允许在 read 命令行中直接指定一个提示。**

运行脚本如下

```
#!/bin/bash

read -p "输入网站名:" website
echo "你输入的网站名是 $website" 
exit 0
```

测试结果为：

```
输入网站名:www.runoob.com
你输入的网站名是 www.runoob.com
```



## 2.2 > 覆盖 和 >> 追加





## 2.3 echo

echo [选项] [输出内容]       （输出内容到控制台）

| 选项 | 说明                     |
| ---- | ------------------------ |
| -n   | 不换行输出               |
| -e   | 支持反斜线控制的字符转换 |

| 控制字符 | 作用                |
| -------- | ------------------- |
| \\       | 输出\本身           |
| \n       | 换行符              |
| \t       | 制表符，也就是Tab键 |

 



## 2.4 ln链接

- ln -s [原文件或目录] [软链接名]  （给原文件创建一个软链接）
- ln [原文件或目录] [软链接名]   （给原文件创建一个链接）




## 2.5 时间

### date

①显示当前时间信息

```
[root@hadoop101 ~]# date
Wed Jun 16 10:28:01 CST 2021
```

②显示当前时间年月日

```
[root@hadoop101 ~]# date +%Y-%m-%d
2021-06-16
```

③显示当前时间年月日时分秒

```
[root@hadoop101 ~]# date "+%Y-%m-%d %H:%M:%S"
2021-06-16 10:27:41
```

④显示昨天

```
[root@hadoop101 ~]# date -d '1 days ago'
Tue Jun 15 10:26:48 CST 2021

[root@hadoop101 ~]# date -d '-1 days'
Tue Jun 15 10:26:48 CST 2021
```

⑤显示明天时间

```
[root@hadoop101 ~]# date -d '-1 days ago'
Thu Jun 17 10:27:22 CST 2021

[root@hadoop101 ~]# date -d '1 days'
Thu Jun 17 10:27:22 CST 2021
```

⑥显示上个月时间

```
[root@hadoop101 ~]# date -d '1 month ago'
Sun May 16 10:27:07 CST 2021

[root@hadoop101 ~]# date -d '-1 month'
Sun May 16 10:27:07 CST 2021
```

需要注意的是取下个月的命令存在bug，执行如下命令会得到21-10，但是正常应该得到21-09，需要注意
`date -d "2021-08-31 +1 month" +%y-%m`

⑦修改系统时间

```
[root@hadoop101 ~]# date -s "2017-06-19 20:52:18"
```

>date +%Y	（功能描述：显示当前年)
date +%m	（功能描述：显示当前月份）
date +%d		（功能描述：显示当前是哪一天）
date "+%Y-%m-%d %H:%M:%S"		（功能描述：显示年月日时分秒）
 

### cal

 查看日历

（1）查看当前月的日历

```
[root@hadoop101 ~]# cal
```

（2）查看2017年的日历

```
[root@hadoop101 ~]# cal 2017
```



## 2.6 压缩和解压缩

### tar

- tar -zcvf [压缩文件] [源文件] 		（压缩文件）
- tar -zxvf [文件] -C [解压路径]	（解压文件）

| tar  | 打包               |
| ---- | ------------------ |
| -z   | 打包同时压缩，.gz文件需要添加       |
| -c   | 产生.tar打包文件   |
| -v   | 显示详细信息       |
| -f   | 指定压缩后的文件名 |
| -x   | 解包.tar文件       |

例：

- `tar -zcvf houma.tar.gz houge.txt bailongma.txt`  将文件houge.txt和bailongma.txt压缩为houma.tar.gz

- `tar -zcvf xiyou.tar.gz xiyou/`   将目录进行压缩
- `tar -zxvf xiyou.tar.gz -C /opt`   解压到/opt目录下



### zip/unzip

对比gzip/gunzip，zip/unzip可以压缩文件和目录且保留源文件。

**①zip：压缩**

- zip  [选项] [生成的文件名]  [需要压缩的一个或多个文件]

| zip选项 | 功能     |
| ------- | -------- |
| -r      | 压缩目录 |



**②unzip：解压缩**

- unzip [选项] [文件]

| unzip | 解包                                      |
| :---- | ----------------------------------------- |
| -d    | 解包目录                                  |
| -f    | 更新现有的文件                            |
| -n    | 解压缩时不要覆盖原有的文件                |
| -P    | 使用zip的密码选项                         |
| -o    | 不必先询问用户，unzip执行后覆盖原有的文件 |

 

### **gzip/gunzip**

只能压缩文件不能压缩目录，不保留原来的文件。

gzip 文件 （只能将文件压缩为*.gz文件）

gunzip 文件.gz	（解压缩文件命令）





## 2.7 cron定时任务

- crontab [选项]

| crond | 系统定时任务                  |
| ----- | ----------------------------- |
| -e    | 编辑crontab定时任务           |
| -l    | 查询crontab任务               |
| -r    | 删除当前用户所有的crontab任务 |

例： crontab -e 

（1）进入crontab编辑界面。会打开vim编辑你的工作。

（2）每隔1分钟，向/root/bailongma.txt文件中添加一个11的数字

*/1 * * * * /bin/echo ”11” >> /root/bailongma.txt

（3）可以用tail  -f  目标文件来实施监控追加的内容


**查看日志**
 可以用tail -f /var/log/cron.log观察

Cron表达式见文章：<https://www.jianshu.com/writer#/notebooks/46619194/notes/75177408>



## 2.8 ls

**ls [选项] [目录或是文件]**

| 选项 | 功能                                                      |
| ---- | --------------------------------------------------------- |
| -a   | 全部的文件，连同隐藏档( 开头为 . 的文件) 一起列出来(常用) |
| -l   | 长数据串列出，包含文件的属性与权限等等数据；(常用)        |



## 2.9 cd

cd  [参数]

| 参数        | 功能                                 |
| ----------- | ------------------------------------ |
| cd 绝对路径 | 切换路径                             |
| cd 相对路径 | 切换路径                             |
| cd ~或者cd  | 回到自己的家目录                     |
| cd -        | 回到上一次所在目录                   |
| cd ..       | 回到当前目录的上一级目录             |
| cd -P       | 跳转到实际物理路径，而非快捷方式路径 |

**例：**cd  -P  \$(dirname \$p1) ； pwd  先跳转到文件的所在目录，再打印\$p1文件的实际路径



## 2.10 rm

- rm [选项] [deleteFile]	（删除文件或目录）

| 选项 | 功能                                     |
| ---- | ---------------------------------------- |
| -r   | 递归删除目录中所有内容                   |
| -f   | 强制执行删除操作，而不提示用于进行确认。 |
| -v   | 显示指令的详细执行过程                   |

 



## 2.11 复制

**概述**

①cp（copy）：只能在本机中复制

②scp（secure copy）：可以复制文件给远程主机

scp  -r  test.sh  hxr@hadoop102:/root

③rsync（remote sync）：功能与scp相同，但是不会改文件属性

rsync  -av  test.sh   test.sh  hxr@hadoop102:/root

④nc（netcat）：监听端口，可以实现机器之间传输文件。



### cp

- cp [选项] [sourcefile] [destfile] 				（功能描述：复制source文件到dest）

| 选项 | 功能                                                         |
| ---- | ------------------------------------------------------------ |
| -r   | 递归复制整个文件夹                                           |
| -a   | 复制目录后其文件属性会发生变化 想要使得复制之后的目录和原目录完全一样,可以使用cp -a |
| -d   | 如果复制的文件是软链接，那么复制后软链接不会失效 |
| -l    | 不复制文件，只是生成链接文件。 |

强制覆盖不提示的方法：\cp

 

### scp

- scp [选项] [文件] [用户@远程地址:路径]	（可以复制文件给远程主机）

| 选项 | 功能             |
| ---- | ---------------- |
| -r   | 递归复制整个目录 |
| -v   | 显示复制过程     |

例：scp  -r  test.sh  hxr@bigdata1:/root



### rsync

- rsync [选项] [文件] [用户@远程地址:路径]	（功能与scp相同，但是不会改文件属性）

| 选项 | 功能         |
| ---- | ------------ |
| -a   | 归档拷贝     |
| -v   | 显示复制过程 |
| --hard-links | 保留硬链结 |

例：rsync  -av  test.sh   hxr@bigdata1:/root



### nc

- nc [选项] 

| 选项 | 功能                                   |
| ---- | -------------------------------------- |
| -l   | 启动侦听模式                           |
| -p   | 指定监听端口                           |
| -w   | 超时秒数，后面跟数字                   |
| -v   | 输出交互或出错信息，新手调试时尤为有用 |
| -u   | 指定nc使用UDP协议，默认为TCP           |
| -s   | 指定发送数据的源IP地址，适用于多网卡机 |

例：

nc -lp 10000 > nc_test.txt

nc -w 1 hadoop102 < nc_test.txt



## 2.12 ssh

- ssh ip -l  root ip -p 22  ps -ef	（在指定节点上以root用户执行ps命令）
- ssh ip -l root	（以root用户登录到指定节点上）

远程登录时默认使用的私钥为~/.ssh/id_rsa

## 2.12.1 配置远程登陆
生成密钥对
```
ssh-keygen -t rsa
```
将公钥发送到本机
```
ssh-copy-id localhost
```
将密钥发送到需要登录到本机的服务器上
```
rsync -av id_rsa [user]@[ip]:~/.ssh
```
修改密钥的权限
```
chmod 600 id_rsa
```
远程登陆
```
ssh -i ~/.ssh/id_rsa [user]@[ip]
```
如果有多个节点需要远程登陆，可以在.ssh下创建config并输入
```
Host [alias]
  HostName [ip]
  User [user]
  Port 22
  IdentityFile ~/.ssh/id_rsa
```
再次登陆
```
ssh [alias]
```

<br>
### 2.12.2 启动ssh隧道
| 参数 | 说明 |
| --- | --- |
| -C | 使用压缩功能，是可选的，加快速度。 |
| -P | 用一个非特权端口进行出去的连接。 |
| -f | SSH完成认证并建立port forwarding后转入后台运行。 |
| -N | 不执行远程命令。该参数在只打开转发端口时很有用（V2版本SSH支持） |

**①正向代理：**
- 用法1：远程端口映射到其他机器
HostB 上启动一个 PortB 端口，映射到 HostC:PortC 上，在 HostB 上运行：
   ```
   HostB$ ssh -L 0.0.0.0:PortB:HostC:PortC user@HostC
   ```
   这时访问 HostB:PortB 相当于访问 HostC:PortC（和 iptable 的 port-forwarding 类似）。

- 用法2：本地端口通过跳板映射到其他机器
HostA 上启动一个 PortA 端口，通过 HostB 转发到 HostC:PortC上，在 HostA 上运行：
   ```
   HostA$ ssh -L 0.0.0.0:PortA:HostC:PortC  user@HostB
   ```
   这时访问 HostA:PortA 相当于访问 HostC:PortC。

>两种用法的区别是，第一种用法本地到跳板机 HostB 的数据是明文的，而第二种用法一般本地就是 HostA，访问本地的 PortA，数据被 ssh 加密传输给 HostB 又转发给 HostC:PortC。

<br>
**②反向代理：**
所谓“反向代理”就是让远端启动端口，把远端端口数据转发到本地。

HostA 将自己可以访问的 HostB:PortB 暴露给外网服务器 HostC:PortC，在 HostA 上运行：

```
HostA$ ssh -R HostC:PortC:HostB:PortB  user@HostC
```

那么链接 HostC:PortC 就相当于链接 HostB:PortB。
使用时需修改 HostC 的 /etc/ssh/sshd_config 的一条配置如下，不然启动的进程监听的ip地址为127.0.0.1，即只有本机可以访问该端口。
```
GatewayPorts yes
```

相当于内网穿透，比如 HostA 和 HostB 是同一个内网下的两台可以互相访问的机器，HostC是外网跳板机，HostC不能访问 HostA，但是 HostA 可以访问 HostC。
那么通过在内网 HostA 上运行 `ssh -R` 告诉 HostC，创建 PortC 端口监听，把该端口所有数据转发给我（HostA），我会再转发给同一个内网下的 HostB:PortB。
同内网下的 HostA/HostB 也可以是同一台机器，换句话说就是**内网 HostA 把自己可以访问的端口暴露给了外网 HostC。**

**例：**比如在我的内网机192.168.32.244上有一个RabbitMQ的客户端，端口号为15672。现在我希望在外网上访问固定ip的云服务器chenjie.asia的6009端口，通过跳板机192.168.32.243来转发请求到192.168.32.244:15672，从而实现在外网访问内网服务的功能，即内网穿透。
①在192.168.32.244上启动RabbitMQ服务
```
docker run -d -p 5672:5672 -p 15672:15672  --name rabbitmq rabbitmq:management
```
②将chenjie.asia云服务器的私钥复制到跳板机192.168.32.243的~/.ssh下，并重命名为id_rsa。通过如下命令看是否可以远程登陆到云服务，可以登陆则进行下一步。
```
[root@192.168.32.243 /]# ssh chenjie.asia
```
③修改chenjie.asia服务器的ssh配置文件 /etc/ssh/sshd_config ，允许其他节点访问
```
GatewayPorts yes
```
然后重启sshd服务
```
systemctl restart sshd
```
④在跳板机192.168.32.243启动ssh反向代理
```
ssh -R 0.0.0.0:6009:192.168.32.244:15672 root@chenjie.asia
```
这个进程在关闭session时会停止，可以添加启动参数 `-CPfN` 

>这样就实现了FRP等内网穿透框架的功能。相当于再 跳板机192.168.32.243上启动了 frpc，而再 云服务器chenjie.asia 上启动了 frps。


## 2.13 curl

- curl [选项] [URL]

| 选项 | 说明 |
|-----|-----|
| -A | 参数指定客户端的用户代理标头，即User-Agent |
| -b | 参数用来向服务器发送 Cookie |
| -d | 发送 POST 请求的数据体(会自动将请求类型转为POST) |
| -F | 用来向服务器上传二进制文件 |
| -G | 用来构造 URL 的查询字符串 |
| -H | 添加 HTTP 请求的标头 |
| -L | 让 HTTP 请求跟随服务器的重定向。curl 默认不跟随重定向 |
| --limit-rate | 限制 HTTP 请求和回应的带宽，模拟慢网速的环境 |
| -o | 将服务器的回应保存成文件，等同于wget命令 |
| -O | 将服务器回应保存成文件，并将 URL 的最后部分当作文件名 |
| -s | 不输出错误和进度信息 |
| -u | 设置服务器认证的用户名和密码 |
| -v | 输出通信的整个过程，用于调试 |
| -x | 指定 HTTP 请求的代理 |
| -X | 指定 HTTP 请求的方法 |

例：
- curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com
- curl -d "user=nickname&password=12345" http://www.yahoo.com/login.cgi
- curl -F 'file=@photo.png;filename=me.png' https://google.com/profile
- curl -G -d 'q=kitties' -d 'count=20' https://google.com/search （同https://google.com/search?q=kitties&count=20）
- curl -H 'Accept-Language: en-US' https://google.com
- curl --limit-rate 200k https://google.com  (带宽限制在每秒 200K 字节)
- curl -o example.html https://www.example.com  （将www.example.com保存成example.html）
- curl -s -o /dev/null https://google.com  （让 curl 不产生任何输出）
- curl -u 'hxr:12345' https://google.com/login  （设置用户名为bob，密码为12345，然后将其转为 HTTP 标头Authorization: Basic Ym9iOjEyMzQ1，同curl https://bob:12345@google.com/login）
- curl -x socks5://james:cats@myproxy.com:8080 https://www.example.com  （指定 HTTP 请求通过myproxy.com:8080的 socks5 代理发出）
- curl -X POST https://www.example.com  （发送POST请求）


## 2.14 setcap

以 root 身份执行的程序有了所有特权，这会带来安全风险。Kernel 从 2.2 版本开始，提供了 Capabilities 功能，它把特权划分成不同单元，可以只授权程序所需的权限，而非所有特权。

例如：linux不允许非root账号只用1024以下的端口，使用root启动命令nginx，会导致nginx权限过高太危险。所以用setcap命令

**sudo setcap cap_net_bind_service=+eip /bigdata/nginx/sbin/nginx**



## 2.15 关机重启命令

**正确的关机流程为**：sync > shutdown > reboot > halt

（1）sync  			（功能描述：将数据由内存同步到硬盘中）

（2）halt 			（功能描述：关闭系统，等同于shutdown -h now 和 poweroff）

（3）reboot 		（功能描述：就是重启，等同于 shutdown -r now）

（4）shutdown [选项] [时间]	

| 选项 | 功能          |
| ---- | ------------- |
| -h   | -h=halt关机   |
| -r   | -r=reboot重启 |

| 时间 | 功能                                   |
| ---- | -------------------------------------- |
| now  | 立刻关机                               |
| 时间 | 等待多久后关机（时间单位是**分钟**）。 |



| 常用快捷键 | 功能                    |
| ---------- | ----------------------- |
| ctrl + c   | 停止进程                |
| ctrl+l     | 清屏；彻底清屏是：reset |
| ctrl + q   | 退出                    |
| **上下键** | 查找执行过的命令        |
| ctrl +alt  | linux和Windows之间切换  |

## 2.16 history 查看已经执行过历史命令
- history		（功能描述：查看已经执行过历史命令）

## 2.17 mv
- mv [选项]  [源文件或目录] [目标文件或目录]

| 选项 | 说明 |
|---|---|
| -b |	若需覆盖文件，则覆盖前先行备份 |
| -f | 若目标文件或目录与现有的文件或目录重复，则直接覆盖现有的文 件或目录 |
| -i | 盖前先行询问用户 |
| --suffix=<附加字尾> | -b 参数一并使用，可指定备份文件的所要附加的字尾 |
| -u | 在移动或更改文件名时，若目标文件已存在，且其文件日期比源文件新，则不覆盖目标文件 |
| -v | 执行时显示详细的信息 |


## 2.18 telnet
- telnet [ip] [port]   用于检测端口是否正常开启

**安装**
`yum install -y telnet-server telnet`


## 2.19 jps
- jps   用于显示运行的java进程

| 选项 | 说明 |
|---|---|
| -l | 输出完全的包名，应用主类名，jar的完全路径名 |
| -m | 输出传入 main 方法的参数 |
| -q | 只输出进程 ID |
| -v | 输出jvm参数 |
| -V | 输出通过flag文件传递到JVM中的参数 |

## 2.20 删除乱码文件
`ls -i` 显示文件的节点号
`find -inum 节点号 -delete` 删除指定的节点即可删除对应的文件


<br>
# 三、系统相关命令

## 3.1 服务命令

### systemctl

启动一个服务：`systemctl start postfix.service`
关闭一个服务：`systemctl stop postfix.service`
重启一个服务：`systemctl restart postfix.service`
显示一个服务的状态：`systemctl status postfix.service`

在开机时启用一个服务：`systemctl enable postfix.service`
在开机时禁用一个服务：`systemctl disable postfix.service`
注：在enable的时候会打印出来该启动文件的位置



列出所有已经安装的服务及状态：
`systemctl list-units`
`systemctl list-unit-files`
查看服务列表状态:
`systemctl list-units --type=service`

查看服务是否开机启动： `systemctl is-enabled postfix.service`
查看已启动的服务列表： `systemctl list-unit-files | grep enabled`
查看启动失败的服务列表： `systemctl --failed`

查看服务日志：`journalctl -u postfix -n 10 -f`

### chkconfig

**命令类似systemctl，用于操作native service。**

添加脚本为服务(需要指定启动级别和优先级)：`chkconfig --add [脚本]`
删除服务：`chkconfig --del [脚本]`
单独查看某一服务是否开机启动的命令 ：`chkconfig --list [服务名]`
单独开启某一服务的命令 ：`chkconfig [服务名] on `
单独关闭某一服务的命令：`chkconfig [服务名] off`
查看某一服务的状态：`/etc/intd.d/[服务名] status`



启用服务就是在当前"runlevel"的配置文件目录  `/etc/systemd/system/multi-user.target.wants`里，建立 /usr/lib/systemd/system 里面对应服务配置文件的软链接；禁用服务就是删除此软链接，添加服务就是添加软连接。



## 3.2 用户命令

### 相关文件

```
# 查看所有用户
vim /etc/passwd 

# 查看关键用户
cat /etc/passwd|grep -v nologin|grep -v halt|grep -v shutdown|awk -F":" '{ print $1"|"$3"|"$4 }'|more

# 查看所有用户组
cat /etc/group
```


### useradd

- useradd 用户名			（功能描述：添加新用户）

- useradd -g 组名 用户名	（功能描述：添加新用户到某个组）
- useradd -G 组名 用户名 （功能描述：添加新用户到同名组同时添加到指定组）


### passwd

- passwd 用户名	（功能描述：设置用户密码）



### id

- id [用户名]		（查看用户的所在组等信息）

  

### su

su 用户名称   （切换用户，只能获得用户的执行权限，不能获得环境变量）

su - 用户名称		（切换到用户并获得该用户的环境变量及执行权限）

echo  \$PATH    打印环境变量



### userdel

- userdel  用户名		（功能描述：删除用户但保存用户主目录，即删除了/etc/passwd、/etc/shadow、/etc/group/、/etc/gshadow四个文件里的该账户和组的信息）

- userdel -r 用户名		（功能描述：删除用户和用户主目录，即除了删除用户信息，还会删除/home下用户文件和/var/spool/mail下用户邮箱。）
  
  



### who

- whoami	（功能描述：显示自身用户名称；sudo权限执行则whoami为root） 
- who am i	（功能描述：显示登录用户的用户名）



### sudo

**设置普通用户具有root权限**

修改 /etc/sudoers 文件，找到下面一行(91行)，在root下面添加一行，如下	所示：

```
hxr   ALL=(ALL)     ALL
```

或者配置成采用sudo命令时，不需要输入密码

```
hxr   ALL=(ALL)     NOPASSWD:ALL
```

修改完毕，现在可以用hxr 帐号登录，然后用命令 sudo ，即可获得root权限进行操作。

### 以某一用户执行命令
```
[root@bigdata1 ~]# sudo -i -u hxr yarn --daemon start nodemanager
```
- -i表示重新加载环境变量
- -u表示以该参数作为用户执行命令

```
[root@bigdata1 ~]# sudo -i -u azkaban bash -c "cd /opt/module/azkaban/azkaban-exec;bin/start-exec.sh"
```
以azkaban用户执行引号中的命令

### usermod

- usermod -g 用户组 用户名      （功能：将用户加入到用户组）
- usermod -a -G 用户组 用户名   （功能：原分组不变，将用户加入到其他用户组）

| 选项 | 功能                                   |
| ---- | -------------------------------------- |
| -g   | 修改用户的初始登录组，给定的组必须存在 |
| -a | 在原来所属组的基础上追加到另一个组 |

### gpasswd 
gpasswd -d [username] [groupname]   将用户从组中删除


## 3.3 用户组管理命令

用户组的管理涉及用户组的添加、删除和修改。组的增加、删除和修改实际上就是对	/etc/group文件的更新。

### 查看创建了哪些组

- cat  /etc/group 

### groups

- groups [用户] 	（查看用户所在组）

### newgrp 

- newgrp [组名]	（更新组内成员）

### groupadd

- groupadd [组名]	（ 新增组）

### groupdel 

- groupdel [组名]	（删除组）

### groupmod 

- groupmod  -n [新组名] [老组名]	（修改组）



## 3.4 文件命令

### chmod

![1623830113278.png](https://upload-images.jianshu.io/upload_images/21580557-6b66dc0e5bc848fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

0首位表示类型  - 代表文件     d 代表目录    l 链接文档(link file)

**三种特殊权限suid、sgid、sticky**
- suid：此文件的使用者在使用此文件的过程中会临时获得该文件的所有者的身份及部分权限，suid数字法表示为4；
   ```
   chmod u+s file
   chmod 4755 file

   -rwsr-xr-x. 1 root root 27832 Jun 10  2014 /usr/bin/passwd
   ```
- sgid：此文件的使用者在使用此文件的过程中会临时获得该文件的所有者的组及部分权限；sgid数字法表示为2；
   ```
   chmod g+s file
   chmod 2755 file

   -rwxr-sr-x. 1 root root 48568 Mar 23  2017 /bin/cat
   ```
- sticky：可以阻止用户滥用 w 写入权限(禁止操作别人的文档)；sticky数字法表示为1。
   ```
   chmod o+t file
   chmod 1755 file

   drwxrwxrwt. 17 root root 4096 Apr  4 10:02 /tmp
   ```
>可以将这几个数字进行累加，如果是6，表示4+2，即同时拥有suid和sgid权限。

例子:
- SUID: 
用户修改密码，是通过运行命令passwd来实现的。最终必须要修改/etc/passwd文件，如下是passwd命令和/etc/passwd文件的权限
   ```
   -rw-r--r-- 1 root root 2520 Jul 12 18:25 passwd
   -r-s--s--x 1 root root 16336 Feb 14 2003 /etc/passwd
   ```
   普通用户可以使用passwd命令进行密码的修改，但是普通用户无法对/etc/passwd文件进行修改，所以给passwd添加了SUID权限，当普通用户执行时临时获取了root用户的身份和权限。
- SGID: 
Linux系统有一个/dev/kmem的设备文件，是一个字符设备文件，里面存储了核心程序要访问的数据，包括用户的口令。所以这个文件不能给一般的用户读写，权限设为：
   ```
   cr--r----- 1 root system 2, 1 May 25 1998 kmem
   ```
   但ps等程序要读这个文件，而ps的权限设置如下：
   ```
   -r-xr-sr-x 1 bin system 59346 Apr 05 1998 ps
   ```
   这是一个设置了SGID的程序，而ps的用户是bin，不是root，所以不能设置 SUID来访问kmem，但bin和root都属于system组，而且ps设置了SGID，一般用户执行ps，就会获得system组用户的权限，而文件kmem的同组用户的权限是可读，所以一般用户执行ps就没问题了。
- SBIT（Sticky Bit）目前只针对目录有效，对于目录的作用是：当用户在该目录下建立文件或目录时，仅有自己与 root才有权力删除。
最具有代表的就是/tmp目录，任何人都可以在/tmp内增加、修改文件（因为权限全是rwx），但仅有该文件/目录建立者与 root能够删除自己的目录或文件。

<br>
**变更文件权限方式一**

- chmod  [{ugoa}{+-=}{rwx}] [文件或目录]	（修改文件或目录的权限）

例：chmod u-x,o+x houge.txt

**变更文件权限方式二**

- chmod  [mode=421 ]  [文件或目录]	（修改文件或目录的权限）

例：chmod  -R  777  /mnt/  修改整个文件夹的文件权限



| 选项 | 功能     |
| ---- | -------- |
| -R   | 递归操作 |

  

### chown

- chown [选项] [最终用户] [文件或目录]	（改变文件所有者）

| 选项 | 功能     |
| ---- | -------- |
| -R   | 递归操作 |

例：递归改变文件所有者和所有组 chown  -R  hxr:hxr  /mnt



### chgrp 

- chgrp [最终用户组] [文件或目录]	（改变文件所属组）



## 3.5 查找命令

### find

- find [搜索范围] [选项]	（查找文件或者目录）

| 选项            | 功能                                      |
| --------------- | ----------------------------------------- |
| -name<包含字符> | 以文件或目录名查找                        |
| -user<用户名>   | 查找属于指定用户名的所有文件              |
| -size<文件大小> | 按照文件大小查找  +n 大于  -n小于   n等于 |



### grep 

- grep [选项] [查找内容] [源文件]	（过滤查找，可以使用"|"管道符）

| 选项 | 功能                       |
| ---- | -------------------------- |
| -n   | 显示匹配行及行号。         |
| -r   | 递归查找当前目录及其子目录 |
| -i   | 忽略大小写                 |
| -v   | 排除字段                   |
| -E   | 正则查找                   |

例：

- ps -ef | grep -E namenode | grep -v grep | wc -l	（正则匹配namenode的进程，然后进行计数）

- grep -E '123|abc' test.txt	（找出文件test.txt中包含123或者包含abc的行）
  egrep '123|abc' test.txt	（用egrep同样可以实现）

  awk '/123|abc/' filename	（用awk实现同样的功能）

- grep -rn "bigdata123" *  （查找当前目录下所有文件文本中包含指定文本的文件，-r表示递归，-n显示行号）


### which 

- whichis  [命令]	（查找命令脚本所在位置）





## 3.6 软件管理

### rpm

- rpm -qa	（功能描述：查询所安装的所有rpm软件包）
- rpm -qa | grep [软件名]	（一般会采用过滤查询）
- rpm -ivh [RPM包全名]	（安装rpm包）

- rpm -e --nodeps 软件包	（不管依赖直接卸载）

| 选项     | 功能                                                         |
| -------- | ------------------------------------------------------------ |
| -qa      | 查询所有安装包                                               |
| -i       | -i=install，安装                                             |
| -v       | -v=verbose，显示详细信息                                     |
| -h       | -h=hash，进度条                                              |
| -U       | -U=update，升级                                              |
| -e       | 卸载软件包                                                   |
| --nodeps | 卸载软件时，不检查依赖。这样的话，那些使用该软件包的软件在此之后可能就不能正常工作了。 |

 例：rpm –ivh <http://www.linuxcast.net/software.rpm>	(支持通过http\ftp协议形式安装)



### yum

YUM（全称为 Yellow dog Updater, Modified）是一个在Fedora和RedHat以及CentOS中的Shell前端软件包管理器。基于RPM包管理，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软件包，无须繁琐地一次次下载、安装。

- yum [选项] [参数]

| 选项         | 功能                          |
| ------------ | ----------------------------- |
| -y           | 对所有提问都回答“yes”         |
| search   | 搜索可安装的软件   |
| install      | 安装单个软件                 |
| groupinstall | 安装一个安装包，安装包中包含了多个软件 |
| update       | 更新rpm软件包                 |
| check-update | 检查是否有可用的更新rpm软件包 |
| remove       | 删除指定的rpm软件包           |
| list         | 显示软件包信息                |
| clean        | 清理yum过期的缓存             |
| deplist      | 显示yum软件包的所有依赖关系   |

**显示已经安装的软件包**
- yum list installed

**查找可以安装的软件包 **
- yum list tomcat



**修改网络YUM源**

默认的系统YUM源，需要连接国外apache网站，网速比较慢，可以修改关联的网络YUM源为国内镜像的网站，比如阿里云或网易163。

```
1) 安装wget
yum install -y wget
2) 备份/etc/yum.repos.d/CentOS-Base.repo文件
cd /etc/yum.repos.d/
mv CentOS-Base.repo CentOS-Base.repo.back
3) 下载阿里云的Centos-6.repo文件
wget -O CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
4) 重新加载yum
yum clean all
yum makecache
```





### wget

yum install -y wget

- wget [选项] [url]	（网络文件下载）

| 选项         | 功能                          |
| ------------ | ----------------------------- |
| -d           | 打印大量调试信息              |
| -q           | 安静模式 (无信息输出)         |
| -i           | 下载本地或外部 FILE 中的 URLs |

例：

- wget -d http://192.168.1.168	（下载192.168.1.168首页并且显示下载信息）

- wget -q http://192.168.1.168	（下载192.168.1.168首页并且不显示任何信息）

- wget -i filelist.txt	（批量下载的情形，把所有需要下载文件的地址放到 filename.txt 中，然后 wget 就会自动为你下载所有文件了）





## 3.7 系统信息命令

**常用的命令**

| 选项     | 描述                            |
| -------- | ------------------------------- |
| top      | 查看进程所占用的内存、cpu等信息 |
| df -h    | 查看磁盘存储情况                |
| iotop    | 查看进程的磁盘io读写            |
| iotop -o | 查看磁盘io读写占用较高的进程    |
| uptime   | 查看报告系统运行时长            |
| ps -ef   | 查看进程                        |





### netstat

netstat -anp |grep 进程号	（显示网络统计信息和端口占用情况）

```
	netstat -nlp	| grep 端口号	（功能描述：查看网络端口号占用情况）
```

| 选项 | 功能                                     |
| ---- | ---------------------------------------- |
| -n   | 拒绝显示别名，能显示数字的全部转化成数字 |
| -l   | 仅列出有在listen（监听）的服务状态       |
| -p   | 表示显示哪个进程在调用                   |
| -t   | 仅显示tcp相关选项                        |
| -u   | 查看所有的udp连接                        |



### ps

- ps  aux | grep xxx		（功能描述：查看系统中所有进程，可以加管道符筛选）

- ps  -ef | grep xxx		（功能描述：可以查看子父进程之间的关系）

注：如果想查看进程的**CPU占用率和内存占用率**，可以使用aux; 如果想查看**进程的父进程ID**可以使用ef;

| 选项 | 功能                         |
| ---- | ---------------------------- |
| -a   | 选择所有进程                 |
| -u   | 显示所有用户的所有进程       |
| -x   | 显示没有终端的进程           |
| -ef  | 显示所有进程信息，连同命令行 |

**ps aux显示信息说明**

![1623834519328.png](https://upload-images.jianshu.io/upload_images/21580557-d3d7fc0bde8d80fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> USER：该进程是由哪个用户产生的;
> PID：进程的ID号;
> %CPU：该进程占用CPU资源的百分比，占用越高，进程越耗费资源；
> %MEM：该进程占用物理内存的百分比，占用越高，进程越耗费资源；
> VSZ：该进程占用虚拟内存的大小，单位KB；
> RSS：该进程占用实际物理内存的大小，单位KB；
> TTY：该进程是在哪个终端中运行的。其中tty1-tty7代表本地控制台终端，tty1-tty6是本地的字符界面终端，tty7是图形终端。pts/0-255代表虚拟终端。
> STAT：进程状态。常见的状态有：R：运行、S：睡眠、T：停止状态、s：包含子进程、+：位于后台
> START：该进程的启动时间
> TIME：该进程占用CPU的运算时间，注意不是系统时间
> COMMAND：产生此进程的命令名


**ps -ef显示信息说明**

![1623834568481.png](https://upload-images.jianshu.io/upload_images/21580557-c66db336d5852c1c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> UID：用户ID 
> PID：进程ID 
> PPID：父进程ID 
> C：CPU用于计算执行优先级的因子。数值越大，表明进程是CPU密集型运算，执行优先级会降低；数值越小，表明进程是I/O密集型运算，执行优先级会提高。
> STIME：进程启动的时间 
> TTY：完整的终端名称 
> TIME：CPU时间 
> CMD：启动进程所用的命令和参数





### kill

- kill  [选项] [进程号]	（功能描述：通过进程号杀死进程）

- killall [进程名称]	（功能描述：通过进程名称杀死进程，也支持通配符，这在系统因负载过大而变得很慢时很有用）	

| 选项 | 功能                 |
| ---- | -------------------- |
| -9   | 表示强迫进程立即停止 |

 

### pstree 

- pstree [选项]	（查看进程树）

| 选项 | 功能               |
| ---- | ------------------ |
| -p   | 显示进程的PID      |
| -u   | 显示进程的所属用户 |

### 

### netstat

- netstat [选项]

| netstat | 显示网络统计信息和端口占用情况           |
| ------- | ---------------------------------------- |
| -n      | 拒绝显示别名，能显示数字的全部转化成数字 |
| -l      | 仅列出有在listen（监听）的服务状态       |
| -p      | 表示显示哪个进程在调用                   |
| -t      | TCP                                      |
| -u      | UDP                                      |
| -a      | 展示全部的连接                           |
| –i      | 显示网卡列表                             |

> **显示结果**
>
> - Proto:协议名（tcp协议还是udp协议)；
> - recv-Q:网络接收队列
>   表示收到的数据已经在本地接收缓冲，但是还有多少没有被进程取走，recv()；
>   如果接收队列Recv-Q一直处于阻塞状态，可能是遭受了拒绝服务 denial-of-service 攻击；
> - send-Q:网路发送队列
>   对方没有收到的数据或者说没有Ack的,还是本地缓冲区。
>   如果发送队列Send-Q不能很快的清零，可能是有应用向外发送数据包过快，或者是对方接收数据包不够快；
> - Local Address：监听的地址。0.0.0.0表示本地所有IPv4地址，127.0.0.1表示本机的loopback地址，::表示监听本地所有IPv6地址，::1表示IPv6的loopback地址
1)Local Address 部分的0.0.0.0:22 表示监听服务器上所有ip地址的所有(0.0.0.0表示本地所有ip)，比如你的服务器是有172.172.230.210和172.172.230.11两个ip地址，那么0.0.0.0:22此时表示监听172.172.230.210,172.172.230.211,127.0.0.1三个地址的22端口
2):::22 这个也表示监听本地所有ip的22端口，跟上面的区别是这里表示的是IPv6地址，上面的0.0.0.0表示的是本地所有IPv4地址
NOTE：“:::” 这三个: 的前两个"::"，是"0:0:0:0:0:0:0:0"的缩写，相当于IPv6的"0.0.0.0"，就是本机的所有IPv6地址，第三个:是IP和端口的分隔符
3)127.0.0.1:631 这个表示监听本机的loopback地址的631端口(如果某个服务只监听了回环地址，那么只能在本机进行访问，无法通过tcp/ip 协议进行远程访问)
4)::1:631 这个表示监听IPv6的回环地址的631端口,::1这个表示IPv6的loopback地址
5)172.172.230.211:3306 这里我们看到我们的mysqld进程监听的是172.172.230.211的3306端口,这是因为我们在启动的时候指定了bind_address=172.172.230.211参数，如果不指定bind_address的话，mysqld默认监听:::3306(本机所有ip地址的3306端口 -IPv6)
> - Foreign Address：与本机端口通信的外部socket。显示规则与Local Address相同；
> - State：连接状态，状态表如下；
> - PID/Program：PID即进程id，Program即使用该socket的应用程序；

| 状态        | 描述                                                         |
| ----------- | ------------------------------------------------------------ |
| LISTEN      | 首先服务端需要打开一个socket进行监听，状态为LISTEN./* The socket is listening for incoming connections. 侦听来自远方TCP端口的连接请求 */ |
| SYN_SENT    | 客户端通过应用程序调用connect进行active open.于是客户端tcp发送一个SYN以请求建立一个连接.之后状态置为SYN_SENT./*The socket is actively attempting to establish a connection. 在发送连接请求后等待匹配的连接请求 */ |
| SYN_RECV    | 服务端应发出ACK确认客户端的 SYN,同时自己向客户端发送一个SYN. 之后状态置为SYN_RECV/* A connection request has been received from the network. 在收到和发送一个连接请求后等待对连接请求的确认 */ |
| ESTABLISHED | 代表一个打开的连接，双方可以进行或已经在数据交互了。/* The socket has an established connection. 代表一个打开的连接，数据可以传送给用户 */ |
| FIN_WAIT1   | 主动关闭(active close)端应用程序调用close，于是其TCP发出FIN请求主动关闭连接，之后进入FIN_WAIT1状态./* The socket is closed, and the connection is shutting down. 等待远程TCP的连接中断请求，或先前的连接中断请求的确认 */ |
| CLOSE_WAIT  | 被动关闭(passive close)端TCP接到FIN后，就发出ACK以回应FIN请求(它的接收也作为文件结束符传递给上层应用程序),并进入CLOSE_WAIT./* The remote end has shut down, waiting for the socket to close. 等待从本地用户发来的连接中断请求 */ |
| FIN_WAIT2   | 主动关闭端接到ACK后，就进入了 FIN-WAIT-2 ./* Connection is closed, and the socket is waiting for a shutdown from the remote end. 从远程TCP等待连接中断请求 */ |
| LAST_ACK    | 被动关闭端一段时间后，接收到文件结束符的应用程 序将调用CLOSE关闭连接。这导致它的TCP也发送一个 FIN,等待对方的ACK.就进入了LAST-ACK ./* The remote end has shut down, and the socket is closed. Waiting for acknowledgement. 等待原来发向远程TCP的连接中断请求的确认 */ |
| TIME_WAIT   | 在主动关闭端接收到FIN后，TCP 就发送ACK包，并进入TIME-WAIT状态。/* The socket is waiting after close to handle packets still in the network.等待足够的时间以确保远程TCP接收到连接中断请求的确认 */ |
| CLOSING     | 比较少见./* Both sockets are shut down but we still don’t have all our data sent. 等待远程TCP对连接中断的确认 */ |
| CLOSED      | 被动关闭端在接受到ACK包后，就进入了closed的状态。连接结束./* The socket is not being used. 没有任何连接状态 */ |
| UNKNOWN     | 未知的Socket状态。/* The state of the socket is unknown. */  |



### top

- top [选项]	（检查系统的内存和系统健康情况）

| 选项    | 功能                                                         |
| ------- | ------------------------------------------------------------ |
| -d 秒数 | 指定top命令每隔几秒更新。默认是3秒在top命令的交互模式当中可以执行的命令： |
| -i      | 使top不显示任何闲置或者僵死进程。                            |
| -p      | 通过指定监控进程ID来仅仅监控某个进程的状态。                 |

**查使用内存最多的K个进程**

- `ps -aux | sort -k4nr | head -K`
- top (然后按下大写M)

**查看CPU个数**
- top  进入监控页面，再输入数字1，就可以看到CPU个数

**查询结果字段解释**

![1623833857693.png](https://upload-images.jianshu.io/upload_images/21580557-f5bb0e94f5c2af58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


第一行信息为任务队列信息

| 内容                             | 说明                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| 16:58:20                         | 系统当前时间                                                 |
| up 40 day, 1:29                  | 系统的运行时间，本机已经运行40天1小时29分钟                  |
| 4 users                          | 当前登录了4个用户                                            |
| load  average:  0.05, 0.11, 0.13 | 系统在之前1分钟，5分钟，15分钟的平均负载。一般认为小于1时，负载较小。如果大于1，系统已经超出负荷。 |

第二行为进程信息

| 内容              | 说明                                      |
| ----------------- | ----------------------------------------- |
| Tasks:  254 total | 系统中的进程总数                          |
| 1 running         | 正在运行的进程数                          |
| 253 sleeping      | 睡眠的进程                                |
| 0 stopped         | 正在停止的进程                            |
| 0 zombie          | 僵尸进程。如果不是0，需要手工检查僵尸进程 |

第三行为CPU信息

| 内容            | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| Cpu(s):  1.6%us | 用户模式占用的CPU百分比                                      |
| 1.3%sy          | 系统模式占用的CPU百分比                                      |
| 0.0%ni          | 改变过优先级的用户进程占用的CPU百分比                        |
| 97.1%id         | 空闲CPU的CPU百分比                                           |
| 0.0%wa          | 等待输入/输出的进程的占用CPU百分比                           |
| 0.0%hi          | 硬中断请求服务占用的CPU百分比                                |
| 0.0%si          | 软中断请求服务占用的CPU百分比                                |
| 0.0%st          | st（Steal  time）虚拟时间百分比。就是当有虚拟机时，虚拟CPU等待实际CPU的时间百分比。 |

第四行为物理内存信息

| 内容                   | 说明                   |
| ---------------------- | ---------------------- |
| Mem:    16266728 total | 物理内存的总量，单位KB |
| 1612956 free           | 空闲的物理内存数量     |
| 8445832 used           | 已经使用的物理内存数量 |
| 6207940 buffer         | 作为缓冲的内存数量     |

第五行为交换分区（swap）信息

| 内容                 | 说明                         |
| -------------------- | ---------------------------- |
| Swap:   839676 total | 交换分区（虚拟内存）的总大小 |
| 758268 free          | 空闲交换分区的大小           |
| 81408 used           | 已经使用的交互分区的大小     |
| 7312256 avail Mem    | 作为缓存的交互分区的大小     |

 
top命令第六行
| 内容                 | 说明                         |
| -------------------- | ---------------------------- |
| PID  | 进程ID |
| USER   | 进程所有者 |
| PR   | 优先级 |
| NI   | nice值，负值表示高优先级，正值表示低优先级 |
| VIRT   | 进程使用的虚拟内存总量，即进程新申请的内存 VIRT = SWAP + RES |
| RES  | 进程当前使用的内存大小 |
| SHR | 除了自身进程的共享内存，也包括其他进程的共享内存 |
| S | 进程状态 |
| %CPU | 上次更新到现在的CPU时间占用百分比 |
| %MEM | 进程使用的物理内存百分比 |
| TIME+  | 进程使用CPU总时间 |
| COMMAND | 命令名、命令行 |

堆、栈分配的内存，如果没有使用是不会占用实存的，只会记录到虚存。
如果程序占用实存比较多，说明程序申请内存多，实际使用的空间也多。
如果程序占用虚存比较多，说明程序申请来很多空间，但是没有使用。
工作中，遇到过有的程序虚存300G+， 实存只有不到15G。

### iotop

需要安装一下：yum install iotop

- iotop	（查看磁盘IO读写情况）
- iotop  -o	（直接查看输出比较高的磁盘读写程序）



### df

**disk free查看磁盘空间使用情况**

- df  [选项]	（列出文件系统的整体磁盘使用量，检查文件系统的磁盘空间占用情况）

| 选项 | 功能                                                     |
| ---- | -------------------------------------------------------- |
| -h   | 以人们较易阅读的 GBytes, MBytes, KBytes 等格式自行显示； |



### fdisk

- fdisk [选项]	（查看分区，该命令必须在root用户下才能使用）

| 选项 | 功能                         |
| ---- | ---------------------------- |
| -l   | 显示所有硬盘的分区列表       |
| -u   | 与"-l"搭配使用，显示分区数目 |

> 分区说明：
> Device：分区序列
> Boot：引导
> Start：从X磁柱开始
> End：到Y磁柱结束
> Blocks：容量
> Id：分区类型ID
> System：分区类型



### **mount/umount 挂载/卸载**

没有图形化界面，想看某一内存上的内容就需要挂载，从挂载点进入查看里面的文件

- mount [-t vfstype] [-o options] device dir	（功能描述：挂载设备）

- umount [设备文件名或挂载点]	（功能描述：卸载设备）

| 参数       | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| -t vfstype | 指定文件系统的类型，通常不必指定。mount 会自动选择正确的类型。常用类型有：光盘或光盘镜像：iso9660DOS fat16文件系统：msdos[Windows](http://blog.csdn.net/hancunai0017/article/details/6995284) 9x fat32文件系统：vfatWindows NT ntfs文件系统：ntfsMount Windows文件[网络](http://blog.csdn.net/hancunai0017/article/details/6995284)共享：smbfs[UNIX](http://blog.csdn.net/hancunai0017/article/details/6995284)(LINUX) 文件网络共享：nfs |
| -o options | 主要用来描述设备或档案的挂接方式。常用的参数有：loop：用来把一个文件当成硬盘分区挂接上系统ro：采用只读方式挂接设备rw：采用读写方式挂接设备　  iocharset：指定访问文件系统所用字符集 |
| device     | 要挂接(mount)的设备                                          |
| dir        | 设备在系统上的挂接点(mount point)                            |

![wps9.jpg](https://upload-images.jianshu.io/upload_images/21580557-4d35c510dd0f6861.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**开机自动挂载方法：**
打开文件 vi /etc/fstab，添加红框中的内容

![wps10.jpg](https://upload-images.jianshu.io/upload_images/21580557-3f9ef9639d2ddc00.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 查看网络和网卡
ifconfig 或 ip addr

如使用ip addr命令，得到如下打印
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:50:56:8c:82:a9 brd ff:ff:ff:ff:ff:ff
    inet 192.168.101.184/24 brd 192.168.101.255 scope global noprefixroute ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::ac2a:9aa0:1b84:f5ac/64 scope link tentative noprefixroute dadfailed 
       valid_lft forever preferred_lft forever
    inet6 fe80::6a5f:e756:ca09:7d43/64 scope link tentative noprefixroute dadfailed 
       valid_lft forever preferred_lft forever
    inet6 fe80::c12c:47c5:df6d:944d/64 scope link tentative noprefixroute dadfailed 
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:0c:04:4f:c2 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
```
lo是回环网卡。
eth0是阿里云的内网网卡。
docker0是docker创建的网卡。


### 查看核心数

总核数 = 物理CPU个数 X 每颗物理CPU的核数 
总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数

查看物理CPU个数
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

查看每个物理CPU中core的个数(即核数)
cat /proc/cpuinfo| grep "cpu cores"| uniq

查看逻辑CPU的个数
cat /proc/cpuinfo| grep "processor"| wc -l

通过top命令查看CPU个数
top  进入监控页面，再输入数字1，就可以看到CPU个数


### 查看系统架构
uname -a

### 查看静态/临时用户名，系统架构，系统版本等信息
hostnamectl


### 修改hostname
修改hostname有几种方式？
1.  hostname DB-Server                            --运行后立即生效（新会话生效），但是在系统重启后会丢失所做的修改

2. echo DB-Server  > /proc/sys/kernel/hostname  --运行后立即生效（新会话生效），但是在系统重启后会丢失所做的修改

3. sysctl kernel.hostname=DB-Server              --运行后立即生效（新会话生效），但是在系统重启后会丢失所做的修改

4. 修改/etc/sysconfig/network下的HOSTNAME变量，即HOSTNAME=[hostname].localdomain     --需要重启生效，永久性修改。


# 四、配置文件

## 常用配置文件位置

/etc/hosts	本地dns映射地址
/etc/profile 	
/etc/selinux/config		setenforce(临时更改指令：`sudo setenforce 0`)
/etc/sysconfig/network-scripts/ifcfg-eth0	网络配置
/etc/udev/rules.d/7-persistent-net.rules 网卡配置
/etc/sysconfig/network	修改主机名
/etc/sudoers		用户权限

/etc/ntp.conf		ntp时间同步的配置文件
/etc/sysconfig/ntpd		设置系统时间与硬件时间同步

/etc/selinux/config	或  /etc/sysconfig/selinux	安全系统配置文件disable ，可以用指令`sudo setenforce 0`使安全防护临时失效（cdm集群使用ganglia需要将其关闭）

/etc/yum/pluginconf.d/refresh-packagekit.conf	禁止离线更新

/etc/init.d/ntpd restart



## 关闭Linux的THP服务

vim /etc/grub.conf 
添加 transparent_hugepage=never
vim /etc/rc.local
添加：

```shell
if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
  echo never > /sys/kernel/mm/transparent_hugepage/defrag
fi
if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
  echo never > /sys/kernel/mm/transparent_hugepage/enabled
fi
exit 0
```

重启之后，用下面的命令检查：

```
cat /sys/kernel/mm/redhat_transparent_hugepage/enabled
```



## 用户所创建目录的初始权限

[root@hadoop102 ~]# umask 0022   //初始权限为755

always madvise [never]
有 [never]则表示THP被禁用

vim /etc/yum/pluginconf.d/refresh-packagekit.conf	修改：enabled=0		禁止离线更新



## 修改最大文件数和最大进程数

 **①vi /etc/security/limits.conf** ，修改如下内容：

```
   * soft nofile 65536
   * hard nofile 131072
   * soft nproc 4096
   * hard nproc 4096
```

   **②vi /etc/security/limits.d/XX-nproc.conf**，修改为：

```
   * soft nproc 4096
```

   **③vi /etc/sysctl.conf**，添加如下内容：

```
   vm.max_map_count=655360
```

   **④使系统文件生效**

```
   sysctl -p
```



## Hadoop权限不足的问题

解决办法 ：在执行程序的Edit Configurations中 做如下设置，把VM options或Environment variables中加入
-DHADOOP_USER_NAME=xxxxxx （你的hadoop用户）
或System.setProperty("HADOOP_USER_NAME"，“hxr”)



### 时区设置

先配置好服务器节点上的时区
1） 如果在/usr/share/zoneinfo/这个目录下不存在时区配置文件Asia/Shanghai，就要用 tzselect 生成。
 tzselect

2）拷贝该时区文件，覆盖系统本地时区配置
rm /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

3）集群时间同步（同时发给三个窗口）
 sudo date -s '2018-10-18 16:39:30'

<br>
# 参考
http://www.ruanyifeng.com/blog/2019/09/curl-reference.html
