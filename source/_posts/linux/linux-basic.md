---
title: Linux basic 01 —— 读书笔记
date: 2020-10-02 16:30:00
tags:    
    - Linux
    - CentOS
categories:
    - Linux
copyright: false
toc: true
---





> 《鸟哥的私房菜》在线书籍 <http://linux.vbird.org/linux_basic> 的笔记




磁盘的第一个扇区主要记录了两个重要信息，分别是：
- 主要启动记录区(Master Boot Record, MBR)：可以安装开机管理程序的地方，有446 bytes
- 分区表(partition table)：记录整颗硬盘分区的状态，有64 bytes

<!-- more -->



## 磁盘分区

在分区表所在的64 bytes容量中，总共分为四组记录区，每组记录区记录了该区段的起始到结束磁柱的号码。

P(primary)+E(extended)最多叧能有四个，其中E最多叧能有一个。

题：假如我的PC有两颗SATA硬盘，我想在第事颗硬盘分割出6个可用的分割槽(可以被格式化)， 那每个分割槽在Linux系统下的装置文件名为何？分割类型各为何？至少写出两种不同的分割方案。

```text
PPP+E方案:
/dev/sdb1, /dev/sdb2, /dev/sdb3, /dev/sdb5, /dev/sdb6, /dev/sdb7这六个，至于/dev/sdb4这个延伸分割本身仅是提供来给逡辑分割槽建立乀用。

P+E方案:
/dev/sdb1, /dev/sdb5, /dev/sdb6, /dev/sdb7, /dev/sdb8, /dev/sdb9
```



简单地说，整个开机流程到操作系统之前的动作应该是这样：
- BIOS：开机自动执行的韧体，会识别第一个可开机的装置；
- MBR：第一个可开机装置的第一个分区内的主要启动记录区块，内含开机管理程序；
- 开机管理程序(boot loader)：一个可读取核心文件来执行的软件；
- 核心档案（文件）：开始操作系统的功能...


Linux内的所有资料都是以档案的形态来呈现的，所以啰，整个Linux系统最重要的地方就是在于目录树架构

无论如何，底下还是说明一下基本硬碟分割的模式吧！

最简单的分割方法：
这个在上面第二节已经谈过了，就是仅分割出根目录与记忆体置换空间( / & swap )即可。然后再预留一些剩余的磁碟以供后续的练习之用。不过，这当然是不保险的分割方法(所以鸟哥常常说这是『懒人分割法』)！因为如果任何一个小细节坏掉(例如坏轨的产生)，你的根目录将可能整个的损毁～挽救方面较困难！

稍微麻烦一点的方式：
较麻烦一点的分割方式就是先分析这部主机的未来用途，然后根据用途去分析需要较大容量的目录，以及读写较为频繁的目录，将这些重要的目录分别独立出来而不与根目录放在一起，那当这些读写较频繁的磁碟分割槽有问题时，至少不会影响到根目录的系统资料，那挽救方面就比较容易啊！在预设的CentOS环境中，底下的目录是比较符合容量大且(或)读写频繁的目录：
/boot
/
/home
/var
Swap



由二BIOS捉到的磁盘容量丌对，但是至少在整颗磁盘前面的扂区他还读得到啊！ 因此，你叧要将这个磁盘最前面的容量分割出一个小分割槽，幵将这个分割槽不系统启劢文件的放置目录摆在一起， 那就是 /boot 这个目录！就能够解决了！很简单吧！ 其实，重点是：『将启劢扂区所在分割槽规范在小二1024个磁柱以内～』 即可！那怎举做到呢？很简单，在进行安装的时候，规划出三个分区，分别是：
/boot
/
swap



那个/boot只要给100MB左右即可，而且/boot要放在整块硬盘的最前面。在Linux里面，任何一个文件都具有User,Group,Others三种身份的个别权限：

drwxr-xr-- 1 test1 testgroup 5238 Jun 19 10:25 groups/

第一个字元代表这个档案是『目录、档案或连结档等等』：
- 当为[ d ]则是目录，例如上表档名为『.config』的那一行；
- 当为[ - ]则是档案，例如上表档名为『initial-setup-ks.cfg』那一行；
- 若是[ l ]则表示为连结档(link file)；
- 若是[ b ]则表示为装置档里面的可供储存的周边设备(可随机存取装置)；
- 若是[ c ]则表示为装置档里面的序列埠设备，例如键盘、滑鼠(一次性读取装置)。



