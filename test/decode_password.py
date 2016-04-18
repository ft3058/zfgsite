#!/usr/bin/env python3
# encoding: utf-8
__author__ = 'u1404'
import random
from Crypto.Cipher import AES
import crypt
import pwd
from binascii import b2a_hex, a2b_hex
import hashlib

from MySQLdb import Connect
from MySQLdb.cursors import DictCursor as DC
# from crpt import CRYPTOR
# from settings import *

host = '120.131.71.41'  # '127.0.0.1'
port = '3306'
user = 'root'
password = 'xiejt521'
database = 'jump'


def get_conn():
    return Connect(host=host, user=user, passwd=password, db=database, compress=1, cursorclass=DC, charset='utf8')


def get_no_password():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT ip, username, passwd FROM jasset_asset where password is null ;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


class PyCrypt(object):
    """
    This class used to encrypt and decrypt password.
    加密类
    """

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    @staticmethod
    def gen_rand_pass(length=16, especial=False):
        """
        random password
        随机生成密码
        """
        salt_key = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        symbol = '!@$%^&*()_'
        salt_list = []
        if especial:
            for i in range(length - 4):
                salt_list.append(random.choice(salt_key))
            for i in range(4):
                salt_list.append(random.choice(symbol))
        else:
            for i in range(length):
                salt_list.append(random.choice(salt_key))
        salt = ''.join(salt_list)
        return salt

    @staticmethod
    def md5_crypt(string):
        """
        md5 encrypt method
        md5非对称加密方法
        """
        return hashlib.new("md5", string).hexdigest()

    @staticmethod
    def gen_sha512(salt, password):
        """
        generate sha512 format password
        生成sha512加密密码
        """
        return crypt.crypt(password, '$6$%s$' % salt)

    def encrypt(self, passwd=None, length=32):
        """
        encrypt gen password
        对称加密之加密生成密码
        """
        if not passwd:
            passwd = self.gen_rand_pass()

        cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
        try:
            count = len(passwd)
        except TypeError:
            raise Exception('Encrypt password error, TYpe error.')

        add = (length - (count % length))
        passwd += ('\0' * add)
        cipher_text = cryptor.encrypt(passwd)
        return b2a_hex(cipher_text)

    def decrypt(self, text):
        """
        decrypt pass base the same key
        对称加密之解密，同一个加密随机数
        """
        cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
        try:
            plain_text = cryptor.decrypt(a2b_hex(text))
        except TypeError:
            raise Exception('Decrypt password error, TYpe error.')
        return plain_text.rstrip('\0')


def test11():
    KEY = '88aaaf7ffe3c6c04'
    CRYPTOR = PyCrypt(KEY)
    s = '1c135838b11cf2288ef750357b631591acd0b6aadb2de1ebe75be614e60d5fba'

    passwd = CRYPTOR.decrypt(s)
    print 'passwd = ', passwd

    old_passwd = 'yxdown@1007'
    encode_str = CRYPTOR.encrypt(old_passwd)
    print 'encode_str = ', encode_str


def update_pass(old_passwd):
    KEY = '88aaaf7ffe3c6c04'
    CRYPTOR = PyCrypt(KEY)
    encode_str = CRYPTOR.encrypt(old_passwd)
    return encode_str


def update_to_new_password(ip, password):
    conn = get_conn()
    cursor = conn.cursor()
    tmpl_sql = "update jasset_asset set password='%s' where ip='%s';" % (password, ip)
    cursor.execute(tmpl_sql)
    conn.commit()
    cursor.close()
    conn.close()
    return True

if __name__ == '__main__':
    rows = get_no_password()

    for row in rows:
        print row['ip'], row['username'], row['passwd']
        new_password = update_pass(row['passwd'])
        print new_password
        update_to_new_password(row['ip'], new_password)
        print 'update succ'



