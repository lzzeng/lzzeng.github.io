#!/usr/bin/env python3
# coding=utf8

import os
import sys
import requests
import json
import functools
import time
import argparse
# import subprocess
# import traceback
import logging
from enum import Enum


is_py2 = 2 == sys.version_info.major
# if is_py2:
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
# url_tmpl = 'http://money.finance.sina.com.cn/quotes_service/api/' \
#            'json_v2.php/CN_MarketData.getKLineData?symbol={}&datalen={}&scale=30&ma=5'
url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
NumFmt = Enum('NumFmt',
              dict(r='+{:.2f}',
                   g='{:.2f}',
                   rp='+{:.2f}%',
                   gp='{:.2f}%',
                   n='{:.2f}',
                   np='{:.2f}%',
                   rs='\e[01;31m{}\e[00m',
                   gs='\e[01;32m{}\e[00m',
                   bs='\e[00;34m{}\e[00m',
                   w='{}'))
# print(NumFmt.r.value)


def exec_cmd(cmd):
    # commands.getstatusoutput(cmd)
    # subprocess.run(cmd,
    #                shell=True,
    #                stdout=subprocess.PIPE,
    #                stderr=subprocess.PIPE,
    #                encoding="utf-8",
    #                timeout=1)
    os.system('{}'.format(cmd))


def get_param():
    parser = argparse.ArgumentParser()
    parser.add_argument("stock_code", help="the stock code or the stock name, e.g. sz000002  or  万科A")
    # 可选的位置参数
    # parser.add_argument("day", type=int, default=1, nargs='?',
    parser.add_argument("day", nargs='?',
                        help="which day(s), use the number of days before today, e.g."
                             " \"3,1\" or \"1,3\" or \"3,\" or \",1\" or \"3\", by default"
                             " \",\" is the same as \"10,1\", and the quotes are not necessary. Maximum days: 137")

    parser.add_argument("-C", "--no-color", default=True, action="store_false",
                        help="if calculate delta, then color, else no color.")
    parser.add_argument("-Z", "--en", default=False, action="store_true", help="cancel zh-CN")
    # parser.add_argument("-d", "--drange",
    #                      help="begin day and end day split by \',\', use the number of days before today")

    # parser.add_argument("--d1", type=int, default=10,
    #                     help="begin day, use the number of days before today")
    # parser.add_argument("--d2", type=int,
    #                    help="end day, use the number of days before today")
    args = parser.parse_args()
    return args


