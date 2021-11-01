---
title: RESTful介绍
date: 2021-5-25 22:55:40
tags:
    - else
categories:
    - 其它
copyright: false
toc: true
---



> Representational State Transfer，具象状态传输（转换），表现层状态转移。

<!-- more -->



## 是Web服务的一种新的架构风格（一种思想）

面向资源
一种软件架构风格
URL定位资源，用HTTP动词（GET,POST,DELETE,DETC）描述操作，从status code获知结果



## REST架构的主要原则

对网络上所有的资源都有一个资源标志符
对资源的操作不会改变标识符
同一资源有多种表现形式（xml、json）
所有操作都是无状态的（Stateless）



## RESTful设计准则

宾语必须是名词
复数URL
避免多级URL
- 更好的做法是，除了第一级，其他级别都用查询字符串表达
GET /authors/12?categories=2
GET /articles?published=true

传统 vs REST风格

```
http://127.0.0.1/user/query/1 GET
http://127.0.0.1/user/save POST 
http://127.0.0.1/user/update POST
http://127.0.0.1/user/delete GET/POST
```

```
http://127.0.0.1/user/{id} GET
http://127.0.0.1/user POST
http://127.0.0.1/user PUT
http://127.0.0.1/user DELETE

PATCH/collections/identity：返回被修改的属性
```



网络上的所有事物都可以被抽象为资源。
每一个资源都有唯一的资源标识，对资源的操作不会改变这些标识。
所有的操作都是无状态的。



## 状态码

**GET**
安全且幂等
获取表示
变更时获取表示（缓存）
200（OK） - 表示已在响应中发出
204（无内容） - 资源有空表示
301（Moved Permanently） - 资源的URI已被更新
303（See Other） - 其他（如，负载均衡）
304（not modified）- 资源未更改（缓存）
400 （bad request）- 指代坏请求（如，参数错误）
404 （not found）- 资源不存在
406 （not acceptable）- 服务端不支持所需表示
500 （internal server error）- 通用错误响应
503 （Service Unavailable）- 服务端当前无法处理请求

**POST**
不安全且不幂等
使用服务端管理的（自动产生）的实例号创建资源
创建子资源
部分更新资源
如果没有被修改，则不过更新资源（乐观锁）
200（OK）- 如果现有资源已被更改
201（created）- 如果新资源被创建
202（accepted）- 已接受处理请求但尚未完成（异步处理）
301（Moved Permanently）- 资源的URI被更新
303（See Other）- 其他（如，负载均衡）
400（bad request）- 指代坏请求
404 （not found）- 资源不存在
406 （not acceptable）- 服务端不支持所需表示
409 （conflict）- 通用冲突
412 （Precondition Failed）- 前置条件失败（如执行条件更新时的冲突）
415 （unsupported media type）- 接受到的表示不受支持
500 （internal server error）- 通用错误响应
503 （Service Unavailable）- 服务当前无法处理请求

**PUT**
不安全但幂等
用客户端管理的实例号创建一个资源
通过替换的方式更新资源
如果未被修改，则更新资源（乐观锁）
200 （OK）- 如果已存在资源被更改
201 （created）- 如果新资源被创建
301（Moved Permanently）- 资源的URI已更改
303 （See Other）- 其他（如，负载均衡）
400 （bad request）- 指代坏请求
404 （not found）- 资源不存在
406 （not acceptable）- 服务端不支持所需表示
409 （conflict）- 通用冲突
412 （Precondition Failed）- 前置条件失败（如执行条件更新时的冲突）
415 （unsupported media type）- 接受到的表示不受支持
500 （internal server error）- 通用错误响应
503 （Service Unavailable）- 服务当前无法处理请求

**DELETE**
不安全但幂等
删除资源
200 （OK）- 资源已被删除
301 （Moved Permanently）- 资源的URI已更改
303 （See Other）- 其他，如负载均衡
400 （bad request）- 指代坏请求
404 （not found）- 资源不存在
409 （conflict）- 通用冲突
500 （internal server error）- 通用错误响应
503 （Service Unavailable）- 服务端当前无法处理请求



## 为什么要使用Restful

RESTful架构与其他架构的区别
- SOAP WebService
- RESTful Webservice
- 效率和易用性
  - SOAP由于各种需求不断扩充本身协议的内容，导致在SOAP处理方面的性能有所下降。同时在易用性方面以及学习成本上也有所增加。
  - RESTful由于其面向资源接口设计以及操作抽象简化了开发者的不良设计,同时也最大限度的利用了Http最初的应用协议设计理念。
- 安全
  - RESTful对于资源型服务接口来说很合适,同时特别适合效率要求很高,但是对于安全要求不高的场景。
  - SOAP的成熟性可以给需要提供给多开发语言的, 对于安全性
要求较高的接口设计带来便利。
RESTful减少了传统请求的拆装箱操作，结构清晰。
