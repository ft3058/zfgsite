# coding:utf8
"""
get info from :
http://ipinfo.io/

cmds:

curl ipinfo.io

{
  "ip": "58.210.119.10",
  "hostname": "No Hostname",
  "city": "Nanjing",
  "region": "Jiangsu Sheng",
  "country": "CN",
  "loc": "32.0617,118.7778",
  "org": "AS4134 No.31,Jin-rong Street"
}

curl ipinfo.io/8.8.8.8

{
  "ip": "8.8.8.8",
  "hostname": "google-public-dns-a.google.com",
  "city": "Mountain View",
  "region": "California",
  "country": "US",
  "loc": "37.3860,-122.0838",
  "org": "AS15169 Google Inc.",
  "postal": "94040"
}

curl ipinfo.io/8.8.8.8/org

AS15169 Google Inc.

"""
import time
import requests
from jumpserver_model_api import IpInfo, Asset


def run(at):
    # ip = '218.75.155.46'
    ip = at.ip
    url = 'http://ipinfo.io/{ip}'.format(ip=ip)
    print 'url: ', url

    r = requests.get(url)
    """
    {
      "ip": "218.75.155.46",
      "hostname": "No Hostname",
      "city": "Changsha",
      "region": "Hunan",
      "country": "CN",
      "loc": "28.1792,113.1136",
      "org": "AS4134 No.31,Jin-rong Street"
    }
    """
    # print r.content
    d = r.json()
    print d
    print r.status_code

    ip = d.get('ip', '')
    hostname = d.get('hostname', '')
    city = d.get('city', '')
    region = d.get('region', '')
    country = d.get('country', '')
    loc = d.get('loc', '')
    org = d.get('org', '')

    o, created = IpInfo.objects.get_or_create(ip=ip, hostname=hostname, city=city,region=region,
                                              country=country, loc=loc, org=org, asset=at)
    if created:
        print 'created new obj'
    else:
        print 'exists obj:'
        print o.ip

    print 'save succ...'
    print '----------------------------------'
    print


def update_ipinfo():
    from jumpserver_model_api import get_all_assets
    for n, at in enumerate(get_all_assets()):
        try:
            run(at)
        except Exception, e:
            try:
                run(at)
            except: pass
            print str(e)

        print 'complete :', n+1
        time.sleep(1)


if __name__ == '__main__':
    # update_ipinfo()
    from jumpserver_model_api import IpInfo
    objs = IpInfo.objects.all()  # [0:10]
    for i in objs:
        print i.ip, i.country
        if i.country:
            at = Asset.objects.get(ip=i.ip)
            area = i.country[0:2]
            at.area = area
            print area
            at.save()
            print 'update succ...'
            print

    pass
