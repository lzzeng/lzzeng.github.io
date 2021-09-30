---
title: Elasticsearch笔记
date: 2021-7-29 22:55:40
tags:
    - Elasticsearch
categories:
    - DevOps
copyright: false
toc: true
---



## 特点

PB级 结构化和非结构化数据
开源
全文搜索引擎
非规范化，提高搜索性能
<!-- more -->



## 优点

分布式
实时
基于Java，跨平台
json对象作相应，大部分语言支持
和solr相比，多用户管理容易



## 缺点

和solr相比，不支持csv、xml格式的数据
脑裂问题



## 概念

### 节点

它指的是Elasticsearch的单个正在运行的实例。单个物理和虚拟服务器容纳多个节点，这取决于其物理资源的能力，如RAM，存储和处理能力。



### 集群

它是一个或多个节点的集合。 集群为整个数据提供跨所有节点的集合索引和搜索功能。



### 索引

它是不同类型的文档和文档属性的集合。索引还使用分片的概念来提高性能。 例如，一组文档包含社交网络应用的数据。



### 类型/映射

它是共享同一索引中存在的一组公共字段的文档的集合。 例如，索引包含社交网络应用的数据，然后它可以存在用于用户简档数据的特定类型，另一类型可用于消息的数据，以及另一类型可用于评论的数据。



### 文档

它是以JSON格式定义的特定方式的字段集合。每个文档都属于一个类型并驻留在索引中。每个文档都与唯一标识符(称为UID)相关联。



### 碎片

索引被水平细分为碎片。这意味着每个碎片包含文档的所有属性，但包含的数量比索引少。水平分隔使碎片成为一个独立的节点，可以存储在任何节点中。主碎片是索引的原始水平部分，然后这些主碎片被复制到副本碎片中。



### 副本

Elasticsearch允许用户创建其索引和分片的副本。 复制不仅有助于在故障情况下增加数据的可用性，而且还通过在这些副本中执行并行搜索操作来提高搜索的性能。



## Elasticsearch和RDBMS之间的比较

|Elasticsearch|关系型数据库|
|---|---|
|索引|数据库|
|碎片|碎片|
|映射|表|
|字段|字段|
|JSON对象|元组|



## API

### 多索引

- 逗号
  ```
POST http://localhost:9200/index1,index2,index3/_search
  {
   "query":{
    "query_string":{
       "query":"any_string"
    }
   }
  }
  ```
  
- 通配符 * + -

  ```
  POST http://localhost:9200/school*/_search
  POST http://localhost:9200/school*,-schools_gov/_search
  ```

- _all

  ```
  POST http://localhost:9200/_all/_search
  ```

- ignore_unavailable

	```
	POST http://localhost:9200/school*,book_shops/_search?ignore_unavailable=true
	#假设book_shops不存在，响应也不会报404错误
	```
	
- allow_no_indices

	```
	POST http://localhost:9200/schools_pri*/_search?allow_no_indices=true
	```
	
	

### 文档

- 创建

  ```
  POST /schools/school/4
  ```

- 更新

  ```
  PUT ...
  ```

- 版本控制
	- 内部控制（默认）
		- 更新、删除、新增等操作时，自动+1，从1开始
	- 外部控制 version_type: external
		- ?version=2

- 操作类型

	```
	POST http://localhost:9200/tutorials/chapter/1?op_type=create
	```
	
	是一种明确操作类型的操作，防止更新已有文档。指明create后，如果已有该index/type/id则报错version conflict
	
- 指定所需的字段

	- ?fields = name,fees

- 指定超时

	- ?timeout = 3m



## 映射

```
/_mapping?pretty" -H 'Content-Type: application/json' -d'
{
  "properties": {
    "name": { 
      "type":     "text",
      "fielddata": true
    }
  }
}
```



## 聚合搜索

### 平均聚合 avg

```
POST http://localhost:9200/schools/_search
{
 "aggs": {
    "avg_fees": {
      "avg": {
        "field": "fees"
        "missing": 0
      }
    }
  }
}
```



### 基数聚合 cardinality

```
POST http://localhost:9200/schools*/_search
{
  "aggs": {
    "distinct_name_count": {"cardinality": {"field": "name"}}
  }
}
#特定字段的不同值的计数
```



### 扩展统计 extended_stats

```
{
  "aggs" : {
    "fees_stats": { "extended_stats": { "field": "fees" } }
  }
}
```



### 最值聚合 max/min

```
{
  "aggs": {
    "min_fees": {
      "min": {"field": "fees" }
    }
  }
}
```



### 求和 sum

```
{
  "aggs": {
    "sum_fees": {
      "sum": {"field": "fees" }
    }
  }
}
```



### meta

```
{
  "aggs" : {
    "min_fees": {
      "avg": { "field": "fees" } ,
      "meta": {"dsc": "Lowest Fees"}
    }
  }
}

响应如下：
{
   "aggregations":{"min_fees":{"meta":{"dsc":"Lowest Fees"}, "value":2180.0}}
}
```



### 桶聚合 bucket

包含：
**子聚集**
此存储桶聚合会生成映射到父存储桶的文档集合。类型参数用于定义父索引。 例如，我们有一个品牌及其不同的模型，然后模型类型将有以下_parent字段

```
{
   "model" : {
      "_parent" : {
         "type" : "brand"
      }
   }
}
```

还有许多其他特殊的桶聚合，这在许多其他情况下是有用的，它们分别是：

日期直方图汇总/聚合
日期范围汇总/聚合
过滤聚合
过滤器聚合
地理距离聚合
GeoHash网格聚合
全局汇总
直方图聚合
IPv4范围聚合
失踪聚合
嵌套聚合
范围聚合
反向嵌套聚合
采样器聚合
重要条款聚合
术语聚合



## 配置

### 自动创建索引

**elasticsearch.yml**

当请求将JSON对象添加到特定索引时，如果该索引不存在，那么此API会自动创建该索引以及该特定JSON对象的基础映射。 可以通过将以下参数的值更改为false来禁用此功能，这个值是存在于elasticsearch.yml文件中，打开elasticsearch.yml文件设置如下 。
action.auto_create_index:false
index.mapper.dynamic:false
还可以限制自动创建索引，其中通过更改以下参数的值只允许指定模式的索引名称 -
action.auto_create_index:+acc*,-bank*
(其中+表示允许， - 表示不允许)



---

*来源：https://www.yiibai.com/elasticsearch/elasticsearch_aggregations.html*