---
title: 股价查询小工具一枚
date: 2020-09-06 00:30:00
tags:    
    - Python
categories:
    - Python

copyright: true
---



只能查询A股，用到了3个新浪股票数据接口：

```sh
http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData
http://hq.sinajs.cn/?list=sz000002
https://suggest3.sinajs.cn/suggest/key=万科A
```



<!-- more -->



按股票名称查询最新股价、查询 第前3交易日、查询 前3个交易日，按股票代码查询 前3个交易日 效果如下：



<img src="../assets/images2020/image-20200928004218980.png" alt="image-20200928004218980" style="zoom:67%;" />



```sh
# 使用：
[root@VM_0_13_centos ~]# cp stock-price.py /usr/local/bin/stock-price
[root@VM_0_13_centos ~]# chmod +x /usr/local/bin/stock-price

[root@VM_0_13_centos ~]# stock-price -h
usage: stock-price [-h] [-C] [-Z] stock_code [day]

positional arguments:
  stock_code      the stock code or the stock name, e.g. sz000002 or 万科A
  day             which day(s), use the number of days before today, e.g.
                  "3,1" or "1,3" or "3," or ",1" or "3", by default "," is the
                  same as "10,1", and the quotes are not necessary. Maximum
                  days: 137

optional arguments:
  -h, --help      show this help message and exit
  -C, --no-color  cancel color
  -Z, --en        cancel zh-CN
```



[附件：stock-price.py](/assets/files/stock-price.py)

