---
title: Prometheus
date: 2019-03-17 14:51:24
tags:
    - Prometheus
categories:
    - 监控
toc: true
---



---

> 在Docker中运行Prometheus监控组件，包括prometheus, alertmanager, grafana, 及相关exporter，实现基本的业务监控。

<!-- more -->

下图是官方网站上的Prometheus完整架构图：

![Prometheus完整架构图](https://prometheus.io/assets/architecture.png)





---

## Prometheus配置



配置文件目录：

```sh
[root@docker-dev docker-svc]# tree -C -L 4 prometheus/
prometheus/
├── config
│   ├── alertmanager
│   │   ├── alertmanager.yml
│   │   └── template
│   │       └── test.tmpl
│   └── prometheus
│       ├── prometheus.yml
│       └── rules
│           └── default.yml
└── docker-compose.yml
```



docker-compose.yml:

```yaml
version: '3.0'

services:
  alertmanager:
    image: prom/alertmanager
    volumes:
      - ./config/alertmanager:/etc/alertmanager
    ports:
      - "9093:9093"
    environment:
      SERVICE_NAME: alertmanager
      SERVICE_TAGS: "alertmanager,http"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./config/prometheus/rules:/etc/prometheus/rules
      - /etc/localtime:/etc/localtime
    environment:
      SERVICE_NAME: prometheus
      SERVICE_TAGS: "prometheus-target,prometheus,http"
    ports:
      - 9090:9090

  grafana:
    image: grafana/grafana
    volumes:
#      - grafana-storage:/var/lib/grafana
      - /data/grafana:/var/lib/grafana
    
    environment:
      - "GF_SERVER_ROOT_URL=http://grafana.server.name"
      - "GF_SECURITY_ADMIN_PASSWORD=xxxxxx"
      - "SERVICE_NAME=grafana"
      - "SERVICE_TAGS=prometheus-target,grafana,http"
    ports:
      - 3000:3000

  node-exporter:
    image: prom/node-exporter
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    network_mode: host
    ports:
      - 9100:9100
    environment:
      SERVICE_TAGS: "prometheus-target"
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points="^(/rootfs|/host|)/(sys|proc|dev|host|etc)($$|/)"'
      - '--collector.filesystem.ignored-fs-types="^(sys|proc|auto|cgroup|devpts|ns|au|fuse\.lxc|mqueue)(fs|)$$"'
```

