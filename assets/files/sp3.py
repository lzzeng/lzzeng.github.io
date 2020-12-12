#!/usr/bin/env python3
# coding=utf8

"""股价查询小工具"""

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
    parser.add_argument("day", nargs='?',
                        help="which day(s), use the number of days before today,   \
                               e.g. \"3,1\" or \"1,3\" or \"3,\" or \",1\" or \"3\", \
                               by default \",\" is the same as \"10,1\", and \
                               the quotes are not must need. Maximum days: 137")

    parser.add_argument("-C", "--no-color", default=False, action="store_true", help="cancel color")
    parser.add_argument("-Z", "--en", default=False, action="store_true", help="cancel zh-CN")
    # parser.add_argument("--d1", type=int, default=10,
    #                     help="begin day, use the number of days before today")
    # parser.add_argument("--d2", type=int,
    #                    help="end day, use the number of days before today")
    args = parser.parse_args()
    return args


def fun_run_time(func):
    """计算代码执行时间，未使用
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kw):
        time_start = time.time()
        _res = func(*args, **kw)
        time_end = time.time()
        print('%.3f s' % (time_end - time_start))
        return _res

    return wrapper


def get_name(symbol):
    url_ = u'http://hq.sinajs.cn/?list={}'.format(symbol)
    resp = requests.get(url_)
    if 200 == resp.status_code:
        try:
            c = resp.content.decode('cp936')
            st = c.index('="') + 2
            fn = c.index(',')
            return c[st:fn]
        except:
            pass


def get_symbol_info(name):
    url_ = u'https://suggest3.sinajs.cn/suggest/key={}'.format(name)
    resp = requests.get(url_)
    if 200 == resp.status_code:
        try:
            c = resp.content.decode('cp936')
            fn = c.split(',')[2:5]
            return fn
        except:
            pass


def get_price(index, **kw):
    """未使用
    :param index:
    :param kw:
    :return:
    """
    resp = requests.get(url, params=kw)
    if 200 == resp.status_code:
        res_list = json.loads(resp.content)
        return res_list[index]


def get_day_price000(d=1, symbol=None):
    """未使用"""

    if 0 == d:
        d = 1
    _d1 = get_price(0, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    _d2 = get_price(1, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    _d3 = get_price(2, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    _d4 = get_price(3, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    return {
        "symbol": symbol,
        "day": _d1.get("day").split(" ")[0],
        "open": _d1.get("open"),
        "close": _d4.get("close"),
        "high": max(_d1.get("high"), _d2.get("high"), _d3.get("high"), _d4.get("high")),
        "low": min(_d1.get("low"), _d2.get("low"), _d3.get("low"), _d4.get("low")),
    }


def get_price_list(index_st, index_fn, **kw):
    resp = requests.get(url, params=kw)
    if 200 == resp.status_code:
        res_list = json.loads(resp.content)
        return res_list[index_st:index_fn]


def get_day_price(d=1, symbol=None, en=False):
    """获取最近一天的股价
    :param d:
    :param symbol:
    :param en:
    :return:
    """

    if 0 == d:
        d = 1
    d = get_price_list(0, 4, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    _res = {
        "symbol": symbol,
        "day": d[0].get("day").split(" ")[0],
        "open": d[0].get("open"),
        "close": d[3].get("close"),
        "low": min([d[i].get("low") for i in range(4)]),
        "high": max([d[i].get("high") for i in range(4)]),
    }
    day_price = [[_res.get("day"), _res.get("open"), _res.get("low"), _res.get("high"), _res.get("close")]]
    # row0 = ["日期", "开盘", "最低", "最高", "收盘"] if not en \
    row0 = [u"日期", u"开盘", u"最低", u"最高", u"收盘"] if not en \
        else ["Date", "Open", "Low", "High", "Close"]
    day_price.insert(0, row0)
    del row0
    return _res, day_price


def get_days_price(d2_=1, d1_=1, symbol=None, is_delta=True, en=False):
    """
    获取 第前max(d1,d2)天 ~ 第前min(d1,d2)天之间每日股价
    d2=10, d1=1 表示 第前10天 至 第前1天
    d2=1, d1=10 表示 第前1天 至 第前10天, 顺序和上相反
    :param d2_:
    :param d1_:
    :param symbol:
    :param is_delta: 是否计算涨跌（仅打印涨跌时会按彩色输出，故以是否彩色输出的参数代替）
    :param en:
    :return:
    """

    if 0 == d1_:
        d1_ = 1

    is_reversed = False
    if d2_ < d1_:
        d1_, d2_ = d2_, d1_
        is_reversed = True

    d = get_price_list(0, 4 * (d2_ - d1_ + 1), symbol=symbol, datalen=4 * d2_, scale=60, ma=5)
    _res = []
    for i in range(d2_ - d1_ + 1):
        t_res = {
            "symbol": symbol,
            "day": d[4 * i].get("day").split(" ")[0],
            "open": d[4 * i].get("open"),
            "close": d[3 + 4 * i].get("close"),
            "low": min([d[j + 4 * i].get("low") for j in range(4)]),
            "high": max([d[j + 4 * i].get("high") for j in range(4)]),
        }
        _res.append(t_res)

    if is_reversed:
        _res = reversed(_res)

    days_prices = [[x.get("day"), x.get("open"), x.get("low"), x.get("high"), x.get("close")] for x in _res]
    # row0 = ["日期", "开盘", "最低", "最高", "收盘", "涨幅"] if not en \
    row0 = [u"日期", u"开盘", u"最低", u"最高", u"收盘", u"涨幅"] if not en \
        else ["Date", "Open", "Low", "High", "Close", "Percent"]

    if is_delta:
        days_prices = delta_price(days_prices)
    else:
        row0.pop()

    days_prices.insert(0, row0)
    del row0
    return _res, days_prices


def delta_price(days_prices=None):
    p0 = days_prices[0]
    _res = [p0]
    for p in days_prices[1:]:
        b, b2, b3, b4 = [float(p[i]) - float(p0[4]) for i in range(1, 5)]
        bp4 = (float(p[4]) - float(p0[4])) / float(p0[4]) * 100
        fb, fb2, fb3, fb4 = [NumFmt.r.value.format(bb) if bb > 0 else NumFmt.g.value.format(bb) for
                             bb in [b, b2, b3, b4]]
        fbp4 = NumFmt.rp.value.format(bp4) if bp4 > 0 else NumFmt.gp.value.format(bp4)
        z1, z2, z3, z4 = ['{a:.2f}({b})'.format(a=float(p[i]), b=fbb) for
                          i, fbb in [(1, fb), (2, fb2), (3, fb3), (4, fb4)]]
        zp4 = '{b}'.format(b=fbp4)
        pz = [p[0], z1, z2, z3, z4, zp4]
        p0 = p
        _res.append(pz)
    p0 = days_prices[0]
    _res[0] = [p0[0] + "*"] + [v for v in p0[1:]] + ['--']
    return _res


def pretty_output(text):
    """利用shell命令处理输出
    +m.n +m.n% 会被染红
    -m.n -m.n% 会被染绿
    :param text:
    :return:
    """

    exec_cmd(r"echo -e '{}' |column -t |sed 's/\(+[0-9]\+\.[0-9]\+%\?\)/\\\\e[01\;31m\1\\\\e[00m/g;"
             r"s/\(-[0-9]\+\.[0-9]\+%\?\)/\\\\e[01\;32m\1\\\\e[00m/g;' |xargs -I {} echo -e {}"
             .format(text if not is_py2 else text.encode("utf8"), "{}", "{}"))


def print_latest(d, symbol, en=False):
    resp = get_day_price(d, symbol, en=en)[1]
    out_ = ""
    for x in resp:
        out_ += "\t".join(x) + "\n"
    pretty_output(out_)


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
    except:
        pass

    try:
        stock_name = get_name(s)
        if not stock_name:
            print("stock name not found")
            exit()

        # 股票名称、代码
        if is_py2:
            if not pa.no_color:
                exec_cmd("echo -e '{} {}'".format(NumFmt.bs.value.format(stock_name.encode('utf8')),
                                                  NumFmt.bs.value.format(s)))
            else:
                exec_cmd("echo -e '{} {}'".format(stock_name.encode('utf8'), s))
        else:
            if not pa.no_color:
                exec_cmd("echo -e '{} {}'".format(NumFmt.bs.value.format(stock_name),
                                                  NumFmt.bs.value.format(s)))
            else:
                exec_cmd("echo -e '{} {}'".format(stock_name, s))

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

        res = get_days_price(d2, d1, s, is_delta=not pa.no_color, en=pa.en)[1]
        output = ""
        for r in res:
            ts = "\t".join(r) + "\n"
            output += ts
            
        pretty_output(output)
    except Exception as e:
        logging.exception(e)
        pass
