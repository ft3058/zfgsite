# coding:utf-8

import time
import paramiko


def change_passwd(host, port, username, password, new_pwd, timeout=10):
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)

        ssh = s.invoke_shell()
        time.sleep(1)
        ssh.send('passwd root\n')

        buff = ''
        while 1:
            if '新的 密码' in buff or 'Password:' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                time.sleep(1)
                # print 'buff1: %s' % buff

        ssh.send(new_pwd)
        ssh.send('\n')

        buff = ''
        while 1:
            if '新的 密码' in buff or 'Password:' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
        ssh.send(new_pwd + '\n')

        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            buff += resp
        s.close()
        result = buff

        return 'ok', result
    except Exception, e:
        return 'fail', str(e)


def init_server():
    """

    :return:
    """


if __name__ == '__main__':
    # host, port, username, password, new_pwd = '111.7.165.43', 16543, 'root', 'qq@20171328', '123456bgf'  # qq@20171328'
    # res = change_passwd(host, port, username, password, new_pwd)
    # print res
    print u'succ'