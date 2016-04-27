# coding:utf8
"""
| $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysLocation.0
from multiple-concurrent-queries.py
"""
import os, sys
from random import choice
from Queue import Queue
from threading import Thread
from twisted.internet.defer import DeferredList
from twisted.internet.task import react
from pysnmp.hlapi.twisted import *
from snmp_api import get_cmd_val, get_next_cmd_val
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

# from juser.models import User
from jasset.models import Asset

q = Queue()
THREAD_NUM = 1


def init_all_assets():
    # assets = Asset.objects.all()
    assets = Asset.objects.filter(ip='112.123.169.32')  # 111.7.165.42 218.75.155.46
    for t in assets:
        q.put({'ip': t.ip})

def success((errorStatus, errorIndex, varBinds), hostname):
    if errorStatus:
        print('%s: %s at %s' % (hostname,
                                errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


def failure(errorIndication, hostname):
    print('%s failure: %s' % (hostname, errorIndication))


index = 1

class SnmpThread(Thread):

    def __init__(self, thread_name):
        super(SnmpThread, self).__init__()
        self.thread_name = thread_name

    def run(self):
        global index
        print u'%s is running...' % self.thread_name
        while True:
            if q.qsize() <= 0:
                print u'there is no more tasks.'
                break
            else:
                dic = q.get()
                ip = dic['ip']
                print 'ip: %s' % ip
                for key in CHECK_KEY_LIST:
                    # get_cmd_val(addr, community_index, community_name, oid, port=161)
                    res = get_next_cmd_val(ip, 'my-agent' + str(index), COMMUNITY_NAME, OIDS[key])
                    index += 1
                    if len(res) == 1:
                        print 'ERROR: %s' % res[0]
                    else:
                        errorIndication, errorStatus, errorIndex, varBinds = res
                        print 'key:', key, errorIndication, errorStatus, errorIndex, varBinds

        print u'%s is ended..'


def main():
    # ip = 'demo.snmplabs.com'
    # ip = '123.56.195.124'
    init_all_assets()

    thread_list = []
    for i in range(1, THREAD_NUM+1):
        t = SnmpThread('name_%d' % i)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    main()


