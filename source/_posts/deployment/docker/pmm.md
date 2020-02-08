---
title: PMM数据库性能监控
date: 2019-06-14 19:51:24
tags:
    - Docker
    - MySQL
categories: 
    - Docker
toc: true
---



---

> Percona Monitoring and Management (PMM)是一款开源的MySQL、MongoDB性能监控工具，PMM客户端负责收集DB监控数据，PMM服务端从已连接的客户端拉取数据，并通过第三方软件Grafana展示图表。

<!-- more -->


```yaml
version: '2'

services:
  pmm-data:
    image: percona/pmm-server:1.1.1
    container_name: pmm-data
    volumes:
      - /opt/prometheus/data
      - /opt/consul-data
      - /var/lib/mysql
      - /var/lib/grafana
    entrypoint: /bin/true

  pmm-server:
    image: percona/pmm-server:1.1.1
    container_name: pmm-server
    ports:
      - 8088:80
    restart: always
    environment:
      - SERVICE_80_NAME=pmm
      - SERVICE_80_TAGS=pmm,http
      - SERVER_USER=admin
      - SERVER_PASSWORD=${PMM_SERVER_PASSWORD}
      - METRICS_RETENTION=720h
      - METRICS_MEMORY=4194304
      - METRICS_RESOLUTION=5s
      - QUERIES_RETENTION=30
    volumes_from:
      - pmm-data
```



或者

```sh
#!/bin/sh

tag0=$1
tag=${tag0:=1.1.1}

docker stop pmm-server
docker rm pmm-server pmm-data

docker create \
   -v /opt/prometheus/data \
   -v /opt/consul-data \
   -v /var/lib/mysql \
   -v /var/lib/grafana \
   --name pmm-data \
   percona/pmm-server:$tag /bin/true
   
   
docker run -d \
   -p 8088:80 \
   --volumes-from pmm-data \
   --name pmm-server \
   -e SERVER_USER=admin \
   -e SERVICE_80_NAME=pmm \
   -e SERVICE_80_TAGS=pmm,http,ui \
   -e SERVER_PASSWORD=${PMM_SERVER_PASSWORD} \
   --restart always \
   percona/pmm-server:$tag

```

