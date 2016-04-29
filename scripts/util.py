# coding:utf8
"""
disk names :

HOST-RESOURCES-MIB::hrStorageDescr.1 = STRING: Physical memory
HOST-RESOURCES-MIB::hrStorageDescr.3 = STRING: Virtual memory
HOST-RESOURCES-MIB::hrStorageDescr.6 = STRING: Memory buffers
HOST-RESOURCES-MIB::hrStorageDescr.7 = STRING: Cached memory
HOST-RESOURCES-MIB::hrStorageDescr.10 = STRING: Swap space
HOST-RESOURCES-MIB::hrStorageDescr.31 = STRING: /
HOST-RESOURCES-MIB::hrStorageDescr.35 = STRING: /dev/shm
HOST-RESOURCES-MIB::hrStorageDescr.36 = STRING: /boot
HOST-RESOURCES-MIB::hrStorageDescr.37 = STRING: /home

disk total:
HOST-RESOURCES-MIB::hrStorageSize.1 = INTEGER: 8018388
HOST-RESOURCES-MIB::hrStorageSize.3 = INTEGER: 12212684
HOST-RESOURCES-MIB::hrStorageSize.6 = INTEGER: 8018388
HOST-RESOURCES-MIB::hrStorageSize.7 = INTEGER: 493640
HOST-RESOURCES-MIB::hrStorageSize.10 = INTEGER: 4194296
HOST-RESOURCES-MIB::hrStorageSize.31 = INTEGER: 25803080
HOST-RESOURCES-MIB::hrStorageSize.35 = INTEGER: 1002298
HOST-RESOURCES-MIB::hrStorageSize.36 = INTEGER: 396672
HOST-RESOURCES-MIB::hrStorageSize.37 = INTEGER: 93244370

disk used:


"""

import subprocess


def exec_cmd(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	lines = []
	for line in p.stdout.readlines():
		l = line.strip()
		if l:
			lines.append(l)
	
	retval = p.wait()
	# print 'retval: ', retval
	return retval, lines


if __name__ == '__main__':
	# cmd = 'snmpwalk -v 2c -c youxun 182.162.20.39 .1.3.6.1.2.1.25.2.3.1.3'
	cmd = 'snmpwalk -v 2c -c youxun 182.162.20.39 .1.3.6.1.2.1.6.9.0'
	cmd = 'snmpwalk -v 2c -c youxun 182.162.20.39 .1.3.6.1.2.1.25.2.3.1.6'
	retval, lines = exec_cmd(cmd)
	if retval == 0:
		for l in lines:
			print l
	else:
		print 'retval is error: val=', retval


