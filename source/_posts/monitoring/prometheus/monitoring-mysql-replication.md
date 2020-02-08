---
title: Prometheus监控MySQL主从同步
date: 2019-08-17 14:51:24
tags:
    - Prometheus
    - MySQL
categories:
    - 监控
toc: true
---



---

> 利用node_exporter从*.prom文件读取指标数据

<!-- more -->



## 获取数据的脚本

getKeys.sh:

```sh
#!/bin/sh

mypath=$(cd `dirname $0`; pwd)
cd $mypath

echo "executing all shell scripts ..."
for sh in `ls *.sh |grep -v $0`
do
  echo "will execute: ./$sh > ${sh}.prom"
  eval "./$sh > ${sh}.prom"
done
```



获取主从同步延迟数据的脚本pt-heart.sh：

```sh
out=`pt-heartbeat -D your_dbname --table=heartbeat --check --host=x.x.x.x --port=xx --user=xx --password=xxxxxx --master-server-id=xxx --print-master-server-id`
v=`echo "$out" |awk '{print $1}'`
m=`echo "$out" |awk '{print $2}'`
echo "pt_heart{server_id=\"$m\"} $v"
```

具体示例：

```sh
out=`pt-heartbeat -D test_sync --table=heartbeat --check --host=10.1.7.211 --port=3306 --user=root --password=xxxxxx --master-server-id=100 --print-master-server-id`
...
```



脚本位置：

```sh
[root@docker-dev node_exporter_keys]# pwd
/srv/node_exporter_keys
[root@docker-dev node_exporter_keys]# tree .
.
├── getkeys.sh
├── procs.sh
├── procs.sh.prom
├── pt-heart.sh
└── pt-heart.sh.prom
```



### 设置定时任务

设置crontab定时任务：

```sh
* * * * * /srv/node_exporter_keys/getkeys.sh
```



输出的文件pt-heart.sh.prom：

```
pt_heart{server_id="100"} 0.00
```



修改node_exporter启动参数：

分两种情形：

- 通过docker运行node_exporter

```yaml
version: '3.0'

services:
  node-exporter:
    image: prom/node-exporter
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
      - /srv/node_exporter_keys:/var/extra_keys:ro # 映射到/var/extra_keys
    ports:
      - 9100:9100
    command:
      - '--collector.textfile.directory=/var/extra_keys' # 指定从/var/extra_keys读取*.prom
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points="^(/rootfs|/host|)/(sys|proc|dev|host|etc)($$|/)"'
      - '--collector.filesystem.ignored-fs-types="^(sys|proc|auto|cgroup|devpts|ns|au|fuse\.lxc|mqueue)(fs|)$$"
```



- 通过supervisor运行node_exporter

```ini
[program:node_exporter]
command=/path/to/node_exporter --collector.textfile.directory=/srv/node_exporter_keys
directory=/path/to
user=root
startsecs=3
redirect_stderr=true
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=3
stdout_logfile=/var/log/node_exporter.log
```



最后，访问相应的http://your-host:9100/metrics，查看是否有新增的指标名称pt_heart。
