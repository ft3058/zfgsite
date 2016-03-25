"""
/home/wxd/env_jump_wxd/bin/python /home/wxd/project/jumpserver/test/check_conn.py
['60.169.76.31', 7631, 'root', 'a917da869b01']
<class 'paramiko.channel.ChannelFile'>
- uid=root
- gid=root
- port = 19873
- list = no
- max connections=36000
- use chroot=no
- log file=/var/log/rsyncd.log
- pid file=/var/run/rsyncd.pid
- lock file=/var/run/rsyncd.lock
- auth users = root
- strict modes = yes
- secrets file = /etc/rsyncd.up
- ignore errors = yes
- read only = no
- hosts allow = *
- hosts deny = *
-
-
- # ++++++++ 391k.com config  ++++++++
-
- [391kCom]
- path=/home/391k
- [391kComApk]
- path=/home/391k/apk
- [391kComAzs]
- path=/home/391k/azs
- [391kComBt]
- path=/home/391k/bt
- [391kComDownnds]
- path=/home/391k/downnds
- [391kComDnb]
- path=/home/391k/dnb
-
succ

Process finished with exit code 0
"""


import paramiko

def test():
    # s = '111.38.14.133 	14133 	root 	28a65a71ea7e'
    # s = '119.36.192.21 	19221 	root 	206ca3f0971f'
    s = '112.123.169.55 	22 	root 	876eb976ee03'
    s = '60.169.76.31 	7631 	root 	a917da869b01'  # 391kCom
    s = '112.123.169.36 	16936 	root 	yxdown@10070'
    s = filter(None, [x.strip() if n != 1 else int(x.strip()) for n, x in enumerate(s.split(' '))])
    print s

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(s[0], s[1], s[2], s[3], timeout=4)

    # cmd = "ls -al /home/391k/apk"
    cmd = "cat /etc/rsyncd.conf"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print type(stdout)
    txt = stdout.read()

    # with open('391.txt', 'w') as f:
    for l in txt.split('\n'):
        print '-', l
        # f.write(l + '\n')

    print u'succ'
    # error while file num too many
    '''
    print '----------------'
    print type(stderr), stderr
    lines = stdout.readlines()  # .decode('gbk')
    ssh.close()
    for l in lines:
        print l.strip()
    '''

def get_ssh(host, port, username, password,timeout=5):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)
    return s

def test1():
    ip = '111.7.165.40'
    host, port, username, password = ip, 1640, 'root', 'qq@20171328'
    ssh = get_ssh(host, port, username, password)
    print 'ssh: ', ssh

if __name__ == '__main__':
    # test()
    test1()
    pass
