# 一、普通路由规则
## 1.1 域名路由规则的写法：

**①预定义域名列表 geosite:**

以 geosite: 开头，后面是一个预定义域名列表名称，如 geosite:google ，意思是包含了Google旗下绝大部分域名；或者 geosite:cn，意思是包含了常见的大陆站点域名。常用名称及域名列表：

```
category-ads：包含了常见的广告域名。

category-ads-all：包含了常见的广告域名，以及广告提供商的域名。

cn：相当于 geolocation-cn 和 tld-cn 的合集。

apple：包含了 Apple 旗下绝大部分域名。

google：包含了 Google 旗下绝大部分域名。

microsoft：包含了 Microsoft 旗下绝大部分域名。

facebook：包含了 Facebook 旗下绝大部分域名。

twitter：包含了 Twitter 旗下绝大部分域名。

telegram：包含了 Telegram 旗下绝大部分域名。

geolocation-cn：包含了常见的大陆站点域名。

geolocation-!cn：包含了常见的非大陆站点域名，同时包含了 tld-!cn。

tld-cn：包含了 CNNIC 管理的用于中国大陆的顶级域名，如以 .cn、.中国 结尾的域名。

tld-!cn：包含了非中国大陆使用的顶级域名，如以 .hk（香港）、.tw（台湾）、.jp（日本）、.sg（新加坡）、.us（美国）.ca（加拿大）等结尾的域名。
```

更多域名类别，请查看 data 目录


**②域名 domain:**

由 domain: 开始，后面是一个域名。例如 domain:baiyunju.cc ，匹配 www.baiyunju.cc 、baiyunju.cc，以及其他baiyunju.cc主域名下的子域名。

不过，前缀domain:可以省略，只输入域名，其实也就成了纯字符串了。


**③完整匹配 full:**

由 full: 开始，后面是一个域名。例如 full:baiyunju.cc 只匹配 baiyunju.cc，但不匹配 www.baiyunju.cc 。



**④纯字符串**

比如直接输入 sina.com, 可以分行，也可以不分行以“,”隔开，可以匹配 sina.com、sina.com.cn 和 www.sina.com，但不匹配 sina.cn。



**⑤正则表达式 regexp:**

由 regexp: 开始，后面是一个正则表达式。例如 regexp:\.goo.*\.com$ 匹配 www.google.com、fonts.googleapis.com，但不匹配 google.com。



**从外部文件中加载域名规则 ext:**

比如 ext:file:tag，必须以 ext:（全部小写）开头，后面跟文件名（不含扩展名）file 和标签 tag，文件必须存放在 V2Ray 核心的资源目录中，文件格式与 geosite.dat 相同，且指定的标签 tag 必须在文件中存在。

说明：普通用户常用的也就是上面的“纯字符串”规则写法，比如，在代理（或直连）栏下填写 baiyunju.cc,　就可以让网站通过代理（或直连）上网。


## 1.2 IP路由规则的写法:
**①geoip:**
以 geoip:（全部小写）开头，后面跟双字符国家代码，如 geoip:cn ，意思是所有中国大陆境内的 IP 地址，geoip:us 代表美国境内的 IP 地址。

特殊值：
geoip:private，包含所有私有地址，如127.0.0.1（本条规则仅支持 V2Ray 3.5 以上版本）。

**②IP：**
如 127.0.0.1，20.194.25.232

**③CIDR：**
如 10.0.0.0/8。

**从外部文件中加载 IP 规则：**
如 ext:file:tag，必须以 ext:（全部小写）开头，后面跟文件名（不含扩展名）file 和标签 tag，文件必须存放在 V2Ray 核心的资源目录中，文件格式与 geoip.dat 相同，且指定的 tag 必须在文件中存在。


<br>
# 二、高级路由

