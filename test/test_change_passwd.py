__author__ = 'wxd'
import time
import paramiko

s = '111.7.165.43 	16543 	root 	qq@20171328'
s = filter(None, [x.strip() if n != 1 else int(x.strip()) for n, x in enumerate(s.split(' '))])
print s

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(s[0], s[1], s[2], s[3], timeout=4)


def cat_text():
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

    for l in lines:
        print l.strip()
    '''

def output(txt):
    print '----output----'
    # with open('391.txt', 'w') as f:
    for l in txt.split('\n'):
        print '-', l
        # f.write(l + '\n')


def test():
    cmd = "passwd root"
    stdin, stdout, stderr = ssh.exec_command(cmd)

    txt = stdout.read()
    output(txt)
    print '--1--'
    time.sleep(1)
    stdin.write('qq@20171328'+'\n')
    time.sleep(1)
    txt = stdout.read()
    output(txt)

    stdin.write('qq@20171328'+'\n')
    stdin.flush()

    txt = stdout.read()
    output(txt)

    print u'succ'


test()
ssh.close()