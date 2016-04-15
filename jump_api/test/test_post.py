# coding:utf-8
"""
date: 2016/4/8
desc:
"""
import json
import requests

url = 'http://127.0.0.1/tb_model/json'

params = {
    'url': u'http://www.taobao.com',
    'title': u'2016新款男童夏装套装2-3-4-5-6-7岁儿童装运动女童韩版短袖T恤潮',
    'price': u'166',

    'sub_title': 'self.sub_title',
    'city': 'self.city',
    'sell_cnt': 'self.sell_cnt'
}
data = json.dumps(params, ensure_ascii=False).encode('utf8')
print 'data: ', data
headers = {'content-type': 'application/json; charset=UTF-8'}

r = requests.post(url, data=data, headers=headers, verify=False)
dic = r.json()
print u'响应结果:', dic
