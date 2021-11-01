---
title: Shell basic 02
date: 2020-11-01 16:30:00
tags:    
	- Shell
categories:
    - Shell
copyright:
toc: true
---





## 重定向

```
ls /opt/abc >/dev/null 2>&1  # /dev/null位桶, 2>& 须连着
ls /opt/abc &>/dev/null  # &> 须连着
echo "error: ..." 2>/var/log/err.log
ls /opt/abc >./a.log 2>&1
ls /opt/abc 1>./a.log 2>&1
```

<!-- more -->



## 扩展

```
# *扩展
[root@localhost t]# ls
1000-2.txt  1000.txt  xaa  xab  xac  xad

[root@localhost t]# ls *
1000-2.txt  1000.txt  xaa  xab  xac  xad
[root@localhost t]# echo *
1000-2.txt 1000.txt xaa xab xac xad
[root@localhost t]# echo "*"
*

[root@localhost t]# echo x*
xaa xab xac xad
[root@localhost t]# echo [[:digit:]]*
1000-2.txt 1000.txt
[root@localhost t]# echo [0-9]*
1000-2.txt 1000.txt
[root@localhost t]# echo [!x]*
1000-2.txt 1000.txt
```


```
# 路径扩展
[root@localhost zlz]# echo /opt/www/*/*.log
/opt/www/logs/access.log /opt/www/logs/error.log
```



```
# 波浪线扩展为家目录
[root@localhost zlz]# echo ~
/root
[root@localhost t]# echo ~zeng
/home/zeng
```



```
# 算术扩展 $
[root@localhost zlz]# echo $((2+2))
4

# 参数扩展
[root@localhost zlz]# echo $USER
root

# 命令替换
[root@localhost zlz]# ls -l $(which cat)
-rwxr-xr-x. 1 root root 54048 Nov 19  2015 /usr/bin/cat

# 反引号命令替换
[root@localhost zlz]# ls -l `which cat`
-rwxr-xr-x. 1 root root 54048 Nov 19  2015 /usr/bin/cat
```



以上算术扩展、参数扩展、命令替换都视作$表达式，相当于变量，非单引号包围可被解析，否则不解析：

```
[root@localhost zlz]# echo '$(which cat)'
$(which cat)
[root@localhost zlz]# echo '`which cat`'
`which cat`
[root@localhost zlz]# echo '$USER'
$USER
[root@localhost zlz]# echo '$((2+2))'
$((2+2))
```



```
# {}扩展
[root@kafka-1 ~]# echo {a..c}{0..2} |xargs -n 3
a0 a1 a2
b0 b1 b2
c0 c1 c2

[root@localhost zlz]# echo a{A{1,2},B{3,4}}b
aA1b aA2b aB3b aB4b
```



## 特殊权限

**setuid**

应用于可执行文件，会将有效用户ID（effective user ID）从真实用户（实际执行程序的用户）ID更改为程序属主的有效用户ID。

**setgid**

会将有效组ID（effective group ID）从真实用户的真实组ID（real group ID）更改为文件属主的有效组ID。

**sticky**

用于将可执行文件标记为“不可交换”。Linux会忽略文件上设置的粘滞位，如果对目录设置了粘滞位，则能够阻止用户删除或者重命名其中的文件，除非用户是该目录的属主，或者是文件的属主，又或者是超级用户。粘滞位常用来控制对共享目录（如/tmp）的访问。



## cp

cp不加选项参数复制时，访问时间、修改时间都会变，加上 `-p` 或 `--preserve` 可保持，但change时间（状态改变时间）是按最新的。状态改变时间通过chmod命令更改文件属性时也会更新。文件通过sed或vi修改保存，3个时间都更新为最新时间，通过echo追加内容时modify时间和change时间会更新为最新时间。

Linux中文件没有创建时间的概念。



## su & sudo

sudo不需要启动新的shell，也不需要加载其他用户的环境。这意味着sudo不需要引用命令。

sudo不需要输入root密码，如果通过visudo或直接编辑/etc/sudoers文件配置免密sudo，那么可以免密执行，否则输入sudo提权密码。而 `su -` 或 `su` 是真正切换到root用户环境，需要输入root密码。

