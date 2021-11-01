---
title: bash编程 —— 读写配置
date: 2020-09-13 16:30:00
tags:    
	- Shell
categories:
    - Shell
copyright: true
toc: true
---



> shell读写配置

<!-- more -->



## 读取配置

```sh
#!/bin/sh

######################
# 读取ini配置文件，字典法
######################

declare -A d
function read_ini() {
    ini_file=$1
    if [ -f "${ini_file}" ]; then
      while read line; do
#        if [ -z $(echo "$line" | sed "s/^[^#]*\[\w+\].*$//") ]; then
        if echo "$line" |grep -xq '^\s*\[[a-zA-Z0-9_\-]\+\].*$'; then
#          sec=$(echo "$line" | sed "s/^[^#]*\[\(.\+\)\].*$/\1/")
          sec=$(echo "$line" | sed "s/^\s*\[\([a-zA-Z0-9_\-]\+\)\].*$/\1/")
          flag=1
        fi

        if [ 1 -eq $flag ] && echo "$line" |grep -xq '^\s*\w\+\s*=\s*.*$'; then
#          item=$(echo "$line" |sed "s/^\s*\([a-zA-Z0-9_\-]\+\)\s*=.*$/\1/")
          item=$(echo "$line" |sed "s/^\s*\(\S\+\)\s*=.*$/\1/")
          value=$(echo "$line" |sed "s/^.*=\s*\(.\+\)\s*$/\1/")
          key="$sec/$item"
          d[$key]=$value
        fi
      done <"${ini_file}"
    fi
}

read_ini a.ini
echo ${d[students/name]}
echo ${d[students/name2]}
echo "End."

```



## 写入配置

```sh
#!/bin/sh

######################
# 修改ini配置文件，不存在section或item时
# ，追加item 或 增加 section和item
######################


function write_ini() {
  # usage: write_ini <ini_file> <section> <item> <value>
  ini_file=$1
  section=$2
  item=$3
  value=$4
  flag=0
  is_found=0

  if [ -f "${ini_file}" ]; then
    while read line; do
      #      if [ -z $(echo "$line" | sed "s/^[^#]*\[${section}\].*$//") ]; then
      if echo "$line" | grep -xq "^\s*\[${section}\].*$"; then
        flag=1
      fi

      #      if [ 1 -eq $flag ] && [ -z $(echo "$line" | sed "s/^[^#]*${item}.*$//") ]; then
      if [ 1 -eq $flag ] && echo "$line" | grep -xq "^\s*${item}\s*=\s*.*$"; then
        echo "$line" | sed "s/=.*$/=${value}/"
        flag=0
        is_found=1
      else
        echo "$line"
      fi
    done <"${ini_file}"   # 从文件读取行，循环内的变量退出循环后仍有效；似乎~如果从管道读取则不然。
  fi
  echo $flag,$is_found # 附上while循环中的变量值
}

function write() {
  # usage: write <ini_file> <section> <item> <value>
  ini_file=$1
  section=$2
  item=$3
  value=$4
  out=$(write_ini $@)               # 被$()方式调用，与直接write_ini，变量作用域不同; 因在子进程中运行？
  ret=$(echo "$out" | tail -n 1)
  res=$(echo "$out" | head -n -1)
#  echo $flag,$is_found             # write_ini中flag是1，此处是0！
  flag=$(echo "$ret" | cut -d, -f1)
  is_found=$(echo "$ret" | cut -d, -f2)
  if [ $flag -eq 0 ]; then
    echo "$res"
    echo ""
    echo "[${section}]"
    echo "${item}=${value}"
  elif [ $is_found -eq 0 ]; then
    echo "$res" | sed "/\[${section}\]/a\\${item}=${value}"
  fi
}

write a.ini students name2 lucy2
write a.ini students3 name3 lucy3
```



## 其它

```sh
# !/bin/bash

##################
# 读取、修改ini, item不存在时不会新建
##################

INIFILE=$1
SECTION=$2
ITEM=$3
NEWVAL=$4

function ReadINIfile() {
#  ReadINI=$(awk -F= '/\['$SECTION'\]/{a=1}a==1&&$1~/'$ITEM'/{print $2;exit}' $INIFILE)
  ReadINI=$(awk -F '=' -v it="$ITEM" '/\['$SECTION'\]/{a=1}a==1&&$1==it{print $2;exit}' $INIFILE)
#  ReadINI=$(awk -F '=' -v it="$ITEM" '/\['$SECTION'\]/{a=1}{if(a==1&&$1==it){print $2;exit}}' $INIFILE)
  echo $ReadINI
}

function WriteINIfile() {
  sed -i "/^\[$SECTION\]/,/^\[/ {/^\[$SECTION\]/b;/^\[/b;s/^$ITEM*=.*/$ITEM=$NEWVAL/g;}" $INIFILE
}

if [ "$4" = "" ]; then
  ReadINIfile $1 $2 $3
else
  WriteINIfile $1 $2 $3 $4
fi
```

