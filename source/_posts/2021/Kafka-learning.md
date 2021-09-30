---
title: Kafka学习
date: 2021-4-29 22:55:40
tags:
    - Kafka
categories:
    - Hadoop
copyright: false
toc: true
---



```sh
# 创建主题
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topic-1
```

<!-- more -->


```
# 列出topic
bin/kafka-topics.sh  --list --zookeeper localhost:2181

# 订阅消费
bin/kafka-console-consumer.sh --bootstrap-server 192.168.19.208:9092 --topic duanjt_test --from-beginning

# 删除topic
bin/kafka-topics.sh --delete --topic topic-01 --zookeeper localhost:2181
Note: This will have no impact if delete.topic.enable is not set to true.

# 生产者压测-批量创建消息
bin/kafka-producer-perf-test.sh --topic topic-1 --num-records 10000 --record-size 1024 --throughput -1 --producer-props bootstrap.servers=192.168.19.208:9092 acks=1

# 消费者测试
bin/kafka-consumer-perf-test.sh --bootstrap-server 127.0.0.1:9092 --topic perf_test --messages 1000000 --threads 8 --reporting-interval 1000
```



## 性能测试

### 生产者性能测试

```sh
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 2 --topic topic-2
Created topic topic-2.
...
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 64 --topic topic-64
Created topic topic-64.

[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-producer-perf-test.sh --topic topic-2 --num-records 10000 --record-size 1024 --throughput -1 --producer-props bootstrap.servers=192.168.19.208:9092 acks=1
...
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-producer-perf-test.sh --topic topic-64 --num-records 10000 --record-size 1024 --throughput -1 --producer-props bootstrap.servers=192.168.19.208:9092 acks=1
10000 records sent, 5614.823133 records/sec (5.48 MB/sec), 611.42 ms avg latency, 1299.00 ms max latency, 551 ms 50th, 1189 ms 95th, 1266 ms 99th, 1299 ms 99.9th.
```



### 消费者性能测试

```sh
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-consumer-perf-test.sh --bootstrap-server 192.168.19.208:9092 --topic topic-2 --messages 10000
...
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-consumer-perf-test.sh --bootstrap-server 192.168.19.208:9092 --topic topic-64 --messages 10000
start.time, end.time, data.consumed.in.MB, MB.sec, data.consumed.in.nMsg, nMsg.sec, rebalance.time.ms, fetch.time.ms, fetch.MB.sec, fetch.nMsg.sec
2021-09-19 11:23:23:801, 2021-09-19 11:23:24:480, 9.7656, 14.3824, 10000, 14727.5405, 428, 251, 38.9069, 39840.6375
```



结果如下：

| 分区数（副本因子=2） | 生产速度（第二次测试） | 生产速度 |消费速度 |
| ---- | ---- | ---- | ---- |
|2|9.53 MB/sec|6.90 MB/sec|41.21 MB/sec|
|4|8.74 MB/sec|5.92 MB/sec|35.03 MB/sec|
|8|8.99 MB/sec|7.59 MB/sec|39.23 MB/sec|
|16|11.37 MB/sec|8.43 MB/sec|<font color=red>46.81 MB/sec</font>|
|32|<font color=red>12.19 MB/sec</font>|<font color=red>10.34 MB/sec</font>|43.03 MB/sec|
|64|10.90 MB/sec|5.48 MB/sec|38.90 MB/sec|