接下来的字元中，以三个为一组，且均为『rwx』的三个参数的组合。
u: user 即 owner
g: group
o: others  !! 不是owner


目录的x代表的是使用者能否进入该目录成为工作目录的用途！

除了基本r, w, x权限外，在Linux传统的Ext2/Ext3/Ext4档案系统下，我们还可以设定其他的系统隐藏属性，这部份可使用chattr来设定，而以lsattr 来查看，最重要的属性就是可以设定其不可修改的特性！让连档案的拥有者都不能进行修改！这个属性可是相当重要的，尤其是在安全机制上面(security)！


CentOS 7.x 下：

```sh
[root@VM_0_13_centos linux-learning]# ls -ld /bin; ls -ld /sbin; ls -ld /lib; ls -ld /lib64; ls -ld /var/lock; ls -ld /var/run;
lrwxrwxrwx. 1 root root 7 Mar  7  2019 /bin -> usr/bin
lrwxrwxrwx. 1 root root 8 Mar  7  2019 /sbin -> usr/sbin
lrwxrwxrwx. 1 root root 7 Mar  7  2019 /lib -> usr/lib
lrwxrwxrwx. 1 root root 9 Mar  7  2019 /lib64 -> usr/lib64
lrwxrwxrwx. 1 root root 11 Mar  7  2019 /var/lock -> ../run/lock
lrwxrwxrwx. 1 root root 6 Mar  7  2019 /var/run -> ../run
```



目录规范：<http://linux.vbird.org/linux_basic/0210filepermission.php>

