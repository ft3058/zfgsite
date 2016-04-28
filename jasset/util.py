# coding:utf8
import string
# import numbers
# import traceback
from random import choice
from jlog.models import CustomLog


def write_log(user='', host='', ip='', cmd='', title='', result=''):
    try:
        clog = CustomLog(user=user,
                         host=host,
                         ip=ip,
                         cmd=cmd,
                         title=title,
                         result=result)
        clog.save()
    except Exception, e:
        # print 'error: %s' % str(e)
        # print traceback.print_exc()
        pass


def get_random_str(count=10):
    s = string.ascii_letters + '0123456789'
    tmp = ''.join([choice(s) for x in range(count)])
    return tmp


if __name__ == '__main__':
    print get_random_str()


