---
title: awk命令
date: 2020-10-01 16:30:00
tags:    
	- Shell
categories:
    - Shell
copyright: 
toc: true
---



```sh
awk '{c[$1]++;}END{for(k in c){print k": "c[k];}}' /var/log/nginx/myalert_access.log
113.118.106.137: 17
113.116.28.35: 4171
```

<!-- more -->



## 统计ip访问次数



### 示例1

myalert_access日志格式如下：

```sh
116.7.8.112 - - [14/Jun/2020:18:08:06 +0000] "GET / HTTP/1.1" 302 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36" "-"
```



统计：

```sh
awk '{c[$1]++;}END{for(k in c){print k": "c[k];}}' /var/log/nginx/myalert_access.log
113.118.106.137: 17
113.116.28.35: 4171
112.97.49.195: 20
116.7.8.112: 440
```



### 示例2

日志：
```sh
Nov 25 13:33:03 VM_0_13_centos sshd[9327]: Invalid user ftp_user from 1.213.195.154 port 37113
```

统计：
```sh
[root@VM_0_13_centos ~]# awk '{a[$1]+=1;}END{for(i in a){print a[i]" "i;}}' /var/log/secure
1532 Sep
12542 Nov
3895 Oct
107725 Aug
```
