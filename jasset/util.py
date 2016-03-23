# coding:utf8
import string
import numbers
from random import choice


def get_random_str(count=10):
    s = string.ascii_letters + '0123456789'
    tmp = ''.join([choice(s) for x in range(count)])
    return tmp


if __name__ == '__main__':
    print get_random_str()


