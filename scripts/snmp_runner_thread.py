# coding:utf8
"""
| $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysLocation.0
from multiple-concurrent-queries.py
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
from jmonitor.models import TcpConnCount
from util import *

q = Queue()
THREAD_NUM = 10


def parse_tcp_conn_count(retval, lines, ip, dic):
    if retval == 0:
        s = lines[0]
        print 'lines[0]: %s' % s
        cnt = int(s.split(':')[-1].strip())       
    else:
        print 'retval is error: val=', retval 
        cnt = 0

    obj = TcpConnCount()
    obj.cnt=cnt
    obj.ip=ip
    obj.save()
    print 'save succ'



def failure(errorIndication, hostname):
    print('%s failure: %s' % (hostname, errorIndication))


def init_all_assets():
    assets = Asset.objects.all()
    # assets = Asset.objects.filter(ip='112.123.169.32')  # 111.7.165.42 218.75.155.46
    for t in assets:
        q.put({'ip': t.ip})


class SnmpThread(Thread):

    def __init__(self, thread_name):
        super(SnmpThread, self).__init__()
        self.thread_name = thread_name

    def run(self):
        print u'%s is running...' % self.thread_name
        while True:
            if q.qsize() <= 0:
                print u'there is no more tasks.'
                break
            else:
                dic = q.get()
                ip = dic['ip']
                print 'ip: %s' % ip
                community_name = COMMUNITY_NAME1
                if ip in NEW_ASSETS:
                    community_name = COMMUNITY_NAME2

                # tcp conn
                cmd = 'snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.6.9.0' % (community_name, ip)
                retval, lines = exec_cmd(cmd)
                parse_tcp_conn_count(retval, lines, ip, dic)              

                '''    
                for dic in OID_LIST:
                    if dic['method'] == 'get':
                        # res = get_cmd_val(ip, 'my-agent', community_name, dic['oid'])

                        res = get_cmd_val(ip, 'my-agent', community_name, dic['oid'])
                    elif dic['method'] == 'walk':
                        res = get_next_cmd_val(ip, 'my-agent', community_name, dic['oid'])

                    if len(res) == 1:
                        print 'ERROR: %s' % res[0]
                    else:
                        result = success(res, ip, dic)
                        print 'result = ', result'''


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


def test():
    pass

if __name__ == '__main__':

    while True:
        main()
        time.sleep(60*5)
    # test()