**①V2RayN高级路由策略PAC设置规则**
```
[
  {
    "outboundTag": "proxy",
    "domain": [
      "#以下三行是GitHub网站，为了不影响下载速度走代理",
      "github.com",
      "githubassets.com",
      "githubusercontent.com"
    ]
  },
  {
    "outboundTag": "block",
    "domain": [
      "#阻止CrxMouse鼠标手势收集上网数据",
      "mousegesturesapi.com"
    ]
  },
  {
    "outboundTag": "direct",
    "domain": [
      "bitwarden.com",
      "bitwarden.net",
      "baiyunju.cc",
      "letsencrypt.org",
      "adblockplus.org",
      "safesugar.net",
      "#下两行谷歌广告",
      "googleads.g.doubleclick.net",
      "adservice.google.com",
      "#【以下全部是geo预定义域名列表】",
      "#下一行是所有私有域名",
      "geosite:private",
      "#下一行包含常见大陆站点域名和CNNIC管理的大陆域名，即geolocation-cn和tld-cn的合集",
      "geosite:cn",
      "#下一行包含所有Adobe旗下域名",
      "geosite:adobe",
      "#下一行包含所有Adobe正版激活域名",
      "geosite:adobe-activation",
      "#下一行包含所有微软旗下域名",
      "geosite:microsoft",
      "#下一行包含微软msn相关域名少数与上一行微软列表重复",
      "geosite:msn",
      "#下一行包含所有苹果旗下域名",
      "geosite:apple",
      "#下一行包含所有广告平台、提供商域名",
      "geosite:category-ads-all",
      "#下一行包含可直连访问谷歌网址，需要替换为加强版GEO文件，如已手动更新为加强版GEO文件，删除此行前面的#号使其生效",
      "#geosite:google-cn",
      "#下一行包含可直连访问苹果网址，需要替换为加强版GEO文件，如已手动更新为加强版GEO文件，删除此行前面的#号使其生效",
      "#geosite:apple-cn"
    ]
  },
  {
    "type": "field",
    "outboundTag": "proxy",
    "domain": [
      "#GFW域名列表",
      "geosite:gfw",
      "geosite:greatfire"
    ]
  },
  {
    "type": "field",
    "port": "0-65535",
    "outboundTag": "direct"
  }
]
```
>说明：上面V2Ray高级路由规则集，完美实现了PAC代理模式，效果完全一样。其原理是，GFW黑名单中的域名走代理，剩余的其他连接0-65535所有端口的所有国内、外网站流量全部直连。
>如需要更新官方geo文件，请参考[《V2Ray路由规则加强版资源文件geoip.dat、geosite.dat下载网址、更新方法》](https://baiyunju.cc/7583)https://baiyunju.cc/7583　。
>其中，第三行直连域名规则中的域名较多，其实这一行”direct”规则原本可以全部删掉，但是在使用中发现，有一些本来可以直连的域名，也被放入GFW列表中走代理了，为了避免有漏网域名没走直连，因此直接将之前基础路由功能中的直接域名列表复制过来，与后面两行规则并不冲突。


**②Whitelist白名单（绕过大陆代理模式）**
也就是CNNIC 管理的用于中国大陆的顶级域名，以及服务器位于中国内陆的IP，全部直连，其他所有网址代理。

不过，其中有一些可以连接没有被墙的国外网址，也放进了直连规则内，如果不需要可以自己修改。
```
[
  {
    "port": "",
    "outboundTag": "proxy",
    "ip": [],
    "domain": [
      "#以下三行是GitHub网站，为了不影响下载速度走代理",
      "github.com",
      "githubassets.com",
      "githubusercontent.com"
    ],
    "protocol": []
  },
  {
    "type": "field",
    "outboundTag": "block",
    "domain": [
      "#阻止CrxMouse鼠标手势收集上网数据",
      "mousegesturesapi.com",
      "#下一行广告管理平台网址，在ProductivityTab（原iChrome）浏览器插件页面显示",
      "cf-se.com"
    ]
  },
  {
    "type": "field",
    "port": "",
    "outboundTag": "direct",
    "ip": [
      "geoip:private",
      "geoip:cn"
    ],
    "domain": [
      "bitwarden.com",
      "bitwarden.net",
      "gravatar.com",
      "gstatic.com",
      "baiyunju.cc",
      "letsencrypt.org",
      "adblockplus.org",
      "safesugar.net",
      "#下两行谷歌广告",
      "googleads.g.doubleclick.net",
      "adservice.google.com",
      "#【以下全部是geo预定义域名列表】",
      "#下一行包含所有私有域名",
      "geosite:private",
      "#下一行包含常见大陆站点域名和CNNIC管理的大陆域名，即geolocation-cn和tld-cn的合集",
      "geosite:cn",
      "#下一行包含所有Adobe旗下域名",
      "geosite:adobe",
      "#下一行包含所有Adobe正版激活域名",
      "geosite:adobe-activation",
      "#下一行包含所有微软旗下域名",
      "geosite:microsoft",
      "#下一行包含微软msn相关域名少数与上一行微软列表重复",
      "geosite:msn",
      "#下一行包含所有苹果旗下域名",
      "geosite:apple",
      "#下一行包含所有广告平台、提供商域名",
      "geosite:category-ads-all",
      "#下一行包含可直连访问谷歌网址，需要替换为加强版GEO文件，如已手动更新为加强版GEO文件，删除此行前面的#号使其生效",
      "#geosite:google-cn",
      "#下一行包含可直连访问苹果网址，需要替换为加强版GEO文件，如已手动更新为加强版GEO文件，删除此行前面的#号使其生效",
      "#geosite:apple-cn"
    ],
    "protocol": []
  },
  {
    "type": "field",
    "port": "0-65535",
    "outboundTag": "proxy"
  }
]
```

**③全局代理**
所有上网连接全部走代理。
```
[
  {
    "port": "",
    "outboundTag": "block",
    "ip": [],
    "domain": [
      "#阻止CrxMouse鼠标手势收集上网数据",
      "mousegesturesapi.com",
      "#下一行广告管理平台网址，在ProductivityTab（原iChrome）浏览器插件页面显示",
      "cf-se.com"
    ],
    "protocol": []
  },
  {
    "type": "field",
    "port": "0-65535",
    "outboundTag": "proxy"
  }
]
```

**④全局直连**

所有上网连接全部直连。
```
[
  {
    "port": "",
    "outboundTag": "block",
    "ip": [],
    "domain": [
      "#阻止CrxMouse鼠标手势收集上网数据",
      "mousegesturesapi.com",
      "#下一行广告管理平台网址，在ProductivityTab（原iChrome）浏览器插件页面显示",
      "cf-se.com"
    ],
    "protocol": []
  },
  {
    "port": "",
    "outboundTag": "proxy",
    "ip": [],
    "domain": [
      "#下一行ProductivityTab（原iChrome）浏览器插件",
      "ichro.me"
    ],
    "protocol": []
  },
  {
    "type": "field",
    "port": "0-65535",
    "outboundTag": "direct"
  }
]
```


**⑤全局阻断**
阻断所有上网连接。
```
[
  {
    "type": "field",
    "port": "0-65535",
    "outboundTag": "block",
    "ip": [],
    "domain": [],
    "protocol": []
  }
]
```

>**几点重要说明:** 高级路由功能中“预定义规则集列表”中的各行规则，不要随意改变排列顺序。因为，越在上面的规则，优先级别越大。调整顺序后，也会改变代理模式。
例如，在黑名单PAC代理模式规则集中，第二行是“proxy”代理规则，如果里面添加了域名baiyunju.cc，而第三行“direct”直连规则中，也添加了baiyunju.cc这个网址，那么，因为第二行比第三行更靠前，因此baiyunju.cc会按照第二行的规则连接网络，忽略第三行的设置。

<br>
# 三、域名解析策略
“AsIs”、”IPIfNonMatch”、”IPOnDemand”三个域名解析策略是什么意思，有什么区别？

- “AsIs”：只使用域名进行路由选择。快速解析，不精确分流。默认值。
- “IPIfNonMatch”：当域名没有匹配任何规则时，将域名解析成 IP（A 记录或 AAAA 记录）再次进行匹配；当一个域名有多个 A 记录时，会尝试匹配所有的 A 记录，直到其中一个与某个规则匹配为止；
解析后的 IP 仅在路由选择时起作用，转发的数据包中依然使用原始域名；理论上解析比”AsIs”稍慢，但使用中通常不会觉察到。
- “IPOnDemand”：当匹配时碰到任何基于 IP 的规则，将域名立即解析为 IP 进行匹配。解析最精确，也最慢。

<br>
**V2Ray域名策略解析选择哪个更好？**
虽然V2Ray官方解释”AsIs”是默认值，但是实际上，在几款主流客户端中，有的默认值是”AsIs”，有的是”IPIfNonMatch”。

因此，选择”AsIs”或”IPIfNonMatch”都可以。

但是，如果在自定义路由设置规则时，添加了匹配IP的路由代理规则，比如geoip:cn、geoip:private，或者直接添加的IP地址规则，那么，建议必须选择位于中间的”IPIfNonMatch”，不然，匹配IP地址的路由规则不会生效。

<br>
# 四、代理模式
“清除系统代理”、“自动配置系统代理”、“不改变系统代理”，是什么意思？应选择哪一个？哪个是V2Ray全局代理？
- “清除系统代理”：禁用Windows系统（IE）代理，不能翻墙；
- “自动配置系统代理”：全局代理模式，所有连接走VPN（再通过V2Ray客户端的路由设置进行分流，达到类似PAC代理模式的效果）；
- “不改变系统代理”：根据Windows设置内的代理状态决定是否开启代理，也就是维持Windows系统（IE）设置。
