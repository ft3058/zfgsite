# coding:utf8
__author__ = 'wxd'

import paramiko


CONN = '120.131.71.41 	32812 	root 	Q9Nf8KkU53gc6zT'
s = filter(None, [x.strip() if n != 1 else int(x.strip()) for n, x in enumerate(CONN.split(' '))])
print s


class CateServer(object):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(s[0], s[1], s[2], s[3], timeout=6)

    def outprint(self, stdout):
        print type(stdout)
        txt = stdout.read()
        # with open('391.txt', 'w') as f:
        for l in txt.split('\n'):
            print '-', l
            # f.write(l + '\n')

    def test(self):
        # cmd = "ls -al /home/391k/apk"
        cmd = "cat /etc/rsyncd.conf"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        self.outprint(stdout)
        print u'succ'


    def update_jump_code(self):
        cmd = "ls -al /data/www/yxyw/jumpserver"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        self.outprint(stdout)

    def __del__(self):
        try:
            self.ssh.close()
        except:
            pass
        print 'del ssh succ'


if __name__ == '__main__':
    cs = CateServer()
    # cs.test()
    cs.update_jump_code()