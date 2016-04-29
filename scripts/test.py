# coding:utf8
"""

"""

import os, sys


dic = {}
with open('host_disk_info.txt') as f:
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

