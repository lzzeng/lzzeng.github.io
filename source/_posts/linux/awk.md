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



## 统计IP访问次数



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



## 关联查询

从 `ll` 命令的结果筛选出Documents  Downloads Pictures的行：

```sh
[root@kafka-1 ~]# ll
total 4
-rw-------. 1 root root 2744 Feb 15  2020 anaconda-ks.cfg
drwxr-xr-x. 2 root root    6 Feb 15  2020 Desktop
drwxr-xr-x. 2 root root    6 Feb 15  2020 Documents
drwxr-xr-x. 2 root root    6 Feb 15  2020 Downloads
drwxr-xr-x. 2 root root    6 Feb 15  2020 Music
drwxr-xr-x. 2 root root    6 Feb 15  2020 Pictures
drwxr-xr-x. 2 root root    6 Feb 15  2020 Public
drwxr-xr-x. 2 root root    6 Feb 15  2020 Templates
drwxr-xr-x. 2 root root    6 Feb 15  2020 Videos

[root@kafka-1 ~]# echo Documents Downloads Pictures |tr ' ' '\n' |awk -v vline="`ll |sed 's/^/echo /'`" 'BEGIN{while(vline |getline) txt[$NF]=$0;} {print txt[$0];}'
drwxr-xr-x. 2 root root 6 Feb 15 2020 Documents
drwxr-xr-x. 2 root root 6 Feb 15 2020 Downloads
drwxr-xr-x. 2 root root 6 Feb 15 2020 Pictures
```



从文件 `score` 中查找a c e的记录：

```sh
[root@localhost code]# cat score
a 90
b 99
c 95
d 88
e 80
f 89
g 94
[root@localhost code]# echo a c e |tr ' ' '\n' |awk 'BEGIN{while(getline < "./score") txt[$1]=$0 } {print txt[$1];}'
a 90
c 95
e 80
```



## 列出已挂载的磁盘

```sh
[root@kafka-1 ~]# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   20G  0 disk 
├─sda1   8:1    0  300M  0 part /boot
├─sda2   8:2    0    2G  0 part [SWAP]
└─sda3   8:3    0 17.7G  0 part /
sr0     11:0    1 1024M  0 rom  
[root@kafka-1 ~]# 
[root@kafka-1 ~]# lsblk |awk '{if($6=="disk") d=$1; if(substr($7,1,1)=="/") print d;}' |sort -u
sda
```

