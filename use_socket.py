# coding:utf8
import os
import subprocess
import sys


SCRIPT_NAME = 'run_websocket.py'
SELF_NAME = 'use_socket.py'
PYTHON_PATH = '/home/wxd/env_jump_wxd/bin/python'
USAGE = u'usage: %s %s [start|kill] \n' % (PYTHON_PATH, SELF_NAME)


def kill_proc():
    cmd = "ps aux | grep '%s'"
    cmd %= SCRIPT_NAME
    print cmd

    f = os.popen(cmd)
    lines = f.read()

    pid_list = []

    for line in lines.split('\n'):
        if 'grep' in line or not line.strip():
            continue
        words = filter(None, [x.strip() for x in line.split(' ')])
        pid_list.append(words[1])

    if pid_list:
        for pid in pid_list:
            try:
                os.system("kill -9 %s" % pid)
                print u'kill process id [%s] succ ' % pid
            except Exception, e:
                print u'kill process error: %s' % str(e)
    else:
        print u'No pids !!!'


def start_proc():
    cmd = "setsid %s %s" % (PYTHON_PATH, SCRIPT_NAME)
    try:
        # f = os.popen(cmd)
        subprocess.Popen(cmd.split(' '))
        print 'start succ'
    except Exception, e:
        print u'start %s error: %s' % (SCRIPT_NAME, str(e))

if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) != 2:
        print USAGE
    else:
        op = argvs[1]
        if op not in ['start', 'kill']:
            print USAGE
        else:
            print u'receive argv: %s \n' % argvs[1]
            if 'start' == op:
                start_proc()
            elif 'kill' == op:
                kill_proc()

