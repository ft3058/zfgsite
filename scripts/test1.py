# coding:utf8
"""

"""
import time
import requests
from jumpserver_model_api import IpInfo, Asset, get_all_assets

for at in get_all_assets():
    # at = Asset.objects.get(id=403)
    ipinfo = IpInfo.objects.filter(asset=at)
    if ipinfo:
        print ipinfo[0].country
        print at.ip
    else:
        print 'not found asset of ip:', at.ip
