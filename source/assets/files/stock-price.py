#!/usr/bin/env python3
# coding=utf8

import os
import sys
import requests
import json
import functools
import time
import argparse
import subprocess
import traceback
import logging


is_py2 = 2 == sys.version_info.major
# url_tmpl = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&datalen={}&scale=30&ma=5'
url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
rgb = dict(r='\e[01;31m+{:.2f}\e[00m',
           rs='\e[01;31m{}\e[00m',
           bs='\e[00;34m{}\e[00m',
           rp='\e[01;31m+{:.2f}%\e[00m',
           g='\e[01;32m{:.2f}\e[00m',
           gp='\e[01;32m{:.2f}%\e[00m',
           w='{}')


def exec_cmd(cmd):
    # commands.getstatusoutput(cmd_String)
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
                        help="which day(s), use the number of days before today,   \
                               e.g. \"3,1\" or \"1,3\" or \"3,\" or \",1\" or \"3\", \
                               by default \",\" is the same as \"10,1\", and the quotes are not must need. Maximum days: 137")

    parser.add_argument("-C", "--no-color", default=True, action="store_false", help="cancel color")
    parser.add_argument("-Z", "--en", default=True, action="store_false", help="cancel zh-CN")
    # parser.add_argument("-d", "--drange",
    #                      help="begin day and end day split by \',\', use the number of days before today")

    # parser.add_argument("--d1", type=int, default=10,
    #                     help="begin day, use the number of days before today")
    # parser.add_argument("--d2", type=int,
    #                    help="end day, use the number of days before today")

    args = parser.parse_args()
    return args


def fun_run_time(func):
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
    r = requests.get(url, params=kw)
    if 200 == r.status_code:
        res_list = json.loads(r.content)
        return res_list[index]


def get_price_list(index_st, index_fn, **kw):
    r = requests.get(url, params=kw)
    if 200 == r.status_code:
        res_list = json.loads(r.content)
        return res_list[index_st:index_fn]


# @fun_run_time
def get_day_price(d=1, symbol=None):
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


# @fun_run_time
def get_day_price2(d=1, symbol=None):
    if 0 == d: d = 1
    d = get_price_list(0, 4, symbol=symbol, datalen=4 * d, scale=60, ma=5)
    res = {
        "symbol": symbol,
        "day": d[0].get("day").split(" ")[0],
        "open": d[0].get("open"),
        "close": d[3].get("close"),
        "low": min([d[i].get("low") for i in range(4)]),
        "high": max([d[i].get("high") for i in range(4)]),
    }
    return res, [res.get("day"), res.get("open"), res.get("low"), res.get("high"), res.get("close")]


# @fun_run_time
def get_days_price2(d2=1, d1=1, symbol=None, is_delta=False):
    if 0 == d1:
        d1 = 1

    is_reversed = False
    if d2 < d1:
        t = d2
        d2 = d1
        d1 = t
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

    if is_delta:
        days_prices = delta_price(days_prices)

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
        fb = rgb['r'].format(b) if b > 0 else rgb['g'].format(b)
        fb2 = rgb['r'].format(b2) if b2 > 0 else rgb['g'].format(b2)
        fb3 = rgb['r'].format(b3) if b3 > 0 else rgb['g'].format(b3)
        fb4 = rgb['r'].format(b4) if b4 > 0 else rgb['g'].format(b4)
        fbp4 = rgb['rp'].format(bp4) if bp4 > 0 else rgb['gp'].format(bp4)
        z1 = '{a:.2f}({b})'.format(a=float(p[1]), b=fb)
        z2 = '{a:.2f}({b})'.format(a=float(p[2]), b=fb2)
        z3 = '{a:.2f}({b})'.format(a=float(p[3]), b=fb3)
        z4 = '{a:.2f}({b})'.format(a=float(p[4]), b=fb4)
        zp4 = '{b}'.format(b=fbp4)
        pz = [p[0], z1, z2, z3, z4, zp4]
        p0 = p
        res.append(pz)

    p0 = days_prices[0]
    res[0] = [p0[0] + " *"] + [v + '\t' for v in p0[1:]] + ['--']
 
    return res


if __name__ == '__main__':
    try:
        pa = get_param()
        d2, d1 = (str(pa.day) + ',').split(',')[:2]
        s = pa.stock_code
        if is_py2:
            s = s.decode('utf8')

        if len(s) < 10:
            s = get_symbol_info(s)[1]

        is_int = False
        if pa.day is None:
            day = 1
        else:
            day = int(pa.day)
            is_int = True
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        pass

    try:
        sname = get_name(s)
        if not sname:
            print("stock name not found")
            exit()

        if is_py2:
            if pa.no_color:
                exec_cmd("echo -e '{}'".format(rgb['bs'].format(sname.encode('utf8'))))
            else:
                exec_cmd("echo -e '{}'".format(sname.encode('utf8')))
        else:
            if pa.no_color:
                exec_cmd("echo -e '{}'".format(rgb['bs'].format(sname)))
            else:
                exec_cmd("echo -e '{}'".format(sname))

        # 最近一天
        if pa.day is None or is_int:
            if pa.no_color:
                if pa.en:
                    exec_cmd("echo -e '{}'".format('\t'.join(["日期\t", "开盘", "最低", "最高", "收盘"])))
                else:
                    exec_cmd("echo -e '{}'".format('\t'.join(["Date\t", "Open", "Low", "High", "Close"])))
            else:
                if pa.en:
                    exec_cmd("echo -e '{}'".format('\t'.join(["日期\t", "开盘", "最低", "最高", "收盘"])))
                else:
                    exec_cmd("echo -e '{}'".format('\t'.join(["Date\t", "Open", "Low", "High", "Close"])))
            exec_cmd("echo -e '{}'".format('--' * 23))
            print('\t'.join(get_day_price2(day, s)[1]))
            exit()

        # 多天
        if pa.no_color:
            if pa.en:
                exec_cmd("echo -e '{}'".format('\t\t'.join(["日期", "开盘", "最低", "最高", "收盘", "涨幅"])))
            else:
                exec_cmd("echo -e '{}'".format('\t\t'.join(["Date", "Open", "Low", "High", "Close", "Percent"])))
        else:
            if pa.en:
                exec_cmd("echo -e '{}'".format('\t'.join(["日期\t", "开盘", "最低", "最高", "收盘"])))
            else:
                exec_cmd("echo -e '{}'".format('\t'.join(["Date\t", "Open", "Low", "High", "Close"])))

        if pa.no_color:
            exec_cmd("echo -e '{}'".format('--' * 43))
        else:
            exec_cmd("echo -e '{}'".format('--' * 23))

        if pa.day is None or is_int:
            print('\t'.join(get_day_price2(day, s)[1]))
        elif not d1:
            d1 = 1
            try:
                d2 = int(d2)
            except:
                d2 = 10

            for r in get_days_price2(d2, d1, s, is_delta=pa.no_color)[1]:
                exec_cmd("echo -e '{}'".format('\t'.join(r)))
        else:
            try:
                d1 = int(d1)
            except:
                d1 = 1

            try:
                d2 = int(d2)
            except:
                d2 = 10

            for r in get_days_price2(d2, d1, s, is_delta=pa.no_color)[1]:
                exec_cmd("echo -e '{}'".format('\t'.join(r)))
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        logging.exception(e)
        pass

