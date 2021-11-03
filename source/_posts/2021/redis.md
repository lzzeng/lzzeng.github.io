---
title: Redis笔记02
date: 2021-03-27 22:55:40
tags:
    - Redis
categories:
    - DevOps
copyright: false
toc: true
---





> [Redis笔记01](https://lzzeng.github.io/2021/redis-questions/)



## 线程模型

单线程模型，文件事件处理器通过IO多路复用 监听多个socket（socket执行accept read write close等操作产生文件事件），然后由文件事件处理器处理文件事件。

<!-- more -->



## 持久化方式

rdb：快照

```
save 900 1
save 300 10
save 60 10000
```


aof： 默认配置的是 appendonly no，改成yes打开AOF模式



## 如何连接Redis

1～使用实现了一致性哈希算法的proxy中间件twemproxy
2～Java使用Jedis、ShardedJedis、JedisPool、JedisSentinelPool（哨兵模式）或JedisCluster（Redis cluster模式）连接redis



Jedis 2.9.1存在的一个bug: <https://blog.csdn.net/u013527895/article/details/103121558>

Jedis加载redis集群的第一个节点如果异常不在线，并且redis设置了密码的话，会因连接异常退出不再尝试下一个节点。所谓第一个节点，就是所有redis节点加载到HashSet<HostAndPort>集合后集合里第一个元素。

```java
//src/main/java/redis/clients/jedis/JedisClusterConnectionHandler.java
  private void initializeSlotsCache(Set<HostAndPort> startNodes, GenericObjectPoolConfig poolConfig, int connectionTimeout, int soTimeout, String password, String clientName) {
    for (HostAndPort hostAndPort : startNodes) {
      Jedis jedis = null;
      try {
        jedis = new Jedis(hostAndPort.getHost(), hostAndPort.getPort(), connectionTimeout, soTimeout);
        if (password != null) {
          jedis.auth(password);
        }
        if (clientName != null) {
          jedis.clientSetname(clientName);
        }
        cache.discoverClusterNodesAndSlots(jedis);
        break;
      } catch (JedisConnectionException e) {
        // try next nodes
      } finally {
        if (jedis != null) {
          jedis.close();
        }
      }
    }
  }
```



## Jedis连接Redis代码参考

深入剖析Redis客户端Jedis的特性和原理: <https://baijiahao.baidu.com/s?id=1715292157796722813&wfr=spider&for=pc>



主从模式连接：Jedis

```java
import redis.clients.jedis.Jedis;

public class MasterAndSlaveTest {
    public static void main(String[] args) throws InterruptedException {
        Jedis jedis_M = new Jedis("192.168.248.129",6379); //主机
        Jedis jedis_S = new Jedis("192.168.248.129",6380); //从机
        
        //遵循“配从不配主”的模式
        jedis_S.slaveof("192.168.248.129",6379);
        
        jedis_M.set("class", "8888"); //主机去写
        
        //内存中读写太快，防止读在写之前先完成而出现null的情况，这里做一下延迟
        Thread.sleep(2000);
        String result = jedis_S.get("class"); //从机去读
        System.out.println(result);
    }
}
```



多个redis实例（非cluster）：ShardedJedis，一致性哈希算法

```java
import java.util.ArrayList;
import java.util.List;
import redis.clients.jedis.JedisShardInfo;
import redis.clients.jedis.ShardedJedis;

List<JedisShardInfo> shards = new ArrayList<>();
JedisShardInfo info = null ;
for (String address : addresss.split(",")) {
    String[] hostAndPort = address.split(":");
    info = new JedisShardInfo(hostAndPort[0], Integer.valueOf(hostAndPort[1]));
    shards.add(info);
}
shardedJedis = new ShardedJedis(shards);
shardedJedis.set("a", "123");
shardedJedis.get("a");
```



哨兵模式连接：JedisSentinelPool

```java 
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.JedisSentinelPool

//1.设置sentinel 各个节点集合
Set<String> sentinelSet = new HashSet<>();
sentinelSet.add("192.168.14.101:26379");
sentinelSet.add("192.168.14.102:26379");
sentinelSet.add("192.168.14.103:26379");

//2.设置jedispool 连接池配置文件
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(10);
config.setMaxWaitMillis(1000);

//3.设置mastername,sentinelNode集合,配置文件,Redis登录密码
JedisSentinelPool jedisSentinelPool = new JedisSentinelPool("mymaster",sentinelSet,config,"123");
Jedis jedis = null;
try {
    jedis = jedisSentinelPool.getResource();
    //获取Redis中key=hello的值
    String value = jedis.get("hello");
    System.out.println(value);
} catch (Exception e) {
    e.printStackTrace();
} finally {
    if(jedis != null){
        jedis.close();
    }
}
```



cluster模式连接：JedisCluster，哈希槽算法

```java
 import java.util.HashSet;
 import java.util.Set;
 import redis.clients.jedis.HostAndPort;
 import redis.clients.jedis.JedisCluster;

 public class TestJedisCluster {
  public static void main(String[] args) {
    //1、创建jedidsCluster客户端
    //创建一个set集合，用来封装所有redis节点的信息
    Set<HostAndPort> nodes = new HashSet<>();
    
    nodes.add(new HostAndPort("192.168.23.12", 7001));
    nodes.add(new HostAndPort("192.168.23.12", 7002));
    nodes.add(new HostAndPort("192.168.23.12", 7003));
    //...
    
    JedisCluster cluster = new JedisCluster(nodes);
    
    String name = cluster.get("user:id:1:name");
    cluster.set("user:id:1:address", "你好呀");
    String address = cluster.get("user:id:1:address");
    
    System.out.println("name:"+name);
    System.out.println("address:"+address);     
    if(null!=cluster){
        cluster.close();
    }}}
```



## 集群操作

5.0版本之前使用redis-trib.rb ruby脚本操作redis集群，5.0以上统一使用redis-cli操作。

redis cluster半数以下的节点陆续下线后，集群仍可正常提供服务，节点重新上线后，节点上原master变成slave，后面不发生异常的话，不会自动调转过来。



---

（待续）