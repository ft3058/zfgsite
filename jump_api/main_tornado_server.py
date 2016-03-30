# -*- coding: utf-8 -*-
import tornado.web
from tornado.web import RequestHandler as RH
import tornado.ioloop
from tornado.options import define, options, parse_command_line

from crpt import CRYPTOR
from util import check_ip, check_port
from db_util import check_exists, insert_asset, update_asset
from settings import PORT


define('port', default=PORT, help='run on the port', type=int)

"""
curl -d "ip=1.2.3.4&port=22&account=root&password=12345678&checkCode=0000" "http://127.0.0.1:5000/jasset/asset/add_post/"
curl -d "ip=1.2.3.4&port=22&account=root&password=12345678&checkCode=0000" "http://120.131.71.41:5000/jasset/asset/add_post/"

"""


class MainHandler(RH):


    def get(self):
        # self.render('a.html',title='haha',items=l)
        self.write('hello')

    def post(self):
        """
        curl -d "ip=1.2.3.4&port=22&account=root&password=12345678&checkCode=0000" "http://127.0.0.1:5000/jasset/asset/add_post/"
        """
        try:
            print 'remote_ip: ', self.request.remote_ip
            ip = self.get_argument('ip')
            port = self.get_argument('port')
            account = self.get_argument('account')
            password = self.get_argument('password')
            checkCode = self.get_argument('checkCode')

            isip = check_ip(ip)
            if not isip:
                return 'invalid ip: %s' % ip

            isport = check_port(port)
            if not isport:
                return 'invalid port: %s' % port

            print 'ip = ', ip
            print 'port = ', port
            print 'account = ', account
            print 'password = ', password
            print 'checkCode = ', checkCode

            passwd = password
            password = CRYPTOR.encrypt(password)

            ifexists = check_exists(ip)
            if ifexists:
                print 'update: ', ip, password, passwd
                update_asset(ip, port, account, passwd, password, checkCode)
            else:
                print 'insert: ', ip, password, passwd
                insert_asset(ip, port, account, passwd, password, checkCode)
            self.write('success')
        except Exception, e:
            self.write(str(e))


def main():
    parse_command_line()
    app = tornado.web.Application([
        ('/jasset/asset/add_post/', MainHandler),
    ],)

    print 'jump server api run at port: ', PORT
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()