---
title: Redis in Docker
date: 2019-07-14 19:51:24
tags:
    - Docker
    - Redis
categories: 
    - Docker
toc: true
---



---

### 连接redis

- docker redis-cli连接redis

```sh
[root@localhost redis]# docker inspect redis_redis_1 |grep net
            "NetworkMode": "redis_localnet",
            "SandboxKey": "/var/run/docker/netns/a498b7651db0",
                "redis_localnet": {
```
<!-- more -->



```sh
[root@localhost redis]# docker run -it --network redis_localnet --rm redis redis-cli -h redis
redis:6379> get k
(nil)
redis:6379> exit
[root@localhost redis]# docker run -it --rm redis redis-cli -h 192.168.80.2
192.168.80.2:6379> set k abc
OK
192.168.80.2:6379> get k
"abc"
192.168.80.2:6379> exit
[root@localhost redis]# docker run -it --network redis_localnet --rm redis redis-cli -h redis
redis:6379> get k
"abc"
redis:6379> del k
(integer) 1
redis:6379>
```



- 从其它redis节点访问

```sh
[root@localhost ~]# docker run -it --rm redis redis-cli -h 10.1.7.211
Unable to find image 'redis:latest' locally
latest: Pulling from library/redis
27833a3ba0a5: Already exists 
cde8019a4b43: Pull complete 
97a473b37fb2: Pull complete 
c6fe0dfbb7e3: Pull complete 
39c8f5ba1240: Pull complete 
cfbdd870cf75: Pull complete 
Digest: sha256:000339fb57e0ddf2d48d72f3341e47a8ca3b1beae9bdcb25a96323095b72a79b
Status: Downloaded newer image for redis:latest
10.1.7.211:6379> get k
(nil)
10.1.7.211:6379> set k abcdefg
OK
10.1.7.211:6379> exit
```



### Redis集群

- 创建

```sh
#!/bin/sh

para=""
port=8000 # 6个节点8001——8006
for i in `seq 1 6`
do
# host? 192.168.*
#  ipaddr=$(docker inspect new_redis_redis${i}_1 |jq '.[0].NetworkSettings.Networks.new_redis_default.IPAddress' |sed 's/\"//g')
# bridge? 172.*
  ipaddr=$(docker inspect new_redis_redis${i}_1 |jq '.[0].NetworkSettings.Networks.bridge.IPAddress' |sed 's/\"//g')
  let port=port+1
  echo $ipaddr:$port
  para="$para $ipaddr:$port"
done

echo $para # 172.17.0.12:8001 172.17.0.8:8002 172.17.0.13:8003 172.17.0.9:8004 172.17.0.10:8005 172.17.0.11:8006
docker run --rm -it inem0o/redis-trib create --replicas 1 $para
```



- 查看

```sh
[root@localhost new_redis]# docker run --rm -it inem0o/redis-trib info 172.17.0.11:8006
172.17.0.8:8002@18002 (f015467b...) -> 178239 keys | 5462 slots | 1 slaves.
172.17.0.12:8001@18001 (17687354...) -> 178166 keys | 5461 slots | 1 slaves.
172.17.0.13:8003@18003 (2097e0e6...) -> 178106 keys | 5461 slots | 1 slaves.
[OK] 534511 keys in 3 masters.
32.62 keys per slot on average.
```



