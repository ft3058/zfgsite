# coding:utf8
import time
from datetime import datetime as dt
import paramiko
import traceback
from util import write_log
from jasset.models import Asset
from jasset.asset_api import get_object


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

        cmd = 'cd /tmp\n'
        write_log(ip=host, cmd=cmd, title='install_softs')
        ssh.send(cmd)

        buff = ''
        while 1:
            if '# ' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                time.sleep(1)
                # print 'buff1: %s' % buff
        write_log(ip=host, cmd=cmd, title='install_softs', result='entered /tmp')

        # install wget first
        cmd = 'yum install wget -y\n'
        write_log(ip=host, cmd=cmd, title='install_softs')
        ssh.send(cmd)
        while 1:
            if 'Nothing to do' in buff or 'Complete!' in buff:
                # print u'install wget succ..'
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
        write_log(ip=host, cmd=cmd, title='install_softs', result='succ')

        # print 'start wget install.sh'
        cmd = 'wget http://softck.yxdown.com/others/install/install.sh\n'
        ssh.send(cmd)
        write_log(ip=host, cmd=cmd, title='install_softs', result='succ')

        buff = ''
        while 1:
            if ('saved' in buff or '已保存' in buff) and '# ' in buff:
                # print u'down install.sh succ..'
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
            # print '------------------'
            # print 'buff: ', buff
            time.sleep(1)

        cmd = 'nohup sh install.sh &\n'
        write_log(ip=host, cmd=cmd, title='install_softs', result='succ')
        ssh.send(cmd)
        time.sleep(1)

        ssh.send('\n')
        time.sleep(5)
        # print 'wait for install.sh complete ... '

        t1 = time.time()
        retry_times = 0
        while 1:
            try:
                retry_times += 1
                cmd = 'ps -ef | grep install.sh\n'
                ssh.send(cmd)
                time.sleep(1)
                resp = ssh.recv(9999)
                # print '++++++++++++++++++++++++out start+++++++++++++++++++++++++++'
                # print 'retry times: %d' % retry_times
                # print resp
                write_log(ip=host, cmd=cmd, title='install_softs', result=resp)
                # print '++++++++++++++++++++++++out end+++++++++++++++++++++++++++++'
                # print
                if 'reboot NOW' in resp:
                    write_log(ip=host, cmd=cmd, title='install_softs', result="reboot NOW")
                    return 'ok', 'wait for restart !'
            except Exception, e:
                if 'Socket is closed' in str(e):
                    write_log(ip=host, cmd=cmd, title='install_softs', result="Socket is closed, wait for restart !")
                    return 'ok', 'wait for restart !'
                else:
                    write_log(ip=host, cmd=cmd, title='install_softs', result="fail, %s" % str(e))
                    return 'fail', str(e)
            time.sleep(3)

        s.close()

        t2 = time.time()
        # print 'all second: ', int(t2 - t1)
        result = 'succ'

        write_log(ip=host, cmd='', title='install_softs', result="complete all")
        return 'ok', result
    except Exception, e:
        write_log(ip=host, cmd='', title='install_softs', result="Exception while install_softs(): %s" % str(e))
        try:
            s.close()
        except:
            pass
        return 'fail', str(e)


def get_ssh(host, port, username, password,timeout=10):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)
    return s


def get_new_port_by_ip__(ip):
    """ manual """
    sp = ip.split('.')
    part1 = sp[-2] if len(sp[-2]) <= 2 else sp[-2][:2]
    part2 = sp[-1] if len(sp[-1]) <= 2 else sp[-1][:2]
    return int(part1+part2)


def get_new_port_by_ip(ip):
    """ get new password and port from db """
    asset = get_object(Asset, ip=ip)
    return asset.passwd, str(asset.port)


def copy_files_and_restart_service(host, port, username, password, script_dir):
    try:
        s = get_ssh(host, port, username, password)
        ssh = s.invoke_shell()
        cmd = 'cd %s\n' % script_dir
        write_log(ip=host, cmd=cmd, title='copy_file', result="")
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        # print 'complete..'

        cmd = '/bin/cp *.sh /root \n'
        write_log(ip=host, cmd=cmd, title='copy_file', result="")
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        # print 'complete..'

        cmd = '/bin/rm /usr/local/nginx/conf/vhost/*.conf \n'
        write_log(ip=host, cmd=cmd, title='copy_file', result="")
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        # print 'complete..'

        cmd = '/bin/cp *.conf /usr/local/nginx/conf/vhost/ \n'
        write_log(ip=host, cmd=cmd, title='copy_file', result="")
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        # print 'complete..'

        cmd = 'service nginx restart \n'
        write_log(ip=host, cmd=cmd, title='copy_file', result="")
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(1)
        # print 'complete..'
        write_log(ip=host, cmd='', title='copy_file', result="copy complete .. ")
        s.close()
    except:
        try:
            s.close()
        except:
            pass


def init_server(host, port, username, password, script_path):
    try:
        # 1. install software
        write_log(ip=host, user=username, title='start to install softs', result="%s-%s-%s-%s-%s" % (host, str(port), username, password, script_path))
        tag, res = install_softs(host, port, username, password)

        # print 'install tag, res = ', tag, res
        if not script_path and tag == 'ok':
            return 'ok', 'install.sh run success!'

        # 2. copy file and restart nginx
        elif tag == 'ok' or 'SSH session not active' in res:
            # connect first
            retry_times = 0
            password, port = get_new_port_by_ip(host)
            # print 'new password, port : ', password, port
            write_log(ip=host, cmd='', title='start connect', result="ip:%s -new:  password:%s port:%s" % (host, password, port))

            while retry_times <= 99:
                try:
                    ssh = get_ssh(host, port, username, password)
                    # print 'connect succ..'
                    write_log(ip=host, cmd='paramiko get_ssh()', title='ping ssh', result="ssh connect succ")
                    ssh.close()
                    break
                except Exception, e:
                    # print '----------------------------------'
                    # print 'connect error:', str(e)
                    # print 'retry_times = ', retry_times
                    write_log(ip=host, cmd='paramiko get_ssh()', title='ping ssh', result="ssh : connect error: %s" % str(e))
                    retry_times += 1
                    try:
                        ssh.close()
                    except:pass
                    time.sleep(5)
            else:
                write_log(ip=host, cmd='paramiko get_ssh()', title='ping ssh', result='connect time out after retart !!, retry times: %d' % retry_times)
                return 'fail', 'connect time out after retart !!, retry times: %d' % retry_times

            # script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
            # print 'start copy file....'
            write_log(ip=host, cmd='', title='copy_file', result="start copy files")
            copy_files_and_restart_service(host, port, username, password, script_path)
            write_log(ip=host, cmd='', title='copy_file', result="copy files succ, init server complete !!")
            return 'ok', 'init server complete !!'
        else:
            return tag, res
    except Exception, e:
        txt = 'exception while init server: %s' % str(e)
        return 'fail', txt

if __name__ == '__main__':
    ip = '111.7.165.40'
    port = get_new_port_by_ip(ip)
    # print 'port: ', port
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
    # print u'succ'