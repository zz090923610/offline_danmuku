# -*- coding: utf-8 -*- 
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
    for idx in range(len(a['i']['d'])):
        itm = a['i']['d'][idx]
        pos_full = itm['@p'].split(',')
        txt = itm['#text']
        if pos_full[1] < '7':
            res_list.append({"stime": float(pos_full[0]), 'font_size': int(pos_full[2]),
                             'font_color': hex(int(pos_full[3])), "text": txt})
        else:
            print(pos_full, txt)
    res_list = sorted(res_list, key=lambda k: k['stime'])
    return res_list
