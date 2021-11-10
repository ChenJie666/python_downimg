# 一、起因
最近在学习Elasticsearch的分析器，苦于没有中文贴，只能上[es的官网](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)进行学习。在公司的时候能正常上网，但是到家后发现家里的网络无法访问，提示 `访问 www.elastic.co 的请求遭到拒绝`，于是想到通过使用别家的网络进行访问。

**准备：**一台有公网ip的服务器（我这里选择了一台腾讯云服务器）

<br>
# 二、实现
## 方式一、通过SSR实现
参见dockerhub上的镜像：[https://registry.hub.docker.com/r/4kerccc/shadowsocksr](https://registry.hub.docker.com/r/4kerccc/shadowsocksr)

#### 搭建服务器端的SSR（ShadowSocksR）
**启动容器（shadowsocksr 容器中的22和80端口用于远程登陆和ssr连接）：**
```
docker run -itd -p 1000:22 -p 80:80 --name ssr 4kerccc/shadowsocksr:latest
```

**如果需要通过xshell连接：**
ip：116.62.148.11
port：1000
用户名：root 
密码：4ker.cc

**默认配置为：**
远程端口: 80 (此端口为容器端口，使用时请换位本地映射端口)
密码: 4ker.cc
认证协议: auth_sha1_v4
混淆方式: http_simple
加密方法: chacha20

**如何修改端口和密码：**
进入容器或远程连接后 修改/etc/shadowsocks.json文件
里面80为端口，4ker.cc为连接密码，都可自行修改.
修改后重启容器即可。

#### SSR的WIN客户端
上网搜一下就有

**注：之前还是挺好用的，但是最近貌似访问不了了，而且安全性、客户端等各个方面都没有v2ray好用，因此推荐使用v2ray实现！！！**

<br>
## 方式二、通过v2ray实现
#### 创建配置文件
vim /root/v2ray/conf/config.json
```
{
  "log" : {
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log",
    "loglevel": "warning"
  },
  "inbounds": [{
    "port": 8002, //端口
    "protocol": "vmess",//传输协议
    "listen":"0.0.0.0",
    "settings": {
      "clients": [
        {
          "id": "C9157CBE-405E-D56B-7118-0C160D0F3DF9",//这里GUID请通过工具生成
          "level": 1,
          "alterId": 64
        }
      ]
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  }]
}
```
#### 安装v2ray
```
docker run \
--restart=always \
--name=v2ray \
--net=host \
-v /root/v2ray/conf/config.json:/etc/v2ray/config.json \
-v /root/v2ray/log:/var/log/v2ray \
-d \
v2ray/official:latest
```
#### 配置win客户端
**步骤如下**
1. **下载压缩包**
网上下一个win端的客户端

2. **解压后打开v2rayN.exe**
![image.png](https://upload-images.jianshu.io/upload_images/21580557-7e0e6a041dc58e35.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 添加服务器

![image.png](https://upload-images.jianshu.io/upload_images/21580557-b5a12b2c993cdd21.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

根据传输协议选择添加的服务器类型，端口、用户ID、alterId需要与配置文件中的一致；

4. 右键测试服务器速度，如果测速正常则连接成功
![image.png](https://upload-images.jianshu.io/upload_images/21580557-5f77ab0e11a49ecf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5. 启动代理
![image.png](https://upload-images.jianshu.io/upload_images/21580557-54eb61bfdd8b7187.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<br>
# 三、结果
进入[测速网站](https://www.speedtest.cn/)进行测速，发现测速节点变成了中国腾讯云，表明搭建成功
![image.png](https://upload-images.jianshu.io/upload_images/21580557-d39312b71eb829cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

访问[es的官网](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)可以进行愉快的学习了！

<br>
# 四、配置文件
- guiNConfig.json：记录了添加的服务器的详细信息
- config.json：v2ray的原生的配置文件，即v2ray启动时读取的配置文件，用于指定代理规则。通过客户端启动v2ray时，会将该服务器的配置信息重新写入到config.json文件中。所以直接在该配置文件中修改配置项，通过客户端启动时并不会生效，需要在客户端中修改配置才会生效。

# 五、访问内网
可以通过 frp内网穿透 + v2ray请求转发 实现对内网的访问。即将v2ray的请求通过frp映射到外网，外网通过请求frp的端口访问v2ray，通过v2ray访问内网中的任意服务。
注：不知道为啥，windows版的v2ray不会代理内网IP，只能通过解析一个域名给内网IP，通过域名才能进行访问，而安卓版的就不用这么麻烦，可以直接访问内网IP。弄了很久都想不明白，后来干脆在手机上下了一个 [VPN热点]，给它ROOT权限，然后通过手机共享网络给电脑，这样就可以随意访问内网了。
