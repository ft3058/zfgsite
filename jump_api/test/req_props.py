# coding:utf-8
"""
时间:2016/4/10
说明:
"""
import requests


url = 'https://mdetail.tmall.com/mobile/itemPackage.do?itemId=528005737952'

HEADERS = {
    # 'Host': 'www.sse.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
    'Accept': '*/*',
    'Cache-Control': 'max-age=0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
    'Connection': 'keep-alive',
}

r = requests.get(url, headers=HEADERS)
print r.status_code
d = r.json()

for dic in d['model']['list'][0]['v']:
    print dic['k'], dic['v']