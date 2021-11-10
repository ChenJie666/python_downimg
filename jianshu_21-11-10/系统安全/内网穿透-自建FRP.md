#一、概念
- ipv4：IP(Internet Protocol，互联网协议)是网络层的一个被路由协议，是一个封装协议或标识协议，它封装了一个非常重要的标识信息就是IP地址，IP地址用来标识网络中的主机。

| 类型          | 地址块                                             | 地址范围                                                     |
| ------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| 默认路由      | 224.0.0.0/4                                        | 224.0.0.0-239.255.255.255                                    |
| 有限广播地址  | -                                                  | 255.255.255.255                                              |
| 环回地址      | 127.0.0.0/8                                        | 127.0.0.0-127.255.255.255                                    |
| Test-Nest地址 | 190.0.2.0/24                                       | 190.0.2.0-192.255.255.255                                    |
| 链路本地地址  | 169.254.0.0/16                                     | 169.254.0.0-169.254.255.255                                  |
| 私有地址空间  | 10.0.0.0/18<br />172.16.0.0/12<br />192.168.0.0/16 | 10.0.0.0-10.255.255.255<br />172.16.0.0-172.31.255.255<br />192.168.0.0-192.168.255.255 |
| 多播          | 224.0.0.0/4                                        | 224.0.0.0-239.255.255.255                                    |
| 实验地址      | 240.0.0.0/4                                        | 224.0.0.0-255.255.255.254                                    |

- 端口：在Internet上，各主机间通过TCP/IP协议发送和接收数据包，各个数据包根据其目的主机的ip地址来进行互联网络中的路由选择。为了把数据包发送到目的主机的指定进程中，引入了端口机制。当目的主机接收到数据包后，将根据报文首部的目的端口号，把数据发送到相应端口，而与此端口相对应的那个进程将会领取数据并等待下一组数据的到来。
　
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7eb21bf32b3b618b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**简单理解内网机与外网通讯过程：**
1. 路由器实现了网关的功能，其wan口连接外网，获得了公网ip，其lan口连接的是内网，分配了私有ip。
2. 计算机接入到局域网中，路由器如果开启了DHCP，会自动为该计算机分配一个内网地址。
3. 当该内网机的某一个进程与外网机通讯时，会携带自己的ip:port信息。当数据包进入路由器后，路由器会修改该数据包的源地址为自己的外网地址，并分配一个端口。同时将端口映射信息记录到NAT表中。
4. 外网机收到数据包，并向修改后的地址(即路由器地址)返回数据。数据到达路由器后，查询NAT表再将地址改为内网机地址和端口，并转发到指定的内网机端口上。
5. 相反的，**外网机无法主动与内网机进行连接**。因为无法通过私有地址在公网上定位这个内网机。



<br>
# 二、解决方案
##2.1 端口映射
添加路由器端口与内网IP和端口的映射，当外网请求该端口时，会根据配置的映射规则将数据包路由到指定的内网机中。这样外部可以通过公网IP和端口号，来访问内网的设备。


**但是国内环境很难做到通过端口映射访问内网机：** 获取的IP并不是真正的公网IP，而是上层路由器的私有地址。层层嵌套，而我们无法对上层路由器进行端口映射。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-2572fdb24afa8114.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

DDNS：因为是动态IP，会经常变动。需要在你的主路由上设置DDNS，每隔几分钟扫描一次，并把变化传递到域名服务器，让域名也时时刻刻和动态IP绑定。

## 2.2 内网穿透
NAT可以分为锥型和对称型，其中锥型又可以分为完全锥型和限制型锥型，限制型锥型又可分为ip限制型锥型和端口限制型锥型。

