# coding:utf8
"""

218.75.155.46	22	root	20ebf66325a3

Load

           1 minute Load: .1.3.6.1.4.1.2021.10.1.3.1
           5 minute Load: .1.3.6.1.4.1.2021.10.1.3.2
           15 minute Load: .1.3.6.1.4.1.2021.10.1.3.3
CPU

           percentage of user CPU time:    .1.3.6.1.4.1.2021.11.9.0
           raw user cpu time:                  .1.3.6.1.4.1.2021.11.50.0
           percentages of system CPU time: .1.3.6.1.4.1.2021.11.10.0
           raw system cpu time:              .1.3.6.1.4.1.2021.11.52.0
           percentages of idle CPU time:   .1.3.6.1.4.1.2021.11.11.0
           raw idle cpu time:                   .1.3.6.1.4.1.2021.11.53.0
           raw nice cpu time:                  .1.3.6.1.4.1.2021.11.51.0
Memory Statistics

           Total Swap Size:                .1.3.6.1.4.1.2021.4.3.0
           Available Swap Space:         .1.3.6.1.4.1.2021.4.4.0
           Total RAM in machine:          .1.3.6.1.4.1.2021.4.5.0
           Total RAM used:                  .1.3.6.1.4.1.2021.4.6.0
           Total RAM Free:                   .1.3.6.1.4.1.2021.4.11.0
           Total RAM Shared:                .1.3.6.1.4.1.2021.4.13.0
           Total RAM Buffered:              .1.3.6.1.4.1.2021.4.14.0
           Total Cached Memory:           .1.3.6.1.4.1.2021.4.15.0

"""
server_list = [
    {'ip': '123.56.195.124', 'name': 'public'},
    {'ip': 'localhost', 'name': 'public'},
    {'ip': '218.75.155.46', 'name': 'yxdown'},
]

S = server_list[2]


OIDS_bak = {
    'tcp_conn_count': '.1.3.6.1.2.1.6.9.0',
    'disc_total_size': '.1.3.6.1.2.1.25.2.3.1.5',
    'disc_used_size': '.1.3.6.1.2.1.25.2.3.1.6',

    'all_interface': '.1.3.6.1.2.1.31.1.1.1.1',
    # 'ifInOctets': '.1.3.6.1.2.1.2.2.1.10',
    # 'ifOutOctets': '.1.3.6.1.2.1.31.1.1.1.6',
    'ifHCInOctets': '.1.3.6.1.2.1.31.1.1.1.6',  # 64bit
    'ifHCOutOctets': '.1.3.6.1.2.1.31.1.1.1.10',# 64bit

    # --------------------------
    # SNMPv2-MIB::sysDescr.0 = Linux localhost.localdomain 2.6.32-504.el6.x86_64 #1 SMP Wed Oct 15 04:27:16 UTC 2014 x86_64
    'sys_info': (1,3,6,1,2,1,1,1,0),
    'load': (1,3,6,1,4,1,2021,10,1,3,1),
    'memory_total': (1,3,6,1,4,1,2021,4,5,0),
    'memory_free': (1,3,6,1,4,1,2021,4,6,0),
    'memory_buffered': (1,3,6,1,4,1,2021,4,14,0),
    'memory_cached': (1,3,6,1,4,1,2021,4,15,0),
    'cpu_idle': (1,3,6,1,4,1,2021,11,11,0),

    # from cacti
    'hrDiskIOIndex': (1,3,6,1,4,1,2021,13,15,1,1,1),
    'hrStorageIndex': (1,3,6,1,2,1,25,2,3,1,1),
    'hrStorageDescr': '.1.3.6.1.2.1.25.2.3.1.3',

    # SNMPv2-MIB::sysUpTime.0 = 901903107
    'sysUpTime': (1, 3, 6, 1, 2, 1, 1, 3, 0),
    'snmpTrapAddress': (1, 3, 6, 1, 6, 3, 18, 1, 3, 0),
    'snmpTrapCommunity': (1, 3, 6, 1, 6, 3, 18, 1, 4, 0),
    'snmpTrapOID': (1, 3, 6, 1, 6, 3, 1, 1, 4, 1, 0),
    'snmpTrapEnterprise': (1, 3, 6, 1, 6, 3, 1, 1, 4, 3, 0),
    # '_genTrap = ObjectIdentifier((1, 3, 6, 1, 6, 3, 1, 1, 5, 1))
}

OIDS = {
    # 'tcp_conn_count':   '.1.3.6.1.2.1.6.9.0',
    'tcp_conn_count':   (1,3,6,1.2,1,6,9,0),
    'disc_total_size':  '.1.3.6.1.2.1.25.2.3.1.5',
    'disc_used_size':   '.1.3.6.1.2.1.25.2.3.1.6',

    'all_interface':    '.1.3.6.1.2.1.31.1.1.1.1',
    'ifHCInOctets':     '.1.3.6.1.2.1.31.1.1.1.6',
    'ifHCOutOctets':    '.1.3.6.1.2.1.31.1.1.1.10',
}

CHECK_KEY_LIST = OIDS.keys()
COMMUNITY_NAME = 'yxdown'