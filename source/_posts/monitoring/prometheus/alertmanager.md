---
title: Alertmanager介绍
date: 2019-03-17 14:51:24
tags:
    - Prometheus
categories:
    - 监控
toc: true
---



---

![img](../../../assets/images2019/alertmanager.assets/prometheus-alert-artich.png)

<!-- more -->

>  Alertmanager作为一个独立的组件，负责接收并处理来自Prometheus Server(也可以是其它的客户端程序)的告警信息。Alertmanager可以对这些告警信息进行进一步的处理，比如当接收到大量重复告警时能够消除重复的告警信息，同时对告警信息进行分组并且路由到正确的通知方，Prometheus内置了对邮件，Slack等多种通知方式的支持，同时还支持与Webhook的集成，以支持更多定制化的场景。



