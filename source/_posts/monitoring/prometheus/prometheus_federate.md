---
title: Prometheus联邦
date: 2019-03-17 14:51:24
tags:
    - Prometheus
categories:
    - 监控
toc: true
---



---

> Prometheus联邦

<!-- more -->



prometheus.yml示例：

```yaml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 1m
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - x.xx.xxx.xxx:9093
    scheme: http
    timeout: 10s
rule_files:
- /etc/prometheus/rules/*.yml

scrape_configs:
- job_name: federate
  honor_labels: true
  params:
    match[]:
    - '{job=~"\\w.*"}'
    #- '{job=~"[a-zA-Z_].*"}'
  metrics_path: /federate
  scheme: http
  static_configs:
  - targets:
    - x.xx.xxx.xxx:9090
	
- job_name: federate2
  honor_labels: true
  params:
    match[]:
    - '{job=~"\\w.*"}'
  scrape_interval: 30s
  scrape_timeout: 30s
  metrics_path: /federate
  scheme: http
  static_configs:
  - targets:
    - x.xx.xxx.xxx:xxxx

- job_name: federate_pmm_server
  scrape_interval: 30s
  scrape_timeout:  30s
  honor_labels: true
  metrics_path: /prometheus/federate
  basic_auth:
    username: "xxx"
    password: "xxx"
  params:
    match[]:
      - '{job=~"\\w.*"}'
  static_configs:
    - targets:
      - x.xx.xxx.xxx:xxxx
```