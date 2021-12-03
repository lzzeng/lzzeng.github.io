---
title: 【摘】Linux日志
date: 2021-4-25 22:55:40
tags:
    - Linux
categories:
    - Linux
copyright: false
---



在Linux系统中，有三个主要的日志子系统：**连接时间日志，进程统计日志，错误日志**

<!-- more -->

**连接时间日志**

由多个程序执行，把记录写入到/var/log/wtmp和/var/run/utmp，login等程序更新wtmp和utmp文件，使系统管理员能够跟踪谁在何时登录到系统。

**进程统计日志**

进程统计日志由系统内核执行。当一个进程终止时，为每个进程往进程统计文件（pacct或acct）中写一个记录。进程统计的目的是为系统中的基本服务提供命令使用统计。

**错误日志**

错误日志由syslogd执行。各种系统守护进程、用户程序和内核通过syslog向文件/var/log/messages报告值得注意的事件。另外有许多UNIX程序创建日志。像HTTP和FTP这样提供网络服务的服务器也保持详细的日志。



文本类型的日志：

```
/var/log/messages  
/var/log/dmesg
/var/log/secure
/var/log/cron
/var/log/maillog
/var/log/yum.log
```

/var/log/messages日志格式：

```
Dec 19 17:39:06 localhost sz[17833]: [root] ConfigActivity.xml/ZMODEM: 287531 Bytes, 343933 BPS
1. 产生这个事件的时间是：Dec 19 17:39:06
2. 事件的来源主机为：localhost
3. 产生这个事件的程序和进程号为：sz[17833]
4. 这个事件实际的日志信息为：[root] ConfigActivity.xml/ZMODEM: 287531 Bytes, 343933 BPS
```



二进制日志：

```
/var/log/wtmp
/var/log/lastlog
/var/run/utmp
这三个文件中保存了系统用户登录、退出等相关事件的事件信息，不能直接使用tail、less等文本查看工具进行浏览，需要使用who/w/users/finger/id/last/lastlog和ac等用户查询命令来获取日志信息
```



系统日志：

/var/log/lastlog：记录最后一次用户成功登陆的时间、登陆IP等信息
/var/log/messages：记录Linux操作系统常见的系统和服务错误信息
/var/log/secure：Linux系统安全日志，记录用户和工作组变坏情况、用户登陆认证情况
/var/log/btmp：记录Linux登陆失败的用户、时间以及远程IP地址
/var/log/cron：记录crond计划任务服务执行情况
auth.log：登录认证的信息记录
boot.log：系统启动时的程序服务的日志信息
dmesg：启动时显示在屏幕上的内核缓冲信息和硬件信息, dmesg命令用于显示开机信息
faillog：用户登录失败详细信息记录
kern.log：内核产生的信息记录



rsyslog管理的日志：

| 日志              | 说明                                                         |
| ----------------- | :----------------------------------------------------------- |
| /var/log/message  | 系统启动后的信息和错误日志，是Red Hat Linux中最常用的日志之一 |
| /var/log/secure   | 安全相关的日志信息                                           |
| /var/log/maillog  | 邮件相关的日志信息                                           |
| /var/log/cron     | 定时任务相关的日志信息                                       |
| /var/log/spooler  | UUCP和news设备相关的日志信息                                 |
| /var/log/boot.log | 守护进程启动和停止相关的日志消息                             |



**rsyslog** 是一个快速处理收集系统日志的程序，提供了高性能、安全功能和模块化设计。rsyslog 是syslog 的升级版，它将多种来源输入输出转换结果到目的地。

相关配置文件：/etc/rsyslog.conf, /etc/rsyslog.d/, /etc/sysconfig/rsyslog



日志轮转配置文件：**/etc/logrotate.conf**

自定义日志转储：**/etc/logrotate.d/**

示例：将所有类型错误级别为info的日志转储到/var/log/test.log日志文件中，并设置/var/log/test.log达到1KB后进行转储，转储10次，压缩，转储后重启rsyslog服务。

在/etc/rsyslog.conf添加一行配置：

```
[root@localhost ~]# tail /etc/rsyslog.conf
#$ActionQueueSaveOnShutdown on # save messages to disk on shutdown
#$ActionQueueType LinkedList   # run asynchronously
#$ActionResumeRetryCount -1    # infinite retries if host is down
# remote host is: name/ip:port, e.g. 192.168.0.1:514, port optional
#*.* @@remote-host:514
# ### end of the forwarding rule ###

## custom ...
*.info /var/log/test.log
```

```
[root@localhost ~]# cat /etc/logrotate.d/test.log
/var/log/test.log {
 rotate 10
 size = 1k
 compress
 postrotate
  killall -HUP rsyslogd
 endscript
}
```


