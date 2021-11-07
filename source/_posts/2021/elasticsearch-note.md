---
title: Elasticsearch笔记02
date: 2021-08-15 22:55:40
tags:
    - Elasticsearch
categories:
    - DevOps
copyright: false
toc: true
---





## 倒排索引

倒排索引是单词文档矩阵的一种存储形式
分词系统将文档切分成单词序列

> 单词文档矩阵 = 单词词典 + 倒排文件
> 单词词典：所有单词的集合，包括单词本身的信息和指向倒排列表的指针
> 倒排文件：所有单词的倒排列表顺序地存储在磁盘里形成的文件

倒排列表最简单的形式仅记录包含某个单词的文档编号(DocID)，复杂一些的，还记录了单词在某个文档出现的次数，即单词频率（TF），还可能包含某个单词的文档数，即文档频率（DF）,和单词在文档中的位置（Pos）

<!-- more -->




## ES操作记录

版本：7.5



### 创建索引（同时创建映射）

```
curl -XPUT http://localhost:9200/book -H "Content-Type: application/json" -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "long"
      },
      "name": {
        "type": "text"
      },
      "book_url": {
        "type": "keyword"
      },
      "price": {
        "type": "double"
      }
    }
  }
}'
```

7.0之后的版本没有type的概念（见[Removal of mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html)）。如果需要迁移包含多个type的旧索引到新版本ES里，可以创建多个index分别对应一个type，或者只创建一个index并增加type字段，然后使用[reindex](https://www.elastic.co/guide/en/elasticsearch/reference/7.15/docs-reindex.html)迁移文档。



### 用PUT还是POST？

操作具体的资源用PUT，操作集合资源用POST，POST非幂等性。

> _settings需用PUT不能用POST
> _search不能用PUT



### 查看映射

```
[root@localhost es_api_test]# curl -s -XGET http://localhost:9200/book/_mapping |jq
```



### 创建一个文档、查看

```
PUT /user/_doc/1
{
  "username": "dream-hammer",
  "message": "abc123"
}
```

```
# curl创建
curl -XPUT  -H 'Content-Type: application/json' http://localhost:9200/user/_doc/1 -d '{"username": "dream-hammer","message": "abc123"}'
# curl查询
curl -s -XPOST localhost:9200/user/_search -H 'Content-Type: application/json' -d '{"query": {"match_all": {}}}' |jq
```

```
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "user",
        "_type": "_doc",
        "_id": "1",
        "_score": 1,
        "_source": {
          "username": "dream-hammer",
          "message": "abc123"
        }
      }
    ]
  }
}
```



### 更新一个文档

```
PUT /user/_doc/1
{
  "message": "def321"
}

{
  "_index" : "user",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 7,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 10,
  "_primary_term" : 1
}
```



### 乐观更新

```
PUT /user/_doc/1?version=7
{
  "message": "def3210"
}
```

报错如下：

```
{
  "error": {
    "root_cause": [
      {
        "type": "action_request_validation_exception",
        "reason": "Validation Failed: 1: internal versioning can not be used for optimistic concurrency control. Please use `if_seq_no` and `if_primary_term` instead;"
      }
    ],
    "type": "action_request_validation_exception",
    "reason": "Validation Failed: 1: internal versioning can not be used for optimistic concurrency control. Please use `if_seq_no` and `if_primary_term` instead;"
  },
  "status": 400
}
```

version不能用于乐观并发更新。改用seq_no和primary_term如下：

```
GET /user/_doc/1  # 查看当前seq_no, primary_term
PUT /user/_doc/1?if_seq_no=10&if_primary_term=1
{
  "message": "def3210"
}
```



### 批量创建文档

```sh
[root@localhost es_api_test]# cat songs.bulk
{"index": {"_index": "songs", "_type": "_doc"}}
{"id": 1, "name": "风筝误", "time": "04:31", "artist": "刘珂矣", "album": "半壶纱", "cover": "https://s5.music.126.net/style/web2/img/default/default_album.jpg", "url": "static/media/风筝误.mp3"}
...
```

```
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@songs.bulk"    #是--data-binary，不是-d，否则提示parse_exception
```



### 查看索引

```
[root@localhost es_api_test]# curl http://localhost:9200/_cat/indices?v
health status index                    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .kibana_task_manager_1   zKnjGTdrRgyElkST2F-Bdw   1   0          2            0     31.6kb         31.6kb
yellow open   songs                    2-yMj8ikTYay4k8f_CIQ2g   1   1         25            0     28.4kb         28.4kb
green  open   .apm-agent-configuration nP5HnnIYQhWqjcd17By6lA   1   0          0            0       283b           283b
green  open   .kibana_1                zZuFlefIRhaHHBdJiYovuw   1   0         10            3     43.4kb         43.4kb
```



### 查看集群健康状态

```sh
[root@localhost es_api_test]# curl http://localhost:9200/_cluster/health?pretty
{
  "cluster_name" : "docker-cluster",
  "status" : "yellow",    #yellow状态
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 4,
  "active_shards" : 4,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 1,    #unassigned 1
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 80.0
}
```



### 查看分片

```sh
[root@localhost es_api_test]# curl http://localhost:9200/_cat/shards/songs?v
index shard prirep state      docs  store ip         node
songs 0     p      STARTED      25 28.4kb 172.24.0.2 1583abe64b70
songs 0     r      UNASSIGNED
```



### 查看文档数

```sh
[root@localhost es_api_test]# curl http://localhost:9200/songs/_count?pretty
{
  "count" : 25,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  }
}
```



### 基数聚合

```
POST /songs/_search
{
  "aggs": {
    "distinct_name_count": {"cardinality": {"field": "name"}}
  }
}
```

报错信息如下：

```
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [name] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
      }
    ],
...
```

解决方法：

1. 改name为name.keyword
2. 设置fileddata=true

```
POST /songs/_mapping
{
  "properties": {
     "name": {
       "type": "text", 
       "fielddata": true
     }
  }
}
```



### 获取索引前50个文档

```
GET|POST /songs/_search?size=50

GET|POST /songs/_search?size=50
{
  "query": {
    "match_all": {}
  }
}

GET|POST /songs/_search
{
  "query": {
    "match": {
      "name.keyword": "风筝误"
    }
  }
}
```



### 用GET还是POST?

有点奇怪，GET也可以带请求体，ES官网的search语法[示例](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-span-containing-query.html)都是GET。

> GET请求是是依靠URI检索数据的，RFC没有规定不能有响应体，只是说GET通过URI标识并**获取**了一个资源，且再次获取不会重新请求，可以减少网络负担。



```sh
[root@localhost ~]# curl -s -XPOST localhost:9200/songs/_search?size=50 -H 'Content-Type: application/json' -d '{"query": {"match_all": {}}}' 2>/dev/null  |jq
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 25,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "songs",
        "_type": "_doc",
        "_id": "vwFbiHsBbxOPhTYXJGC2",
        "_score": 1,
        "_source": {
          "id": 1,
          "name": "风筝误",
          "time": "04:31",
          "artist": "刘珂矣",
          "album": "半壶纱",
          "cover": "https://s4.music.126.net/style/web2/img/default/default_album.jpg",
          "url": "static/media/风筝误.mp3"
        }
      },
      ...
    ]
  }
}
```



生成jsonp

```sh
[root@localhost ~]# curl -s -XPOST localhost:9200/songs/_doc/_search?size=50 -H 'Content-Type: application/json' -d '{"query": {"match_all": {}}}' 2>/dev/null  |jq |awk 'BEGIN{flag=0}{if($0~/"_source":/){print "{"; flag=1}else if(flag){print $0;} if($0~/^\s*}$/){flag=0}}' |sed 's/\s*}/},/g;' |sed '1 s/^{/{"data": [{/' |sed '$ s/,$/]}/' |jq |sed '1 i callBack(' |sed '$ s/$/);/'
callBack(
{
  "data": [
    {
      "id": 1,
      "name": "风筝误",
      "time": "04:31",
      "artist": "刘珂矣",
      "album": "半壶纱",
      "cover": "https://s4.music.126.net/style/web2/img/default/default_album.jpg",
      "url": "static/media/风筝误.mp3"
    },
    ...
  ]
});
```



### 其它API

- [es-api-memo](https://lzzeng.github.io/docs/docs/log-analysis/es-api-memo.html)
- [Elasticsearch笔记01](https://lzzeng.github.io/2021/Elasticsearch/)