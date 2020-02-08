---
title: yum安装rabbitmq
date: 2019-06-15 14:51:24
tags:
    - else
categories:
    - 其它
toc: true
---



> 系统：CentOS 7.6

<!-- more -->

```sh
wget https://github.com/rabbitmq/erlang-rpm/releases/download/v22.0.1/erlang-22.0.1-1.el7.x86_64.rpm

wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.15/rabbitmq-server-3.7.15-1.el7.noarch.rpm

yum install erlang-22.0.1-1.el7.x86_64.rpm rabbitmq-server-3.7.15-1.el7.noarch.rpm
```

