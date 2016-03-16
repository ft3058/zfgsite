# coding:utf8
"""
srwxr-x---  1 root    root           0 Feb  8 07:02 Aegis-<Guid(5A2C30A2-A87D-490A-9281-6765EDAD7CBA)>
-rw-r--r--  1 root    root           0 Feb 23 12:37 a.txt
-rw-r--r--  1 root    root    45065714 Mar  9 16:41 csto-stderr---supervisor-cJTnSC.log
-rw-------  1 root    root    52428838 Feb 24 18:32 csto-stderr---supervisor-cJTnSC.log.1
-rw-------  1 root    root           0 Feb  8 07:02 csto-stdout---supervisor-iud7cZ.log
-rw-r--r--  1 root    root           0 Mar  9 16:37 empty
-rw-r--r--  1 root    root           0 Mar  9 16:38 empty file name.txt
-rw-r--r--  1 root    root           0 Mar  9 16:37 file
-rw-------  1 root    root       15035 Mar  6 02:17 get_new_proxy-stderr---supervisor-MOH_Bc.log


dr-xr-x---.  2 root root 4096 2016-11-03/12:01:03 .
dr-xr-xr-x. 23 root root 4096 2015-01-12/18:53:11 ..
-rw-------   1 root root 4438 2016-11-03/11:08:30 .bash_history
-rw-r--r--.  1 root root   18 2009-20-05/18:45:02 .bash_logout
-rw-r--r--.  1 root root  176 2009-20-05/18:45:02 .bash_profile
-rw-r--r--.  1 root root  176 2004-23-09/11:59:52 .bashrc
-rw-r--r--   1 root root 1369 2016-23-02/17:47:14 chang-passwd.sh
-rw-r--r--.  1 root root  100 2004-23-09/11:59:52 .cshrc
-rwxr-xr-x   1 root root 1582 2016-10-03/17:16:38 del-sync.sh
-rwxr-xr-x   1 root root  304 2015-03-08/11:45:47 kill-sync.sh
-rw-r--r--   1 root root  253 2016-23-02/17:47:06 miyue.sh
-rwxr-xr-x   1 root root  123 2015-03-08/11:47:32 nginx.sh
-rwxr-xr-x   1 root root 2894 2016-10-03/17:16:22 rsync.sh
-rw-r--r--.  1 root root  129 2004-04-12/05:42:06 .tcshrc
-rw-------   1 root root 6816 2016-10-03/17:21:25 .viminfo


"""

import paramiko


class File(object):
    def __init__(self, fname, user, group, size, sdt):
        self.fname = fname
        self.user = user
        self.group = group
        self.size = size
        self.sdt = sdt

    def __str__(self):
        s = 'file name: %s\n' % self.fname
        s += 'user: %s\n' % self.user
        s += 'group: %s\n' % self.group
        s += 'size: %s\n' % self.size
        s += 'sdt: %s\n' % self.sdt
        return s


def parse_files(lines):
    file_obj_list = []
    for l in lines:
        l = l.strip()
        '''
        if l.startswith('d'):
            continue'''
        # normal value: [u'-rw-r--r--', u'1', u'root', u'root', u'0', u'Mar', u'9', u'16:37', u'name.txt']
        # new :            -rwxr-xr-x   1 root root  123 2015-03-08/11:47:32 nginx.sh
        sp = filter(None, [x.strip() for x in l.split(' ')])
        if len(sp) < 7:
            continue
        fname = l.split(sp[5])[-1].strip()
        if fname.startswith('.'):
            continue
        fobj = File(fname, sp[2], sp[3], sp[4], sp[5])
        file_obj_list.append(fobj)
    return file_obj_list


def check():
    '''
    IP = '115.29.185.223'
    PORT = 22
    USERNAME = 'root'
    PASSWORD = 'Password114418'
    '''
    IP = '222.132.12.103'
    PORT = 12103
    USERNAME = 'root'
    PASSWORD = 'b9de304202a0'  # yxdown@1007 b9de304202a0 qq@20171328

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, PORT, USERNAME, PASSWORD)

    cmd = "ls -al /tmp"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.readlines()
    ssh.close()

    parse_files(lines)


