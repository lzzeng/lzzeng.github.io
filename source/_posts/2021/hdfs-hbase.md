---
title: HDFS和HBase
date: 2021-5-29 22:55:40
tags:
    - Hadoop
categories:
    - Hadoop
copyright: false
---



## HDFS

HDFS是Hadoop分布式文件系统。
一个HDFS集群主要由一个NameNode和很多个Datanode组成：Namenode管理文件系统的元数据，而Datanode存储了实际的数据。
<!-- more -->
HDFS采用一种称为机架感知(rack-aware)的策略来改进数据的可靠性、可用性和网络带宽的利用率。

副本：在大多数情况下，副本系数是3，HDFS的存放策略是将一个副本存放在本地机架的节点上，一个副本放在同一机架的另一个节点上，最后一个副本放在不同机架的节点上。



## HBase

HBase是Google Bigtable的开源实现，类似Google Bigtable利用GFS作为其文件存储系统，HBase利用Hadoop HDFS作为其文件存储系统。

利用Hadoop MapReduce来处理HBase中的海量数据。




为什么在HDFS上使用HBase？
- HBase 在 HDFS 之上提供了：
  - 高并发实时随机写，通过 LSM（内存+顺序写磁盘）的方式提供了 HDFS 所不拥有的实时随机写及修改功能
  - 高并发实时点读及扫描（了解一下 LSM 算法），在文件系统之上有数据库，在业务层面，HBase 完全可以独立于 HDFS
- HDFS为HBase提供了高可靠性的底层存储支持
- Hadoop MapReduce为HBase提供了高性能的计算能力，Zookeeper为HBase提供了稳定服务和failover机制。Pig和Hive还为HBase提供了高层语言支持，使得在HBase上进行数据统计处理变的非常简单。 Sqoop则为HBase提供了方便的RDBMS（关系型数据库）数据导入功能，使得传统数据库数据向HBase中迁移变的非常方便
- HBASE可以满足大规模数据的实时处理需求
	- HDFS面向批量访问模式，不是随机访问模式
	- Hadoop可以很好地解决大规模数据的离线批量处理问题，但是，受限于Hadoop MapReduce编程框架的高延迟数据处理机制，使得Hadoop无法满足大规模数据实时处理应用的需求

Hadoop的四个主要组成部分：核心包，HDFS文件系统，MapReduce模型，yarn资源调度框架。