- 锥型：锥型NAT的特点是，主动使用同样的端口去和不同的服务器或和相同的服务器，不同的端口建立连接时，NAT的映射也会使用同样的端口；
  - 完全锥型：如果在NAT网关已经建立了一个NAT映射，那么任何外网的机器都可以通过这个映射来访问内网的电脑；
  - ip限制型锥型：如果在NAT网关已经建立了一个NAT映射，那么只有与其建立映射的ip才能通过NAT访问内网的电脑。
  - 端口限制型锥型：在ip限制型锥型的基础上，对端口同样有限制。即如果在NAT网关已经建立了一个NAT映射，那么只有与其建立映射的ip和端口才能通过NAT访问内网的电脑。
- 对称型：对称型特点是，每次内网机访问外网NAT都会随机映射端口。只有和内网机建立连接的ip和端口向其发送数据才不会被丢弃。对称型NAT和端口限制型锥型是一样的，对ip和端口都有限制。

### 2.2.1 UDP打洞
UDP打洞是使两个处于NAT中的内网机通过服务端的协调直接建立连接。

两个NAT中的内网机需要进行UDP打洞，下图展示了不同NAT类型是否可以实现打洞。
| 类型       | 类型       | 是否支持打洞   |
| ------------ | ------------ | -------- |
| 全锥型       | 全锥型       | 全锥型   
| 全锥型       | 受限锥型     | 支持     |
| 全锥型       | 端口受限锥型 | 支持     |
| 全锥型       | 对称型       | 支持     |
| 受限锥型     | 受限锥型     | 支持     |
| 受限锥型     | 端口受限锥型 | 支持     |
| 受限锥型     | 对称型       | 支持     |
| 端口受限锥型 | 端口受限锥型 | 支持     |
| 端口受限锥型 | 对称型       | 无法打通   |
| 对称型       | 对称型       | 无法打通 |

**第一种：完全锥型NAT和完全锥型NAT进行穿透**
A和B是两个完全锥型的NAT，其穿透流程如下：
1. A和B都连接到服务端后，服务端知道了A和B的外网ip和端口。
2. 服务端通知A向B发送消息，因为B已经和服务端建立了连接，所以NAT映射是存在的（消息到达NAT后会转发到对应的内网机)且完全锥型NAT允许任何外网的机器通过这个映射来访问内网的电脑。
3. 这样A就可以与B建立UDP连接。同理B与A也可以建立UDP连接。

**第二种：ip限制型NAT和ip限制型NAT进行穿透**
A和B是两个完全锥型的NAT，其穿透流程如下：
1. 任何外网的机器都可以通过这个映射来访问内网的电脑
2. 服务端通知A向B发送消息，因为B已经和服务端建立了连接，所以NAT映射是存在的（消息到达NAT后会转发到对应的内网机)，但是ip限制型NAT只允许与其建立连接的ip才能通过NAT访问内网的电脑。A发送给B的数据包都被B丢弃了。
3. 服务端通知B向A发送消息，因为A已经建立了与B通讯的映射(锥型NAT的同一内网机会复用已有的映射)，那么A就可以收到B的消息，接着A会给B发送一个同意建立连接的请求，最终二者建立了一个稳定的UDP连接。

**第三种：端口限制型NAT和端口限制型NAT进行穿透**
原理和第二种差不多。


**优点：**服务端可以理解为红娘，只是为两个NAT进行牵线，当两个NAT建立连接后即可直接进行通讯，服务端不参与通讯，即服务端的带宽不影响通讯。

**缺点：**家里的路由器（包括办宽带时送的光猫），使用的都是完全锥型NAT，但是上层的机房为了公共安全，使用的一般都是对称NAT，也就说是我们绝大多数人使用的都是对称NAT，所以想要进行UDP打洞还是非常困难的。

