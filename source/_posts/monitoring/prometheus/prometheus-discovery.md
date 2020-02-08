---
title: Prometheus自动发现配置
date: 2019-03-17 14:51:24
tags:
    - Prometheus
categories:
    - 监控
toc: true
---



---

> Prometheus支持基于Consul自动发现

<!-- more -->

prometheus.yml:

```yaml
global:
  scrape_interval:     1s
  scrape_timeout:      1s
  evaluation_interval: 5s

alerting:
  alertmanagers:
  - static_configs:
    - targets: ['10.1.7.211:9093']

rule_files:
  - 'rules/*.yml'
 
scrape_configs:
  - job_name: prometheus
    metrics_path: /metrics
    static_configs:
    - targets: ['localhost:9090']
      labels:
        instance: prometheus


  - job_name: consul_sd
    consul_sd_configs:
    - server: '192.168.100.140:8500'
      datacenter: dc01
      services: []

    relabel_configs:
    - source_labels: [__meta_consul_tags]
      regex: '.*,prometheus-target,.*'
      action: keep

    - source_labels: [__meta_consul_service]
      target_label: sn

  - job_name: consul_sd_dev
    consul_sd_configs:
    - server: '10.1.7.211:8500'
      datacenter: dc1
      services: []

    relabel_configs:
    - source_labels: [__meta_consul_tags]
      regex: '.*prometheus-target.*'
      action: keep

    - source_labels: ['__address__']
#      regex: '.*:(.*)'
      regex: '127.0.0.1:(.*)'
      target_label: '__address__'
      replacement: '10.1.7.211:$1'
```

