---
title: kubespray安装K8s
date: 2019-05-10 19:51:24
tags:
    - K8s
categories: 
    - K8s
toc: true
---



---

> kubespray项目地址: <https://github.com/kubernetes-sigs/kubespray>
>
> 官方参考：<http://192.168.100.150/k8s/kubespray-k8s/0812/kubespray/#/docs/getting-started>
>
> 项目分支：release-2.11
>
> K8s版本：1.15.1

<!-- more -->



*[Kubernetes (K8s)](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) is an open-source system for automating deployment, scaling, and management of containerized applications.*

[**Kubernetes (K8s)**](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/) 是一个开源容器编排引擎，用于自动化容器化应用程序的部署，扩展和管理。



![Deployment evolution](https://d33wubrfki0l68.cloudfront.net/26a177ede4d7b032362289c6fccd448fc4a91174/eb693/images/docs/container_evolution.svg)

*应用部署方式的演变历史：物理机部署  => 虚拟机部署  => 容器化部署*



## 准备



因国外网络问题，安装前需作必要的修改，写成预处理脚本如下：

pre-install.sh:

```sh
#!/bin/sh

### 安装git并clone官方安装脚本
yum install git -y
kube_version=v1.15.1
if [ ! -d kubespray ]; then
  git clone https://github.com/kubernetes-sigs/kubespray
  cd kubespray
  git checkout release-2.11
  cd -
fi

cd kubespray
if [ ! -d inventory/mycluster ]; then
  cp -r inventory/sample inventory/mycluster
fi

### 更新pip及安装依赖
if [ "$1" = "-U" ]; then
  easy_install pip
  pip install pip==8.0.3
  pip uninstall requests
  pip install -U pip
  pip install -U setuptools
  pip install -r requirements.txt
fi

################### 所有修改仅涉及以下4个文件，可事先改好另存覆盖
#inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml
#roles/download/defaults/main.yml
#roles/kubespray-defaults/defaults/main.yaml
#inventory/mycluster/

################### 若不事先准备改好的文件，可使用以下命令修改：
### 改版本号
sed -i "s/^kube_version:.*$/kube_version: $kube_version/" roles/kubespray-defaults/defaults/main.yaml
sed -i "s/^kube_version:.*$/kube_version: $kube_version/" roles/download/defaults/main.yml
sed -i "s/^kube_version:.*$/kube_version: $kube_version/" inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml

### 改镜像源
kube_image_repo=mirrorgooglecontainers
sed -i "s/^kube_image_repo:.*$/kube_image_repo: $kube_image_repo/" inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml

sed -i "s/^kube_image_repo:.*$/kube_image_repo: $kube_image_repo/" roles/download/defaults/main.yml
sed -i "s/k8s.gcr.io/$kube_image_repo/g" roles/download/defaults/main.yml
sed -i "s#gcr.io/google_containers#$kube_image_repo#g" roles/download/defaults/main.yml
sed -i "s/gcr.io/$kube_image_repo/g" roles/download/defaults/main.yml
sed -i "s#(k8s.)?gcr.io(/google_containers)?#$kube_image_repo#g" roles/download/defaults/main.yml

#nodelocaldns_version: 1.15.1
nodelocaldns_image_repo=lzzeng/k8s-dns-node-cache
sed -i 's#^nodelocaldns_image_repo:.*$'"#nodelocaldns_image_repo: $nodelocaldns_image_repo#" roles/download/defaults/main.yml

### 改二进制文件下载地址
download_url=http://192.168.100.150/k8s/$kube_version
sed -i 's#^kubeadm_download_url:.*$#kubeadm_download_url: '\""$download_url"'/kubeadm\"#' roles/download/defaults/main.yml
sed -i 's#^hyperkube_download_url:.*$#hyperkube_download_url: '\""$download_url"'/hyperkube\"#' roles/download/defaults/main.yml
sed -i 's#^calicoctl_download_url:.*$#calicoctl_download_url: '\""$download_url"'/calicoctl-linux-amd64\"#' roles/download/defaults/main.yml #1.15.1 使用 3.7.3
sed -i 's#^etcd_download_url:.*$#etcd_download_url: '\""$download_url"'/etcd-v3.3.10-linux-amd64.tar.gz\"#' roles/download/defaults/main.yml #1.15.1 使用 v3.3.10
sed -i 's#^cni_download_url:.*$#cni_download_url: '\""$download_url"'/cni-plugins-linux-amd64-v0.8.1.tgz\"#' roles/download/defaults/main.yml #1.15.1 使用 v0.8.1
sed -i 's#^crictl_download_url:.*$#crictl_download_url: '\""$download_url"'/critest-v1.15.0-linux-amd64.tar.gz\"#' roles/download/defaults/main.yml #1.15.1 使用 v1.15.0

### 可以修改内存限制，使得1G内存也可以执行安装
#sed -i 's/^minimal_node_memory_mb:.*$/minimal_node_memory_mb: 500/' roles/kubernetes/preinstall/defaults/main.yml
#sed -i 's/^minimal_master_memory_mb:.*$/minimal_master_memory_mb: 500/' roles/kubernetes/preinstall/defaults/main.yml
#sed -i 's/ansible_memtotal_mb\s*>=\s*[0-9]\+/ansible_memtotal_mb >= 500/' roles/kubernetes/preinstall/tasks/0020-verify-settings.yml

### docker加速
cat <<EOF >> inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml
# Debian docker-ce repo
docker_debian_repo_base_url: "https://mirrors.aliyun.com/docker-ce/linux/debian"
docker_debian_repo_gpgkey: "https://mirrors.aliyun.com/docker-ce/linux/debian/gpg"
dockerproject_apt_repo_base_url: "https://mirrors.aliyun.com/docker-engine/apt/repo"
dockerproject_apt_repo_gpgkey: "https://mirrors.aliyun.com/docker-engine/apt/gpg"
docker_options: "--insecure-registry= --registry-mirror=https://registry.docker-cn.com --graph= "
EOF

### 打印ansible命令
echo "再kubespray根目录执行以下命令安装或重置："
echo ansible-playbook -i inventory/mycluster/hosts.ini --become --become-user=root cluster.yml
echo ansible-playbook -i inventory/mycluster/hosts.ini --become --become-user=root reset.yml
```



inventory/mycluster/hosts.ini示例：

node1、node2是master调度节点，node1~node3是etcd节点，node3~node6是工作节点。

```ini
[all]
node1    ansible_host=192.168.100.79 ip=192.168.100.79
node2    ansible_host=192.168.100.80 ip=192.168.100.80
node3    ansible_host=192.168.100.81 ip=192.168.100.81
node4    ansible_host=192.168.100.216 ip=192.168.100.216
node5    ansible_host=192.168.100.217 ip=192.168.100.217
node6    ansible_host=192.168.100.218 ip=192.168.100.218

[kube-master]
node1
node2

[etcd]
node1
node2
node3

[kube-node]
node3
node4
node5
node6

[k8s-cluster:children]
kube-master
kube-node
```



## 安装

另找一个执行ansible的机器，并授权使其可以免密登录node1~node6：

```sh
ssh-keygen		          # 这几条命令都会提示手动确认
ssh-copy-id root@node1
ssh-copy-id root@node2
...
```

执行安装：

```sh
# 执行上述准备好的预处理脚本（对应v1.15.1版本）
sh pre-install.sh
# 按上述修改好hosts.ini后，执行ansible编排任务，等待结束即可
ansible-playbook -i inventory/mycluster/hosts.ini --become --become-user=root cluster.yml
```



## 登录

获取登录kubernetes-dashboard的token:

```sh
kubectl get svc --all-namespaces | grep kubernetes-dashboard
kubectl -n kube-system describe $(kubectl -n kube-system get secret -n kube-system -o name | grep namespace) | grep token
```

未使用keepalived时，可通过其一master登录：<https://192.168.100.79:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/>



## keepalived配置示例

node1 (master-1) 的/etc/keepalived/keepalived.conf：

```ini
! Configuration File for keepalived

global_defs {
   router_id LVS_DEVEL
}

vrrp_script check_haproxy {
    script "killall -0 haproxy"
    interval 3
    weight -2
    fall 10
    rise 2
}

vrrp_instance VI_1 {
    state MASTER
    interface ens32
    virtual_router_id 78
    priority 120
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass xxxxxxxxxxxxxxxx
    }
    virtual_ipaddress {
        192.168.100.78
    }
    track_script {
        check_haproxy
    }
}
```



node2 (master-2) 的/etc/keepalived/keepalived.conf：

```ini
! Configuration File for keepalived

global_defs {
   router_id LVS_DEVEL
}

vrrp_script check_haproxy {
    script "killall -0 haproxy"
    interval 3
    weight -2
    fall 10
    rise 2
}

vrrp_instance VI_1 {
    state BACKUP
    interface ens32
    virtual_router_id 78
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass xxxxxxxxxxxxxxxx
    }
    virtual_ipaddress {
        192.168.100.78
    }
    track_script {
        check_haproxy
    }
}
```

仅`state BACKUP`和`priority 100`两处不同。



---

**补充（1.14.1）**

- 修改了配置文件中的镜像地址

  - inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml
  - roles/download/defaults/main.yml

  大部分镜像可以改从registry.cn-hangzhou.aliyuncs.com/google_containers获取。

  

- 不能直接下载的软件

  通过浏览器（已设置google代理）下载kubeadm和hyperkube，放置在内网文件服务器中。hyperkube和kubeadm包会被下载到所有k8s节点的/tmp/releases目录下。

```yaml
# kubeadm_download_url: https://storage.googleapis.com/kubernetes-release/release/v1.14.1/bin/linux/amd64/kubeadm
# hyperkube_download_url: https://storage.googleapis.com/kubernetes-release/release/v1.14.1/bin/linux/amd64/hyperkube
```



- 不能从Ali镜像库获取的镜像

  - k8s.gcr.io/cluster-proportional-autoscaler-amd64:1.4.0
  - k8s.gcr.io/k8s-dns-node-cache:1.15.1

  

- 执行

```sh
pip install -r requirements.txt

ansible-playbook -i inventory/mycluster/hosts.ini --become --become-user=root cluster.yml
```



- 如何清理

```sh
ansible -i inventory/mycluster/hosts.ini all -m script -a '/opt/clean.sh'
# 或者
ansible-playbook -i inventory/mycluster/hosts.ini --become --become-user=root reset.yml
```



clean.sh:

```sh
#!/bin/sh

rm -rf /etc/kubernetes/
rm -rf /var/lib/kubelet
rm -rf /var/lib/etcd
rm -rf /usr/local/bin/kubectl
rm -rf /etc/systemd/system/calico-node.service
rm -rf /etc/systemd/system/kubelet.service
systemctl stop etcd.service
systemctl disable etcd.service
systemctl stop calico-node.service
systemctl disable calico-node.service
docker stop $(docker ps -q)
docker rm $(docker ps -a -q)
systemctl restart docker
```



- 安装完成后修改节点标签

```sh
kubectl label node node3 node-role.kubernetes.io/worker=""  #标记worker

kubectl label node node3 node-role.kubernetes.io/node="" #标记node

kubectl label node node3  "node-role.kubernetes.io/worker"- # 删除worker标记
```



---

### Kubernetes Dashboard



- 以NodePort方式暴露服务

  修改代码，使用NodePort方式访问Dashboard。

```yaml
# ./roles/kubernetes-apps/ansible/templates/dashboard.yml.j2
# ------------------- Dashboard Service ------------------- #
      targetPort: 8443
  type: NodePort    //添加这一行   
  selector:
k8s-app: kubernetes-dashboard
```



- 获取token

```sh
kubectl get svc --all-namespaces | grep kubernetes-dashboard

kubectl -n kube-system describe $(kubectl -n kube-system get secret -n kube-system -o name | grep namespace) | grep token
```



- 非NodePort方式访问

  <https://192.168.100.78:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/>（192.168.100.78是VIP或者某个master节点IP）



---

**后续操作**

以上完成的是带有kubernetes dashboard的初始环境的搭建，之后还要进行 替换Ingress、设置AD认证、安装管理工具等，此不涉及。