### 2.2.2 中继
![](http://upload-images.jianshu.io/upload_images/21580557-98306761082c6120.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1080/q/50)

中继最可靠但也是最低效的一种P2P通信实现，其原理是通过一个有公网IP的服务器中间人对两个内网客户端的通信数据进行中继和转发，当服务端连接的客户端比较少，且网络流量不大时，效果还不错。但是如果有很多客户端连接并且网络流量很多，服务端的压力就会很大。


<br>
#三、自建FRP实现
![image.png](https://upload-images.jianshu.io/upload_images/21580557-23d0682d9a0befcf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

实现方式多种多样，如果没有公网服务器的话，可以使用花生壳等软件。有公网服务器的话可以自行搭建内网穿透服务，推荐使用 **FRP** 。

**以下是FRP的具体实现。**

<br>
## 3.1 TCP穿透
### 3.1.1 服务端(linux)部署
创建/root/docker/frp/frps/frps.ini文件。
bind_port是服务端与客户端进行绑定的端口号。
dashboard相关是对可视化页面的配置。
```
[common]
bind_port = 7000

dashboard_port = 7500
dashboard_user = admin
adshboard_pwd = admin
```
```
docker run --restart=always --network host -d -v /root/docker/frp/frps/frps.ini:/etc/frp/frps.ini --name frps snowdreamtech/frps
```

访问面板[http://chenjie.asia:7500](http://chenjie.asia:7500/)

>注：chenjie.asia是我的云服务器的域名。

<br>
### 3.1.2 客户端(linux)部署
#### 部署
创建配置文件/root/docker/frp/frpc/frpc.ini。
配置文件中server_addr和server_port是服务端的地址和接口，客户端通过该地址和端口与服务端建立连接。
配置文件中的第二个中括号中的内容是隧道的名称，不能有重复，隧道会将remote_port端口映射为local_port端口。所以服务端会监听remote_port端口，该端口也不能重复。
```
[common]
server_addr = chenjie.asia
server_port = 7000

[frpc_chenjie.asia]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6002
```
启动容器
```
docker run --restart=always --network host -d -v /root/docker/frp/frpc/frpc.ini:/etc/frp/frpc.ini --name frpc snowdreamtech/frpc
```

<br>
#### 日志信息
**查看客户端日志：**start proxy success表示绑定服务端成功。
```
2021/05/08 00:01:25 [I] [service.go:304] [48a7398b795499be] login to server success, get run id [48a7398b795499be], server udp port [0]
2021/05/08 00:01:25 [I] [proxy_manager.go:144] [48a7398b795499be] proxy added: [ssh]
2021/05/08 00:01:25 [I] [control.go:180] [48a7398b795499be] [ssh] start proxy success
```
**查看服务端日志：**client login info: ip [39.182.6.165:6210]  表示39.182.6.165:6210这台内网机绑定到了服务端，其公网ip为39.182.6.165，NAT映射端口为6210。
```
2021/05/07 16:04:55 [I] [service.go:449] [48a7398b795499be] client login info: ip [39.182.6.165:6210] version [0.36.2] hostname [] os [windows] arch [amd64]
2021/05/07 16:04:55 [I] [tcp.go:63] [48a7398b795499be] [ssh] tcp proxy listen port [6000]
2021/05/07 16:04:55 [I] [control.go:446] [48a7398b795499be] new proxy [ssh] success
```

<br>
#### 验证
客户端与服务端建立连接，并在服务端添加了端口映射，即访问服务端的6002接口，会自动路由到客户端的22端口。
```
[root@iotmars ~]# ssh chenjie.asia -l root -p 6002
The authenticity of host '[chenjie.asia]:6002 ([81.68.79.183]:6002)' can't be established.
ECDSA key fingerprint is SHA256:3AjLn6Er93Kdd9Z/DelFo45ub9epUNyTIJ4J82++Uq8.
ECDSA key fingerprint is MD5:d8:3d:14:59:94:c5:3a:4a:e9:2b:df:06:6a:2d:4d:80.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[chenjie.asia]:6002,[81.68.79.183]:6002' (ECDSA) to the list of known hosts.
root@chenjie.asia's password: 
Last failed login: Sat May  8 01:19:25 CST 2021 from 138.36.3.180 on ssh:notty
There were 135 failed login attempts since the last successful login.
Last login: Sat May  8 01:00:48 2021 from 39.182.6.165
[root@VM-0-13-centos ~]#
```
登录客户端成功。

<br>
### 3.1.3 客户端(win)
#### 部署
下载[https://github.com/fatedier/frp/releases](https://github.com/fatedier/frp/releases)中的win最新版。

**修改配置文件frpc.ini**
```
[common]
server_addr = chenjie.asia
server_port = 7000

[home_desktop]
type = tcp
local_ip = 127.0.0.1
local_port = 10010
remote_port = 6001
```
**启动客户端**
```
frpc.exe -c frpc.ini &
```

<br>
#### 验证
客户端与服务端建立连接，并在服务端添加了端口映射，即访问服务端的6001接口，会自动路由到内网机的10010端口。

**在内网机上启动微服务，端口为10010。接口层代码如下：**
```
@RestController
public class XxlController {
    @GetMapping("/test")
    public String test(){
        return "内网穿透成功!!!";
    }
}
```
**通过外网机访问服务端的6001**
```
[root@iotmars ~]# curl http://chenjie.asia:6001/test
内网穿透成功!!!
```

<br>
## 3.2 HTTP/HTTPS穿透
### 3.2.1 服务端(linux)部署
**修改配置文件frps.ini如下。重启容器** `docker restart frps`。
```
[common]
bind_addr = 0.0.0.0
bind_port = 7000

dashboard_port = 7500
dashboard_user = admin
adshboard_pwd = admin
# 验证客户端token
privilege_token = my_token 
# HTTP主机使用的端口，如果和nginx的800端口冲突，可以通过nginx反向代理到该端口
vhost_http_port = 80
# HTTPS主机使用的端口
vhost_https_port = 443
```
### 3.2.2 客户端(linux)部署
**配置文件frpc.ini如下，custom_domains与服务端的域名一致。重启容器** `docker restart frpc`
```
[common]
server_addr = chenjie.asia
server_port = 7000

privilege_token = my_token

[244_tcp]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6005

[244_http]
type = http
local_ip = 127.0.0.1
local_port = 80
custom_domains = chenjie.asia

[244_https]
type = https
local_ip = 127.0.0.1
local_port = 443
custom_domains = chenjie.asia
```
**配置nginx**
```conf
server {
    listen 80;
    listen [::]:80;

    server_name http.cj.com https.cj.com;
    charset utf-8;

    access_log /var/log/nginx/frpc.log main;
    error_log /var/log/nginx/frpc.err;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
}
```

访问[http://chenjie.asia](http://chenjie.asia/)得到内网机nginx上的index.html网页，内网穿透成功。

也可以在nginx的html文件夹下放入自己的前端项目供外网访问，或者配置nginx转发到其他服务。

<br>
# 四、参考
[UDP打洞介绍得很清楚  https://www.bilibili.com/read/cv6189209](https://www.bilibili.com/read/cv6189209)
[FRP的Github地址 https://github.com/fatedier/frp/releases](https://github.com/fatedier/frp/releases)
[FRP的DockerHub地址 https://registry.hub.docker.com/r/snowdreamtech/frps](https://registry.hub.docker.com/r/snowdreamtech/frps)

<br>
# 五、配合v2ray
使用FRP将v2ray等梯子软件的端口穿透到外网中，外网的节点的所有请求都可以通过v2ray来代理，这样就相当于将外网的节点加入到了内网之中。

**客户端设置**
在 设置 -> 参数设置  -> v2rayN设置 中勾选如下

![图片.png](https://upload-images.jianshu.io/upload_images/21580557-08c3bc27749ffe7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但是这样只能通过域名访问，需要设置v2ray客户端允许ip代理


<br>
# 六、使用SSH反向代理实现
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
