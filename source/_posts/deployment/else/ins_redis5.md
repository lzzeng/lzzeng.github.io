---
title: yum安装redis
date: 2019-08-07 14:51:24
tags:
    - Redis
    - else
categories:
    - 其它
toc: true
---



>  系统：CentOS 7.6



```sh
rpm -Uvh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -Uvh https://centos7.iuscommunity.org/ius-release.rpm
yum install redis5-5.0.5 -y
```

<!-- more -->