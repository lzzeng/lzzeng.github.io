---
title: ELK in K8s
date: 2019-04-15 14:51:24
tags:
    - K8s
    - ELK
categories:
    - K8s
toc: true
---



---

## 示例配置

<!-- more -->


- elk-rc.yaml

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: elk-rc
  labels:
    k8s-app: elk
spec:
  selector:
    k8s-app: elk
  template:
    metadata:
      labels:
        k8s-app: elk
    spec:
      containers:
        - image: docker.elastic.co/elasticsearch/elasticsearch:6.6.0
          name: elasticsearch
          ports:
            - containerPort: 9200
          volumeMounts:
            - name: es-storage
              mountPath: /usr/share/elasticsearch/data
              subPath: elasticsearch/data
        - image: docker.elastic.co/logstash/logstash:6.6.0
          name: logstash
          ports:
            - containerPort: 9600
            - containerPort: 5000
        - image: docker.elastic.co/kibana/kibana:6.6.0
          name: kibana
          env:
            - name: ELASTICSEARCH_URL
              value: http://127.0.0.1:9200
          ports:
            - containerPort: 5601
      volumes:
        - name: es-storage
          persistentVolumeClaim:
            claimName: pvc001
```



- elk-svc-kibana.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kibana
  labels:
    k8s-app: elk
spec:
  type: LoadBalancer
  selector:
    k8s-app: elk
  ports:
    - port: 5601
      name: kibana
```



- elk-svc-logstash.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: logstash
  labels:
    k8s-app: elk
spec:
  selector:
    k8s-app: elk
  ports:
    - port: 8600
      name: logstash
```



- pv.yaml

```yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv001
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: "/path/to/nfs"
    server: x.xx.xxx.xxx
    
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc001
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 20Gi
  storageClassName: nfs
```



创建NFS持久卷：

```sh
kubectl create -f pv.yaml
```



部署ELK：

```sh

kubectl create -f elk-rc.yaml
kubectl create -f elk-svc-logstash.yaml
kubectl create -f elk-svc-kibana.yaml
kubectl get pods
kubectl get svc
```

