# -*- coding: utf-8 -*-
from bisect import bisect_left

import xmltodict


def danmuku_xml_to_dict(xml_path):
    with open(xml_path, 'rb') as f:
        res = f.read().decode('utf8')
    a = xmltodict.parse(res)
    """
    stime: 弹幕出现时间 (s)
    mode: 弹幕类型 (< 7 时为普通弹幕)
    size: 字号
    color: 文字颜色
    date: 发送时间戳
    pool: 弹幕池ID
    author: 发送者ID
    dbid: 数据库记录ID（单调递增）
    """
    res_list = []
    type_dict = {}
    for idx in range(len(a['i']['d'])):
        itm = a['i']['d'][idx]
        pos_full = itm['@p'].split(',')
        txt = itm['#text']
        f_color = hex(int(pos_full[3]))[2:]
        if len(f_color) != 6:
            f_color = '00' + f_color
        f_color = "#" + f_color
        if pos_full[1] < '7':
            type_dict[pos_full[1]] = True
            res_list.append(DanmukuDict({"stime": float(pos_full[0]), 'font_size': int(pos_full[2]),
                                         'font_color': f_color, "text": txt}))
        else:
            print(pos_full, txt)
    res_list = sorted(res_list)
    print(type_dict)
    return res_list


class DanmukuDict(dict):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        assert 'stime' in dictionary
        for key in dictionary:
            self[key] = dictionary[key]

    def __lt__(self, other):
        if type(other) == int or type(other) == float:
            return self['stime'] < other
        return self['stime'] < other['stime']

    def __le__(self, other):
        if type(other) == int or type(other) == float:
            return self['stime'] <= other
        return self['stime'] <= other['stime']

    def __gt__(self, other):
        if type(other) == int or type(other) == float:
            return self['stime'] > other
        return self['stime'] > other['stime']

    def __ge__(self, other):
        if type(other) == int or type(other) == float:
            return self['stime'] >= other
        return self['stime'] >= other['stime']

    def __eq__(self, other):
        if type(other) == int or type(other) == float:
            return self['stime'] == other
        return self['stime'] == other['stime']


def find_ge_idx(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return i
    raise ValueError
