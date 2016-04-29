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
	retval, lines = exec_cmd(cmd)
	if retval == 0:
		for l in lines:
			print '-', l
	else:
		print 'retval is error: val=', retval


