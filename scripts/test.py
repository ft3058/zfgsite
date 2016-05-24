# coding:utf8
"""

"""

import os, sys


def parse_disk():
  dic = {}
  with open('files/host_disk_info.txt') as f:
    for i in f.readlines():
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

  print dic

def parse_interface():
  dic0 = {'in': '', 'out': ''}
  dic1 = {'in': '', 'out': ''}
  with open('files/interface.txt') as f:
    for i in f.readlines():
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
          if 'ifHCInOctets.' + dic0['id'] in l:
            dic0['in'] = l.split(':')[-1].strip()
          elif 'ifHCInOctets.' + dic1['id'] in l:
            dic1['in'] = l.split(':')[-1].strip()

        elif 'ifHCOutOctets' in l:
          # IF-MIB::ifHCOutOctets.1 = Counter64: 356609255540
          if 'ifHCOutOctets.' + dic0['id'] in l:
            dic0['out'] = l.split(':')[-1].strip()
          elif 'ifHCOutOctets.' + dic1['id'] in l:
            dic1['out'] = l.split(':')[-1].strip()

  if dic0['in'] not in ['', '0']:
    return dic0
  else:
    return dic1



dic = parse_interface()
print dic