---
title: sed命令
date: 2020-10-01 16:30:00
tags:    
	- Shell
categories:
    - Shell

copyright: true
toc: true
---



## 替换中文

```sh
sed 's/[^ -z]/*/g'
```



## 按行逆序输出

```sh
sed -e '1!G; h; $!d'
```

<!-- more -->

示例：

```sh
[root@VM_0_13_centos ~]# seq 4 |sed -e '1!G; h; $!d'
4
3
2
1

# 更简单的命令  tac
[root@VM_0_13_centos linux-learning]# seq 3 |tac
3
2
1
```



`1!G;h;$!d` 可拆解为三个命令:

- 1!G —— 只有第一行不执行G命令，将hold space中的内容append回到pattern space
- h —— 第一行都执行h命令，将pattern space中的内容拷贝到hold space中
- $!d —— 除了最后一行不执行d命令，其它行都执行d命令，删除当前行

*摘自:  <https://blog.csdn.net/weixin_38149264/article/details/78074300>*



## 对符合条件的行操作

```sh
[root@VM_0_13_centos opt]# find /opt -type f -name "*.tgz"
/opt/note/K8s/yaml/elk/elk2020/e/helm/elasticsearch-7.6.0.tgz
[root@VM_0_13_centos opt]# find /opt -type f -name "*.tgz" | sed -n -e '/^\/opt\/note\//{s?/opt/note/?Note:?; p};'		# 暂未找到替代/的方法
Note:K8s/yaml/elk/elk2020/e/helm/elasticsearch-7.6.0.tgz
```



## 变量含sed分割符

```sh
#!/bin/sh

###################
# sed替换目标字符为变量内容时，如果
# 变量内容中含有sed分隔符，需要处理
###################

s="The remote SSH server rejected X11 forwarding request."

assert(){
  if [ "$1" = "$2" ]; then
    echo "ok"
    return 0
  else
    echo "[$1] is not equal to [$2]"
    return 1
  fi
}

w="accepted"
echo "$s" |sed "s/rejected/$w/g"

w="@ccepted"
echo "$s" |sed "s/rejected/$w/g"

#w="accept/ed"
#echo "$s" |sed "s/rejected/$w/g"    # sed: -e expression #1, char 20: unknown option to `s'

echo "--------------1"
w0="a#cc/ept/ed"
w=$(echo "$w0" |sed 's#/#\\/#g')     # 替换为变量的内容时，需先对变量处理，将其中包含的sed分隔符替换成\开头的
echo "$w"
assert "`echo "$s" |sed "s/rejected/$w/g"`"  "The remote SSH server $w0 X11 forwarding request."
echo $?
```



## 手机号匹配

```sh
#!/bin/sh

###################
# sed 匹配手机号示例
###################

phone="my phone is 86+15612348888. his phone is 13912348889. haha!"
echo ">>: $phone"

echo "$phone" |sed 's/1(3[0-9]|5[1689]|8[6789])[0-9]{8}/xxx/'          # err

echo "$phone" |sed 's/\(^\|[^0-9]\)\([0-9]\{3,4\}-\)\?1\(3[0-9]\|5[1689]\|8[6789]\)[0-9]\{8\}/\1***/g'
# 分三段提取 \2\3\4
echo "$phone" |sed 's/\(^\|[^0-9]\)\([0-9]\{2,4\}[+-]\?\)\?\(13[0-9]\|15[1689]\|18[6789]\)\([0-9]\{8\}\)/\1[\2\3\4]/g'
echo "$phone" |sed 's/\(^\|[^0-9]\)\([0-9]\{2,4\}[+-]\?\)\?\(13[0-9]\|15[1689]\|18[6789]\)\([0-9]\{8\}\)/\1***/g'
echo "$phone" |sed 's/\([0-9]\{2,4\}[+-]\?\)\?\(13[0-9]\|15[1689]\|18[6789]\)\([0-9]\{8\}\)/***/g'
```



## 提取IP

```sh
#!/bin/bash

#######################
# 用途：提取ip各段数字
#######################


# 方法1
echo "method 1: "
str="192.168.31.65"
OLD_IFS="$IFS" #保存旧的分隔符
IFS="."
array=($str)
IFS="$OLD_IFS" # 将IFS恢复成原来的
for i in "${!array[@]}"; do
    echo "$i=>${array[i]}"
done

for i in ${array[@]}; do
    echo -n "$i "
done

echo

# 方法2
str="192.168.31.66"
s2=$(echo "$str" |sed 's/\./ /g')
arr2=($s2)
echo -n "method 2: "
echo ${arr2[@]}

# 方法2-2
str="192.168.31.67"
arr3=($(echo "$str" |sed 's/\./ /g'))
echo -n "method 3: "
echo ${arr3[@]}
```

