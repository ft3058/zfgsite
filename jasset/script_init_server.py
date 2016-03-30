# coding:utf8
import time
from datetime import datetime as dt
import paramiko
import traceback


def install_softs(host, port, username, password, timeout=10):
    """
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
        not_found_time = 0
        while 1:
            if test_cmd_exists(s):
                print 'install.sh exists, continue', dt.now()
            else:
                not_found_time += 1
                print 'install.sh not found times = [ %d ] ---->' % not_found_time, dt.now()
                if not_found_time > 3:
                    print 'not_found_time > 3, break'
                    break
            time.sleep(3)

        t2 = time.time()
        print 'all second: ', int(t2 - t1)
        s.close()
        result = 'succ'

        return 'ok', result
    except Exception, e:
        return 'fail', str(e)

def test_cmd_exists(s, kw='sh install.sh'):
    try:
        ssh = s.invoke_shell()
        ssh.send('ps -ef | grep install.sh\n')
        time.sleep(1)
        resp = ssh.recv(9999)
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print 'resp: ', resp
        if kw in resp:
            return True
        return False
    except Exception, e:
        print traceback.print_exc()
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
    cmd = 'cd %s\n' % script_dir
    print 'run CMD: ', cmd
    ssh.send(cmd)
    time.sleep(0.5)
    print 'complete..'

    cmd = '/bin/cp *.sh /root \n'
    print 'run CMD: ', cmd
    ssh.send(cmd)
    time.sleep(0.5)
    print 'complete..'

    cmd = '/bin/rm /usr/local/nginx/conf/vhost/*.conf \n'
    print 'run CMD: ', cmd
    ssh.send(cmd)
    time.sleep(0.5)
    print 'complete..'

    cmd = '/bin/cp *.conf /usr/local/nginx/conf/vhost/ \n'
    print 'run CMD: ', cmd
    ssh.send(cmd)
    time.sleep(0.5)
    print 'complete..'

    cmd = 'service nginx restart \n'
    print 'run CMD: ', cmd
    ssh.send(cmd)
    time.sleep(1)
    print 'complete..'

    s.close()


def init_server(host, port, username, password, script_path):
    try:
        tag, res = install_softs(host, port, username, password)

        print 'install tag, res = ', tag, res
        if tag == 'ok' or 'SSH session not active' in res:
            # connect first
            retry_times = 0
            port = get_new_port_by_ip(host)
            print 'new port: ', port
            while retry_times <= 99:
                try:
                    ssh = get_ssh(host, port, username, password)
                    print 'connect succ..'
                    ssh.close()
                    break
                except Exception, e:
                    print '----------------------------------'
                    print 'connect error:', str(e)
                    print 'retry_times = ', retry_times
                    retry_times += 1
                    time.sleep(5)
            else:
                return 'fail', 'connect time out after retart !!, retry times: %d' % retry_times

            # script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
            print 'start copy file....'
            copy_files_and_restart_service(host, port, username, password, script_path)
            return 'ok', 'init server complete !!'
        else:
            return tag, res
    except Exception, e:
        txt = 'exception while init server: %s' % str(e)
        return 'fail', txt

if __name__ == '__main__':
    ip = '111.7.165.40'
    port = get_new_port_by_ip(ip)
    print 'port: ', port
    host, port, username, password = ip, port, 'root', 'qq@20171328'
    script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
    init_server(host, port, username, password, script_dir)

    # ssh = get_ssh(host, port, username, password)
    # exists = test_cmd_exists(ssh, kw='aaa')

    '''
    script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
    print 'start copy file....'
    copy_files_and_restart_service(host, port, username, password, script_dir)
    '''
    print u'succ'