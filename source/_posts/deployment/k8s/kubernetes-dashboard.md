---
title: Kubernetes Dashboard
date: 2019-07-25 14:51:24
tags:
    - K8s
categories: 
    - K8s
toc: true
---



---

#### 登录

- 获取token

```sh
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | awk '/^deployment-controller-token-/{print $1}') | awk '$1=="token:"{print $2}'
```

<!-- more -->

```sh
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep kubernetes-dashboard-token |awk '{print $1}') | grep token: | awk '{print $2}'
```

```sh
kubectl -n kube-system describe $(kubectl -n kube-system get secret -n kube-system -o name | grep namespace) | grep token:
```



- 创建ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard-minimal
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kubernetes-dashboard
  namespace: kube-system
```



- URL

<https://{master_ip}:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/>
