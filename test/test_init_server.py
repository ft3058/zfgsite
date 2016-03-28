# coding:utf8
import time
import paramiko





def init_server(host, port, username, password, timeout=10):
    """

    :return:
    """
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)

        ssh = s.invoke_shell()
        time.sleep(1)
        ssh.send('cd /tmp\n')

        buff = ''
        while 1:
            if '# ' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                time.sleep(1)
                # print 'buff1: %s' % buff
        print 'entered /tmp'

        # install wget first
        ssh.send('yum install wget -y\n')
        while 1:
            if 'Nothing to do' in buff or 'Complete!' in buff:
                print u'install wget succ..'
                break
            else:
                resp = ssh.recv(9999)
                buff += resp

        ssh.send('wget http://softck.yxdown.com/others/install/install.sh\n')

        buff = ''
        while 1:
            if 'saved' in buff and '# ' in buff:
                print u'wget install.sh succ..'
                break
            else:
                resp = ssh.recv(9999)
                buff += resp

        print 'succ wget install.sh'

        time.sleep(2000)

        ssh.send('nohup sh install.sh &\n')

        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff += resp
        s.close()
        result = buff

        return 'ok', result
    except Exception, e:
        return 'fail', str(e)

if __name__ == '__main__':
    host, port, username, password = '111.7.165.40', 22, 'root', 'qq@20171328'
    res = init_server(host, port, username, password)
    print res
    print u'succ'