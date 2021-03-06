# coding:utf8
"""
[u'5.135.162.69', u'root', 1669L, u'5LjsEzddznua']
[u'5.135.159.96', u'root', 1596L, u'noDjj2pkxRT9']
[u'5.135.186.39', u'root', 22L, u'fUFmTeCSzwzb']
"""

import os, sys, time
from Queue import Queue
from threading import Thread
# from snmp_api import get_cmd_val, get_next_cmd_val
from const import *

proj_path = "/data/www/yxyw/jump"
try:
    from local_vars import *
except: pass
print 'proj_path:', proj_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from jasset.models import Asset, AssetGroup, AssetGroup1
from jmonitor.models import TcpConnCount, DiskSize
from util import *


def init_all_assets():
    prop_list = []
    assets = Asset.objects.all()
    # assets = Asset.objects.filter(ip='112.123.169.32')  # 111.7.165.42 218.75.155.46
    for t in assets:
        # q.put({'ip': t.ip})
        prop_list.append([t.ip, t.get_username(), t.port, t.passwd])
    return prop_list



if __name__ == '__main__':
    """
    snmpwalk -v 2c -c youxun 37.59.60.46 ifDescr                                              
    """


    prop_list = init_all_assets()
    for i in prop_list:
        print '++', i

    l = [
        [u'5.135.162.69', u'root', 1669L, u'5LjsEzddznua'],
        [u'5.135.159.96', u'root', 1596L, u'noDjj2pkxRT9'],
        [u'5.135.186.39', u'root', 22L, u'fUFmTeCSzwzb'],
    ]
    error_ip = []

    community_names = ['youxun', 'yxdown']
    for i in prop_list:
        checked = False
        cname = ''

        for name in community_names:    # snmpwalk -v 2c -c youxun 37.59.60.46 ifDescr
            cmd = u'snmpwalk -v 2c -c %s %s ifDescr' % (name, i[0])
            print 'cmd:', cmd
            retval, lines = exec_cmd(cmd)
            print retval, lines
            print '---------------------------------------------'
            if str(retval) == '0' or 'IF-MIB' in ''.join(lines):
                checked = True
                cname = name

        obj = Asset.objects.get(ip=i[0])

        # yxdown,youxun,unknown
        if checked:
            print 'ip:', i[0], cname
            obj.comm_name = cname
        else:
            print 'ip: ', i[0], 'unknown'
            error_ip.append(i[0])
            obj.comm_name = 'unknown'
        obj.save()
        print u'update ip:%s succ' % i[0]
        print


    for x in error_ip:
        print '**', x


