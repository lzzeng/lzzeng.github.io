---
title: Shell basic 01
date: 2020-10-01 16:30:00
tags:    
	- Shell
categories:
    - Shell

copyright: 
toc: true
---



| 参数处理 | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| $#       | 传递到脚本的参数个数                                         |
| $*       | 以一个单字符串显示所有向脚本传递的参数。 如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。 |
| $$       | 脚本运行的当前进程ID号                                       |
| $!       | 后台运行的最后一个进程的ID号                                 |
| $@       | 与$*相同，但是使用时加引号，并在引号中返回每个参数。 如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。 |
| $-       | 显示Shell使用的当前选项，与set命令功能相同。                 |
| $?       | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。 |

<!-- more -->




## 条件判断

```sh
-a file exists.
-b file exists and is a block special file.
-c file exists and is a character special file.
-d file exists and is a directory.
-e file exists (just the same as -a).
-f file exists and is a regular file.
-g file exists and has its setgid(2) bit set.
-G file exists and has the same group ID as this process.
-k file exists and has its sticky bit set.
-L file exists and is a symbolic link.
-n string length is not zero.
-o Named option is set on.
-O file exists and is owned by the user ID of this process.
-p file exists and is a first in, first out (FIFO) special file or named pipe.
-r file exists and is readable by the current process.
-s file exists and has a size greater than zero.
-S file exists and is a socket.
-t file descriptor number fildes is open and associated with a terminal device.
-u file exists and has its setuid(2) bit set.
-w file exists and is writable by the current process.
-x file exists and is executable by the current process.
-z string length is zero.
```



## 字符串截取

```sh
a=abc123abc123

${a:-2:12} abc123abc123
${a:-2:6} abc123abc123
${a:0-2:12} 23
${a:0-2} 23
${a:0-2:}
${a::-2} abc123abc1
${a:0:-2} abc123abc1
${a::0-2} abc123abc1

${a#a} bc123abc123
${a##a} bc123abc123
${a#*a} bc123abc123
${a##*a} bc123

${a%3} abc123abc12
${a%%3} abc123abc12
${a%3*} abc123abc12
${a%%3*} abc12
```



## 选项参数

getopts 和 getopt 的用法

ref: 
- <https://www.cnblogs.com/FrankTan/archive/2010/03/01/1634516.html>
- <https://www.cnblogs.com/tommyjiang/p/10629848.html>

```sh
# -al 
GETOPT_ARGS=`getopt -o s:e:n::c: -al sdate:,edate:,numprocs::,cfile: -- "$@"`

#echo "$GETOPT_ARGS"
eval set -- "$GETOPT_ARGS"

while [ -n "$1" ]
do
    case "$1" in
        -s|--sdate) sdate=$2; shift 2;;
        -e|--edate) edate=$2; shift 2;;
        -n|--numprocs) numprocs=$2; shift 2;;
        -c|--cfile) cfile=$2; shift 2;;
        --) break ;;
        *) echo $1,$2,$show_usage; break ;;
    esac
done
```



## shell 求差集 并集 交集

ref: <https://blog.csdn.net/nwpulei/article/details/38556595>

```sh
[root@VM_0_13_centos shell-basic]# cat a
1
2
3
5
3
4
[root@VM_0_13_centos shell-basic]# cat b
4
6
5
8
[root@VM_0_13_centos shell-basic]# ua=$(cat a |sort |uniq)      # a 不重复集
[root@VM_0_13_centos shell-basic]# echo $ua
1 2 3 4 5
[root@VM_0_13_centos shell-basic]# ub=$(cat b |sort |uniq)      # b 不重复集
[root@VM_0_13_centos shell-basic]# echo $ub
4 5 6 8
[root@VM_0_13_centos shell-basic]# uaub=$(echo -e "$ua\n$ub" |sort |uniq -u)      # a和b的差集
[root@VM_0_13_centos shell-basic]# echo $uaub
1 2 3 6 8

[root@VM_0_13_centos shell-basic]# uab=$(echo -e "$ua\n$ub\n$ub" |sort |uniq -u)  # b相对a的补集
[root@VM_0_13_centos shell-basic]# echo $uab
1 2 3
[root@VM_0_13_centos shell-basic]# uba=$(echo -e "$ua\n$ua\n$ub" |sort |uniq -u)  # a相对b的补集
[root@VM_0_13_centos shell-basic]# echo $uba
6 8

[root@VM_0_13_centos shell-basic]# cat a b |sort |uniq                             # 并集
[root@VM_0_13_centos shell-basic]# a_b=$(echo -e "$ua\n$ub" |sort |uniq)           # 并集2
[root@VM_0_13_centos shell-basic]# echo $a_b
1 2 3 4 5 6 8
[root@VM_0_13_centos shell-basic]# ab=$(echo -e "$ua\n$ub" |sort |uniq -d)        # 交集
[root@VM_0_13_centos shell-basic]# echo $ab
4 5
```