sudo命令的-i选项可用于启动一个交互式的超级用户Shell会话（和 `su -` 差不多）。

```sh
su -c 'ls -l /root /*'
sudo ls -l /root /*
```



## cat

常用于显示短文本，也可以配合split用来连接多个文件。

split分割文件：

```sh
[root@localhost t]# seq 1000 > 1000.txt
[root@localhost t]# ll 1000.txt
-rw-r--r--. 1 root root 3893 Oct 31 06:44 1000.txt
[root@localhost t]# split -b 1KB 1000.txt
[root@localhost t]# ll
total 20
-rw-r--r--. 1 root root 3893 Oct 31 06:44 1000.txt
-rw-r--r--. 1 root root 1000 Oct 31 06:45 xaa
-rw-r--r--. 1 root root 1000 Oct 31 06:45 xab
-rw-r--r--. 1 root root 1000 Oct 31 06:45 xac
-rw-r--r--. 1 root root  893 Oct 31 06:45 xad
[root@localhost t]# 
[root@localhost t]# getconf PAGESIZE
4096
[root@localhost t]# ls -sl
total 20
4 -rw-r--r--. 1 root root 3893 Oct 31 06:44 1000.txt
4 -rw-r--r--. 1 root root 1000 Oct 31 06:45 xaa
4 -rw-r--r--. 1 root root 1000 Oct 31 06:45 xab
4 -rw-r--r--. 1 root root 1000 Oct 31 06:45 xac
4 -rw-r--r--. 1 root root  893 Oct 31 06:45 xad
```

顺便记一下，ls -l 第一行total表示总的占用空间（单位：KB）。一个block占4KB，一个文件至少占一个block。



cat连接文件：

```
[root@localhost t]# cat xa* > 1000-2.txt
[root@localhost t]# ll
total 24
-rw-r--r--. 1 root root 3893 Oct 31 06:56 1000-2.txt
-rw-r--r--. 1 root root 3893 Oct 31 06:44 1000.txt
-rw-r--r--. 1 root root 1000 Oct 31 06:45 xaa
-rw-r--r--. 1 root root 1000 Oct 31 06:45 xab
-rw-r--r--. 1 root root 1000 Oct 31 06:45 xac
-rw-r--r--. 1 root root  893 Oct 31 06:45 xad
[root@localhost t]# 
[root@localhost t]# diff 1000.txt 1000-2.txt 
[root@localhost t]#
```



在控制台不带参数cat，通过ctrl-D发送EOF结束输入：

```sh
[root@localhost zlz]# cat > test_cat.log
this is line1        
line2
[root@localhost zlz]# cat test_cat.log 
this is line1
line2
```



## tee

tee，管道T形转接头。

```sh
[root@localhost t]# ls
1000-2.txt  1000.txt  1.txt  xaa  xab  xac  xad
[root@localhost t]# ls |tee 1.txt |grep xa
xaa
xab
xac
xad
[root@localhost t]# cat 1.txt
1000-2.txt
1000.txt
1.txt
xaa
xab
xac
xad
```



## 共享目录

```
[zeng@localhost opt]$ groups
zeng
[zeng@localhost opt]$ umask
0002
[zeng@localhost opt]$ sudo groupadd share
[zeng@localhost opt]$ sudo usermod -a -G share zeng
[zeng@localhost opt]$ groups zeng
zeng : zeng share

# 添加其他用户到share组
$ sudo useradd -m -c "John Doo" -s /bin/bash -G share john

[zeng@localhost opt]$ sudo mkdir /opt/share
[zeng@localhost opt]$ ls -ld share
drwxr-xr-x. 2 root root 6 Oct 31 09:49 share

[zeng@localhost opt]$ sudo chown :share share
[zeng@localhost opt]$ ls -ld share
drwxr-xr-x. 2 root share 6 Oct 31 09:49 share

[zeng@localhost opt]$ sudo chmod g+sw share  # 或者chmod 2775
[zeng@localhost opt]$ ls -ld share
drwxrwsr-x. 2 root share 6 Oct 31 09:49 share

[zeng@localhost opt]$ 
[zeng@localhost opt]$ vi share/f01
[zeng@localhost opt]$ mkdir share/d01

# ！！centos下实测提示无权限，但上述步骤应该是正确的
```



