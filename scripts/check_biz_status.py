# coding:utf8
"""
218.75.155.46 	22 	root 	20ebf66325a3 生成新密码 	YiWan.com 	android

"""
from threading import Thread
import paramiko
from jumpserver_model_api import Asset


def get_ssh(ip, port, username, password):
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(ip, port, username, password, timeout=10)
    return ssh1


def get_exec_output_lines(txt):
    lines = []
    for l in txt.split('\n'):
        l = l.strip()
        if l:
            lines.append(l)
    return lines

def check_biz(ip, port, username, passwd):
    """
    ip = '218.75.155.46'
    port = 22
    username = 'root'
    password = '20ebf66325a3'
    """
    ssh = get_ssh(ip, port, username, passwd)

    cmd = 'cat /root/rsync.sh'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    txt = stdout.read()
    ssh.close()
    lines = get_exec_output_lines(txt)

    module_name_list = []
    for i in lines:
        if '--password-file=' in i and '--port=' in i and '::' in i:
            # print i
            module_name = i.split('::')[-1].split(' ')[0].strip()
            if module_name and module_name != 'NginxConf':
                module_name_list.append(module_name)

    return module_name_list


def checking_biz(ip_list):
    for ip in ip_list:
        at = Asset.objects.filter(ip=ip)
        if not at:
            continue
        at = at[0]
        gp1_list = at.group1.all()
        origin_biz_list = []

        for gp1 in gp1_list:
            if gp1 and gp1.module_path:
                ppaths = gp1.module_path.split(',')
                for i in ppaths:
                    mod_name = i.split('=')[0].strip()
                    if mod_name and mod_name not in origin_biz_list:
                        origin_biz_list.append(mod_name)
        print 'origin_biz_list = ', origin_biz_list

        curr_biz_list = check_biz(ip, at.port, at.username, at.passwd)
        print 'curr_biz_list = ', curr_biz_list


if __name__ == '__main__':
    ll = ['218.75.155.46']
    checking_biz(ll)