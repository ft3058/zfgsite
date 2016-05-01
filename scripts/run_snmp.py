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

from jasset.models import Asset
from jmonitor.models import TcpConnCount, DiskSize, InterfaceIo
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


def get_disk_dic(lines):
    dic = {}

    for i in lines:
        l = i.strip()
        if l:
            # lines.append(i.strip())
            if 'hrStorageDescr' in l:
                # HOST-RESOURCES-MIB::hrStorageDescr.37 = STRING: /home
                name = l.split(':')[-1].strip()
                if name == '/home':
                    dic['name'] = '/home'
                    dic['id'] = l.split('hrStorageDescr.')[-1].split('=')[0].strip()
            elif 'hrStorageAllocationUnits.' in l and dic.get('id', 'nnnn') in l:
                # HOST-RESOURCES-MIB::hrStorageAllocationUnits.37 = INTEGER: 4096 Bytes
                dic['unit'] = l.split(':')[-1].strip().split(' ')[0].strip()
            elif 'hrStorageSize.' in l and dic.get('id', 'nnnn') in l:
                # HOST-RESOURCES-MIB::hrStorageSize.37 = INTEGER: 478383983
                dic['total_size'] = int(l.split(':')[-1].strip()) * int(dic['unit']) / (1024*1024*1024)
            elif 'hrStorageUsed.' in l and dic.get('id', 'nnnn') in l:
                # HOST-RESOURCES-MIB::hrStorageUsed.37 = INTEGER: 478379861
                dic['used_size'] = int(l.split(':')[-1].strip()) * int(dic['unit']) / (1024*1024*1024)

    return dic

def get_interface_dic(lines):
  dic0 = {'in': '', 'out': ''}
  dic1 = {'in': '', 'out': ''}
  for i in lines:
    l = i.strip()
    if l:
      if '::ifName' in l:
        # IF-MIB::ifName.2 = STRING: eth0
        if 'eth0' in l.lower():
          dic0['name'] = 'eth0'
          dic0['id'] = l.split('ifName.')[-1].split('=')[0].strip()
        elif 'eth1' in l.lower():
          dic1['name'] = 'eth1'
          dic1['id'] = l.split('ifName.')[-1].split('=')[0].strip()

      elif 'ifHCInOctets' in l:
        # IF-MIB::ifHCInOctets.1 = Counter64: 356609255540
        if 'ifHCInOctets.' + dic0.get('id', 'nnn') in l:
          dic0['in'] = l.split(':')[-1].strip()
        elif 'ifHCInOctets.' + dic1.get('id', 'nnn') in l:
          dic1['in'] = l.split(':')[-1].strip()

      elif 'ifHCOutOctets' in l:
        # IF-MIB::ifHCOutOctets.1 = Counter64: 356609255540
        if 'ifHCOutOctets.' + dic0.get('id', 'nnn') in l:
          dic0['out'] = l.split(':')[-1].strip()
        elif 'ifHCOutOctets.' + dic1.get('id', 'nnn') in l:
          dic1['out'] = l.split(':')[-1].strip()

  res_dic = dic1
  if dic0['in'] not in ['', '0']:
    res_dic = dic0

  if res_dic['in'] == '':
    res_dic['in'] = '0'
  if res_dic['out'] == '':
    res_dic['out'] = '0'

  return res_dic

def parse_host_disk(retval, lines, ip, dic):
    total_size, used_size = 0, 0
    if retval == 0:
        dic = get_disk_dic(lines)
        if dic:
            total_size, used_size = dic.get('total_size', 0), dic.get('used_size', 0)
    else:
        print 'retval is error: val=', retval 

    obj = DiskSize()
    obj.ip = ip
    obj.total = total_size
    obj.used = used_size
    obj.save()
    print 'save disk size succ'

def parse_interface(retval, lines, ip, dic):
    name, insize, outsize = 'eth_none', 0L, 0L
    if retval == 0:
        dic = get_interface_dic(lines)
        if dic:
            name, insize, outsize = dic.get('name', 'eth_no'), long(dic.get('in', 0)), long(dic.get('out', 0))
    else:
        print 'retval is error: val=', retval

    obj = InterfaceIo()
    obj.ip = ip
    obj.name = name
    obj.insize = insize
    obj.outsize = outsize
    obj.save()
    print 'save interface size succ'

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

                # disk size 
                # snmpwalk -v 2c -c  yxdown 218.75.155.46 .1.3.6.1.2.1.25.2.3
                cmd = 'snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.25.2.3' % (community_name, ip)
                retval, lines = exec_cmd(cmd)
                parse_host_disk(retval, lines, ip, dic)

                # interface
                cmd = 'snmpwalk -v 2c -c %s %s .1.3.6.1.2.1.31.1.1.1' % (community_name, ip)
                retval, lines = exec_cmd(cmd)
                parse_interface(retval, lines, ip, dic)

        print u'%s is ended..' % self.thread_name


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