IP = '222.132.12.103'
PORT = 12103
USERNAME = 'root'
PASSWORD = 'b9de304202a0'  # yxdown@1007 b9de304202a0 qq@20171328
LS_CMD_TMPL = 'ls -l --time-style="+%Y-%d-%m/%H:%M:%S" '
SEE_CONF_CMD = "cat /etc/rsyncd.conf"


class RsyncCheck(object):

    def __init__(self):
        self.repo_file_list = []
        self.module_path_dict = {}

    def get_ssh(self, ip, port, username, password):
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(ip, port, username, password, timeout=10)
        return ssh1

    def diff(self, file_list):
        # fname, user, group, size, sdt
        file_not_exists = []
        file_err_time = []
        file_err_size = []
        file_count = len(file_list)
        for n, i in enumerate(self.repo_file_list):
            found = False
            for j in file_list:
                if j.fname == i.fname:
                    # print 'j fname:', j.fname, 'i fname:', i.fname
                    found = True
                    if j.size != i.size:
                        file_err_size.append(i)
                    if j.sdt != i.sdt:
                        file_err_time.append(i)
                    break
            if not found:
                file_not_exists.append(i)
            # print 'file_not_exists:', len(file_not_exists), 'file_err_time:', len(file_err_time), 'file_err_size: ', len(file_err_size), '%d/%d' % (n+1, len(self.repo_file_list))

        return file_not_exists, file_err_size, file_err_time, file_count

    def compare_files(self, down_asset, module_name, cmd):
        if not down_asset or not module_name:
            return

        # path = self.module_path_dict.get(module_name)
        ssh = self.get_ssh(down_asset.ip, down_asset.port, down_asset.username, down_asset.passwd)

        stdin, stdout, stderr = ssh.exec_command(cmd)
        txt = stdout.read()
        ssh.close()
        lines = self.get_exec_output_lines(txt)
        down_file_list = parse_files(lines)
        file_not_exists, file_err_size, file_err_time, file_count = self.diff(down_file_list)
        repo_file_count = len(self.repo_file_list)

        return file_not_exists, file_err_size, file_err_time, file_count, repo_file_count

    def get_exec_output_lines(self, txt):
        lines = []
        for l in txt.split('\n'):
            l = l.strip()
            if l:
                lines.append(l)
        return lines

    def fetch_repo_files(self, path):
        ssh = self.get_ssh(IP, PORT, USERNAME, PASSWORD)
        cmd = LS_CMD_TMPL + path
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # lines = stdout.readlines()
        txt = stdout.read()
        ssh.close()
        lines = self.get_exec_output_lines(txt)

        self.repo_file_list = []
        self.repo_file_list = parse_files(lines)

    def get_module_key_dict(self, ip, port, username, password, setrepo=False):
        module_path_dict = {}
        ssh = self.get_ssh(ip, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(SEE_CONF_CMD)
        txt = stdout.read()
        ssh.close()
        lines = self.get_exec_output_lines(txt)
        line_list = filter(None, [x.strip() for x in lines])
        for n, i in enumerate(line_list):
            if i.startswith('[') and i.endswith(']'):
                k = i[1:-1].strip()
                v = line_list[n+1].replace('path=', '')
                module_path_dict[k] = v
                # print 'k:', k, 'v:', v
        if setrepo:
            self.module_path_dict = module_path_dict
        else:
            return module_path_dict


if __name__ == '__main__':
    print 'start...'
    # check()
    rc = RsyncCheck()
    module_name = '391kComApk'
    # rc.compare_files([], '')
    rc.cat_rsyncd_conf()
    path = rc.module_path_dict.get(module_name)
    if path:
        rc.fetch_repo_files(path)
        if rc.repo_file_list:
            print u'found file :'
            for l in rc.repo_file_list:
                print '+', l
                print '---------------------'
            print 'file count: ', len(rc.repo_file_list)

            # at = Asset()
            # rc.compare_files([at], module_name)

        else:
            print u'Empty repo_file_list!!!'
    else:
        print u'not found module name: %s' % module_name

    '''
---------------------
file count:  40389
not_exists count:  0
err_size count:  95
err_time count:  40389
total file count: 40468/40389
[11/Mar/2016 13:37:57] "POST /jmonitor/rsync/status_check/?asset_id_all=23 HTTP/1.1" 200 19
Validating models...

    '''


    print 'end...'
