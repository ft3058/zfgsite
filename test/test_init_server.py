# coding:utf8
import time
from datetime import datetime as dt
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
        print 'start wget install.sh'
        ssh.send('wget http://softck.yxdown.com/others/install/install.sh\n')

        buff = ''
        while 1:
            if ('saved' in buff or '已保存' in buff) and '# ' in buff:
                print u'down install.sh succ..'
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
            print '------------------'
            print 'buff: ', buff
            time.sleep(1)

        print 'start to run install.sh...'

        ssh.send('nohup sh install.sh &\n')
        time.sleep(1)
        ssh.send('\n')
        time.sleep(5)

        print 'wait for install.sh complete ... '

        t1 = time.time()
        while 1:
            if test_cmd_exists(s):
                print 'install.sh exists, continue', dt.now()
            else:
                print 'not exists... break', dt.now()
                break
            time.sleep(2)

        t2 = time.time()
        print 'all second: ', int(t2 - t1)
        s.close()
        result = 'succ'

        return 'ok', result
    except Exception, e:
        return 'fail', str(e)

def test_cmd_exists(s, kw='install.sh'):
    ssh = s.invoke_shell()
    ssh.send('ps -ef | grep sh\n')
    time.sleep(1)
    resp = ssh.recv(9999)
    # print 'resp: ', resp
    if kw in resp:
        return True
    return False

def get_ssh(host, port, username, password,timeout=10):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)
    return s

def get_new_port_by_ip(ip):
    sp = ip.split('.')
    part1 = sp[-2] if len(sp[-2]) <= 2 else sp[-2][:2]
    part2 = sp[-1] if len(sp[-1]) <= 2 else sp[-1][:2]
    return int(part1+part2)


def copy_files_and_restart_service(host, port, username, password, script_dir):
    s = get_ssh(host, port, username, password)
    ssh = s.invoke_shell()
    ssh.send('cd %s\n' % script_dir)
    time.sleep(1)
    ssh.send('/bin/cp *.sh /root \n')
    time.sleep(1)
    ssh.send('/bin/cp *.conf /usr/local/nginx/conf/vhost/ \n')
    time.sleep(1)
    ssh.send('service nginx restart \n')
    time.sleep(5)
    s.close()

if __name__ == '__main__':
    ip = '111.7.165.40'
    port = get_new_port_by_ip(ip)
    print 'port: ', port
    host, port, username, password = ip, port, 'root', 'qq@20171328'

    tag, res = init_server(host, port, username, password)
    # ssh = get_ssh(host, port, username, password)
    # exists = test_cmd_exists(ssh, kw='aaa')
    print 'install tag, res = ', tag, res
    if tag == 'ok' or 'SSH session not active' in res:
        # connect first
        wait_second = 0
        while wait_second <= 60*10:
            try:
                ssh = get_ssh(host, port, username, password)
                print 'connect succ..'
                ssh.close()
                break
            except Exception, e:
                print '----------------------------------'
                print 'connect error:', str(e)
                print 'wait_second = ', wait_second
                wait_second += 5
                time.sleep(5)

        script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
        print 'start copy file....'
        copy_files_and_restart_service(host, port, username, password, script_dir)
        print 'complete init server !!!!'
    else:
        print 'exception while init server'

    '''
    script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
    print 'start copy file....'
    copy_files_and_restart_service(host, port, username, password, script_dir)
    '''
    print u'succ'