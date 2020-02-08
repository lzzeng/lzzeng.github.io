---
title: MySQL主从配置
date: 2019-09-22 14:51:24
tags:
    - MySQL
categories:
    - 其它
toc: true
---



## mysql配置

master端my.cnf配置示例：

<!-- more -->

```ini
[client]
default-character-set=utf8

[mysql]
default-character-set=utf8

[mysqld]
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake

## 设置server_id，一般设置为IP，同一局域网内注意要唯一
server_id=100  
## 复制过滤：也就是指定哪个数据库不用同步（mysql库一般不同步）
binlog-ignore-db=mysql  
## 开启二进制日志功能，可以随便取，最好有含义（关键就是这里了）
log-bin=edu-mysql-bin  
## 为每个session 分配的内存，在事务过程中用来存储二进制日志的缓存
binlog_cache_size=1M  
## 主从复制的格式（mixed,statement,row，默认格式是statement）
binlog_format=mixed  
## 二进制日志自动删除/过期的天数。默认值为0，表示不自动删除。
expire_logs_days=7  
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
```



slave端my.cnf配置示例：

```ini
[client]
default-character-set=utf8

[mysql]
default-character-set=utf8

[mysqld]
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake

## 设置server_id，一般设置为IP,注意要唯一
server_id=101
## 复制过滤：也就是指定哪个数据库不用同步（mysql库一般不同步）
binlog-ignore-db=mysql
## 开启二进制日志功能，以备Slave作为其它Slave的Master时使用
log-bin=edu-mysql-slave1-bin
## 为每个session 分配的内存，在事务过程中用来存储二进制日志的缓存
binlog_cache_size=1M
## 主从复制的格式（mixed,statement,row，默认格式是statement）
binlog_format=mixed
## 二进制日志自动删除/过期的天数。默认值为0，表示不自动删除。
expire_logs_days=7
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
## relay_log配置中继日志
relay_log=edu-mysql-relay-bin
## log_slave_updates表示slave将复制事件写进自己的二进制日志
log_slave_updates=1
## 防止改变数据(除了特殊的线程)
read_only=1
```



## master端添加slave端复制账号

```mysql
CREATE USER 'slave'@'%' IDENTIFIED BY 'xxxxxx'; #slave密码xxxxxx，下面change master时用到
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%';
# mysql 5.7也可以一行命令
# GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%' IDENTIFIED BY 'xxxxxx';

# 'slave'@'%' 或 'slave'@'172.17.0.3' #172.17.0.3是slave容器的ip
# 但不能写虚拟机的ip（本实验是通过docker-compose非host网络模式创建2个mysql实例，未验证host模式是否可以）
```



## 获取master信息

```mysql
# mysql -uroot -p
...
flush tables with read lock; # 锁表，start slave后解锁 UNLOCK TABLES
show master status;
+----------------------+----------+--------------+------------------+-------------------+
| File                 | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+----------------------+----------+--------------+------------------+-------------------+
| edu-mysql-bin.000001 |      769 |              | mysql 
```



## slave端设定master

```mysql
change master to master_host='172.17.0.2', master_user='slave', master_password='xxxxxx', master_port=3306, master_log_file='edu-mysql-bin.000001', master_log_pos=769, master_connect_retry=30; # 172.17.0.3是master的IP，docker中通过docker inspect查看

# change master to master_host='172.17.0.2'时172.17.0.2是master容器的IP，不能使用虚拟机的IP

###
change master to master_host='172.17.0.2', master_user='slave', master_password='slave', master_port=3306, master_log_file='edu-mysql-bin.000033', master_log_pos=72831102, master_connect_retry=30;
```



## slave启动、查看

```mysql
mysql> start slave;
mysql> show slave status \G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 172.17.0.3
                  Master_User: slave
                  Master_Port: 3306
                Connect_Retry: 30
              Master_Log_File: edu-mysql-bin.000001
          Read_Master_Log_Pos: 29661
               Relay_Log_File: edu-mysql-relay-bin.000018
                Relay_Log_Pos: 6051
        Relay_Master_Log_File: edu-mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
```
