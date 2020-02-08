---
title: RKE安装K8s HA集群过程记录
date: 2019-04-15 14:51:24
tags:
    - K8s
categories:
    - K8s
toc: true
---



---

### 准备工作

ansible主机清单：

```ini
[rke]
rke ansible_host=192.168.100.228

[k8s]
master01 ansible_host=192.168.101.72
master02 ansible_host=192.168.101.75
master03 ansible_host=192.168.100.229
```

<!-- more -->

安装docker：

```sh
ansible-playbook roles/docker.yml
```

使用ansible之前，需要分发密钥至各节点root用户。



创建rancher用户，并分发密钥：

```sh
ansible-playbook roles/key.yml
```



安装rke、kubectl、helm工具：

```sh
# https://www.cnrancher.com/download/rke/rke_linux-amd64
wget https://www.cnrancher.com/download/rke/rke_linux-amd64
chmod +x rke_linux-amd64
mv rke_linux-amd64 /usr/bin/rke

# https://www.cnrancher.com/download/kubectl/kubectl_amd64-linux
wget https://www.cnrancher.com/download/kubectl/kubectl_amd64-linux
chmod +x kubectl_amd64-linux
mv kubectl_amd64-linux /usr/bin/kubectl

# https://www.cnrancher.com/download/helm/helm-linux.tar.gz
wget https://storage.googleapis.com/kubernetes-helm/helm-v2.12.0-linux-amd64.tar.gz
tar -xf helm-v2.12.0-linux-amd64.tar.gz
mv linux-amd64/helm /usr/bin/helm
mv linux-amd64/tiller /usr/bin/tiller
rm -rf linux-amd64
```



### 创建集群

rancher-cluster.yml:

```yaml
nodes:
  - address: 192.168.101.72
    user: rancher
    role: [controlplane,worker,etcd]
  - address: 192.168.101.75
    user: rancher
    role: [controlplane,worker,etcd]
  - address: 192.168.100.229
    user: rancher
    role: [controlplane,etcd]

services:
  etcd:
    snapshot: true
    creation: 6h
    retention: 24h
```



rke up:

```sh
rke up --config rancher-cluster.yml
```

rke up后会生成kube_config_rancher-cluster.yml



设置kube_config环境变量（或者复制到~/.kube/config ）：

```sh
echo "export KUBECONFIG=/home/rancher/kube_config_rancher-cluster.yml" >> /etc/profile
source /etc/profile
```



### 安装tiller

```sh
# Helm在集群上安装tiller服务以管理charts. 由于RKE默认启用RBAC, 因此我们需要使用kubectl来创建一个serviceaccount，clusterrolebinding才能让tiller具有部署到集群的权限

kubectl -n kube-system create serviceaccount tiller

# 创建ClusterRoleBinding以授予tiller帐户对集群的访问权限
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller

# 安装Helm Server(Tiller)
helm init --service-account tiller --tiller-image registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:v2.12.0 --stable-repo-url https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts
```



### 安装cert-manager

```sh
helm install stable/cert-manager \
  --name cert-manager \
  --namespace kube-system
```



### 安装rancher web

```sh
# 使用helm repo add命令添加Rancher chart仓库地址
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable

helm install rancher-stable/rancher \
  --name rancher \
  --namespace cattle-system \
  --set hostname=xxx.com

helm install rancher-stable/rancher --name rancher --namespace cattle-system --set hostname=xxx.com
```



如果不是通过DNS解析域名，而是通过本地hosts解析，可以通过给cattle-cluster-agent Pod和cattle-node-agent添加主机别名，让其可以正常通信，前提是IP地址可以互通。

```sh
kubectl -n cattle-system patch deployments cattle-cluster-agent --patch '{
    "spec": {
        "template": {
            "spec": {
                "hostAliases": [
                    {
                        "hostnames":
                        [
                            "xxx.com"
                        ],
                            "ip": "192.168.100.228"
                    }
                ]
            }
        }
    }
}'

# 上面这条命令可能报错：Error from server (NotFound): deployments.extensions "cattle-cluster-agent" not found，因为cattle-cluster-agent还没有创建成功

kubectl -n cattle-system patch daemonsets cattle-node-agent --patch '{
    "spec": {
        "template": {
            "spec": {
                "hostAliases": [
                    {
                        "hostnames":
                        [
                            "xxx.com"
                        ],
                            "ip": "192.168.100.228"
                    }
                ]
            }
        }
    }
}'
```



### 安装rancher cli

```sh
wget https://www.cnrancher.com/download/cli/rancher-linux-amd64.tar.gz
mkdir rancher-linux-amd64.tmp.d # 临时目录
tar -xf rancher-linux-amd64.tar.gz -C rancher-linux-amd64.tmp.d
find rancher-linux-amd64.tmp.d -name 'rancher' -type f | xargs -I {} mv {} /usr/bin/;
rm -rf rancher-linux-amd64.tmp.d
```


