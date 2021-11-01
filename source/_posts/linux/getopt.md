---
title: bash编程 —— getopt用法
date: 2020-09-13 16:30:00
tags:    
	- Shell
categories:
    - Shell
copyright: 
toc: 
---



> getopt的用法

<!-- more -->




```sh
#!/bin/sh

filepath=$(cd `dirname $0`; pwd)

show_usage="args: [-s , -e , -n , -c][--sdate=, --edate=, --numprocs=, --cfile=]"

if [[ -z $@ ]];then
  echo $show_usage
  exit 0
fi

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

echo $sdate
echo $edate
echo $numprocs
echo $cfile
```