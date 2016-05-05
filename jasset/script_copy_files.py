# coding:utf8
"""

"""
import time, os
import paramiko
from threading import Thread
from util import write_log
from jumpserver.settings import *

"""
IP = '192.168.4.234'
PORT = 22
USERNAME = 'twotiger'
PASSWORD = '123456'
"""


class CopyThread(Thread):

    def __init__(self):
        super(CopyThread, self).__init__()
        self.host = ''
        self.port = ''
        self.username = ''
        self.password = ''
        self.local_dir = ''
        self.remote_dir = ''
        self.fname_list = ''
        self.logged_user = ''

    def set_params(self, host, port, username, password, local_dir, remote_dir, fname_list, logged_user):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.local_dir = local_dir
        self.remote_dir = remote_dir
        self.fname_list = fname_list
        self.logged_user = logged_user

    def run(self):
        """
        """
        try:
            s = get_ssh(IP, PORT, USERNAME, PASSWORD)
            ssh = s.invoke_shell()

            files = ' '.join([os.path.join(self.local_dir, fn) for fn in self.fname_list])

            scp_cmd = "rsync -avH -progress '-e ssh -p %s' %s %s@%s:%s" % (str(self.port), files, self.username, self.host, self.remote_dir)
            # scp_cmd = "/usr/bin/scp -P %s %s %s@%s:%s" % (str(port), files, username, host, remote_dir)

            print 'scp_cmd = ', scp_cmd
            ssh.send(scp_cmd + '\n')

            buff = ''
            flag = False
            while 1:
                if '(yes/no)' in buff:
                    ssh.send('yes\n')
                    buff = ''
                    time.sleep(1)
                    # print 'send yes..'
                elif 'password:' in buff:
                    ssh.send(self.password+'\n')
                    buff = ''
                    time.sleep(1)
                    flag = True
                    # print 'send password..'
                elif ('# ' in buff or '$ ' in buff) and flag:
                    # print '******************************'
                    # print buff
                    # print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                    # print 'succ'
                    break

                else:
                    # print 'receiving data...'
                    resp = ssh.recv(9999)
                    buff += resp

                # print '------------------------------------------'
                # print 'buff = ', buff
                # print '++++++++++++++++++++++++++++++++++++++++++'
                # print
                time.sleep(1)

            # print 'scp complete..'
            s.close()

            write_log(self.logged_user, self.host, self.host, scp_cmd, 'copy file', 'success')
            return 'ok', 'success'
        except Exception, e:
            # print traceback.print_exc()
            try:
                s.close()
            except Exception, e1:
                write_log(self.logged_user, self.host, self.host, '', 'copy file', str(e1))
            write_log(self.logged_user, self.host, self.host, '', 'copy file', str(e))
            return 'fail', str(e)


def copy_file_to_server(host, port, username, password, local_dir, remote_dir, fname_list, logged_user):
    """
    user rsync for copy
    """
    ct = CopyThread()
    ct.set_params(host, port, username, password, local_dir, remote_dir, fname_list, logged_user)
    ct.start()


def get_ssh(host, port, username, password, timeout=20):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)
    return s


def install_ssh_client(host, port, username, password):
    try:
        print 'start install openssh-clients ... '
        s = get_ssh(host, port, username, password)
        ssh = s.invoke_shell()

        # 1. pre install openssh-clients first
        install_ssh_cmd = "yum install openssh-clients -y"
        # write_log(ip=host, cmd=install_ssh_cmd, title='copy_file', result="")
        print 'run CMD: ', install_ssh_cmd
        ssh.send(install_ssh_cmd + '\n')
        time.sleep(0.5)

        buff = ''
        while 1:
            if '(yes/no)' in buff:
                ssh.send('yes\n')
                buff = ''
                time.sleep(1)
                print 'send yes..'
                continue
            elif 'password:' in buff:
                ssh.send(password+'\n')
                buff = ''
                time.sleep(1)
                print 'send password..'
                continue
            elif 'Complete!' in buff or 'Nothing to do' in buff or '无须任何处理' in buff:
                print '******************************'
                print buff
                print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                print 'succ'
                break

            time.sleep(1)
            print 'receive data...'
            resp = ssh.recv(9999)
            buff += resp

        s.close()
        print 'install openssh-clients complete..'
        return 'ok', 'success'
    except Exception, e:
        # print traceback.print_exc()
        try:
            s.close()
        except: pass
        return 'fail', str(e)


def copy_file_to_server_bak(host, port, username, password, local_dir, remote_dir, fname_list):
    try:
        tag, res = install_ssh_client(host, port, username, password)
        if tag == 'fail':
            return tag, res

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(IP, PORT, USERNAME, PASSWORD)

        '''
        cmd = "ls -al /tmp"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        lines = stdout.readlines()
        for l in lines:
            print l.strip()'''

        ssh = s.invoke_shell()

        # remote_dir = '/root/scripts8'
        # 222.186.37.4 	374 	root 	RcsHQ6rk4o
        # host = '222.186.37.4'
        # port = '374'
        # username = 'root'
        # password = 'RcsHQ6rk4o'
        mkdir_cmd = "/usr/bin/ssh %s@%s -p %s 'mkdir -p %s'" % (username, host, str(port), remote_dir)
        print 'mkdir_cmd = ', mkdir_cmd
        ssh.send(mkdir_cmd + '\n')

        buff = ''
        while 1:

            if '# ' in buff or '$ ' in buff:
                print 'buff = ', buff

                if '(yes/no)' in buff:
                    ssh.send('yes\n')
                    buff = ''
                    print 'send yes..'
                elif 'password:' in buff:
                    ssh.send(password+'\n')
                    buff = ''
                    print 'send password..'
                else:
                    print 'succ'
                    break
            else:
                resp = ssh.recv(9999)
                buff += resp
                print 'resp:'
                print resp
            time.sleep(1)

        print 'mkdir complete..'

        files = ' '.join([os.path.join(local_dir, fn) for fn in fname_list])
        scp_cmd = "/usr/bin/scp -P %s %s %s@%s:%s" % (str(port), files, username, host, remote_dir)
        print 'scp_cmd = ', scp_cmd
        ssh.send(scp_cmd + '\n')

        buff = ''
        while 1:
            if '(yes/no)' in buff:
                ssh.send('yes\n')
                buff = ''
                time.sleep(1)
                print 'send yes..'
            elif 'password:' in buff:
                ssh.send(password+'\n')
                buff = ''
                time.sleep(1)
                print 'send password..'
            elif '# ' in buff or '$ ' in buff:
                print '******************************'
                print buff
                print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                print 'succ'
                break

            if '# ' in buff or '$ ' in buff:
                break
            else:
                print 'receive data...'
                resp = ssh.recv(9999)
                buff += resp

            print '------------------------------------------'
            print 'buff = ', buff
            print '++++++++++++++++++++++++++++++++++++++++++'
            print
            time.sleep(1)

        print 'scp complete..'
        s.close()

        return 'ok', 'success'
    except Exception, e:
        # print traceback.print_exc()
        try:
            s.close()
        except: pass
        return 'fail', str(e)