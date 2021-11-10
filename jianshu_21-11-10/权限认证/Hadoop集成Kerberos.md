# 三、配置
## 3.1 服务端
**编辑 vim /etc/krb5.conf**
```
[logging]
  default = FILE:/var/log/krb5libs.log
  kdc = FILE:/var/log/krb5kdc.log
  admin_server = FILE:/var/log/kadmind.log

[libdefaults]
  default_realm = MARSSENGER.COM
  dns_lookup_realm = false
  dns_lookup_kdc = false
  ticket_filetime = 24h
  renew_lifetime = 7d
  forwardable = true

[realms]
  MARSSENGER.COM = {
    kdc = bigdata3
    admin_server = bigdata3
  }

[domain_realm]
  *.marssenger.com = MARSSENGER.COM
  marssenger.com = MARSSENGER.COM
```
>[realms] 表示域，可以创建多个域
[domain_realm] 表示进行域名转换，匹配到的域名都转换到指定的域

<br>
**编辑 vim /var/kerberos/krb5kdc/kdc.conf**
```
[kdcdefaults]
  kdc_ports = 88
  kdc_tcp_ports = 88
[realms]
  MARSSENGER.COM = {
    #master_key_type = aes256-cts
    acl_file = /var/kerberos/krb5kdc/kadm5.acl
    dict_file = /usr/share/dict/words
    admin_keytab = /var/kerberos/krb5kdc/kadm5.keytab
    supported_enctypes = aes256-cts:normal aes128-cts:normal des3-hmac-sha1:normal arcfour-hmac:normal des-hmac-sha1:normal des-cbc-md5:normal des-cbc-crc:normal
  }
```
>[kdcdefaults] 对kdc进行配置，指定了kdc的端口
[realms] 对域进行详细的配置
keytab是最终获取到的Ticket，可以在Server进行验证。这个keytab是admin的Ticket，不需要去AS和TGS换取Ticket，而是在本地保存了Ticket。
supported_enctypes是支持的加密类型

<br>
**编辑 vim /var/kerberos/krb5kdc/kadm5.acl**
```
*/admin@MARSSENGER.COM  *
```
>符合该规则*/admin的账户，拥有MARSSENGER.COM域的所有权限。account/instance@Realm

<br>
## 3.2 客户端
**编辑 vim /etc/krb5.conf**
```
[logging]
  default = FILE:/var/log/krb5libs.log
  kdc = FILE:/var/log/krb5kdc.log
  admin_server = FILE:/var/log/kadmind.log

[libdefaults]
  default_realm = MARSSENGER.COM
  dns_lookup_realm = false
  dns_lookup_kdc = false
  ticket_filetime = 24h
  renew_lifetime = 7d
  forwardable = true

[realms]
  MARSSENGER.COM = {
    kdc = bigdata3
    admin_server = bigdata3
  }

[domain_realm]
  *.marssenger.com = MARSSENGER.COM
  marssenger.com = MARSSENGER.COM
```
>把服务端配置完的复制过来即可

<br>
# 四、启动
## 4.1 服务端
1. **初始化Kerberos的数据库**
输入`kdb5_util create -s -r MARSSENGER.COM`创建
然后创建密码，我们使用`bigdata123`作为密码
这样就得到了数据库master账户：`K/M@MARSSENGER.COM`，密码`bigdata123`

2. **查看目录/var/kerberos/krb5kdc**
发现多了4个文件principal，principal.kadm5，principal.kadm5.lock，principal.ok

3. **进入kadmin后台**
执行`kadmin.local`，本机登陆不需要密码。

4. **创建管理员用户**
`addprinc root/admin@MARSSENGER.COM`

5. **重启krb5kdc和kadmin服务，并设置开机启动**
`systemctl restart krb5kdc`
`systemctl restart kadmin restart`
`chkconfig krb5kdc on`
`chkconfig kadmin on`

## 4.2 客户端
1. 执行`kinit root/admin@MARSSENGER.COM`，如果没有任何输出，说明服务端已认证完成。

2. 执行`klist`，可以获取该用户的keytab
```
[hxr@cos-bigdata-hadoop-03 krb5kdc]$ sudo klist
Ticket cache: FILE:/tmp/krb5cc_0
Default principal: root/admin@MARSSENGER.COM

Valid starting       Expires              Service principal
2021-07-28T14:58:40  2021-07-29T14:58:40  krbtgt/MARSSENGER.COM@MARSSENGER.COM
```

3. 执行`kadmin`可以远程连接到管理后台。


<br>
# 五、Hadoop配置Kerberos的principal









<br>
# 附：Kerberos相关命令
| 进入kadmin | kadmin.local / kadmin |
| --- | --- |
| 创建数据库 | kdb5_util create -r HADOOP.COM -s　 |
| 启动kdc服务 | systemctl start krb5kdc |
| 启动kadmin服务 | systemctl stop krb5kdc　 |
| 修改当前密码 | kpasswd |
| 测试keytab可用性 | kinit -k -t /home/chen/cwd.keytab [chenweidong@HADOOP.COM](mailto:chenweidong@HADOOP.COM) |
| 查看keytab | klist -e -k -t /home/chen/cwd.keytab　 |
| 清除缓存 | kdestroy |
| 通过keytab文件认证登录 | kinit -kt /home/chen/cwd.keytab [chenweidong@HADOOP.COM](mailto:chenweidong@HADOOP.COM) |

| kadmin模式下： |  |
| --- | --- |
| 生成随机key的principal | addprinc -randkey root/[master@HADOOP.COM](mailto:master@HADOOP.COM) |
| 生成指定key的principal | addprinc -pw admin/[admin@HADOOP.COM](mailto:admin@HADOOP.COM) |
| 查看principal | listprincs |
| 修改admin/admin的密码 | cpw -pw xxxx admin/admin |
| 添加/删除principle | addprinc/delprinc admin/admin |
| 直接生成到keytab | ktadd -k /home/chen/cwd.keytab [chenweidong@HADOOP.COM](mailto:chenweidong@HADOOP.COM)xst -norandkey -k /home/chen/cwd.keytab [chenweidong@HADOOP.COM](mailto:chenweidong@HADOOP.COM) #注意：在生成keytab文件时需要加参数”-norandkey”，否则会导致直接使用kinit [chenweidong@HADOOP.COM](mailto:chenweidong@HADOOP.COM)初始化时会提示密码错误。 |
| 设置密码策略(policy) | addpol -maxlife "90 days" -minlife "75 days" -minlength 8 -minclasses 3 -maxfailure 10 -history 10 user |
| 添加带有密码策略的用户 | addprinc -policy user hello/[admin@HADOOP.COM](mailto:admin@HADOOP.COM) |
| 修改用户的密码策略 | modprinc -policy user1 hello/[admin@HADOOP.COM](mailto:admin@HADOOP.COM) |
| 删除密码策略 | delpol [-force] user |
| 修改密码策略 | modpol -maxlife "90 days" -minlife "75 days" -minlength 8 -minclasses 3 -maxfailure 10 user |
