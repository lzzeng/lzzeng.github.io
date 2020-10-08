---
title: grep命令
date: 2020-10-01 16:30:00
tags:    
	- Shell
categories:
    - Shell

copyright: 
toc: true
---



## 提取匹配到的字符

```sh
[root@VM_0_13_centos demo]# cat phone.txt
987-123-4567
123 456 7890
(123) 456-7890
[root@VM_0_13_centos demo]# grep -o '\-[0-9]\{3\}' phone.txt
-123
-456
-789
[root@VM_0_13_centos demo]# grep -no '\-[0-9]\{3\}' phone.txt
1:-123
1:-456
3:-789
```

<!-- more -->



## help

```sh
/etc/nginx # grep -h
BusyBox v1.30.1 (2019-10-26 11:23:07 UTC) multi-call binary.

Usage: grep [-HhnlLoqvsriwFE] [-m N] [-A/B/C N] PATTERN/-e PATTERN.../-f FILE [FILE]...

Search for PATTERN in FILEs (or stdin)

	-H	Add 'filename:' prefix
	-h	Do not add 'filename:' prefix
	-n	Add 'line_no:' prefix
	-l	Show only names of files that match
	-L	Show only names of files that don't match
	-c	Show only count of matching lines
	-o	Show only the matching part of line
	-q	Quiet. Return 0 if PATTERN is found, 1 otherwise
	-v	Select non-matching lines
	-s	Suppress open and read errors
	-r	Recurse
	-i	Ignore case
	-w	Match whole words only
	-x	Match whole lines only
	-F	PATTERN is a literal (not regexp)
	-E	PATTERN is an extended regexp
	-m N	Match up to N times per file
	-A N	Print N lines of trailing context
	-B N	Print N lines of leading context
	-C N	Same as '-A N -B N'
	-e PTRN	Pattern to match
	-f FILE	Read pattern from file
```



## 若干常用参数

grep -F <your pattern> file

-F 可禁止pattern转义，使按原样匹配

-i 可忽略大小写，可以与 -F 一起用

-n 附带打印行号

-c 仅计数

-x 完整匹配模式（整行匹配）

-v 反向匹配（排除）

-r 递归查找当前目录及子目录下的文件

-o, --only-matching. Print only the matched (non-empty) parts of a matching line, with each such part on a separate output line.

-q 静默模式

  -q时虽然没有输出内容，但有返回状态值，可作为测试条件：

```
/etc/nginx # grep -Fq '30/Sep/2020:18:50:03' /var/log/nginx/myalert_access.log          # 输出为空
/etc/nginx # grep -Fq '30/Ssep/2020:18:50:03' /var/log/nginx/myalert_access.log         # 输出也为空
/etc/nginx # grep -Fq '30/Sep/2020:18:50:03' /var/log/nginx/myalert_access.log; echo $?
0
/etc/nginx # grep -Fq '30/Ssep/2020:18:50:03' /var/log/nginx/myalert_access.log; echo $?
1
/etc/nginx # if grep -Fq '30/Sep/2020:18:50:03' /var/log/nginx/myalert_access.log; then echo Y; else echo N; fi
Y
/etc/nginx # if grep -Fq '30/Ssep/2020:18:50:03' /var/log/nginx/myalert_access.log; then echo N; else echo N; fi
N
```



