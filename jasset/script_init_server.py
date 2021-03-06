# coding:utf8
import re
import os
import time
from datetime import datetime as dt
import paramiko
import traceback
from util import write_log
from jasset.models import Asset
from jasset.asset_api import get_object
from script_copy_files import copy_file_to_server
from jumpserver.settings import LOCAL_FILE_DIR


def get_paths(asset): # 接受Asset对象,返回所有路径列表
    path = []
    group1_list = asset.group1.all()
    if group1_list:
        for gro in group1_list: # 循环所有组
            path.extend(clear_module_path(gro.module_path)) # 传递group1的module_path
        else:
            return path


def clear_module_path(module_path):
    # 接受一个字符参数,返回一个清洗过的路径列表
    paths = []
    module_path_split = re.split('=|,', module_path)
    print module_path_split
    for path in module_path_split:
        counts = path.count('/')
        if counts:
            # if counts > 2:
                # paths.append(path.rsplit('/', 1)[0])
            # else:
                # paths.append(path)
            paths.append(path)
    return paths


def clear_asset(ip, port, username, password, oper_user):
    """清理主机, 删除配置文件
    rm -f *.sh
    killall rsync.sh
    rm -f /usr/local/nginx/conf/vhost/*.conf
    删除group1.module_path 下的路径文件
    cp *.conf /usr/local/nginx/conf/vhost/
    service nginx restart
    """
    s = get_ssh(ip, port, username, password)
    assets = Asset.objects.filter(ip=ip)
    # 删除文件并杀死rsync.sh
    # cmds = ['rm -f *.sh', 'killall rsync.sh', 'rm -f /usr/local/nginx/conf/vhost/*.conf']
    # for cmd in cmds:
    #     s.exec_command(cmd)
    if assets:
        group1_list = get_paths(assets[0])
        if group1_list:
            # cmds = ['rm -rf %s'%(i) for i in group1_list]
            # map(s.exec_command, cmds)
            # write_log(ip=host, cmd=str(cmds), title='clear_asset', result='wait remove module_path', user=oper_user)

            remotedir = '/usr/local/nginx/conf/vhost/'
            remotedir_script_path = assets[0].group1.all()[0].script_path

            if LOCAL_FILE_DIR.endswith('/'):
                lfd = LOCAL_FILE_DIR
            else:
                lfd = LOCAL_FILE_DIR + '/'

            localdir = remotedir_script_path.replace('/var/sercon/', lfd)

            find_conf = os.popen('ls %s *.conf'%localdir).read()
            if not find_conf:
                # cmd = 'service nginx restart'
                # s.exec_command(cmd)
                s.close()
                return '没有conf文件'
            else:
                fname_list = find_conf.split()

                # copy_file_to_server(ip, port, username, password, localdir, remotedir, fname_list, oper_user)
                # cmd = 'service nginx restart'
                # s.exec_command(cmd)
            s.close()
            return '清理完成'
        else:
            s.close()
            return '此资产没有组'
    else:
        s.close()
        return '没有此资产'


    #killall ans
    # write_log(ip=host, cmd=resp, title='asset_init', result='wait 1', user=oper_user)

#


def install_softs(host, port, username, password, oper_user, timeout=10):
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
        # write_log(ip=host, cmd=cmd, title='asset_init', result='success')
        # install wget first
        cmd = 'yum install wget -y\n'
        # write_log(ip=host, cmd=cmd, title='asset_init')
        ssh.send(cmd)
        while 1:
            if 'Nothing to do' in buff or 'Complete!' in buff:
                # print u'install wget succ..'
                break
            else:
                resp = ssh.recv(9999)
                buff += resp
                write_log(ip=host, cmd=resp, title='asset_init', result='wait 1', user=oper_user) # 安装
        # write_log(ip=host, cmd=cmd, title='asset_init', result='success')

        # print 'start wget install.sh'
        cmd = 'wget http://softck.yxdown.com/others/install/install.sh\n'
        ssh.send(cmd)
        # write_log(ip=host, cmd=cmd, title='asset_init', result='success')
        buff = ''
        while 1:
            if ('saved' in buff or '已保存' in buff) and '# ' in buff:
                # print u'down install.sh succ..'
                break
            else:
                write_log(ip=host, cmd=buff, title='asset_init', result='wait 2', user=oper_user) # wget 下载
                resp = ssh.recv(9999)
                buff += resp
            # print '------------------'
            # print 'buff: ', buff
            time.sleep(1)

        cmd = 'nohup sh install.sh &\n'
        write_log(ip=host, cmd=cmd, title='asset_init', result='success' ,user=oper_user)
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
                # print '++++++++++++++++++++++++out end+++++++++++++++++++++++++++++'
                # print
                if 'reboot NOW' in resp:
                    write_log(ip=host, cmd=cmd, title='asset_init', result="reboot NOW success", user=oper_user)
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


        # print 'all second: ', int(t2 - t1)
        result = 'succ'

        write_log(ip=host, cmd='', title='install_softs', result="complete all")
        return 'ok', result
    except Exception, e:
        write_log(ip=host, cmd='', title='install_softs', result="Exception while install_softs(): %s" % str(e), user=oper_user)
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


def init_server(host, port, username, password, script_path, oper_user):
    try:
        # 1. install software
        write_log(ip=host, user=oper_user, title='asset_init', result="%s-%s-%s-%s-%s" % (host, str(port), username, password, script_path))
        tag, res = install_softs(host, port, username, password, oper_user)

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