**/proc**目录：这个目录本身是一个『虚拟档案系统(virtual filesystem)』喔！他放置的资料都是在记忆体当中，例如系统核心、行程资讯(process)、周边装置的状态及网路状态等等。因为这个目录下的资料都是在记忆体当中，所以本身不占任何硬碟空间啊！比较重要的档案例如：/proc/cpuinfo, /proc/dma, /proc/interrupts, /proc/ioports, /proc/net/*等等。



## 查看版本

### uname

```sh
[root@VM_0_13_centos linux-learning]# uname -a
Linux VM_0_13_centos 3.10.0-957.el7.x86_64 #1 SMP Thu Nov 8 23:39:32 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
[root@VM_0_13_centos linux-learning]# uname -s
Linux
[root@VM_0_13_centos linux-learning]# uname -n
VM_0_13_centos
[root@VM_0_13_centos linux-learning]# uname -r
3.10.0-957.el7.x86_64
[root@VM_0_13_centos linux-learning]# uname -m
x86_64
[root@VM_0_13_centos linux-learning]# uname -p
x86_64
[root@VM_0_13_centos linux-learning]# uname -i
x86_64
[root@VM_0_13_centos linux-learning]# uname -o
GNU/Linux

[root@VM_0_13_centos linux-learning]# cat /etc/issue
\S
Kernel \r on an \m

[root@VM_0_13_centos linux-learning]# cat /etc/redhat-release 
CentOS Linux release 7.6.1810 (Core)

[root@VM_0_13_centos linux-learning]# cat /etc/centos-release
CentOS Linux release 7.6.1810 (Core)
```



## 命令

### lsblk

> list block devices



```sh
[root@VM_0_13_centos linux-learning]# lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0     11:0    1  4.4M  0 rom  
vda    253:0    0   50G  0 disk 
└─vda1 253:1    0   50G  0 part /
```



### vmstat

> vmstat reports information about processes, memory, paging, block IO, traps, disks and cpu activity.



```sh
[root@VM_0_13_centos linux-learning]# vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 159888 137604 869576    0    0    11    18    0    0  5  3 92  0  0
```



### ls


ls -Al  与 ls -al 的区别，不包含 . 和 ..

ls -n       # 不需要l

-n ：列出UID与GID而非使用者与群组的名称

```sh
[root@localhost sh]# ls -n
total 4
-rw-r--r--. 1 0 0 309 Nov  1 10:33 fixed-ts.sh

[root@VM_0_13_centos linux-learning]# ls -lS a    # 按大小降序
total 8
-rw-r--r-- 1 root root 4 Oct  4 01:54 b1
-rw-r--r-- 1 root root 3 Oct  4 01:53 b2
-rw-rwxr-x 1 root root 0 Oct  4 01:02 b
[root@VM_0_13_centos linux-learning]# ls -lt a    # 按时间降序 新->旧
total 8
-rw-r--r-- 1 root root 4 Oct  4 01:54 b1
-rw-r--r-- 1 root root 3 Oct  4 01:53 b2
-rw-rwxr-x 1 root root 0 Oct  4 01:02 b
[root@VM_0_13_centos linux-learning]# ls -l a     # 按名称升序
total 8
-rw-rwxr-x 1 root root 0 Oct  4 01:02 b
-rw-r--r-- 1 root root 4 Oct  4 01:54 b1
-rw-r--r-- 1 root root 3 Oct  4 01:53 b2

[root@VM_0_13_centos linux-learning]# ls -Rl a    # R 子目录也ls
a:
total 8
-rw-rwxr-x 1 root root 0 Oct  4 01:02 b
-rw-r--r-- 1 root root 4 Oct  4 01:54 b1
-rw-r--r-- 1 root root 3 Oct  4 01:53 b2

# -F ：根据档案、目录等资讯，给予附加资料结构，例如：
#       *:代表可执行档； /:代表目录； =:代表socket 档案； |:代表FIFO 档案；
[root@VM_0_13_centos linux-learning]# ls -FR .
.:
a/  c

./a:
b*  b1  b2

# -f ：直接列出结果，而不进行排序(ls 预设会以档名排序！)
[root@VM_0_13_centos linux-learning]# ls -f a/
b1  .  ..  b  b2
[root@VM_0_13_centos linux-learning]# ls a/
b  b1  b2
```



### cat 与 tac

tac 可实现按行逆序输出

```sh
[root@VM_0_13_centos linux-learning]# seq 3 |tac
3
2
1
[root@VM_0_13_centos linux-learning]# seq 3 |cat
1
2
3
[root@VM_0_13_centos linux-learning]# seq 3
1
2
3
```



### touch

即使我们复制一个档案时，复制所有的属性，但也没有办法复制ctime 这个属性的。ctime 可以记录这个档案最近的状态(status) 被改变的时间



### umask

如果umask为022，则：
建立文件时：(-rw-rw-rw-) - (-----w--w-) ==> -rw-r--r--        		# 即644
建立目录时：(drwxrwxrwx) - (d----w--w-) ==> drwxr-xr-x        # 即755

在预设的情况中， root的umask会拿掉比较多的属性，root的umask预设是022 ，这是基于安全的考量啦～至于一般身份使用者，通常他们的umask为002 ，亦即保留同群组的写入权力！



### 其它文件管理命令

ref: <http://linux.vbird.org/linux_basic/0220filemanager.php#dir_path>



### 文件特殊权限： SUID, SGID, SBIT

...



## 端口

### 列出所有监听的端口

```sh
netstat -tnlp |awk '{print $4}' |awk -F: '{if($NF~/^[0-9]*$/) print $NF}' |sort |uniq 2>/dev/null
```



## 防火墙

ref: <https://www.linuxprobe.com/chapter-08.html#83_Firewalld>



对指定IP开放指定端口


```sh
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.142.166" port protocol="tcp" port="6379" accept"
firewall-cmd --reload
```



添加、删除2201

```sh
firewall-cmd --zone=public --add-port=2201/tcp --permanent
firewall-cmd --zone=public --remove-port=2201/tcp --permanent
firewall-cmd --reload
```

`--zone=public`：拒绝流入的流量，除非与流出的流量相关；而如果流量与ssh、dhcpv6-client服务相关，则允许流量。



指定网段192.168.10.0/24 INPUT，拒绝其它网段INPUT:

```sh
iptables -I INPUT -s 192.168.10.0/24 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j REJECT
```

允许规则要放在拒绝规则前面，否则被拒绝。



把INPUT规则链的默认策略设置为拒绝：

```sh
iptables -P INPUT DROP
# iptables -L
```

规则链的默认策略拒绝动作只能是DROP，而不能是REJECT。

DROP直接将流量丢弃而且不响应；REJECT则会在拒绝流量后回复一条信息，从而让流量发送方清晰地看到数据被拒绝的响应信息。



向INPUT链中添加允许ICMP流量进入的策略规则:

```sh
iptables -I INPUT -p icmp -j ACCEPT
```



## 网络存储

### NFS

```sh
# yum install nfs-utils -y

服务端：
/nfs 172.17.0.13(rw,no_root_squash,async)


客户端：
mount -t nfs   root@172.17.0.13:/nfs   /mnt
```



## Vim

```sh
# vim 操作：
:g/^#/d     # 删除所有#开头的行
:g/^$/d     # 删除所有空行
...
```
