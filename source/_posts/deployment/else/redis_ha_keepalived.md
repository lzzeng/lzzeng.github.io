---
title: Redis高可用方案KeepAlived配置示例
date: 2019-05-18 14:51:24
tags:
    - Redis
categories:
    - 其它
toc: true
---



---

### 一主两从+三哨兵+KeepAlived

>  Redis (M/1 S/2)+ Sentinel/3 + KA/3 (VIP/1)

<!-- more -->

KA配置示例（其一节点）:

```tex
! Configuration File for keepalived

global_defs {
    router_id redis_swms
}

vrrp_script chk_http_port {     
    script "/usr/local/redis/bin/redis-cli -p 8379 info | grep role:master >/dev/null 2>&1"     
    interval 1 
    timeout 2
    fall 2
    rise 1
}

vrrp_instance VI_1 {
    state BACKUP
    interface eth0
    virtual_router_id 64
    priority 120
    advert_int 1

    unicast_src_ip 10.1.100.25

    unicast_peer {
        10.1.100.23
        10.1.100.24
    }
    
    authentication {
        auth_type PASS
        auth_pass 12345
    }

    virtual_ipaddress {
        10.1.100.22
    }

    track_script {
        chk_http_port
    }
}
```



---

### 一主一从+KeepAlived

>  Redis (M/1 S/1) + KA/2 (VIP/1)



KA配置示例（其一节点）:

```tex
! Configuration File for keepalived

global_defs {
    router_id redis_swms
}

vrrp_script chk_redis {
    script "/opt/scripts/keepalived/redis_check.sh 127.0.0.1 6379"
    interval 1
    timeout 2
    fall 3
}

vrrp_instance VI_1 {
    state BACKUP
    interface ens192
    virtual_router_id 64
    priority 120
    advert_int 1

    unicast_src_ip 192.168.101.65

    unicast_peer {
        192.168.101.66
    }

    authentication {
        auth_type PASS
        auth_pass 12345
    }

    virtual_ipaddress {
        192.168.101.64
    }

    track_script {
        chk_redis
    }

    notify_master "/opt/scripts/keepalived/redis_master.sh 127.0.0.1 192.168.101.66 6379"
    notify_backup "/opt/scripts/keepalived/redis_backup.sh 127.0.0.1 192.168.101.66 6379"
    # notify_fault /opt/scripts/keepalived/redis_fault.sh
    # notify_stop /opt/scripts/keepalived/redis_stop.sh
}
```



redis_master.sh:

```sh
#!/bin/bash

REDISCLI="redis-cli -h $1 -p $3"
LOGFILE="/var/log/redis/keepalived-redis-state.log"
echo "[master]" >> $LOGFILE
date >> $LOGFILE
echo "Being master...." >> $LOGFILE 2>&1
echo "Run MASTER cmd ..." >> $LOGFILE 2>&1
$REDISCLI SLAVEOF $2 $3 >> $LOGFILE
sleep 10 #delay 10 s wait data async cancel sync
echo "Run SLAVEOF NO ONE cmd ..." >> $LOGFILE
$REDISCLI SLAVEOF NO ONE >> $LOGFILE 2>&1
```



redis_backup.sh:

```sh
#!/bin/bash

REDISCLI="redis-cli -h $1 -p $3"
LOGFILE="/var/log/redis/keepalived-redis-state.log"
echo "[backup]" >> $LOGFILE
date >> $LOGFILE
echo "Run SLAVEOF cmd ..." >> $LOGFILE
$REDISCLI SLAVEOF $2 $3 >> $LOGFILE 2>&1
echo "Being slave...." >> $LOGFILE 2>&1
sleep 15 #delay 15 s wait data sync exchange role
```



redis_check.sh:

```sh
#!/bin/bash

ALIVE=`redis-cli -h $1 -p $2 PING`
LOGFILE="/var/log/redis/keepalived-redis-check.log"
echo "[CHECK]" >> $LOGFILE
date >> $LOGFILE
if [ $ALIVE = "PONG" ]; then
  echo "Success: redis-cli -h $1 -p $2 PING $ALIVE" >> $LOGFILE 2>&1
  exit 0
else
  echo "Failed:redis-cli -h $1 -p $2 PING $ALIVE " >> $LOGFILE 2>&1
  exit 1
fi
```

