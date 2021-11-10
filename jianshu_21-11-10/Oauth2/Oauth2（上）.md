# 一、简介

## 1.1 业务场景

公司原来使用的是自建的用户登陆系统，但是只有登陆功能，没有鉴权功能。


现公司有如下业务场景：

1. 需要接入各大智能音箱，音箱需要通过标准的Oauth2授权码模式获取令牌从而拿到服务器资源；
2. 后台管理界面需要操作权限 ；
3. 后期要做开发者平台，需要授权码模式。 

所以在以上业务场景下开始自建Oauth2框架，框架需要兼容公司原有的用户登陆系统。


## 1.3 Oauth2框架
Oauth2扩展了Security的授权机制。


# 二、相关概念

## 2.1 单点登陆

即一个token可以访问多个微服务。


## 2.2 授权方式

### ①授权码模式

第三方应用通过客户端进行登录，如果通过github账号进行登录，那么第三方应用会跳转到github的资源服务器地址，携带了client_id、redirect_uri、授权类型(code模式)和state(防止csrf攻击的token,可以不填)。随后资源服务器会重定向到第三方应用url并携带code和state参数，随后第三方应用携带code、client_id和client_secret再去请求授权服务器，先验证code是否有效，有效则发放认证token，携带该token可以取资源服务器上的资源。

授权码模式（authorization code）是功能最完整、流程最严密的授权模式，code保证了token的安全性，即使code被拦截，由于没有app_secret，也是无法通过code获得token的。



**如当我们登陆CSDN的时候，可以使用第三方Github账号密码进行登陆并获取头像等信息。**

首先需要注册CSDN的信息

- 应用名称
- 应用网站
- 重定向标识 redirect_uri
- 客户端标识 client_id
- 客户端秘钥 client_secret

