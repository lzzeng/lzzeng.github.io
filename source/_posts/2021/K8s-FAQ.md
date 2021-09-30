---
title: K8s若干问题
date: 2021-6-20 22:55:40
tags:
    - K8s
categories:
    - DevOps
copyright: false
toc: true
---



### Kubelet 调用的处理检查容器的IP地址是否打开的程序是？

TCPSocketAction



### 1.8版本的Kubernetes引入了什么？

Taints and Tolerations

<!-- more -->

### 如何在没有选择器的情况下定义服务？

指定外部名称



### 什么是Kubernetes集群中的minions？

它们是集群的工作节点



### ReplicaSet和ReplicationController的区别？

在旧版本的Kubernetes中，只有ReplicationController对象。它的主要作用是确保Pod以你指定的副本数运行，即如果有容器异常退出，会自动创建新的 Pod 来替代；而异常多出来的容器也会自动回收。

ReplicaSet是ReplicationController的替代。ReplicaSet支持集合式的selector。官方强烈建议避免直接使用ReplicaSet，而应该通过Deployment来创建RS和Pod。



### Headless Service？

spec.clusterIP为None。不会被分配cluster IP，kube-proxy不处理，不会对这类服务进行负载均衡和路由。

`ClusterIP`的原理：一个`Service`可能对应多个`EndPoint(Pod)`，`client`访问的是`Cluster IP`，通过`iptables`规则转到`Real Server`，从而达到负载均衡的效果。

ClusterIP方式，dns查询时只会返回`Service`的地址。而headless方式会返回endpoint的IP。



headless使用场景:

第一种：自主选择权，有时候`client`想自己来决定使用哪个`Real Server`，可以通过查询`DNS`来获取`Real Server`的信息。

第二种：`Headless Service`的对应的每一个`Endpoints`，即每一个`Pod`，都会有对应的`DNS`域名；这样`Pod`之间就能互相访问，集群也能单独访问pod。



K8s中资源的全局FQDN格式:
　　Service_NAME.NameSpace_NAME.Domain.LTD.
　　Domain.LTD.=svc.cluster.local.　　　　 # 这是默认k8s集群的域名

假设nginx是一个service：
`nslookup nginx.default.svc.cluster.local 10.200.2.10`

如果后端pod名为web-0,web-1:
`nslookup web-0.nginx.default.svc.cluster.local 10.200.2.11`



### Kubernetes Architecture的组件有哪些？

Kubernetes Architecture包含主节点和工作节点。运行在主节点上的组件有：kube-controller-manager，kube-apiserver，kube-scheduler。工作节点上的组件有：kubelet和kube-proxy。



### ingress的意义？

动态配置服务，减少不必要的端口暴露

k8s对外暴露服务的方式？

- NodePort
- LoadBalancer
- Ingress


ingress controller通过和kubernetes api交互，动态的去感知集群中ingress规则变化，生成相应的nginx配置文件。



### 无选择器的service?

service 其实是一个TCP/UDP 代理，不仅可以代理Pod也可以代理其他的非Pod资源，例如外网的数据库，或者其他的资源。没有配置选择器的service ，endpoints为空，可以给这个service 添加或修改 endpoint



```yaml
apiVersion: v1
kind: Service
metadata:
  name: mynoselector-service
spec:
  ports:
  - protocol: TCP
    port: 50000

---

apiVersion: v1
kind: Endpoints
metadata:
  name: mynoselector-service
subsets:
  - addresses:
    - ip: 13.75.107.151
    ports:
    - port: 3306
```



### K8s版本变化

Alpha（内部测试版）->Beta（测试版）-> GA（正式发布的版本）

**v1.13 2018年12月04日**
kubeadm进入GA，容器存储接口（CSI）进入GA，CoreDNS成为默认DNS服务器

**v1.14 2019年03月26日**
生产级支持Windows节点，kubectl全新文档与kustomize集成，持久本地卷进入GA

**v1.15 2019年06月19日**
核心API可扩展性，kubeadm高可用进入Beta，kubeadm无缝升级所有证书，持续改进CSI。

**v1.16 2019年09月18日**
CRD进入GA，准入控制Webhooks进入GA，IPv4/IPv6双栈协议支持，CSI规范卷大小调整。

**v1.17 2019 年12月10日**
- 云供应商标签 GA：早在 v1.2 版本中就作为测试版功能添加，v1.17 版本中的云供应商标签普遍可用。
- Volume Snapshot 进入 bata 版：Kubernetes Volume Snapshot功能现在是Kubernetes v1.17中的测试版。该功能在 Kubernetes v1.12 中作为 alpha 引入的，在 Kubernetes v1.13 中进行了第二次 alpha，并进行了突破性修改。
- CSI 迁移（Migration）进入 beata 版：Kubernetes 树内（in-tree）存储插件到容器存储接口（CSI）迁移基础架构现在是 Kubernetes v1.17 中的 beata 版。CSI 迁移在 Kubernetes v1.14 中作为 alpha 引入。

**v1.18 2020年3月26日**
https://v1-18.docs.kubernetes.io/blog/2020/03/25/kubernetes-1-18-release-announcement/

Taint Based Eviction，kubectl diff 等


**v1.19 2020年8月27日**
从 Kubernetes 1.19 版本开始，支持窗口将延长到一年。
Ingress 升级为 GA，结构化日志等

**v1.20**
Dockershim弃用

**v1.21**
PodSecurityPolicy 弃用
不可变 ConfigMap/Secret 进入稳定版

当集群包含大量 ConfigMap 和 Secret 时，大量的 watch 事件会急剧增加 kube-apiserver 的负载，并会导致错误配置过快传播到整个集群。在这种情况中，给不需要经常修改的 ConfigMap 和 Secret 设置 `immutable: true` 就可以避免类似的问题。

注意，设置 `immutable: true` 之后，ConfigMap 和 Secret 内容更新时需要删除并重新创建，且使用它们的 Pod 也需要删除重建。