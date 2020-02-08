---
title: Consul介绍
date: 2019-04-25 14:01:24
tags:
    - Consul
categories: 
    - Consul
toc: true
---



---

> [**Consul**](https://www.consul.io/docs/internals/architecture.html) 是一个分布式服务发现与配置的工具。与其他分布式服务注册与发现的方案，Consul的方案更“一站式”，内置了服务注册与发现框架、分布一致性协议实现（不需要ZooKeeper）、健康检查、K/V存储、多数据中心方案。



<!-- more -->

![Consul Architecture](https://www.consul.io/assets/images/consul-arch-420ce04a.png)



- 注册服务（Register Service）

```sh
curl http://<your-consul-url>/v1/agent/service/register -X PUT -i -H "Content-Type:application/json" -d '{
    "Name": "test-name", 
    "Tags": [
        "test-tag"
    ], 
    "EnableTagOverride": false, 
    "ID": "test-id", 
    "Meta": {"version": "1.0"}, 
    "Address": "192.168.100.150", 
    "Port": 8080, 
    "Check": {
        "DeregisterCriticalServiceAfter": "90m", 
        "Args": [], 
        "HTTP": "http://192.168.100.150:8080/", 
        "Interval": "15s"
    }
}'
```



- 注销服务（Deregister Service）

```sh
curl -X PUT http://<your-consul-url>/v1/agent/service/deregister/test-id
```

