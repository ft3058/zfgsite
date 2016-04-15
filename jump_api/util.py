# coding:utf-8
"""
时间:2016/4/9
说明:
"""
import socket, math
import re, traceback
from urlparse import urlsplit
from hashlib import md5
from settings import *


def check_ip(s):
    try:
        socket.inet_aton(s)
        return True
    except:
        print 'invalid ip: %s' % s
        return False


def check_port(port):
    try:
        return port.isdigit()
    except:
        return False



def get_table(table_name=''):
    from pymongo import MongoClient
    db = MongoClient(MONGODB_URI)[DB_NAME]
    if table_name:
        table = db[table_name]
    else:
        table = db[TABLE_NAME]
    return table


def md5_str(s):
    if type(s) == type(u''):
        s = s.encode('utf-8')
    return md5(s).hexdigest()


def get_cleared_url(url):
    return url.split('?')[0]


def get_num(s):
    # 获取数字
    s = s.strip()  # ¥ 41.8
    try:
        r = re.findall(re.compile(r'\d+\.*\d*'), s)[0]
    except:
        r = s.strip()
    return r


def get_num_list(s):
    # 获取数字
    s = s.strip()  # ¥ 41.8
    try:
        r = re.findall(re.compile(r'\d+\.*\d*'), s)
    except:
        r = [s.strip()]
    return r


def _(tmp):
    return tmp[0].strip()


def __(dic, tmp, k, slice=True):
    dic[k] = ''
    if tmp:
        if slice:
            dic[k] = tmp[0].strip()
        else:
            dic[k] = tmp.strip()


def get_pid(url):
    """
    获取url中的pid : https://item.taobao.com/item.htm?id=527767557423&ns=1&abbucket=5#detail
    pid = 527767557423
    """
    pid = ''
    if 'id=' in url:
        querys = urlsplit(url).query.split('&')
        for q in querys:
            if 'id=' in q:
                pid = q[3:]
    return pid


if __name__ == '__main__':
    # print get_pid('https://item.taobao.com/item.htm?id=527767557423&ns=1&abbucket=5#detail')
    # print check_ip('133333.12.11.22')
    print check_port('')
    pass