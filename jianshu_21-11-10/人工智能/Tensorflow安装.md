###概述
**需要安装**
- Anocanda：工具包，包含了python基础环境，默认安装了很多实用的python包，有一个很强大的命令行管理工具conda，以及一个界面的应用管理平台；
- Jupyter notebook：科学计算的notebook工具；
- Pycharm：python开发的IDE；

###1. 首先下载Anaconda
[https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)
从清华镜像源下载后安装。

打开anaconda的命令框Anaconda Prompt，输入python可以看到python的版本。

python -m pip install --upgrade pip 更新pip版本。
conda list  查看库中的所有包

###2. 安装Visual C++
下载安装vc_redis.x64.exe

###3. 安装tensorflow2.2的CPU版本
pip install tensorflow-cpu==2.2.0 -i https://pypi.douban.com/simple/
如果不写-cpu，会根据是否有显卡自动安装对应的版本。

输入import tensorflow，没有报错说明安装完成。输入exit()退出。

###4. 在jupyter notebook中运行
>1. 打开jupyter
jupyter notebook
>2. 创建新的笔记
new -> python3
>3. 导入tensorflow并给一个别名
import tensorflow as tf
>4. 打印tensorflow的版本
tf.__version__

****
<br>
**以上是使用Anaconda安装，以下是使用conda的简易版本Miniconda进行安装**

>**需要先将Anaconda卸载干净**
>1.conda install anaconda-clean
2.anaconda-clean --yes
3.运行Uninstall-Anaconda3.exe

>**设置Miniconda**
>1.安装Miniconda
2.设置conda使用国内源：
在当前用户下创建文件 .
>```
>channels:
>    - defaults
>show_channel_urls: true
>default_channels:
>    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
>    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
>custom_channels:
>    conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
>    msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
>    bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
>    menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
>    pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
>```

>**新增镜像源**
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
>conda config --set show_channel_urls yes
>**删除镜像源**
>conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
>**查看配置的镜像源**
conda config --show-sources

>**安装jupyter notebook**
>安装 
pip install jupyter -i https://pypi.tuna.tsinghua.edu.cn/simple/
启动 
jupyter notebook
注：如果启动报错_ssl导入失败，需要将\Library\bin下的libssl-1_1-x64.dll和libcrypto-1_1-x64.dll文件复制到\DLLs文件夹下。

>**安装tensorflow相关的库**
pip install numpy pandas matplotlib sklearn -i https://pypi.tuna.tsinghua.edu.cn/simple/

<br>
****

###5. 安装tensorflow2.0的GPU版本
CUDA(通用并行计算架构，10.0版本)和cudnn(神经网络加速库，版本号不小于7.4.1)是GPU的两个依赖库，不需要手动安装。
>1. 首先检查显卡驱动版本是否大于410.x
navidia-smi 
>2. 安装基于GPU计算的tensorflow 2.0.0
conda install tensorflow-gpu==2.0.0
>3. 测试是否安装成功
import tensorflow as tf
tf.__version__
tf.test.is_gpu_available()
`返回True表示安装完成`



豆瓣源：-i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
