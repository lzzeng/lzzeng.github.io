---
title: Django笔记
date: 2020-07-29 22:55:40
tags:
    - Python
categories:
    - Python
copyright: false
toc: true
---



## django1.11 和django2.2的版本比较

Django2.*版本和Django1.*版本相比，虽然有很多细小地方的改动，但就其平常和开发者使用比较密切相关的地方来说，主要有如下三个方面：

- url配置方式(主要差异)
- 数据库操作
- 用户认证操作

<!-- more -->



### url配置方式

-  Django1.*中配置url地址使用的是：`url函数`，而Django2.*中配置url地址使用的是：`path函数`
- Django1.*从url地址中提取参数是使用正则表达式来来提取，格式为：`(?P<参数名>正则表达式)`
- Django2.*从url地址中提取参数是使用路由转换器来提取，格式为：`<路由转换器:参数名>`

Django2.*对于提取参数的限制并不如Django1.*的正则方式控制的灵活和严格

可以到django.urls.converters模块中进行查看，比如int路由转换器对应的源码



自定义路由转换器分为两步：

① 自定义路由转换器类，在转换器类中，需要通过regex类属性指明提取参数所对应的正则表达式

② 调用register_converter方法注册自定义的路由转换器，注册之后才能进行使用



2.2中的`re_path`其实就相当于Django1.*中的`url`函数



### 数据库设置



mysql数据库默认的事务隔离级别为：repeatable read(可重复读)

Django2.*会把mysql数据库事务的隔离级别默认设置为：read committed(读取已提交)



ForeignKey和OneToOneField关系中的on_delete参数



### 其它

**is_authenticated和is_anonymous的使用**

在Django框架中，我们可以通过`request.user`获取请求的用户对象，然后通过`request.user.is_authenticated`判断该用户是否是认证用户，或通过`request.user.is_anonymous`判断该用户是否是匿名用户，`is_authenticated`和`is_anonymous`在Django1.*中可以当做方法一样使用，但是在Django2.*中只能当做属性来用



来源：”一文弄懂Django1.*和Django2.*的差异“

---



**版本匹配**
Django 1.11 requires Python 2.7, 3.4, 3.5, 3.6, or 3.7 (as of 1.11.17). 
Django 2.0 supports Python 3.4, 3.5, 3.6, and 3.7. 
Django 2.2 supports Python 3.5, 3.6, 3.7, and 3.8 (as of 2.2.8).
Django 3.1 supports Python 3.6, 3.7, and 3.8. 

https://www.djangoproject.com/download/
https://docs.djangoproject.com/en/3.1/releases/



---



**ORM**

ORM将python代码转换成SQL语句，pymysql等数据库连接库将SQL语句发送给数据库，并返回结果。

优点：

- 面向对象的方式操作数据，提升了效率

- 使python代码与数据库无关

缺点：
- 会牺牲代码执行效率

- 长期使用ORM，会降低编写SQL语句能力



**MVC**

MVC 模式（Model–view–controller）是软件工程中的一种软件架构模式，把软件系统分为三个基本部分：模型（Model）、视图（View）和控制器（Controller）

体现了模块化、分层设计思想：
M —— 数据层、持久层
V —— 视图层、表示层
C —— 控制层、逻辑层

与**MTV**模型的区别，主要在于**MVC**中的C包含了URL路由的功能。

以springMVC框架为例说明：

1、用户发送请求至前端控制器DispatcherServlet。

2、DispatcherServlet收到请求调用HandlerMapping处理器映射器。

3、处理器映射器找到具体的处理器(可以根据xml配置、注解进行查找)，生成处理器对象及处理器拦截器(如果有则生成)一并返回给DispatcherServlet。

4、DispatcherServlet调用HandlerAdapter处理器适配器。

5、HandlerAdapter经过适配调用具体的处理器(Controller，也叫后端控制器)。

6、Controller执行完成返回ModelAndView。

7、HandlerAdapter将controller执行结果ModelAndView返回给DispatcherServlet。

8、DispatcherServlet将ModelAndView传给ViewResolver视图解析器。

9、ViewResolver解析后返回具体View。

10、DispatcherServlet根据View进行渲染视图（即将模型数据填充至视图中）。

11、DispatcherServlet响应用户。


其中，4+5通过HandlerAdapter执行处理器是**适配器模式**。



**SpringMVC工作原理**

第一步:用户发起请求到前端控制器（DispatcherServlet）

第二步：前端控制器请求处理器映射器（HandlerMappering）去查找处理器（Handle）：通过xml配置或者注解进行查找

第三步：找到以后处理器映射器（HandlerMappering）像前端控制器返回执行链（HandlerExecutionChain）

第四步：前端控制器（DispatcherServlet）调用处理器适配器（HandlerAdapter）去执行处理器（Handler）

第五步：处理器适配器去执行Handler

第六步：Handler执行完给处理器适配器返回ModelAndView

第七步：处理器适配器向前端控制器返回ModelAndView

第八步：前端控制器请求视图解析器（ViewResolver）去进行视图解析

第九步：视图解析器像前端控制器返回View

第十步：前端控制器对视图进行渲染

第十一步：前端控制器向用户响应结果


