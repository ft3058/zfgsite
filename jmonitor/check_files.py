# coding:utf8
"""
srwxr-x---  1 root    root           0 Feb  8 07:02 Aegis-<Guid(5A2C30A2-A87D-490A-9281-6765EDAD7CBA)>
-rw-r--r--  1 root    root           0 Feb 23 12:37 a.txt
-rw-r--r--  1 root    root    45065714 Mar  9 16:41 csto-stderr---supervisor-cJTnSC.log
-rw-------  1 root    root    52428838 Feb 24 18:32 csto-stderr---supervisor-cJTnSC.log.1
-rw-------  1 root    root           0 Feb  8 07:02 csto-stdout---supervisor-iud7cZ.log
-rw-r--r--  1 root    root           0 Mar  9 16:37 empty
-rw-r--r--  1 root    root           0 Mar  9 16:38 empty file name.txt
-rw-r--r--  1 root    root           0 Mar  9 16:37 file
-rw-------  1 root    root       15035 Mar  6 02:17 get_new_proxy-stderr---supervisor-MOH_Bc.log
-rw-------  1 root    root     1386928 Mar  6 02:17 get_new_proxy-stdout---supervisor-fBBXrH.log
-rw-r--r--  1 root    root         408 Mar  9 15:31 id_rsa_centos65.pub
srwxrwxrwx  1 mongodb nogroup        0 Feb  8 07:02 mongodb-27017.sock
-rw-r--r--  1 root    root           0 Mar  9 16:37 name.txt
srwxr-x---  1 root    root           0 Mar  3 16:02 qtsingleapp-aegisG-46d2
-rw-r-----  1 root    root           0 Feb  8 07:02 qtsingleapp-aegisG-46d2-lockfile
srwxrwxrwx  1 root    root           0 Feb  8 07:02 qtsingleapp-aegiss-a5d2
-rw-rw-rw-  1 root    root           0 Feb  8 07:02 qtsingleapp-aegiss-a5d2-lockfile
-rw-------  1 root    root       10972 Mar  9 16:09 site_rgb6-stderr---supervisor-MURJSi.log
-rw-------  1 root    root      134288 Mar  9 14:39 site_rgb6-stdout---supervisor-2vv3mu.log
-rw-r--r--  1 root    root       16800 Mar  6 02:17 supervisord.log
-rw-r--r--  1 root    root           5 Feb  8 07:02 supervisord.pid
srwx------  1 root    root           0 Feb  8 07:02 supervisor.sock
-rw-------  1 root    root    11891802 Mar  9 16:41 taskcity-stderr---supervisor-buIBPp.log
-rw-------  1 root    root           0 Feb  8 07:02 taskcity-stdout---supervisor-KT1dzQ.log
"""

import paramiko


class File(object):
    def __init__(self, fname, user, group, size, sdt):
        self.fname = fname
        self.user = user
        self.group = group
        self.size = size
        self.sdt = sdt

    def __str__(self):
        s = 'file name: %s\n' % self.fname
        s += 'user: %s\n' % self.user
        s += 'group: %s\n' % self.group
        s += 'size: %s\n' % self.size
        s += 'sdt: %s\n' % self.sdt
        return s


def parse_files(lines):
    file_obj_list = []
    for l in lines:
        l = l.strip()
        if l.startswith('d'):
            continue
        # normal value: [u'-rw-r--r--', u'1', u'root', u'root', u'0', u'Mar', u'9', u'16:37', u'name.txt']
        sp = filter(None, [x.strip() for x in l.split(' ')])
        if len(sp) < 9:
            continue
        fname = l.split(sp[7])[-1].strip()
        fobj = File(fname, sp[2], sp[3], sp[4], '%s %s %s' % (sp[5], sp[6], sp[7]))
        print '--------'
        print fobj
        print


def check():
    IP = '115.29.185.223'
    PORT = 22
    USERNAME = 'root'
    PASSWORD = 'Password11441890'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, PORT, USERNAME, PASSWORD)

    cmd = "ls -al /tmp"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.readlines()
    ssh.close()

    parse_files(lines)



if __name__ == '__main__':
    check()