def fun_run_time(func):
    """
    计算代码执行时间，未使用
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kw):
        time_start = time.time()
        res = func(*args, **kw)
        time_end = time.time()
        print('%.3f s' % (time_end - time_start))
        return res

    return wrapper


def get_name(symbol):
    url = u'http://hq.sinajs.cn/?list={}'.format(symbol)
    r = requests.get(url)
    if 200 == r.status_code:
        try:
            c = r.content.decode('cp936')
            st = c.index('="') + 2
            fn = c.index(',')
            return c[st:fn]
        except Exception as e:
            pass


def get_symbol_info(name):
    url = u'https://suggest3.sinajs.cn/suggest/key={}'.format(name)
    r = requests.get(url)
    if 200 == r.status_code:
        try:
            c = r.content.decode('cp936')
            fn = c.split(',')[2:5]
            return fn
        except:
            pass


def get_price(index, **kw):
    """
    未使用
    :param index:
    :param kw:
    :return:
    """
    r = requests.get(url, params=kw)
    if 200 == r.status_code:
        res_list = json.loads(r.content)
        return res_list[index]


def get_day_price000(d=1, symbol=None):
    """
    未使用
    """

    if 0 == d:
        d = 1
    d1 = get_price(0, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    d2 = get_price(1, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    d3 = get_price(2, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    d4 = get_price(3, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    return {
        "symbol": symbol,
        "day": d1.get("day").split(" ")[0],
        "open": d1.get("open"),
        "close": d4.get("close"),
        "high": max(d1.get("high"), d2.get("high"), d3.get("high"), d4.get("high")),
        "low": min(d1.get("low"), d2.get("low"), d3.get("low"), d4.get("low")),
    }


def get_price_list(index_st, index_fn, **kw):
    r = requests.get(url, params=kw)
    if 200 == r.status_code:
        res_list = json.loads(r.content)
        return res_list[index_st:index_fn]


def get_day_price(d=1, symbol=None, en=False):
    """
    获取最近一天的股价
    :param d:
    :param symbol:
    :param en:
    :return:
    """

    if 0 == d:
        d = 1
    d = get_price_list(0, 4, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    res = {
        "symbol": symbol,
        "day": d[0].get("day").split(" ")[0],
        "open": d[0].get("open"),
        "close": d[3].get("close"),
        "low": min([d[i].get("low") for i in range(4)]),
        "high": max([d[i].get("high") for i in range(4)]),
    }
    day_price = [[res.get("day"), res.get("open"), res.get("low"), res.get("high"), res.get("close")]]
    # row0 = ["日期", "开盘", "最低", "最高", "收盘"] if not en \
    row0 = [u"日期", u"开盘", u"最低", u"最高", u"收盘"] if not en \
        else ["Date", "Open", "Low", "High", "Close"]
    day_price.insert(0, row0)
    del row0
    return res, day_price


def get_days_price(d2=1, d1=1, symbol=None, is_delta=True, en=False):
    """
    获取 第前max(d1,d2)天 ~ 第前min(d1,d2)天之间每日股价
    d2=10, d1=1 表示 第前10天 至 第前1天
    d2=1, d1=10 表示 第前1天 至 第前10天, 顺序和上相反
    :param d2:
    :param d1:
    :param symbol:
    :param is_delta: 是否计算涨跌（仅打印涨跌时会按彩色输出，故以是否彩色输出的参数代替）
    :param en:
    :return:
    """

    if 0 == d1:
        d1 = 1

    is_reversed = False
    if d2 < d1:
        d1, d2 = d2, d1
        is_reversed = True

    d = get_price_list(0, 4 * (d2 - d1 + 1), symbol=symbol, datalen=4 * d2, scale=60, ma=5)
    res = []
    for i in range(d2 - d1 + 1):
        t_res = {
            "symbol": symbol,
            "day": d[4 * i].get("day").split(" ")[0],
            "open": d[4 * i].get("open"),
            "close": d[3 + 4 * i].get("close"),
            "low": min([d[j + 4 * i].get("low") for j in range(4)]),
            "high": max([d[j + 4 * i].get("high") for j in range(4)]),
        }
        res.append(t_res)

    if is_reversed:
        res = reversed(res)

    days_prices = [[r.get("day"), r.get("open"), r.get("low"), r.get("high"), r.get("close")] for r in res]
    # row0 = ["日期", "开盘", "最低", "最高", "收盘", "涨幅"] if not en \
    row0 = [u"日期", u"开盘", u"最低", u"最高", u"收盘", u"涨幅"] if not en \
        else ["Date", "Open", "Low", "High", "Close", "Percent"]

    if is_delta:
        days_prices = delta_price(days_prices)
    else:
        row0.pop()

    days_prices.insert(0, row0)
    del row0
    return res, days_prices


def delta_price(days_prices=None):
    p0 = days_prices[0]
    res = [p0]
    for p in days_prices[1:]:
        b = float(p[1]) - float(p0[4])
        b2 = float(p[2]) - float(p0[4])
        b3 = float(p[3]) - float(p0[4])
        b4 = float(p[4]) - float(p0[4])
        bp4 = (float(p[4]) - float(p0[4])) / float(p0[4]) * 100
        fb = NumFmt.r.value.format(b) if b > 0 else NumFmt.g.value.format(b)
        fb2 = NumFmt.r.value.format(b2) if b2 > 0 else NumFmt.g.value.format(b2)
        fb3 = NumFmt.r.value.format(b3) if b3 > 0 else NumFmt.g.value.format(b3)
        fb4 = NumFmt.r.value.format(b4) if b4 > 0 else NumFmt.g.value.format(b4)
        fbp4 = NumFmt.rp.value.format(bp4) if bp4 > 0 else NumFmt.gp.value.format(bp4)
        z1 = '{a}({b})'.format(a=NumFmt.n.value.format(float(p[1])), b=fb)
        z2 = '{a}({b})'.format(a=NumFmt.n.value.format(float(p[2])), b=fb2)
        z3 = '{a}({b})'.format(a=NumFmt.n.value.format(float(p[3])), b=fb3)
        z4 = '{a}({b})'.format(a=NumFmt.n.value.format(float(p[4])), b=fb4)
        zp4 = NumFmt.w.value.format(fbp4)
        pz = [p[0], z1, z2, z3, z4, zp4]
        p0 = p
        res.append(pz)

    p0 = days_prices[0]
    res[0] = [p0[0] + "*"] + [v for v in p0[1:]] + ['--']           # *标记起始
    return res


def pretty_output(text):
    """
    利用shell命令处理输出
    +m.n +m.n% 会被染红
    -m.n -m.n% 会被染绿
    :param text:
    :return:
    """

    exec_cmd(r"echo -e '{}' |column -t |sed 's/\(+[0-9]\+\.[0-9]\+%\?\)/\\\\e[01\;31m\1\\\\e[00m/g;"
             r"s/\(-[0-9]\+\.[0-9]\+%\?\)/\\\\e[01\;32m\1\\\\e[00m/g;' |xargs -I {} echo -e {}"
             .format(text if not is_py2 else text.encode("utf8"), "{}", "{}"))
             # .format(text.encode('utf8'), "{}", "{}"))        # py2
             # .format(text, "{}", "{}"))                       # py3


def print_latest(day, s, en=False):
    res = get_day_price(day, s, en=en)[1]
    output = ""
    for r in res:
        output += "\t".join(r) + "\n"
    pretty_output(output)


def get_valid_day(d, v_def=10):
    try:
        d = int(d)
    except:
        d = v_def
    return d


if __name__ == '__main__':
    pa, s, d2, d1, day, is_int = None, None, None, None, None, False
    try:
        pa = get_param()
        d2, d1 = (str(pa.day) + ',').split(',')[:2]
        s = pa.stock_code
        if is_py2:
            s = s.decode('utf8')
        # if len(s) < 10:
        #     s = get_symbol_info(s)[1]
        s = get_symbol_info(s)[1]

        if pa.day is None:
            day = 1
        else:
            day = int(pa.day)
            is_int = True
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        # logging.exception(e)
        pass

    try:
        sname = get_name(s)
        if not sname:
            print("stock name not found")
            exit()

        # 股票名称、代码
        if is_py2:
            if pa.no_color:
                exec_cmd("echo -e '{} {}'".format(NumFmt.bs.value.format(sname.encode('utf8')),
                                                  NumFmt.bs.value.format(s)))
            else:
                exec_cmd("echo -e '{} {}'".format(sname.encode('utf8'), s))
        else:
            if pa.no_color:
                exec_cmd("echo -e '{} {}'".format(NumFmt.bs.value.format(sname), NumFmt.bs.value.format(s)))
            else:
                exec_cmd("echo -e '{} {}'".format(sname, s))

        # 最近一天
        if pa.day is None or is_int:
            print_latest(day, s, en=pa.en)
            exit()

        if pa.day is None or is_int:
            print_latest(day, s, en=pa.en)
        # 多天
        elif not d1:
            d1 = 1
            d2 = get_valid_day(d2, 10)
        else:
            d1 = get_valid_day(d1, 1)
            d2 = get_valid_day(d2, 10)

        res = get_days_price(d2, d1, s, is_delta=pa.no_color, en=pa.en)[1]
        output = ""
        for r in res:
            ts = "\t".join(r) + "\n"
            output += ts
            # output += ts.decode('utf8')                           # py2
            # output += ts.decode('utf8') if is_py2 else ts         # py2 py3

        pretty_output(output)
    except Exception as e:
        logging.exception(e)
        pass
