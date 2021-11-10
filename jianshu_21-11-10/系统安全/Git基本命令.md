# 一、Git登录设置
## 1.1 Git设置秘钥ssh登录，这样在推送和拉去代码时可以免去输入账号密码：
1. 打开Git Bash Here
2. ssh-keygen -t rsa -C 'cj21' 创建公私钥，默认保存在当前用户下的.ssh文件夹中
3. 将id_rsa.pub中的内容粘贴到gitee中的SSH公钥中完成配置。
如果是Github，则点击 settings -> SSH and GPG keys -> New SSH key 将公钥粘贴进去并创建。
如果需要销毁该公钥，则点击 settings -> Account secutiry -> Sessions ，找到目标公钥并删除即可。

## 1.2 Git使用token登录
因为某些原因，使用账号密码登录失败，可以使用token进行登录。
1. 点击 Settings -> Developer settings ->  Generate a personal access token 创建token

<br>
# 二、文件同步
## 2.1 Git推送本地文件
```
$ git init     #初始化当前文件
$ git add .     #将本地文件添加到待提交目录(不包括删除操作)
$ git commit -m '提交文件'      #将待提交目录中的文件提交本地仓库
$ git remote add origin [你的远程库地址]      #关联到远程库
$ git push -u origin master     #当前分支推送到远程仓库的master分支
$ git push origin chenjie:chenjie  #推送到指定分支(将本地chenjie分支推送到远程origin地址的chenjie分支上)
```
注：
```
$git status    #查看文件状态(标红的为修改的文件)
$git add -u      #提交被修改和删除的文件，不含添加的文件
$git add -A      #提交所有的变化
```

## 2.2 复制原分支代码到新分支
1、切换到原分支
```
$ git checkout oldBranch
$ git pull
```
2、从原分支复制到新分支
```
$ git checkout -b newBranch
```
3、将新分支的代码推送到远程服务器
```
$ git push origin newBranch
```
4、拉取远程分支的代码
```
$ git pull
```
5、关联
```
$git branch --set-upstream-to=origin/newBranch
```
6、再次拉取代码
```
$ git pull
```

## 2.3 拉取指定分支的远程仓库代码
```
git clone -b develop XXX 
```

## 2.4 github中的教程
**create a new repository on the command line**
```
echo "# FineDB_Bigdata_Script" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ChenJie666/FineDB_Bigdata_Script.git
git push -u origin main
```

**push an existing repository from the command line**
```
git remote add origin https://github.com/ChenJie666/FineDB_Bigdata_Script.git
git branch -M main
git push -u origin main
```

<br>
# 三、Linux下Git保存用户密码
**Git使用store模式存储账号密码**
store模式，认证信息会被明文保存在一个本地文件中，并且没有过期限制。使用git命令需要认证的时候，就会自动从这里读取用户认证信息完成认证。创建步骤如下：
1. 用户目录下创建文件并编辑文件 `.git-credentials` 如下
```
https://{username}:{password}@github.com 
```
>这里可以直接填写明文的账号密码。但是为了安全，这里的password一般并不是账户的密码，以Github为例，这里使用的是AccessToken（oauth2:access_token），可以在Settings-Developer Settings-Personal access tokens中生成新的密钥，然后配置git-credentials使用此密钥访问。
配置好credentials服务和密钥后，在其它使用git命令需要认证的时候，就会自动从这里读取用户认证信息完成认证了。

2. 在终端下执行 
`git config --global credential.helper store`

3. 可以看到~/.gitconfig文件，会多了一项：
   ```
   [credential]
   helper = store
   ```

当使用的目标地址匹配时，会自动使用该账号密码。


<br>
# 四、Git忽略规则(.gitignore配置)不生效原因和解决
## 4.1 第一种方法:
.gitignore中已经标明忽略的文件目录下的文件，git push的时候还会出现在push的目录中，或者用git status查看状态，想要忽略的文件还是显示被追踪状态。
原因是因为在git忽略目录中，新建的文件在git中会有缓存，如果某些文件已经被纳入了版本管理中，就算是在.gitignore中已经声明了忽略路径也是不起作用的，
这时候我们就应该先把本地缓存删除，然后再进行git的提交，这样就不会出现忽略的文件了。
  
解决方法: git清除本地缓存（改变成未track状态），然后再提交:
```
$ git rm -r --cached .
$ git add .
$ git commit -m 'update .gitignore'
$ git push -u origin master
```

**需要特别注意的是：**
1）.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。
2）想要.gitignore起作用，必须要在这些文件不在暂存区中才可以，.gitignore文件只是忽略没有被staged(cached)文件，
   对于已经被staged文件，加入ignore文件时一定要先从staged移除，才可以忽略。
 
## 4.2 第二种方法:（推荐）
在每个clone下来的仓库中手动设置不要检查特定文件的更改情况。
```
$ git update-index --assume-unchanged PATH    #在PATH处输入要忽略的文件
```

在使用.gitignore文件后如何删除远程仓库中以前上传的此类文件而保留本地文件
在使用git和github的时候，之前没有写.gitignore文件，就上传了一些没有必要的文件，在添加了.gitignore文件后，就想删除远程仓库中的文件却想保存本地的文件。这时候不可以直接使用"git rm directory"，这样会删除本地仓库的文件。可以使用"git rm -r –cached directory"来删除缓冲，然后进行"commit"和"push"，这样会发现远程仓库中的不必要文件就被删除了，以后可以直接使用"git add -A"来添加修改的内容，上传的文件就会受到.gitignore文件的内容约束。

额外说明：git库所在的文件夹中的文件大致有4种状态
| 状态 | 说明 |
| --- | --- |
| Untracked | 未跟踪, 此文件在文件夹中, 但并没有加入到git库, 不参与版本控制. 通过git add 状态变为Staged. |
| Unmodify | 文件已经入库, 未修改, 即版本库中的文件快照内容与文件夹中完全一致. 这种类型的文件有两种去处, 如果它被修改，而变为Modified. 如果使用git rm移出版本库, 则成为Untracked文件 |
| Modified | 文件已修改, 仅仅是修改, 并没有进行其他的操作. 这个文件也有两个去处, 通过git add可进入暂存staged状态,使用git checkout 则丢弃修改过, 返回到unmodify状态, 这个git checkout即从库中取出文件, 覆盖当前修改 |
| Staged | 暂存状态. 执行git commit则将修改同步到库中, 这时库中的文件和本地文件又变为一致, 文件为Unmodify状态. 执行git reset HEAD filename取消暂存, 文件状态为Modified |

 
Git 状态 untracked 和 not staged的区别
1）untrack     表示是新文件，没有被add过，是为跟踪的意思。
2）not staged  表示add过的文件，即跟踪文件，再次修改没有add，就是没有暂存的意思

