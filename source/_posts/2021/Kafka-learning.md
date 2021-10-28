---
title: Kafka笔记
date: 2021-4-29 22:55:40
tags:
    - Kafka
categories:
    - Hadoop
copyright: false
toc: true
---





## 常用命令

```sh
# 创建主题
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topic-1
```

<!-- more -->




```sh
# 列出topic
bin/kafka-topics.sh  --list --zookeeper localhost:2181

# 查看topic信息
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-topics.sh --topic test --describe --zookeeper localhost:2181
Topic: test	TopicId: qmyHki2JRAmbHssyAaGNqw	PartitionCount: 1	ReplicationFactor: 1	Configs: 
	Topic: test	Partition: 0	Leader: 1	Replicas: 1	Isr: 1

# 删除topic
bin/kafka-topics.sh --delete --topic topic-01 --zookeeper localhost:2181
Note: This will have no impact if delete.topic.enable is not set to true.
```




```sh
# 发送消息（通过console）
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-console-producer.sh --broker-list 192.168.19.208:9092 --topic test
>abc
>123 456
>

# 订阅消息
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-console-consumer.sh --bootstrap-server 192.168.19.208:9092 --topic test --from-beginning
abc
123 456
```




```sh
# 生产者压测-批量创建消息
bin/kafka-producer-perf-test.sh --topic topic-1 --num-records 10000 --record-size 1024 --throughput -1 --producer-props bootstrap.servers=192.168.19.208:9092 acks=1

# 消费者压测
bin/kafka-consumer-perf-test.sh --bootstrap-server 127.0.0.1:9092 --topic perf_test --messages 1000000 --threads 8 --reporting-interval 1000
```



<font color=red>问题1</font>：producer通过 `--broker-list localhost:9092` 或 `--bootstrap-server 127.0.0.1:9092` 连接broker失败，而不使用localhost、127.0.0.1改用broker节点IP则可以，是否是配置错了？

```sh
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-console-producer.sh --topic test --bootstrap-server 127.0.0.1:9092
>[2021-10-28 11:45:36,517] WARN [Producer clientId=console-producer] Connection to node -1 (/127.0.0.1:9092) could not be established. Broker may not be available. (org.apache.kafka.clients.NetworkClient)
[2021-10-28 11:45:36,517] WARN [Producer clientId=console-producer] Bootstrap broker 127.0.0.1:9092 (id: -1 rack: null) disconnected (org.apache.kafka.clients.NetworkClient)
...
```



首先，`--broker-list` 选项是过时的，不建议继续使用。consumer无此选项。

```sh
[root@kafka-1 kafka_2.12-2.8.0]# bin/kafka-console-producer.sh --help
This tool helps to read data from standard input and publish it to Kafka.
Option                                   Description                            
------                                   -----------                            
--batch-size <Integer: size>             Number of messages to send in a single 
                                           batch if they are not being sent     
                                           synchronously. (default: 200)        
--bootstrap-server <String: server to    REQUIRED unless --broker-list          
  connect to>                              (deprecated) is specified. The server
                                           (s) to connect to. The broker list   
                                           string in the form HOST1:PORT1,HOST2:
                                           PORT2.                               
--broker-list <String: broker-list>      DEPRECATED, use --bootstrap-server     
                                           instead; ignored if --bootstrap-     
                                           server is specified.  The broker     
                                           list string in the form HOST1:PORT1, 
                                           HOST2:PORT2.
```



 `server.properties` 配置如下：

```ini
############################# Socket Server Settings #############################

# The address the socket server listens on. It will get the value returned from
# java.net.InetAddress.getCanonicalHostName() if not configured.
#   FORMAT:
#     listeners = listener_name://host_name:port
#   EXAMPLE:
#     listeners = PLAINTEXT://your.host.name:9092
#listeners=PLAINTEXT://:9092
##listeners=PLAINTEXT://localhost:9092
listeners=PLAINTEXT://192.168.19.208:9092

# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
#advertised.listeners=PLAINTEXT://your.host.name:9092
##advertised.listeners=PLAINTEXT://localhost:9092
advertised.listeners=PLAINTEXT://192.168.19.208:9092
```

因此，是listeners 和advertised.listeners配置的问题，能使用已注册到zookeeper的地址。按默认配置的话，可以使用localhost或127.0.0.1，不指定具体IP的话，在客户端代码中通过API去连接Kafka就会报错，因为没有获取到服务端的IP，只能从服务器使用localhost连接（localhost可以，指定IP应该也可以吧）。



<font color=red>问题2</font>：：pssh执行 `bin/kafka-server-stop.sh` 未能停止Kafka？

查看stop脚本：

```sh
OSNAME=$(uname -s)
if [[ "$OSNAME" == "OS/390" ]]; then
    if [ -z $JOBNAME ]; then
        JOBNAME="KAFKSTRT"
    fi
    PIDS=$(ps -A -o pid,jobname,comm | grep -i $JOBNAME | grep java | grep -v grep | awk '{print $1}')
elif [[ "$OSNAME" == "OS400" ]]; then
    PIDS=$(ps -Af | grep -i 'kafka\.Kafka' | grep java | grep -v grep | awk '{print $2}')
else
    PIDS=$(ps ax | grep ' kafka\.Kafka ' | grep java | grep -v grep | awk '{print $1}')
fi
```



脚本手动执行获取PID没问题，可能是环境变量的原因，source后执行了一次正常停止了。但start时却不需要source。

```sh
[root@localhost zlz]# pssh -h kafka.ips -i "cd /opt/kafka/kafka_2.12-2.8.0; source ~/.bashrc; sh run-kafka.sh stop"
```



再恢复重试时不加source也能正常停止了。最后发现命令没问题，不需要source。pssh 批量停止Kafka server时，不会马上停止，是陆续停止的，可能有几秒的延迟。即便在各server上手动执行stop，也是如此。

因此没问题。



<font color=red>问题3</font>：advertised.listeners和listeners配置都注释掉，Kafka server不能按默认localhost:9092启动？

仅放开`listeners=PLAINTEXT://:9092`也不行。经测设置 `listeners=PLAINTEXT://localhost:9092` 可以启动，但是producer或consumer连接时会报错。

如果继续设置 `advertised.listeners=PLAINTEXT://localhost:9092`  的话，就又会无法启动server了!

可能需要集群状态数据吧，按localhost连接没试成，不折腾了，改回配置IP加端口的方式。





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