## bash提示符

```sh
export PS1="[\u@\h \W]\\$ "
[ "$PS1" = "\\s-\\v\\\$ " ] && PS1="[\u@\h \W]\\$ "

# 说明：
\u：用户名
\h：短主机名
\W：当前目录
\s：Shell名称
\v：Shell版本号
```



## vi & vim

| 操作                                    | 按键          |
| :-------------------------------------- | ------------- |
| 当前字符前/后继续输入                   | i/a           |
| 当前行首/尾输入                         | I/A           |
| 删除当前字符                            | x             |
| 粘贴到当前行上/下一行                   | P/p           |
| 合并行                                  | J             |
| 后/前一个单词、后/前一个字符、下/上一行 | w/b、l/h、j/k |
| 前/后一个文件（的缓冲区）               | :bn/:bp       |
| 列出缓冲区文件                          | :buffers      |
| 切换到指定缓冲区n                       | :buffer n     |
| 删除以下10行（含当前行）                | :10dd，:d9+   |
| 删除以上10行（含当前行）                | :d9-          |
| 删除以下所有行                          | :dG           |
| 显示/关闭行号                           | :set nu!      |
|                                         |               |



## read命令

### 接参

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
[root@kafka-1 ~]# 
[root@kafka-1 ~]# ll |while read fa ft fu fg fz m d y fn; do echo "$fn: $fz"; done |tail -n +2
anaconda-ks.cfg: 2744
Desktop: 6
Documents: 6
Downloads: 6
Music: 6
Pictures: 6
Public: 6
Templates: 6
Videos: 6
```



### 输入密码

```sh
[root@kafka-1 ~]# read -sp "password: " a
password: [root@kafka-1 ~]# echo $a
abc123
```



### 指定IFS

本命令执行期间新IFS有效：

```sh
[root@kafka-1 ~]# IFS=. read a b c
a.b.c
[root@kafka-1 ~]# echo $a
a
[root@kafka-1 ~]# echo $b
b
[root@kafka-1 ~]# echo $c
c

# 继续执行
[root@kafka-1 ~]# read a b c
a.b.c
[root@kafka-1 ~]# echo $a
a.b.c
[root@kafka-1 ~]# echo $b

[root@kafka-1 ~]# echo $c

```



本shell内新IFS有效（注意分号）：

```sh
[root@kafka-1 ~]# IFS=.; read a b c
a.b.c
[root@kafka-1 ~]# echo $c
c
[root@kafka-1 ~]# read a b c
x.y.z
[root@kafka-1 ~]# echo $c
```



但是 `while read` 或 `for in` 循环中需加分号：

```sh
[root@kafka-1 ~]# IFS=. while read a b c; do echo "$a,$b,$c"; done
-bash: syntax error near unexpected token `do'

[root@kafka-1 ~]# IFS=. for i in a.b.c; do echo "$i ..."; done
-bash: syntax error near unexpected token `do'
[root@kafka-1 ~]# IFS=.; for i in a.b.c; do echo "$i ..."; done
a.b.c ...

[root@kafka-1 ~]# IFS=$'\n' for i in `ll`; do echo "$i"; done
-bash: syntax error near unexpected token `do'
[root@kafka-1 ~]# IFS=$'\n'; for i in `ll`; do echo "$i"; done
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
```



## 软件包管理

打包工具：

| Linux发行版 | 低层工具 | 高层工具 |
| ----------- | -------- | -------- |
| redhat      | rpm      | yum      |
| debian      | dpkg     | apt-get  |



命令：

```sh
# 列出软件包
rpm -qa
dpkg -l

# 软件包是否已安装
rpm -q vim  # redhat
dpkg -s vim  # debian

# 反查软件包
rpm -qf /usr/bin/vim
dpkg -S /usr/bin/vim
```

