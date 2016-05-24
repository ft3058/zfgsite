__author__ = 'wxd'

import paramiko


IP = '222.132.12.103'
PORT = 12103
USERNAME = 'root'
PASSWORD = 'b9de304202a0'  # yxdown@1007 b9de304202a0 qq@20171328
LS_CMD_TMPL = 'ls -l --time-style="+%Y-%d-%m/%H:%M:%S" '
SEE_CONF_CMD = "cat /etc/rsyncd.conf"


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

ssh = get_ssh(IP, PORT, USERNAME, PASSWORD)
SEE_CONF_CMD = "cat /etc/rsyncd.conf"

stdin, stdout, stderr = ssh.exec_command(SEE_CONF_CMD)
txt = stdout.read()
ssh.close()

lines = get_exec_output_lines(txt)
for l in lines:
    print l