如github认证服务器中可以对客户端进行注册，需要填写应用名称、网站地址、应用描述和重定向地址。这样github就记录了该应用并产生一个client_id和client_secret。
![](https://upload-images.jianshu.io/upload_images/21580557-8920517a4fb81ab7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**获取令牌流程图如下：**

![](https://upload-images.jianshu.io/upload_images/21580557-2efd5c632aaa2006.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




**优点**

- 不会造成我们的账号密码泄漏
- Token不会暴露给前端浏览器



**看下测试实例**

```json
# 指定授权方式为code模式，携带客户端id、重定向地址等信息访问。
GET https://oauth.marssenger.com/oauth/authorize?client_id=c1&response_type=code&scope=ROLE_ADMIN&redirect_uri=http://www.baidu.com
# 会跳转到登陆页面，输入账号密码。如果信息正常，会携带code跳转到重定向地址。
https://www.baidu.com/?code=YEQCZO
# 然后携带code访问授权服务器，就可以获取到令牌了。
https://oauth.marssenger.com/oauth/token?client_id=c1&client_secret=123456&grant_type=authorization_code&code=YEQCZO&redirect_uri=http://www.baidu.com
# 最终得到令牌如下
{
    "access_token": "ey......Jgw",
    "token_type": "bearer",
    "refresh_token": "ey......J-A",
    "expires_in": 86399,
    "scope": "ROLE_ADMIN",
    "cre": 1622694842,
    "jti": "fd970e49-082f-492e-9418-b21b45452f2d"
}
```

> access_token：访问令牌，携带此令牌访问资源
> token_type：有MAC Token与Bearer Token两种类型，两种的校验算法不同，RFC 6750建议Oauth2采用 Bearer Token。
> refresh_token：刷新令牌，使用此令牌可以延长访问令牌的过期时间。
> expires_in：过期时间，单位为秒。
> scope：范围，与定义的客户端范围一致。
> cre：自定义添加的令牌创建日期
> jti： jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

**为什么需要使用code去换取token，而不是直接返回token？**
1. 如果直接获取token，那么client_secret需要写在url中，这样容易造成客户端秘密泄漏。
2. 如果重定向地址是http协议传输的，可能导致code被截获泄漏，但是code只能使用一次，所以如果code失效，可以及时发现被攻击。code换取token这一步一般使用的是https协议，避免被中间人攻击。
>The code exchange step ensures that an attacker isn’t able to intercept the access token, since the access token is always sent via a secure backchannel between the application and the OAuth server.


### ②简化模式

第三方应用通过客户端进行登录，通过github账号访问资源服务器，认证完成后重定向到redirect_uri并携带token，省略了通过授权码再去获取token的过程。

适用于公开的浏览器单页应用，令牌直接从授权服务器返回，不支持刷新令牌，且没有code安全保证，令牌容易因为被拦截窃听而泄露。

![](https://upload-images.jianshu.io/upload_images/21580557-b91b7322f333e750.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




**看下测试实例**

```
# 指定授权方式为token模式，携带客户端id、重定向地址等信息访问。
GET https://oauth.marssenger.com/oauth/authorize?client_id=c1&response_type=token&scope=ROLE_ADMIN&redirect_uri=http://www.baidu.com
# 直接获取到了access_token，不支持刷新令牌
https://www.baidu.com/#access_token=ey......u0Q&token_type=bearer&expires_in=86399&cre=1622695736&jti=13a726b2-70d4-421e-8d5b-3a26233214cc
```



### ③密码模式

直接向第三方应用提供资源服务器的账号密码，第三方应用通过账号密码请求获取资源服务器上的资源。会向第三方应用暴露账号密码，除非特别信任该应用。

![](https://upload-images.jianshu.io/upload_images/21580557-40d05c38a28d0253.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




**看下测试实例**

```json
# 指定授权方式为password，携带客户端id密码、用户账号密码等信息访问。
GET https://oauth.marssenger.com/oauth/token?client_id=c1&client_secret=123456&grant_type=password&username=admin&password=abc123&user_type=admin
# 获取令牌
{
    "access_token": "ey......_SA",
    "token_type": "bearer",
    "refresh_token": "ey......brw",
    "expires_in": 86399,
    "scope": "ROLE_ADMIN ROLE_APPLICATION",
    "cre": 1622691146,
    "jti": "c31a69bc-0eba-4e93-8f78-c0f8c04a2b11"
}
```



### ④客户端模式

不通过资源所有者，直接以第三方应用的秘钥和id获取资源服务器的token。

![](https://upload-images.jianshu.io/upload_images/21580557-c43203d68d307f8e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**看下测试实例**

```json
# 指定授权方式为client_credentials，携带客户端id和密码进行访问。
GET https://oauth.marssenger.com/oauth/token?client_id=c1&client_secret=123456&grant_type=client_credentials
# 获取令牌
{
    "access_token": "ey......zMQ",
    "token_type": "bearer",
    "expires_in": 86399,
    "scope": "ROLE_ADMIN ROLE_APPLICATION",
    "cre": 1622697938,
    "jti": "8f962403-c7d8-4d4b-974f-7896a0a31389"
}
```



## 2.3 JWT令牌

Oauth2原生的token是一串随机的hash字符串，存在两个问题：

- token验证需要远程调用认证服务器，效率低
- token无法携带用户数据；

因此使用JWT来取代原生的token。

JWT全称为Json Web Token，使用一种特殊格式的token，token有特定含义，分为三部分：

- 头部Header：包括令牌的类型（即JWT）及使用的哈希算法（如HMAC、SHA256或RSA）。
- 载荷Payload：存放有效信息，如iss（签发者）、exp（过期时间）、sub（授权用户）和创建时间等，也可以自定义字段方便扩展。
- 签名Signature：是对前两部分的数字签名，防止被篡改。

这三部分均用base64Url进行编码，并使用.进行分隔，一个典型的jwt格式的token类似xxxxx.yyyyy.zzzzz。认证服务器通过对称或非对称的加密方式利用payload生成signature，并在header中申明签名方式。这样jwt可以实现分布式的token验证功能，即`资源服务器通过事先维护好的对称或者非对称密钥（非对称的话就是认证服务器提供的公钥），直接在本地验证token`，这种去中心化的验证机制非常适合分布式架构。jwt相对于传统的token来说，解决以下两个痛点：

- 通过验证签名，对于token的验证可以直接在资源服务器本地完成，不需要连接认证服务器；
- 在payload中可以包含用户相关信息，这样就轻松实现了token和用户信息的绑定；
  如果认证服务器颁发的是jwt格式的token，那么资源服务器就可以直接自己验证token的有效性并绑定用户，这无疑大大提升了处理效率且减少了单点隐患。

总结：Header申明算法、Payload是用户信息、对Payload加密得到Signature，三部分用base64编码后通过"."连接组合为token；验证token时只需要根据header中的算法对Payload（默认是HMAC SHA256算法）进行验证。



**JWT优点：**

- jwt基于json，非常方便使用；
- 可以在令牌中自定义丰富的内容，易扩展；
- 通过非对称加密算法和数字签名技术，JWT防止篡改，安全性高；
- 资源服务使用JWT可不依赖认证服务器即可完成授权。

**JWT缺点：**

- 在有效期内，token是无法作废的，用户的签退更多是一个客户端的签退，服务端token仍然有效，你只要使用这个token，仍然可以登陆系统。另外一个问题是续签问题，当然你也可以通过redis去记录token状态，并在用户访问后更新这个状态，但这就是硬生生把jwt的无状态搞成有状态了，而这些在传统的session+cookie机制中都是不需要去考虑的。



**JWT安全加强**

- 避免网络劫持，HTTP协议使用header传递JWT容易泄露，使用HTTPS协议传输更安全。
- 私钥存放在服务器端，保证服务器不被攻破。
- JWT可以被暴力破解，所以需要保证秘钥复杂度，定期更换秘钥。



**以上是理论，下面来看结合实际**

```json
# 通过密码模式请求已经搭建完成的授权服务器
POST https://oauth.marssenger.com/oauth/token?client_id=c1&client_secret=123456&grant_type=password&username=admin&password=abc123&user_type=admin

# 得到令牌如下，token因为太长省略了部分。
{
    "access_token": "ey......t_SA",
    "token_type": "bearer",
    "refresh_token": "ey......mbrw",
    "expires_in": 86399,
    "scope": "ROLE_ADMIN ROLE_APPLICATION",
    "cre": 1622691146,
    "jti": "c31a69bc-0eba-4e93-8f78-c0f8c04a2b11"
}
```

**对其中的access_token进行解析：**

```json
# 令牌中的完整access_token如下
"access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsicmVzMSJdLCJ1c2VyX25hbWUiOiIzNyIsInNjb3BlIjpbIlJPTEVfQURNSU4iLCJST0xFX0FQUExJQ0FUSU9OIl0sImNyZSI6MTYyMjY5MTE0NiwiZXhwIjoxNjIyNzc3NTQ2LCJhdXRob3JpdGllcyI6WyJiYWNrOnVzZXI6dXBkYXRlIiwiYmFjazpjb250ZW50OnVwZGF0ZSIsImJhY2s6Y29udGVudDpsaXN0IiwiYmFjazp1c2VyOmxpc3QiLCJiYWNrOnN5czphbGwiLCJST0xFX3VzZXIiLCJiYWNrOmNvbnRlbnQ6YWxsIiwiYmFjazpjb250ZW50OmFkZCIsImJhY2s6dXNlcjphbGwiLCJiYWNrOnVzZXI6YWRkIiwiYmFjazp1c2VyOmRlbGV0ZSIsImJhY2s6Y29udGVudDpkZWxldGUiXSwianRpIjoiYzMxYTY5YmMtMGViYS00ZTkzLThmNzgtYzBmOGMwNGEyYjExIiwiY2xpZW50X2lkIjoiYzEifQ.lZXI8rhN6XUgbHaXZa6zK2GAdI2nruT_LZpAtBMRIIuQddKu8827juVBqx498Orb3MNC7RzFV_cv365SlE_TaUJ09tW0jnd-8kdPaRIGt11SIg2Jik8EQ3l_t8_XOtZhq6TUjKfPZQfo0egXUO70QzyC9JPFGZQPAUYvwNCZMC0qBkYuI4paUWQoMh0yML25eVMIMf_fTPgxFFicEVzc78yO4PqUrXc-WGlZkRRx6EPyrIhtXVY0uHmBORKlnbPcVDVkcYnLXTUcVumtWRGUw4zsHjGLAWkiUC2ISvBUl5DVQStd9B5R_FzLWuWLNlskFaZ8npbKA9XuUH_CKxt_SA"

# access_token由两个"."分割为三部分，分别为Header，Payload和Signature，通过base64解密Header和Payload后得到：
Header：{"alg":"RS256","typ":"JWT"}
Payload：{
    "aud":[
        "res1"
    ],
    "user_name":"37",
    "scope":[
        "ROLE_ADMIN",
        "ROLE_APPLICATION"
    ],
    "cre":1622691146,
    "exp":1622777546,
    "authorities":[
        "back:user:update",
        "back:content:update",
        "back:content:list",
        "back:user:list",
        "back:sys:all",
        "ROLE_user",
        "back:content:all",
        "back:content:add",
        "back:user:all",
        "back:user:add",
        "back:user:delete",
        "back:content:delete"
    ],
    "jti":"c31a69bc-0eba-4e93-8f78-c0f8c04a2b11",
    "client_id":"c1"
}

# Signature为数字签名，即对内容的摘要通过私钥进行加密，然后在客户端通过公钥解密并与摘要进行对比，保证内容不会被篡改。Header中携带了使用的加密算法信息。
```



## 2.4 网关

有些架构方案中，认证服务负责认证，网关负责校验认证和鉴权，其他API服务负责处理自己的业务逻辑。安全相关的逻辑只存在于认证服务和网关服务中，其他服务只是单纯地提供服务而没有任何安全相关逻辑。

但是个人觉得这样网关承担的责任太大，且每次业务逻辑改变后需要同时修改网关的代码或者将数据库刷新到网关内存中。所以为了方便起见，目前还是将权限信息和鉴权逻辑放到自己的业务中。优化工作后续再做，反正对于整套Oauth2搭建来说，将认证和鉴权工作放到gateway中只是小意思。

目前网关最大的作用就是路由请求了，同时可以设置黑名单进行过滤。



## 2.5 密钥配置

由于需要签名摘要，所以认证服务器需要配置密钥，这里使用RS256进行加密。配置密钥的方式有好多种。

- 方式一：最简单的就是直接将公钥和私钥写在认证服务配置文件中，在项目启动时从配置文件读取。这样公钥可以直接写在资源服务中，也可以通过提供接口的方式让资源服务来请求获取公钥。

- 方式二：通过生成SSL证书的方式，将证书放到资源路径下，然后认证服务运行时读取并解析证书，获取公钥和私钥。这种情况下公钥就必须通过提供接口的方式让资源服务来请求获取公钥。我们还是采取这种方式，因为我觉得更加优雅。
- 方式三：通过jjwt框架生成密钥，每次重启都会更换随机密钥。可以开放公钥接口给其他资源服务。这种很方便，但是并不推荐，因为每次重启认证服务都需要重启资源服务，且会导致之前的token全部失效。



## 2.6 服务划分

将Oauth2服务划分为了两部分，一个是认证服务，一个是用户中心，就是将用户相关的部分拿出来新建一个用户服务。所有令牌相关的操作都在认证服务中完成，所有用户相关的操作都在用户中心完成。

认证服务需要访问用户的信息，可以通过Feign调用用户中心的接口获取资源；用户中心用于处理用户的相关操作，所以是一个资源服务，外部请求需要鉴权后才能进行操作。



# 三、部署

## 3.1 建表语句

```sql
-- used in tests that use HSQL

DROP TABLE IF EXISTS oauth_client_details;
CREATE TABLE oauth_client_details (
  client_id VARCHAR(256) NOT NULL COMMENT '客户端标识',
  resource_ids VARCHAR(256) NULL DEFAULT NULL COMMENT '接入资源列表',
  client_secret VARCHAR(256) NULL DEFAULT NULL COMMENT '客户端秘钥',
  scope VARCHAR(256) NULL DEFAULT NULL COMMENT '客户端权限',
  authorized_grant_types VARCHAR(256) NULL DEFAULT NULL COMMENT '授权模式',
  web_server_redirect_uri VARCHAR(256) NULL DEFAULT NULL COMMENT '重定向地址',
  authorities VARCHAR(256) NULL DEFAULT NULL COMMENT '指定用户的权限范围，如果授权的过程需要用户登陆，该字段不生效，implicit和client_credentials需要',
  access_token_validity int(11) NULL DEFAULT NULL COMMENT '令牌有效时间',
  refresh_token_validity int(11) NULL DEFAULT NULL COMMENT '更新令牌有效时间',
  additional_information VARCHAR(4096) COMMENT '可空',
  autoapprove VARCHAR(256) COMMENT '是否手动确认授权，默认false',
  PRIMARY KEY (client_id) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '接入客户端信息';

DROP TABLE IF EXISTS oauth_code;
CREATE TABLE oauth_code (
    create_time timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    code varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
    authentication blob NULL,
    INDEX code_index(code) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

create table oauth_client_token (

  token_id VARCHAR(256),

  token LONGVARBINARY,

  authentication_id VARCHAR(256) PRIMARY KEY,

  user_name VARCHAR(256),

  client_id VARCHAR(256)

);

create table oauth_access_token (

  token_id VARCHAR(256),

  token LONGVARBINARY,

  authentication_id VARCHAR(256) PRIMARY KEY,

  user_name VARCHAR(256),

  client_id VARCHAR(256),

  authentication LONGVARBINARY,

  refresh_token VARCHAR(256)

);

create table oauth_refresh_token (

  token_id VARCHAR(256),

  token LONGVARBINARY,

  authentication LONGVARBINARY

);


create table oauth_approvals (

userId VARCHAR(256),

clientId VARCHAR(256),

scope VARCHAR(256),

status VARCHAR(10),

expiresAt TIMESTAMP,

lastModifiedAt TIMESTAMP

);

-- customized oauth_client_details table

create table ClientDetails (

  appId VARCHAR(256) PRIMARY KEY,

  resourceIds VARCHAR(256),

  appSecret VARCHAR(256),

  scope VARCHAR(256),

  grantTypes VARCHAR(256),

  redirectUrl VARCHAR(256),

  authorities VARCHAR(256),

  access_token_validity INTEGER,

  refresh_token_validity INTEGER,

  additionalInformation VARCHAR(4096),

  autoApproveScopes VARCHAR(256)

);
```

RBAC表：

```sql
CREATE TABLE `tb_permission` (

  `id` bigint(20) NOT NULL AUTO_INCREMENT,

  `parent_id` bigint(20) DEFAULT NULL COMMENT '父权限',

  `name` varchar(64) NOT NULL COMMENT '权限名称',

  `enname` varchar(64) NOT NULL COMMENT '权限英文名称',

  `url` varchar(255) NOT NULL COMMENT '授权路径',

  `description` varchar(200) DEFAULT NULL COMMENT '备注',

  `created` datetime NOT NULL,

  `updated` datetime NOT NULL,

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8 COMMENT='权限表';


CREATE TABLE `tb_role` (

  `id` bigint(20) NOT NULL AUTO_INCREMENT,

  `parent_id` bigint(20) DEFAULT NULL COMMENT '父角色',

  `name` varchar(64) NOT NULL COMMENT '角色名称',

  `enname` varchar(64) NOT NULL COMMENT '角色英文名称',

  `description` varchar(200) DEFAULT NULL COMMENT '备注',

  `created` datetime NOT NULL,

  `updated` datetime NOT NULL,

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8 COMMENT='角色表';


CREATE TABLE `tb_role_permission` (

  `id` bigint(20) NOT NULL AUTO_INCREMENT,

  `role_id` bigint(20) NOT NULL COMMENT '角色 ID',

  `permission_id` bigint(20) NOT NULL COMMENT '权限 ID',

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8 COMMENT='角色权限表';


CREATE TABLE `tb_user` (

  `id` bigint(20) NOT NULL AUTO_INCREMENT,

  `username` varchar(50) NOT NULL COMMENT '用户名',

  `password` varchar(64) NOT NULL COMMENT '密码，加密存储',

  `phone` varchar(20) DEFAULT NULL COMMENT '注册手机号',

  `email` varchar(50) DEFAULT NULL COMMENT '注册邮箱',

  `account_non_expired` tinyint DEFAULT 1 COMMENT '账户没有过期',

  `account_non_locked` tinyint DEFAULT 1 COMMENT '用户没有被锁定',

  `credentials_non_expired` tinyint DEFAULT 1 COMMENT '凭证没有过期',

  `enabled` tinyint DEFAULT 1 COMMENT '账户是否可用',

  `created` datetime NOT NULL,

  `updated` datetime NOT NULL,

  PRIMARY KEY (`id`),

  UNIQUE KEY `username` (`username`) USING BTREE,

  UNIQUE KEY `phone` (`phone`) USING BTREE,

  UNIQUE KEY `email` (`email`) USING BTREE

) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8 COMMENT='用户表';


CREATE TABLE `tb_user_role` (

  `id` bigint(20) NOT NULL AUTO_INCREMENT,

  `user_id` bigint(20) NOT NULL COMMENT '用户 ID',

  `role_id` bigint(20) NOT NULL COMMENT '角色 ID',

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8 COMMENT='用户角色表';
```

![](https://upload-images.jianshu.io/upload_images/21580557-cb14a5bacd0e4123.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)






## 3.2 密钥配置

### 方式一

写死在配置文件中，启动时直接读取配置就行了。

### 方式二

**步骤一：生成证书**

在jdk的bin目录下使用如下命令

```shell
keytool -genkey -alias jwt -keyalg RSA -keystore uaacenter.jks
```

然后设置keystore password和key password即可，我这里设置的都是uaacenter。

将得到的证书uaacenter.jks放到resources目录下。

**步骤二：认证服务中解析证书**

```java
import cn.hutool.core.codec.Base64;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.core.io.ClassPathResource;
import org.springframework.security.oauth2.provider.token.TokenStore;
import org.springframework.security.oauth2.provider.token.store.JwtAccessTokenConverter;
import org.springframework.security.oauth2.provider.token.store.JwtTokenStore;
import org.springframework.security.rsa.crypto.KeyStoreKeyFactory;

import javax.annotation.Resource;
import java.security.KeyPair;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;

@Configuration
public class TokenConfig {

    @Resource
    private Environment environment;

    @Resource
    private KeyPair keyPair;

    @Bean
    public KeyPair keyPair(){
        String location = environment.getProperty("key-store.location");
        String storepass = environment.getProperty("key-store.storepass");
        String keypass = environment.getProperty("key-store.keypass");
        String alias = environment.getProperty("key-store.alias");
        ClassPathResource resource = new ClassPathResource(location);
        KeyStoreKeyFactory keyStoreKeyFactory = new KeyStoreKeyFactory(resource, storepass.toCharArray());
        return keyStoreKeyFactory.getKeyPair(alias,keypass.toCharArray());
    }

    @Bean
    public RSAPublicKey publicKey() {
        RSAPublicKey aPublic = (RSAPublicKey) keyPair.getPublic();

        System.out.println(Base64.encode(aPublic.getEncoded()));

        return aPublic;
    }

    @Bean
    public RSAPrivateKey privateKey(){
        RSAPrivateKey aPrivate = (RSAPrivateKey) keyPair.getPrivate();

        System.out.println(Base64.encode(aPrivate.getEncoded()));

        return aPrivate;
    }

    /**
     * 将JWT作为令牌
     *
     * @return
     */
    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(accessTokenConverter());
    }

    /**
     * JWT配置
     *
     * @return
     */
    @Bean
    public JwtAccessTokenConverter accessTokenConverter() {
        JwtAccessTokenConverter converter = new JwtAccessTokenConverter();
//        converter.setSigningKey(SIGNING_KEY); //对称秘钥，资源服务器使用该秘钥来验证
        converter.setKeyPair(keyPair);

        return converter;
    }

}
```

**步骤三：开放公钥请求接口**

```java
@RestController
@Slf4j
public class AuthController {

    @Resource
    private RSAPublicKey publicKey;

    /**
     * 获取公钥接口（不鉴权）
     * @return
     */
    @GetMapping("/feign/uaa/publicKey")
    public String publicKey() {
        return "-----BEGIN PUBLIC KEY-----" + Base64.encode(publicKey.getEncoded()) + "-----END PUBLIC KEY-----";
    }

}
```



### 方式三

需要导入依赖

```xml
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.10.5</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.10.5</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.10.5</version>
            <scope>runtime</scope>
        </dependency>
```

```java
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

@Configuration
public class KeyPairConfig {
    
    private final KeyPair keyPair = Keys.keyPairFor(SignatureAlgorithm.RS256);
    @Bean
    public RSAPublicKey publicKey() {
        RSAPublicKey aPublic = (RSAPublicKey) keyPair.getPublic();

        System.out.println(Base64.encode(aPublic.getEncoded()));

        return aPublic;
    }

    @Bean
    public RSAPrivateKey privateKey(){
        RSAPrivateKey aPrivate = (RSAPrivateKey) keyPair.getPrivate();

        System.out.println(Base64.encode(aPrivate.getEncoded()));

        return aPrivate;
    }
}
```





## 3.3 认证服务

### 依赖

```xml
    <properties>
        <spring-boot.version>2.2.5.RELEASE</spring-boot.version>
        <spring-cloud.version>Hoxton.SR3</spring-cloud.version>
        <mybatis-plus.version>3.2.0</mybatis-plus.version>
    </properties>

    <dependencies>
        <!-- springcloud依赖 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>

        <!-- springboot依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.session</groupId>
            <artifactId>spring-session-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>

        <!-- 数据库依赖 -->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>${mybatis-plus.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>

        <!-- 通用工具类 -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.3.3</version>
        </dependency>
        <!-- jjwt工具类 -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.10.5</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.10.5</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.10.5</version>
            <scope>runtime</scope>
        </dependency>

        <!-- 静态webjar资源 -->
        <dependency>
            <groupId>org.webjars</groupId>
            <artifactId>jquery</artifactId>
            <version>3.5.1</version>
        </dependency>
        <dependency>
            <groupId>org.webjars</groupId>
            <artifactId>bootstrap</artifactId>
            <version>4.5.3</version>
        </dependency>

        <!-- 二方库依赖 -->
        <dependency>
            <groupId>com.marssenger.hifun</groupId>
            <artifactId>common</artifactId>
            <version>1.4.18-RELEASES</version>
        </dependency>

    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-parent</artifactId>
                <version>${spring-boot.version}</version>
                <scope>import</scope>
                <type>pom</type>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <scope>import</scope>
                <type>pom</type>
            </dependency>
        </dependencies>
    </dependencyManagement>
```

### 注解

**@EnableAuthorizationServer** 注解来告诉spring框架自动配置一些关于AuthorizationEndpoint以及一些关于AuthorizationServer security的配置。同时，来配置访问的client的一些细节
**@EnableResourceServer**  注解来告诉spring框架自动配置一些关于resource server的配置，比如启用OAuth2AuthenticationProcessingFilter来检查进来的request有没有有效的accesstoken。

### 配置文件

```yaml
server:
  servlet:
    session:
      timeout: 20s
  port: 9501
  
spring:
  profiles:
    active: dev
  application:
    name: security-uaa
  cloud:
    config:
      label: master
      name: ${spring.application.name}
      discovery:
        enabled: true
        service-id: config-server
  thymeleaf:
    prefix: classpath:/views/
    suffix: .html
    cache: false
  datasource:
    url: jdbc:mysql://192.168.32.225:3306/uaa_server?useUnicode=true&characterEncoding=utf-8
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: hxr
  main:
    allow-bean-definition-overriding: true
  redis:
    host: 116.62.148.11
    port: 6380
    password:
    jedis:
      pool:
        max-active: 8
        max-idle: 8
        max-wait: -1s
        min-idle: 0
    session:
      store-type: redis

eureka:
  client:
    service-url:
      defaultZone: http://192.168.32.230:8761/eureka
  instance:
    prefer-ip-address: true
    health-check-url-path: /actuator/health

management:
  endpoints:
    web:
      exposure:
        include: refresh,health,info,env

feign:
  httpclient:
    connection-timeout: 2000

jwt:
  publicKey: "-----BEGIN PUBLIC KEY-----MIIBIjANB......wIDAQAB-----END PUBLIC KEY-----"
  privateKey: "-----BEGIN PRIVATE KEY-----MIIEvQIBADAN......WKGoHLD43js=-----END PRIVATE KEY-----"
  expiration: 3600000
  header: JWTHeaderName

key-store:
  location: uaacenter.jks
  storepass: uaacenter
  alias: uaacenter
  keypass: uaacenter
```



### 实体类

```java
@Component
@Data
@Accessors(chain = true)
public class MyUserDetails implements UserDetails {

    private String username;
    private String password;
    boolean accountNonExpired = true; // 账户没有过期
    boolean accountNonLocked = true; //账户没被锁定 （是否冻结）
    boolean credentialsNonExpired = true; //密码没有过期
    boolean enabled = true; //账户是否可用（是否被删除）
    Collection<? extends GrantedAuthority> authorities; //用户权限集合

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return accountNonExpired;
    }

    @Override
    public boolean isAccountNonLocked() {
        return accountNonLocked;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return credentialsNonExpired;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }
}
```

```java
@Data
@Accessors(chain = true)
public class TbUserPO {

//    /**
//     * 用户名
//     */
//    private String username;
    /**
     * 密码
     */
    private String password;
    /**
     * 账户没有过期
     */
    boolean accountNonExpired = true;
    /**
     * 账户没被锁定 （是否冻结）
     */
    boolean accountNonLocked = true;
    /**
     * 密码没有过期
     */
    boolean credentialsNonExpired = true;
    /**
     * 账户是否可用（是否被删除）
     */
    boolean enabled = true;

    /*--------------------------------------------*/

    /**
     * 用户id
     */
    private Integer id;
    /**
     * 用户名
     */
    private String username;
    /**
     * 手机号
     */
    private String phone;
    /**
     * 邮箱
     */
    private String email;

}
```



### 配置类

**AuthorizationServerConfigurerAdapter类的三个重载方法的配置参数**

- ClientDetailsServiceConfigurer：用来配置客户端详情服务，客户端详情信息在这里进行初始化，可以把客户端详情信息写死在这里或者通过数据库来存储调取详情信息。
- AuthorizationServerEndpointsConfigurer：用来配置令牌（token） 的访问端点和令牌服务（token services）。
- AuthorizationServerSecurityConfigurer：用来配置令牌端点的安全约束（权限）。

**①配置登录页面和允许访问的路径**

```java
import oauth2.utils.PermitAllUrl;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.builders.WebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /**
     * 认证管理器
     *
     * @return
     * @throws Exception
     */
    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                //跨域请求伪造防御失效
                .csrf().disable()
                .authorizeRequests()
                .antMatchers("/administrator/getInfo").hasAnyAuthority("/users/")
                .antMatchers(PermitAllUrl.permitAllUrl("/feign/**","/uaa/geetest/**","/uaa/hxrlogin/**","/uaa/findPassword/**","/uaa/error/**","/test","/forward")).permitAll()
                .anyRequest().authenticated()
                .and()
                .formLogin().loginPage("/uaa/hxrlogin/pages/loginTel.html").loginProcessingUrl("/uaa/login");
//                .and().exceptionHandling().authenticationEntryPoint(new MyLoginUrlAuthenticationEntryPoint())
//                .sessionManagement()
//                .sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        super.configure(auth);
    }

    @Override
    public void configure(WebSecurity web) throws Exception {
        super.configure(web);
    }

}
```

这里将登陆页面设置为路径/uaa/hxrlogin/pages/loginTel.html，然后通过路径映射映射到resource下的静态页面，即public/pages/loginTel.html

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.*;

@Configuration
public class WebMvcConfigurerAdapter implements WebMvcConfigurer {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
//        registry.addViewController("/").setViewName("login");
//        registry.addViewController("/login.html").setViewName("login");
//        registry.addViewController("/uaa/hxrlogin/pages").setViewName("");
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/uaa/hxrlogin/**").addResourceLocations("classpath:hxrlogin/");
//        registry.addResourceHandler("/uaa/public/**").addResourceLocations("classpath:public/");
    }
}
```



**②基础配置**

配置token存储方式、JWT令牌配置、客户端配置、认证管理器配置、令牌增强配置

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.oauth2.config.annotation.configurers.ClientDetailsServiceConfigurer;
import org.springframework.security.oauth2.config.annotation.web.configuration.AuthorizationServerConfigurerAdapter;
import org.springframework.security.oauth2.config.annotation.web.configuration.EnableAuthorizationServer;
import org.springframework.security.oauth2.config.annotation.web.configurers.AuthorizationServerEndpointsConfigurer;
import org.springframework.security.oauth2.config.annotation.web.configurers.AuthorizationServerSecurityConfigurer;
import org.springframework.security.oauth2.provider.ClientDetailsService;
import org.springframework.security.oauth2.provider.client.JdbcClientDetailsService;
import org.springframework.security.oauth2.provider.code.AuthorizationCodeServices;
import org.springframework.security.oauth2.provider.code.JdbcAuthorizationCodeServices;
import org.springframework.security.oauth2.provider.token.*;
import org.springframework.security.oauth2.provider.token.store.JwtAccessTokenConverter;

import javax.annotation.Resource;
import javax.sql.DataSource;
import java.util.Arrays;

/**
 * @Description:
 * @Author: CJ
 * @Data: 2020/6/13 17:01
 */
@Configuration
@EnableAuthorizationServer
public class AuthorizationServer extends AuthorizationServerConfigurerAdapter {

    @Resource
    private BCryptPasswordEncoder bCryptPasswordEncoder;

    //token存储方式
    @Resource
    private TokenStore tokenStore;
    //JWT令牌配置
    @Resource
    private JwtAccessTokenConverter accessTokenConverter;

    //客户端详情服务
    @Autowired
    private ClientDetailsService clientDetailsService;

    //认证管理器
    @Autowired
    private AuthenticationManager authenticationManager;


    /**
     * 将客户端信息存储到数据库
     *
     * @param dataSource
     * @return
     */
    @Bean
    public ClientDetailsService clientDetailsService(DataSource dataSource) {
        JdbcClientDetailsService clientDetailsService = new JdbcClientDetailsService(dataSource);
        clientDetailsService.setPasswordEncoder(bCryptPasswordEncoder);
        return clientDetailsService;
    }

    /**
     * 客户端配置
     *
     * @param clients
     * @throws Exception
     */
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.withClientDetails(clientDetailsService);
//        clients.inMemory()//使用内存存储
//                .withClient("c1") //客户端id
//                .secret(bCryptPasswordEncoder.encode("abc123"))//设置密码
//                .resourceIds("res1")//可访问的资源列表
//                .authorizedGrantTypes("authorization_code", "password", "client_credentials", "implicit", "refresh_token")//该client允许的授权类型
//                .scopes("all")//允许的授权范围
//                .autoApprove(false)//false跳转到授权页面，true不跳转
//                .redirectUris("http://www.baidu.com");//设置回调地址
    }

    @Resource
    private MyTokenEnhancer myTokenEnhancer;

    /**
     * 令牌管理服务
     *
     * @return
     */
    @Bean
    public AuthorizationServerTokenServices tokenServices() {
        DefaultTokenServices services = new DefaultTokenServices();
        services.setClientDetailsService(clientDetailsService); //客户端详情服务
        services.setSupportRefreshToken(true); //支持刷新令牌
        services.setTokenStore(tokenStore); //令牌的存储策略
        //令牌增强,设置JWT令牌
        TokenEnhancerChain tokenEnhancerChain = new TokenEnhancerChain();
        tokenEnhancerChain.setTokenEnhancers(Arrays.asList(myTokenEnhancer,accessTokenConverter));
        services.setTokenEnhancer(tokenEnhancerChain);

//        services.setAccessTokenValiditySeconds(7200); //令牌默认有效时间2小时
//        services.setRefreshTokenValiditySeconds(259200); //刷新令牌默认有效期3天
        return services;
    }

    /**
     * 设置授权码模式的授权码如何存取，暂时采用内存方式
     *
     * @return
     */
//    @Bean
//    public AuthorizationCodeServices authorizationCodeServices(){
//        return new InMemoryAuthorizationCodeServices();
//    }

    @Resource
    private AuthorizationCodeServices authorizationCodeServices;

    /**
     * 授权码存储到数据库
     *
     * @param dataSource
     * @return
     */
    @Bean
    public AuthorizationCodeServices authorizationCodeServices(DataSource dataSource) {
        return new JdbcAuthorizationCodeServices(dataSource);
    }

    /**
     * 令牌访问端点配置
     *
     * @param endpoints
     * @throws Exception
     */
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        endpoints
                .authenticationManager(authenticationManager)//认证管理器
                .authorizationCodeServices(authorizationCodeServices)//授权码服务
                .tokenServices(tokenServices()) //令牌管理服务（设置令牌存储方式和令牌类型JWT）
                .allowedTokenEndpointRequestMethods(HttpMethod.POST)

                .pathMapping("/oauth/authorize","/uaa/oauth/authorize")
                .pathMapping("/oauth/token","/uaa/oauth/token")
                .pathMapping("/oauth/confirm_access","/uaa/oauth/confirm_access");
    }

    /**
     * 对授权端点接口的安全约束
     *
     * @param security
     * @throws Exception
     */
    @Override
    public void configure(AuthorizationServerSecurityConfigurer security) throws Exception {
        security
                .tokenKeyAccess("permitAll()") // /auth/token_key是公开的
                .checkTokenAccess("permitAll()") // /auth/check_token是公开的
                .allowFormAuthenticationForClients(); //允许表单认证（申请令牌）
    }

}
```



### Feign调用用户服务

```java
@FeignClient(name = "SECURITY-USER")
public interface UserCenterFeign {

    /**
     * 以下是认证中心远程调用用户中心的接口
     * @return
     */
    @GetMapping(path = "/feign/user/getTbUser")
    TbUserPO getTbUser(@RequestParam("username") String username);

    @GetMapping(path = "/feign/user/getRoleCodes")
    List<String> getRoleCodes(@RequestParam("username") String username);

    @PostMapping(path = "/feign/user/getAuthorities")
    List<String> getAuthorities(@RequestBody List<String> roleCodes);

}
```





## 3.4 用户服务

### 依赖

```xml
   <properties>
        <spring-boot.version>2.2.5.RELEASE</spring-boot.version>
        <spring-cloud.version>Hoxton.SR3</spring-cloud.version>
        <mybatis-plus.version>3.2.0</mybatis-plus.version>
    </properties>

    <dependencies>
        <!-- spring-cloud相关 -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
        </dependency>

        <!-- spring-boot相关 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- 自动创建数据库表 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- redis相关 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>

        <!-- rabbitMQ相关 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-amqp</artifactId>
        </dependency>

        <!-- 数据库相关 -->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>${mybatis-plus.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>

        <!-- swagger配置 -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.8.0</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.8.0</version>
        </dependency>

        <!-- 工具依赖 -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.12</version>
        </dependency>
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.3.3</version>
        </dependency>

        <!-- jwt工具类 -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.11.2</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.11.2</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.11.2</version>
            <scope>runtime</scope>
        </dependency>

    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-parent</artifactId>
                <version>${spring-boot.version}</version>
                <scope>import</scope>
                <type>pom</type>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <scope>import</scope>
                <type>pom</type>
            </dependency>
        </dependencies>
    </dependencyManagement>
```

### 配置文件

```yaml
server:
  port: 9801

spring:
  application:
    name: security-user
  profiles:
    active: dev
  cloud:
    config:
      label: master
      name: ${spring.application.name}
      discovery:
        enabled: true
        service-id: config-server
  datasource:
    url: jdbc:mysql://192.168.32.225:3306/uaa_server?characterEncoding=utf8&useUnicode=true&useSSL=false&serverTimezone=UTC&allowMultiQueries=true
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: hxr
  redis:
    host: 116.62.148.11
    port: 6380
    password:
    jedis:
      pool:
        max-active: 8
        max-idle: 8
        max-wait: -1s
        min-idle: 0
  rabbitmq:
    host: 116.62.148.11
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
  jpa:
    #配置数据库类型
    database: mysql
    #指定数据库的引擎
    database-platform: org.hibernate.dialect.MySQL57Dialect
    #配置是否打印sql
    show-sql: true
    #Hibernate相关配置
    hibernate:
      #配置级联等级
      #      ddl-auto: create
      ddl-auto: update
    open-in-view: false
#    jackson:
#      property-naming-strategy: CAMEL_CASE_TO_LOWER_CASE_WITH_UNDERSCORES


eureka:
  client:
    service-url:
      defaultZone: http://192.168.32.230:8761/eureka
  instance:
    prefer-ip-address: true
    health-check-url-path: /actuator/health

management:
  endpoints:
    web:
      exposure:
        include: refresh,health,info,env
  endpoint:
    health:
      show-details: always

feign:
  httpclient:
    connection-timeout: 2000

jwt:
  # 老用户系统公钥
  publicKey: "MII......wIDAQAB"
```

### 配置类

**令牌配置**

```java
@Configuration
public class TokenConfig {

//    private static final String SIGNING_KEY = "uaa123";

    @Resource
    private UaaFeign uaaClient;

    @Resource
    private Environment environment;

    @Bean
    public PublicKey hifunPublicKey() throws IOException, NoSuchAlgorithmException, InvalidKeySpecException {
        String hifunPublicKey = environment.getProperty("jwt.publicKey");
        System.out.println("***publicKeyStr：" + hifunPublicKey);
        byte[] keyBytes = (new BASE64Decoder()).decodeBuffer(hifunPublicKey);
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        PublicKey rsaPublicKey = keyFactory.generatePublic(keySpec);
        return rsaPublicKey;
    }

    /**
     * 将Jwt作为令牌
     *
     * @return
     */
    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter());
    }

    /**
     * 配置Jwt令牌（秘钥）
     *
     * @return
     */
    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
//        JwtAccessTokenConverter converter = new JwtAccessTokenConverter();
        MyJwtAccessTokenConverter converter = new MyJwtAccessTokenConverter();
//        converter.setSigningKey(SIGNING_KEY);

        String publicKey = uaaClient.publicKey();
        System.out.println("publicKey: " + publicKey);
        converter.setVerifierKey(publicKey);
        converter.setVerifier(new RsaVerifier(publicKey));

        return converter;
    }

}
```

**基础配置**

```java
import oauth2.config.auth.rewrite.MyAccessDeniedHandler;
import oauth2.config.auth.rewrite.MyAuthExceptionEntryPoint;
import oauth2.config.auth.rewrite.MyTokenExtractor;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.oauth2.config.annotation.web.configuration.EnableResourceServer;
import org.springframework.security.oauth2.config.annotation.web.configuration.ResourceServerConfigurerAdapter;
import org.springframework.security.oauth2.config.annotation.web.configurers.ResourceServerSecurityConfigurer;
import org.springframework.security.oauth2.provider.token.TokenStore;

import javax.annotation.Resource;

@Configuration
public class ResourceServerConfig {

    private static final String RESOURCE_ID = "res1";

    @Resource
    private TokenStore tokenStore;

    @Resource
    private MyAuthExceptionEntryPoint myAuthExceptionEntryPoint;

    @Resource
    private MyAccessDeniedHandler myAccessDeniedHandler;

    @Resource
    private MyTokenExtractor myTokenExtractor;

    @Configuration
    @EnableResourceServer
    public class UserServerConfig extends ResourceServerConfigurerAdapter {
        @Override
        public void configure(ResourceServerSecurityConfigurer resources) throws Exception {
            resources.resourceId(RESOURCE_ID)
                    .tokenStore(tokenStore)
                    .stateless(true)
                    .tokenExtractor(myTokenExtractor)
                    .authenticationEntryPoint(myAuthExceptionEntryPoint)
                    .accessDeniedHandler(myAccessDeniedHandler);
        }

        @Override
        public void configure(HttpSecurity http) throws Exception {
            http.csrf().disable().authorizeRequests()
//                    .antMatchers("/order/**").access("#oauth2.hasScope('ROLE_ADMIN')");
                    .antMatchers("/user/getTbUser**", "/user/getRoleCodes", "/user/getAuthorities","/uc/permission").permitAll()
                    .antMatchers("/user/**").hasAnyAuthority("hifun")/*access("#oauth2.hasScope('ROLE_USER')")*/
                    .antMatchers("/administrator/**").hasAnyAuthority("/users/");
        }
    }

}
```



### Feign

老用户体系的接口

```java
@FeignClient(name = "hifun-service-user")
public interface HifunFeign {

    /**
     * 验证密码
     * @param id
     * @param password
     * @return
     */
    @PostMapping(path = "/password/check", consumes = "application/json")
    String check(@RequestParam("id") Integer id, @RequestBody String password);

    /**
     * 根据手机号获取用户信息
     * @param mobile
     * @return
     */
    @GetMapping(path = "/user/mobile")
    String mobile(@RequestParam("mobile") String mobile);

    /**
     * 根据用户id获取用户信息
     * @param id
     * @return
     */
    @GetMapping(path = "/user/{id}")
    String getUserInfo(@PathVariable("id") Integer id);


}
```

获取认证服务的公钥

```java
@FeignClient("SECURITY-UAA")
public interface UaaFeign {

    @GetMapping(path = "/feign/uaa/publicKey")
    String publicKey();

}
```

过期token接口

```java
@RestController
@Api(value = "需要拦截的token")
public class ExpiredTokenController {

    @Resource
    private RedisTemplate<String,Object> redisTemplate;

    @Resource
    private RedisKeyConfig redisKeyConfig;

    @GetMapping(path = "/feign/user/getExpiredToken")
    public Map<Object,Object> getExpiredToken(){
//        redisTemplate.opsForHash().putIfAbsent(redisKeyConfig.getExpiredTokenKey(),"admin",1601455413);
//        Map<Object, Object> entries = redisTemplate.opsForHash().entries(redisKeyConfig.getExpiredTokenKey());
//        System.out.println("feign调用成功" + entries);
        return redisTemplate.opsForHash().entries(redisKeyConfig.getExpiredTokenKey());
    }

}
```







## 3.5 Gateway网关

**依赖**

```xml
   <properties>
        <spring-cloud.version>Hoxton.SR3</spring-cloud.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <optional>true</optional>
            <scope>runtime</scope>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>

        <!-- swagger -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.9.2</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.9.2</version>
        </dependency>

        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
            <version>3.4</version>
        </dependency>

        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.3.3</version>
        </dependency>

    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <scope>import</scope>
                <type>pom</type>
            </dependency>
        </dependencies>
    </dependencyManagement>
```



### 配置文件

```yaml
server:
  port: 8100

spring:
  application:
    name: gateway-server
  profiles:
    active: dev
  cloud:
    gateway:
#      default-filters:  #全局过滤器
      #        - name: Hystrix
      #          args:
      #           name: fallbackcmd  #使用HystrixCommand打包剩余的过滤器，并命名为fallbackcmd
      #           fallbackUri: forward:/fallback  #配置fallbackUri，降级逻辑被调用
      discovery:
        locator:
          enabled: true
      routes:
        - id: SECURITY-UAA
          uri: lb://SECURITY-UAA
          predicates:
            - Path=/uaa/**
          filters:
            - PreserveHostHeader
        #           - RewritePath=/uaa(?<segment>/?.*), $\{segment}UAA-CENTER
        - id: SECURITY-USER
          uri: lb://SECURITY-USER
          predicates:
            - Path=/uc/**
          filter:
            - PreserveHostHeader
      globalcors: #跨域配置
        corsConfigurations:
          '[/**]':
            allowedOrigins: "*"
            allowedMethods: "*"

eureka:
  client:
    fetch-registry: true
    register-with-eureka: true
    service-url:
      defaultZone: http://hxr:hxr123@192.168.33.236:8761/eureka/
  instance:
    prefer-ip-address: true

#设置feign客户端负载均衡和超时时间(OpenFeign默认支持ribbon)
ribbon:
  #开启ribbon负载均衡
  eureka:
    enabled: true
  # ribbon请求连接的超时时间,默认值5000
  ConnectTimeout: 1000
  # 负载均衡超时时间,默认值5000
  ReadTimeout: 1000
  # 是否开启重试
  OkToRetryOnAllOperations: true
  # 重试期间，实例切换次数
  MaxAutoRetriesNextServe: 2
  # 当前实例重试次数
  MaxAutoRetries: 1


feign:
  hystrix:
    enabled: false # 开启Feign的熔断功能
#  断路器的超时时间需要大于ribbon的超时时间，不然不会触发重试
hystrix:
  command:
    default:
      execution:
        isolation:
          thread:
            timeoutInMilliseconds: 60000 # 设置hystrix的超时时间为60000ms

management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always

cron:
  black-ip: 0 0/5 * * * ?
  sync_expired_token: 0 0/5 * * * ?
```

> 注意：如果放到springcloud框架中，授权码模式登陆需要经过nginx和gateway才会到达微服务，而在gateway中会对请求进行重定向，并将请求头中的信息进行改写。授权码模式下重定向的地址会读取请求头中的信息，所以最终重定向地址会指向微服务而不是nginx。所以在gateway中进行转发时，不能改变请求头中的信息，需要在gateway的配置文件中添加拦截器PreserveHostHeader。
>
> 最终在框架中进行重定向的地址指向nginx。
