# encoding: utf-8
import os, time
from datetime import datetime as dt
import paramiko
import traceback
from util import write_log
from jasset.models import Asset
from jasset.asset_api import get_object


def get_ssh(host, port, username, password, timeout=10):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)
    return s


def copy_file_to_server(host, port, username, password, local_dir, remote_dir, fname_list):
    try:
        # ssh root@123.56.195.124 'mkdir -p /root/scripts'
        s = get_ssh(host, port, username, password)
        ssh = s.invoke_shell()

        # 1. pre install openssh-clients first
        install_ssh_cmd = "yum install openssh-clients -y"
        write_log(ip=host, cmd=install_ssh_cmd, title='copy_file', result="")
        print 'run CMD: ', install_ssh_cmd
        ssh.send(install_ssh_cmd + '\n')
        time.sleep(0.5)

        buff = ''
        while 1:
            if '# ' in buff or '$ ' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                time.sleep(1)
            print 'resp:'
            print resp
        print 'install openssh-clients complete..'
        write_log(ip=host, cmd=install_ssh_cmd, title='copy_file', result="mkdir complete..")
        print '-----------------------------------------------------------------------------------------'

        # 2
        mkdir_cmd = "/usr/bin/ssh %s@%s -p %s 'mkdir -p %s'" % (username, host, str(port), remote_dir)
        write_log(ip=host, cmd=mkdir_cmd, title='copy_file', result="")
        print 'run CMD: ', mkdir_cmd
        ssh.send(mkdir_cmd + '\n')
        time.sleep(0.5)

        buff = ''
        while 1:
            if '# ' in buff or '$ ' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                time.sleep(1)
            print 'resp:'
            print resp
        print 'mkdir complete..'
        write_log(ip=host, cmd=mkdir_cmd, title='copy_file', result="mkdir complete..")
        print '-----------------------------------------------------------------------------------------'

        # 3
        # /usr/bin/scp bash_script5 bash_script6 root@123.56.195.124:/root/scripts
        files = ' '.join([os.path.join(local_dir, fn) for fn in fname_list])
        scp_cmd = "/usr/bin/scp %s %s@%s:%s" % (files, username, host, remote_dir)
        print 'run CMD: ', scp_cmd
        write_log(ip=host, cmd=scp_cmd, title='copy_file', result="")
        ssh.send(scp_cmd + '\n')
        time.sleep(0.5)

        buff = ''
        while 1:
            if '# ' in buff or '$ ' in buff:
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                time.sleep(1)
        print 'scp cmd complete..'
        write_log(ip=host, cmd=scp_cmd, title='copy_file', result="scp cmd complete..")
        s.close()
        return 'ok', 'copy files complete !!'
    except Exception, e:
        txt = 'exception while copy files: %s' % str(e)
        return 'fail', txt

if __name__ == '__main__':
    ip = '123.56.195.124'
    port = 22
    username = 'root'
    password = 'Password114418'
    # s = '123.56.195.124	22	root	Password114418'
    # port = get_new_port_by_ip(ip)
    # print 'port: ', port
    host, port, username, password = ip, port, username, password
    # script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
    local_dir = '/home/u1404/scripts'
    # ssh root@123.56.195.124 'mkdir -p /root/scripts'
    remote_dir = '/root/scripts'
    fname_list = ['bash_script2', 'bash_script3']
    copy_file_to_server(host, port, username, password, local_dir, remote_dir, fname_list)

    # ssh = get_ssh(host, port, username, password)
    # exists = test_cmd_exists(ssh, kw='aaa')

    '''
    script_dir = '/var/serconf/nginx/yxdown.com/phone/apple'
    print 'start copy file....'
    copy_files_and_restart_service(host, port, username, password, script_dir)
    '''
    print u'succ'

