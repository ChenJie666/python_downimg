kubeadm是官方社区推出的一个用于快速部署kubernetes集群的工具。

这个工具能通过两条指令完成一个kubernetes集群的部署：

```
# 创建一个 Master 节点
$ kubeadm init

# 将一个 Node 节点加入到当前集群中
$ kubeadm join <Master节点的IP和端口 >
```

## 1. 安装要求

在开始之前，部署Kubernetes集群机器需要满足以下几个条件：

- 一台或多台机器，操作系统 CentOS7.x-86_x64
- 硬件配置：2GB或更多RAM，2个CPU或更多CPU，硬盘30GB或更多
- 集群中所有机器之间网络互通
- 可以访问外网，需要拉取镜像
- 禁止swap分区

## 2. 学习目标

1. 在所有节点上安装Docker和kubeadm
2. 部署Kubernetes Master
3. 部署容器网络插件
4. 部署 Kubernetes Node，将节点加入Kubernetes集群中
5. 部署Dashboard Web页面，可视化查看Kubernetes资源

## 3. 准备环境

![架构图](K8S部署.assets\f6a54aca2ece495cb90f7e4138e24bd0.png)


```
关闭防火墙：
$ systemctl stop firewalld
$ systemctl disable firewalld

关闭selinux：
$ sed -i 's/enforcing/disabled/' /etc/selinux/config 
$ setenforce 0

关闭swap：
$ swapoff -a  $ 临时
$ vim /etc/fstab  $ 永久

添加主机名与IP对应关系（记得设置主机名）：
$ cat /etc/hosts
192.168.31.62 k8s-master
192.168.31.64 k8s-node1
192.168.31.66 k8s-node2

将桥接的IPv4流量传递到iptables的链：
$ cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
$ sysctl --system
```

## 4. 所有节点安装Docker/kubeadm/kubelet

Kubernetes默认CRI（容器运行时）为Docker，因此先安装Docker。

kubelet:运行在cluster所有节点上,负责启动POD和容器.
kubeadm:用于初始化cluster.
kubectl:kubectl是kubenetes命令行工具，通过kubectl可以部署和管理应用，查看各种资源，创建，删除和更新组件.

### 4.1 安装Docker

```
$ wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo	//下载并以指定的文件名保存
$ yum -y install docker-ce-18.06.1.ce-3.el7
$ systemctl enable docker && systemctl start docker	//设置开机启动服务并启动docker服务
$ docker --version
Docker version 18.06.1-ce, build e68fc7a
```

### 4.2 添加阿里云YUM软件源

```
$ cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
//这是yum的配置文件，根据该配置的参数进行下载
```

### 4.3 安装kubeadm，kubelet和kubectl

由于版本更新频繁，这里指定版本号部署：

```
$ yum install -y kubelet-1.13.3 kubeadm-1.13.3 kubectl-1.13.3 //阿里云把依赖改了，所以会报错，可以用下面这句。
$ yum makecache fast && yum install -y kubelet-1.13.3  kubeadm-1.13.3 kubectl-1.13.3 kubernetes-cni-0.6.0
$ systemctl enable kubelet	//设置开机启动
```

## 5. 部署Kubernetes Master

```
$ kubeadm init \
  --apiserver-advertise-address=192.168.31.62 \	//master启动api组件监听的地址，与其他组件通讯的地址
  --image-repository registry.aliyuncs.com/google_containers \  //设置master拉取的镜像都是国内的
  --kubernetes-version v1.13.3 \	//指定下载的image的版本与k8s的一致
  --service-cidr=10.1.0.0/16 \	//指定service网络的ip地址段，负载均衡的虚拟ip
  --pod-network-cidr=10.244.0.0/16	//容器使用的ip地址
  
  preflight：首先会检查当前平台是否适合安装k8s，然后下载组件所需的镜像；
  kubelet-start：配置环境文件和配置文件，启动kubeadm。
  certs：生成证书存放在/etc/kubernetes/pki路径下。
  kubeconfig：配置文件放在/etc/kubernetes文件夹下。
  control-plane：使用静态pod（生命周期和kubelet相同）下载镜像，pod启动的yaml配置文件在/etc/kubernetes/manifests路径下。
  kubelet：将kubeadm的配置文件保存到k8s中的ConfigMap中存储，用于其他Node加入集群时从中拉取配置。
  patchnode：向k8s的master上报本地使用的docker接口和docker自身的信息。
  bootstraptoken：用于在node加入集群时为node颁发证书和给与授权（RBAC）。
  addons：部署两个插件，CoreDNS和Kube-proxy。CoreDNS为k8s集群中内部提供定向解析的，Kube-proxy为容器之间提供服务发现。
  当输出Kubeadm join时表示环境搭建完成。
```

由于默认拉取镜像地址k8s.gcr.io国内无法访问，这里指定阿里云镜像仓库地址。

使用kubectl工具：

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config  //将k8s生成的文件复制到默认读取的路径下
sudo chown $(id -u):$(id -g) $HOME/.kube/config
$ kubectl get nodes
NAME        STATUS     ROLES    AGE   VERSION
hadoop101   NotReady   master   74m   v1.13.3
NotReady是因为没有安装容器网络
```

## 6. 安装Pod网络插件（CNI）

```
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml

内部会下载quay.io/coreos/flannel:v0.11.0-amd64镜像，可以通过docker pull quay.io/coreos/flannel:v0.11.0-amd64进行下载

组件用于不同容器间的网络通讯。通过kubectl get pods -n kube-system指令查看状态
NAME                                READY   STATUS    RESTARTS   AGE
coredns-78d4cf999f-28gm6            1/1     Running   0          113m
coredns-78d4cf999f-54hxl            1/1     Running   0          113m
etcd-hadoop101                      1/1     Running   0          112m
kube-apiserver-hadoop101            1/1     Running   0          112m
kube-controller-manager-hadoop101   1/1     Running   0          112m
kube-flannel-ds-amd64-7bk8l         1/1     Running   0          13s
kube-proxy-kq2nb                    1/1     Running   0          113m
kube-scheduler-hadoop101            1/1     Running   0          113m
```

确保能够访问到quay.io这个registery。

## 7. 加入Kubernetes Node

Master是全局的调度者，Node是任务的执行者。

向集群添加新节点，执行在kubeadm init输出的kubeadm join命令：

```
$  kubeadm join 192.168.5.101:6443 --token 1u0a2u.3g111z3lh5hkzt9b --discovery-token-ca-cert-hash sha256:d88240269fd3c6ab18ce89b5567d2f989bc857d0eeda04314d2c8685d9777e9f

内部会下载quay.io/coreos/flannel:v0.11.0-amd64镜像，可以通过docker pull quay.io/coreos/flannel:v0.11.0-amd64进行下载。

加入集群的内部流程：Node携带Master生成的token向Master申请一个证书，访问API server获取相应的配置应用到本地，再启动pod和kubelet，上报本地docker的信息到master。

kubectl get pods -n kube-system
NAME                                READY   STATUS    RESTARTS   AGE
coredns-78d4cf999f-28gm6            1/1     Running   0          141m
coredns-78d4cf999f-54hxl            1/1     Running   0          141m
etcd-hadoop101                      1/1     Running   0          140m
kube-apiserver-hadoop101            1/1     Running   0          140m
kube-controller-manager-hadoop101   1/1     Running   0          140m
kube-flannel-ds-amd64-7bk8l         1/1     Running   0          27m
kube-flannel-ds-amd64-l9cc2         1/1     Running   0          22m
kube-flannel-ds-amd64-zmdsv         1/1     Running   0          17m
kube-proxy-2vc72                    1/1     Running   0          22m
kube-proxy-gz6lk                    1/1     Running   0          17m
kube-proxy-kq2nb                    1/1     Running   0          141m
kube-scheduler-hadoop101            1/1     Running   0          140m
多了两个flannel节点

如果一直Init，可以kubectl delete pods kube-flannel-ds-amd64-xxx -n kube-system进行删除，系统会自动再生成一个pod。
```

## 8. 测试kubernetes集群

在Kubernetes集群中创建一个pod，验证是否正常运行：

```
$ kubectl create deployment nginx --image=nginx	//创建pod，会先拉取镜像
$ kubectl expose deployment nginx --port=80 --type=NodePort//暴露应用，让外部访问
$ kubectl get pod,svc
```

访问地址：http://NodeIP:Port  

## 9. 部署 Dashboard

```
$ wget https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
将配置文件下载到本地，然后修改配置。
①默认镜像国内无法访问，修改镜像地址为： lizhenliang/kubernetes-dashboard-amd64:v1.10.1
②Dashboard Service启动的type设置为type:NodePort
③还可以设置dashboard的映射端口

通过kubectl apply -f kubernetes-dashboard.yaml将配置文件应用

$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
```



默认Dashboard只能集群内部访问，修改Service为NodePort类型，暴露到外部：

```
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
spec:
  type: NodePort
  ports:
    - port: 443
      targetPort: 8443
      nodePort: 30001
  selector:
    k8s-app: kubernetes-dashboard
```

```
$ kubectl apply -f kubernetes-dashboard.yaml
```

访问地址：http://NodeIP:30001

创建service account并绑定默认cluster-admin管理员集群角色：

```
//在kube-system命名空间下创建serviceaccount，名为为dashboard-admin
$ kubectl create serviceaccount dashboard-admin -n kube-system

//将cluster-admin(超级管理员)权限绑定到dashboard-admin
$ kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin

//查看该dashboard-admin，查找到的token名为dashboard-admin-token-6vhb6
$ kubectl get secret -n kube-system

//查看具体的token内容并复制到令牌登陆的密钥输入处
$ kubectl describe secrets -n kube-system $(kubectl -n kube-system get secret | awk '/dashboard-admin/{print $1}')
```

使用输出的token登录Dashboard。

![登录.jpg](K8S部署.assets\427958f31a6149a59f92f2ce0f4d213a.png)

![界面.jpg](K8S部署.assets\8830c432736b4880878f5b8f36b95c31.png)



