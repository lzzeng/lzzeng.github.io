---
title: 《深入浅出MySQL》学习笔记
date: 2020-11-25 22:55:40
tags:
    - MySQL
categories:
    - DevOps
copyright: false
toc: true
---



## 权限

分配select,insert权限

```mysql
grant select,insert on sakila.* to 'z1'@'localhost' identified by '123';
```

<!-- more -->

收回insert权限

```mysql
revoke insert on sakila.* from 'z1'@'localhost';
```



## 查看帮助

查看帮助信息

可以用`? contents`命令来显示所有可供查询的分类

查看show关键字用法：`? show`

查看create table用法：`? create table`

---
MySQL 5.0之后，提供了一个新的数据库information_schema，用来记录MySQL中的元数据信息。

通过查询元数据 来获取批量操作表的SQL语句：

```mysql
select concat('drop table test1.',table_name,';') from tables where table_schema='test1' and table_name like 'tmp%';
```



## 数值类型

MySQL 支持所有标准 SQL 中的数值类型，其中包括严格数值类型（ INTEGER、SMALLINT、DECIMAL和NUMERIC），以及近似数值数据类型（FLOAT、REAL和DOUBLE PRECISION），并在此基础上做了扩展。扩展后增加了TINYINT、MEDIUMINT和BIGINT这3种长度不同的整型，并增加了BIT类型，用来存放位数据。

**浮点数、定点数**

精度和标度 计数法 (M,D)

float(5,2)、double(5,2)、decimal(5,2)

不指定M,D的话

默认：float, double, decimal(10,0)

如果不写精度和标度，则会按照实际精度值显示，如果有精度和标度，则会自动将四舍五入后的结果插入，系统不会报错；定点数如果不写精度和标度，则按照默认值decimal(10,0)来进行操作，并且如果数据超越了精度和标度值，系统则会报错。

    Query OK, 1 row affected, 1 warning (0.00 sec)
    mysql> show warnings;



**BIT 类型**

```mysql
select bin(id),hex(id) from t2;

alter table t2 modify id bit(2);

insert into t2 values(2);
```

转换后的二进制数不能超过预定义的bit类型的长度



## 日期时间类型

**timestamp类型**

MySQL只给表中的第一个TIMESTAMP字段设置默认值为系统日期，如果有第二个TIMESTAMP类型，则默认值设置为0值

```mysql
show create table t \G;

mysql> alter table t modify id2 timestamp default current_timestamp;
ERROR 1293 (HY000): Incorrect table definition; there can be only one TIMESTAMP column with CURRENT_TIMESTAMP in DEFAULT or ON UPDATE clause
```

timestamp和时区有关系：

    mysql> show variables like 'time_zone';
    +---------------+--------+
    | Variable_name | Value |
    +---------------+--------+
    | time_zone | SYSTEM |
    +---------------+--------+

最大2038-01-19 11:14:07  +08:00时区

最小1970-01-01 08:00:01

TIMESTAMP支持的时间范围较小，其取值范围从19700101080001到2038年的某个时间，而DATETIME是从 1000-01-01 00:00:00到 9999-12-31 23:59:59，范围更大。



## 字符型

MySQL包括了CHAR、VARCHAR、BINARY、VARBINARY、BLOB、TEXT、ENUM和SET等多种字符串类型。



### binary 类型

    CREATE TABLE t (c BINARY(3));

当保存BINARY值时，在值的最后通过填充“0x00”（零字节）以达到指定的字段定义长度。



### 枚举类型 enum

```mysql
mysql> create table t2 (gender enum('M', 'F'));
Query OK, 0 rows affected (0.03 sec)

mysql> desc t2;
+--------+---------------+------+-----+---------+-------+
| Field  | Type          | Null | Key | Default | Extra |
+--------+---------------+------+-----+---------+-------+
| gender | enum('M','F') | YES  |     | NULL    |       |
+--------+---------------+------+-----+---------+-------+
1 row in set (0.00 sec)

mysql> insert into t2 values('M'),('1'),(2),('f'),(null);
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> select * from t2;
+--------+
| gender |
+--------+
| M      |
| M      |
| F      |
| F      |
| NULL   |
+--------+
5 rows in set (0.00 sec)
```



### set 类型

    Create table t (col set('a','b','c','d'));
    insert into t values('a,b'),('a,d,a'),('a,b'),('a,c'),('a');
    
    1～8成员的集合，占1个字节。??????
    9～16成员的集合，占2个字节。
    17～24成员的集合，占3个字节。
    25～32成员的集合，占4个字节。
    33～64成员的集合，占8个字节。


