---
title: Gitlab CI/CD Practice —— Gitlab Runner in Docker/K8s
date: 2019-04-12 14:51:24
tags:
    - Gitlab
categories:
    - CICD
toc: true
---



---

> GitLab Runner is the open source project that is used to run your jobs and send the results back to GitLab. It is used in conjunction with [GitLab CI](https://about.gitlab.com/product/continuous-integration/), the open-source continuous integration service included with GitLab that coordinates the jobs

<!-- more -->

### gitlab-runner in Docker

```sh
[root@zlz srv]# docker exec -it gitlab-runner /bin/bash

root@9e069893788a:/# gitlab-runner register
Runtime platform                                    arch=amd64 os=linux pid=33 revision=fa86510e version=11.9.2
Running in system-mode.
Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
http://xxx.com/
Please enter the gitlab-ci token for this runner:
peWrQo7zxksbVhsuTncq
Please enter the gitlab-ci description for this runner:
[9e069893788a]: test gitlab cid^H^H
Please enter the gitlab-ci tags for this runner (comma separated):
test,zlztest
Registering runner... succeeded                     runner=peWrQo7z
Please enter the executor: docker-ssh, parallels, virtualbox, kubernetes, docker, shell, ssh, docker+machine, docker-ssh+machine:
docker
Please enter the default Docker image (e.g. ruby:2.1):
alpine:latest
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded! 
root@9e069893788a:/#
```



### gitlab-runner in k8s

```sh
helm repo add gitlab https://charts.gitlab.io
helm install --name gitlab-runner -f values.yml gitlab/gitlab-runner
```



values.yml：

```yaml
imagePullPolicy: IfNotPresent
gitlabUrl: http://xxx.com/
runnerRegistrationToken: "peWrQo7zxksbVhsuTncq"
unregisterRunners: true
concurrent: 10
checkInterval: 30
rbac:
  create: false
  clusterWideAccess: false
metrics:
  enabled: true
runners:
  image: ubuntu:16.04
  privileged: false
  cache: {}
  builds: {}
  services: {}
  helpers: {}
resources: {}
affinity: {}
nodeSelector: {}
tolerations: []
hostAliases: []
podAnnotations: {}
```



或者

```sh
apiVersion: v1
kind: ConfigMap
metadata:
  name: gitlab-runner
  namespace: default
data:
  config.toml: |
    concurrent = 2

    [[runners]]
      name = "Kubernetes Runner"
      url = "http://xxx.com/"
      token = "peWrQo7zxksbVhsuTncq"
      executor = "kubernetes"
      [runners.kubernetes]
        namespace = "default"
        image = "busybox"

---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: gitlab-runner
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      name: gitlab-runner
  template:
    metadata:
      labels:
        name: gitlab-runner
    spec:
      containers:
      - args:
        - run
        image: gitlab/gitlab-runner:latest
        imagePullPolicy: IfNotPresent
        name: gitlab-runner
        volumeMounts:
        - mountPath: /etc/gitlab-runner
          name: config
      restartPolicy: Always
      volumes:
      - configMap:
          name: gitlab-runner
        name: config
```



创建runner然后进入容器手动注册。

```sh
kubectl apply -f <yaml>
gitlab-ci-multi-runner register
# 或者
gitlab-runner register
```



或者

```sh
kubectl create -f gitlab-sc.yml
helm install --name gitlab-runner --namespace gitlabci -f values.yml gitlab/gitlab-runner
```



相关yaml：

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: gitlabci
  labels:
    name: gitlabci

---
# Source: gitlab-runner/templates/service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gitlab-runner-admin
  namespace: gitlabci

---
# Source: gitlab-runner/templates/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: "ClusterRole"
metadata:
  name: gitlab-runner-admin
  namespace: gitlabci
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

---
# Source: gitlab-runner/templates/role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: "ClusterRoleBinding"
metadata:
  name: gitlab-runner-admin
  namespace: gitlabci
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: "ClusterRole"
  name: gitlab-runner-admin
subjects:
- kind: ServiceAccount
  name: gitlab-runner-admin
  namespace: gitlabci
```

