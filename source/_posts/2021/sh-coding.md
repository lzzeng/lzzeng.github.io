---
title: bash编程 —— 3例
date: 2021-09-25 23:55:40
tags:
    - Shell
categories:
    - Shell
copyright:
toc: true
---



## 固定时间间隔

每5s执行一次命令：

```sh
while true
do
  sleep 5
  echo "`date '+%S'`: doing ..."
done
```

此写法很简单，但会产生累积误差。

<!-- more -->

改成如下可自动校正，使每个周期的实际执行时刻和预期执行时刻的偏差保持在0.1s以内：

```sh
tperiod=5
let tnext=`date '+%s'`+tperiod
let tend=`date '+%s'`+tperiod*1000  # 可设定截止时刻，如果无限循环，可去掉tend相关的行

while true
do
  tnow=`date '+%s'`
  sleep 0.1

  if [ $tnow -gt $tend ]; then
    echo "end."
    break
  fi

  if [ $tnow -le $tnext ]; then
    continue
  fi

  let tnext+=tperiod

  echo "`date '+%S'`: doing ..."
done
```



## 错误归并

题目：开发一个简单错误记录功能小模块，能够记录出错的代码所在的文件名称和行号。

处理：
1. 记录最多8条错误记录，循环记录，最后只用输出最后出现的八条错误记录。对相同的错误记录只记录一条，但是**错误计数增加。最后一个斜杠后面的带后缀名的部分（保留最后16位）和行号完全匹配的记录才做算是”相同“的错误记录。**
2. 超过16个字符的文件名称，只记录文件的最后有效16个字符。
3. 输入的文件可能带路径，记录文件名称不能带路径。**也就是说，哪怕不同路径下的文件，如果它们的名字的后16个字符相同，也被视为相同的错误记录。**
4. 循环记录时，只以第一次出现的顺序为准，后面重复的不会更新它的出现时间，仍以第一次为准。



```
示例输入：
D:\zwtymj\xccb\ljj\cqzlyaszjvlsjmkwoqijggmybr 645
E:\je\rzuwnjvnuz 633
C:\km\tgjwpb\gy\atl 637
F:\weioj\hadd\connsh\rwyfvzsopsuiqjnr 647
E:\ns\mfwj\wqkoki\eez 648
D:\cfmwafhhgeyawnool 649
E:\czt\opwip\osnll\c 637
G:\nt\f 633
F:\fop\ywzqaop 631
F:\yay\jc\ywzqaop 631

输出：
rzuwnjvnuz 633 1
atl 637 1
rwyfvzsopsuiqjnr 647 1
eez 648 1
fmwafhhgeyawnool 649 1
c 637 1
f 633 1
ywzqaop 631 2
```



shell解法：

```sh
txt=$(cat)
fname_row_uniq_count=$(echo "$txt" |sed 's/^.*\\//' |awk '{print substr($1,length($1)-15)" "$2}' |sort |uniq -c)
fname_row_sorted_latest8=$(echo "$txt" |sed 's/^.*\\//' |awk '{t=substr($1,length($1)-15)" "$2; if(a[t]!=1) {a[t]=1; print t;}}' |tail -n8)

IFS=$'\n'
for line in $fname_row_sorted_latest8
do
   echo "$fname_row_uniq_count" |grep -E "^\s*[0-9]+\s$line$" |awk '{print $2" "$3" "$1}'
done
# 或者
echo "$fname_row_sorted_latest8" |awk -v vline="`echo "$fname_row_uniq_count" |sed 's/^/echo /'`" 'BEGIN{while(vline |getline) d[$2" "$3]=$1;} {print $0" "d[$0];}'
```



## 四舍五入

题目：输入一个正的小数，输出四舍五入结果

```sh
# S0:
read a
b=$(echo "$a" |cut -d. -f1)
b2=$(echo "$a" |cut -d. -f2)
[ "${b2:0:1}" -ge 5 ] && echo $((b+1)) || echo $b


# S1:
IFS=. read b b2
[ "${b2:0:1}" -ge 5 ] && echo $((b+1)) || echo $b

# S2:
read a
b=${a%.*}
b2=${a#*.}
[ "${b2:0:1}" -ge 5 ] && echo $((b+1)) || echo $b

# S4: 特别解法
read a
printf "%.0f" "$a"1  # 4.5是特例，结果不是5，而是4；由于都是小数，一律末尾加一个1 可防止4.5=4
```