```sh
[root@localhost new_redis]# docker run --rm -it redis redis-cli -h 172.17.0.12 -p 8001
172.17.0.12:8001> cluster nodes
6104ad4f30a511d642aebb1bce8dd77bb5d10621 172.17.0.11:8006@18006 slave 2097e0e6a66c6adb6ddbe3bc783663d390a9360d 0 1557199119530 6 connected
f9a309feda3b442dbf555712c7ff47026dc4700b 172.17.0.9:8004@18004 slave 1768735459c96a46722b1f0f038c125fa88aef83 0 1557199119000 4 connected
f015467b0439b9694a6d633cc62a2502079e74f7 172.17.0.8:8002@18002 master - 0 1557199120532 2 connected 5461-10922
1768735459c96a46722b1f0f038c125fa88aef83 172.17.0.12:8001@18001 myself,master - 0 1557199118000 1 connected 0-5460
2097e0e6a66c6adb6ddbe3bc783663d390a9360d 172.17.0.13:8003@18003 master - 0 1557199120030 3 connected 10923-16383
8126fa4d990c4e08cdb7d3e2ebf59771445b3a1a 172.17.0.10:8005@18005 slave f015467b0439b9694a6d633cc62a2502079e74f7 0 1557199119530 5 connected
```



---

### Redis单节点单实例



docker-compose.yml:

```yaml
version: '3'

services:
    redis:
        image: redis
        ports:
            - "6379:6379"
        volumes:
            - ./data:/data
            - ./conf/redis.conf:/etc/redis.conf
        networks:
            localnet:
                aliases:
                    - my-redis-server
        command: ["redis-server", "/etc/redis.conf"]

networks:
    localnet:
```



---

### 单节点redis集群

docker-compose.yml:

```yaml
version: '3'

services:
 redis1:
  image: redis-cluster
  restart: always
  volumes:
   - /data/redis/6381/data:/data
  environment:
   - REDIS_PORT=6381
  ports:
    - '6381:6381'       #服务端口
    - '16381:16381'   #集群端口

 redis2:
  image: redis-cluster
  restart: always
  volumes:
   - /data/redis/6382/data:/data
  environment:
   - REDIS_PORT=6382
  ports:
    - '6382:6382'
    - '16382:16382'

 redis3:
  image: redis-cluster
  restart: always
  volumes:
   - /data/redis/6383/data:/data
  environment:
   - REDIS_PORT=6383
  ports:
    - '6383:6383'
    - '16383:16383'

 redis4:
  image: redis-cluster
  restart: always
  volumes:
   - /data/redis/6384/data:/data
  environment:
   - REDIS_PORT=6384
  ports:
    - '6384:6384'
    - '16384:16384'

 redis5:
  image: redis-cluster
  restart: always
  volumes:
   - /data/redis/6385/data:/data
  environment:
   - REDIS_PORT=6385
  ports:
    - '6385:6385'
    - '16385:16385'

 redis6:
  image: redis-cluster
  restart: always
  volumes:
   - /data/redis/6386/data:/data
  environment:
   - REDIS_PORT=6386
  ports:
    - '6386:6386'
    - '16386:16386'
```



redis.conf:

```ini
#端口
port REDIS_PORT
#开启集群
cluster-enabled yes
#配置文件
cluster-config-file nodes.conf
cluster-node-timeout 5000
#更新操作后进行日志记录
appendonly yes
#设置主服务的连接密码
# masterauth
#设置从服务的连接密码
# requirepass
```



entrypoint.sh:

```sh
#!/bin/sh
#只作用于当前进程,不作用于其创建的子进程
set -e
#$0--Shell本身的文件名 $1--第一个参数 $@--所有参数列表
# allow the container to be started with `--user`
if [ "$1" = 'redis-server' -a "$(id -u)" = '0' ]; then
    sed -i 's/REDIS_PORT/'$REDIS_PORT'/g' /usr/local/etc/redis.conf
    chown -R redis .  #改变当前文件所有者
    exec gosu redis "$0" "$@"  #gosu是sudo轻量级”替代品”
fi

exec "$@"
```



Dockerfile:

```yaml
FROM redis

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

# ENV REDIS_PORT 8000
# ENV REDIS_PORT_NODE 18000
EXPOSE $REDIS_PORT
# EXPOSE $REDIS_PORT_NODE

COPY entrypoint.sh /usr/local/bin/
COPY redis.conf /usr/local/etc/
RUN chmod 777 /usr/local/etc/redis.conf
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["redis-server", "/usr/local/etc/redis.conf"]
```

