#!/usr/bin/env python3
# coding:utf-8

"""python整齐输出多列（含中英文字符）的方法"""

import sys
import csv

is_py2 = 2 == sys.version_info.major


def pretty_col(rows, title=True, print_title=True, fields=None):
    """
    :param rows: List[List] or List[Dict] type
    :param title: whether row0 is title or not. always True when <rows> is List[Dict] type
    :param print_title: print title or not when <title> is True,
    :param fields: specify columns order
    :return:
    """

    def is_zh(ch):
        """
        部分编码范围的字符一个字符占2个普通字符的宽度，不齐全
        :param ch:
        :return:
        """

        if is_py2:
            if u'\u4e00' <= ch <= u'\u9fa5':
                return True
            elif u'\u3000' <= ch <= u'\u303F':
                return True
            elif u'\uff00' <= ch <= u'\uff60':
                return True
            else:
                return False
        else:
            if '\u4e00' <= ch <= '\u9fa5':
                return True
            elif '\u3000' <= ch <= '\u303F':
                return True
            elif '\uff00' <= ch <= '\uff60':
                return True
            else:
                return False

    def str_width(string):
        count = 0
        for ch in string.decode('utf8') if is_py2 else string:
            if is_zh(ch):
                count += 2
            else:
                count += 1
        return count

    if len(rows) == 0:
        return

    row_list = rows
    # if type(rows[0]) is dict:
    # if isinstance(rows[0], OrderedDict) or isinstance(rows[0], dict):
    if type(rows[0]).__name__ in ["dict", "OrderedDict"]:
        title = True
        if not fields:
            fields = rows[0].keys()
        row_list = [[d.get(k) for k in fields] for d in rows]
        row_list.insert(0, fields)

    if type(rows[0]) is list:
        if fields:
            fields_cols = fields
            if isinstance(fields[0], str):
                row0 = rows[0]
                fields_cols = [row0.index(m) for m in fields]
            row_list = [[r[i] for i in fields_cols] for r in row_list]

    columns_list = list(zip(*row_list))
    c_len = [max(map(str_width, col)) for col in columns_list]
    c_len = [w + 4 - w % 4 for w in c_len]
    r_len = sum(c_len) - 2

    nr = 0
    for row in row_list:
        nr += 1
        # if 1 == nr and title and not print_title:
        #     continue
        # line = "".join([x + " " * (c_len[i] - str_width(x)) for i, x in enumerate(row)])
        # print(line)
        # if 1 == nr and title and print_title:
        #     print("*" * r_len)
        line = "".join([x + " " * (c_len[i] - str_width(x)) for i, x in enumerate(row)])
        if 1 == nr and title:
            if print_title:
                print(line)
                print("*" * r_len)
            continue
        print(line)


def show_all():
    with(open("contact.txt", "r")) as f:
        name_dict_list = list(csv.DictReader(f))

    pretty_col(name_dict_list, title=True, fields=["姓名", "phone", "qq", "email", "remark"])
    print("")
    pretty_col(name_dict_list, title=True, print_title=False,
               fields=["姓名", "phone", "qq", "email", "remark"])
    print("")
    pretty_col(name_dict_list, title=True)
    print("")
    pretty_col(name_dict_list, title=True, print_title=False)


def show_all2():
    with(open("contact.txt", "r")) as f:
        name_list = list(csv.reader(f))

    pretty_col(name_list, title=True, fields=["姓名", "qq", "phone", "email", "remark"])
    print("")
    pretty_col(name_list, title=True, print_title=False, fields=[0, 1, 3, 2])
    print("")
    pretty_col(name_list, title=True)
    print("")
    pretty_col(name_list, title=False, fields=["姓名", "email", "remark"])
    print("")
    pretty_col(name_list, title=False, fields=[0, 3])
    print("")
    pretty_col(name_list, title=False)


if __name__ == '__main__':
    """contact.txt:

姓名,phone,qq,email,remark
张三33333333333333333333333333,15688886666,666999,zhangsan@qq.com,无
李四44444444444444444444444444444444444444444444444444,13188889999,999777,lisi@qq.com,2020
王!@#ii@()（）【】五5555555,156787888991,8882222222222222,ww@qq.com,2019
    """

    show_all()
    print("")
    print("")
    print("")
    print("")
    show_all2()
