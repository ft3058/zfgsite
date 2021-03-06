# coding: utf-8
import re
import time
import json
import os
import sys
import os.path
import threading
import datetime
from datetime import datetime as dt
import traceback

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.gen
import tornado.httpclient
from tornado.websocket import WebSocketHandler, WebSocketClosedError

from tornado.options import define, options
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, AsyncNotifier
import select

# from jumpserver.api import ServerError
from connect import Tty, User, Asset, PermRole, logger, get_object, PermRole, gen_resource
from connect import TtyLog, Log, Session, user_have_perm, get_group_user_perm, MyRunner, ExecLog
from jasset.models import AssetParent
from jumpserver.models import db

try:
    import simplejson as json
except ImportError:
    import json


define("port", default=3000, help="run on the given port", type=int)
define("host", default='0.0.0.0', help="run port on given host", type=str)


def require_auth(role='user'):
    def _deco(func):
        def _deco2(request, *args, **kwargs):
            username = request.get_argument('username', '')  # get auth by username
            db.close_connection()
            print 'close_connection()@2016-4-22'
            if request.get_cookie('sessionid'):
                session_key = request.get_cookie('sessionid')
            else:
                session_key = request.get_argument('sessionid', '')

            logger.debug('Websocket: session_key: %s' % session_key)
            if session_key:
                session = get_object(Session, session_key=session_key)
                logger.debug('Websocket: session: %s' % session)
                if session and datetime.datetime.now() < session.expire_date:
                    user_id = session.get_decoded().get('_auth_user_id')
                    user = get_object(User, id=user_id)
                    if user:
                        logger.debug('Websocket: user [ %s ] request websocket' % user.username)
                        request.user = user
                        if role == 'admin':
                            if user.role in ['SU', 'GA']:
                                return func(request, *args, **kwargs)
                            logger.debug('Websocket: user [ %s ] is not admin.' % user.username)
                        else:
                            return func(request, *args, **kwargs)
                else:
                    logger.debug('Websocket: session expired: %s' % session_key)
                    # session = get_object(Session, session_key=session_key)
                    logger.debug('session is expired, create session by username: %s' % username)
                    if username:
                        # user_id = session.get_decoded().get('_auth_user_id')
                        # user = get_object(User, id=user_id)
                        user = get_object(User, username=username)
                        if user:
                            logger.debug('Websocket: user [ %s ] request websocket' % user.username)
                            request.user = user
                            if role == 'admin':
                                if user.role in ['SU', 'GA']:
                                    return func(request, *args, **kwargs)
                                logger.debug('Websocket: user [ %s ] is not admin.' % user.username)
                            else:
                                return func(request, *args, **kwargs)
                        else:
                            logger.debug('get Null User by username:' + username)
                    else:
                        logger.debug('Websocket: username is null...')

            else:
                # session = get_object(Session, session_key=session_key)
                logger.debug('session is null, create session by username: %s' % username)
                if username:
                    # user_id = session.get_decoded().get('_auth_user_id')
                    # user = get_object(User, id=user_id)
                    user = get_object(User, username=username)
                    if user:
                        logger.debug('Websocket: user [ %s ] request websocket' % user.username)
                        request.user = user
                        if role == 'admin':
                            if user.role in ['SU', 'GA']:
                                return func(request, *args, **kwargs)
                            logger.debug('Websocket: user [ %s ] is not admin.' % user.username)
                        else:
                            return func(request, *args, **kwargs)
                    else:
                        logger.debug('get Null User by username:' + username)
                else:
                    logger.debug('Websocket: username is null...')

            try:
                request.close()
            except AttributeError:
                pass
            logger.warning('Websocket: Request auth failed.')
        return _deco2
    return _deco


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        print 'args = ', args
        print 'kwargs = ', kwargs
        super(MyThread, self).__init__(*args, **kwargs)

    def run(self):
        try:
            super(MyThread, self).run()
        except WebSocketClosedError:
            pass


class EventHandler(ProcessEvent):
    def __init__(self, client=None):
        self.client = client

    def process_IN_MODIFY(self, event):
        self.client.write_message(f.read())


def file_monitor(path='.', client=None):
    wm = WatchManager()
    mask = IN_DELETE | IN_CREATE | IN_MODIFY
    notifier = AsyncNotifier(wm, EventHandler(client))
    wm.add_watch(path, mask, auto_add=True, rec=True)
    if not os.path.isfile(path):
        logger.debug("File %s does not exist." % path)
        sys.exit(3)
    else:
        logger.debug("Now starting monitor file %s." % path)
        global f
        f = open(path, 'r')
        st_size = os.stat(path)[6]
        f.seek(st_size)

    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            print "keyboard Interrupt."
            notifier.stop()
            break


class MonitorHandler(tornado.websocket.WebSocketHandler):
    clients = []
    threads = []

    def __init__(self, *args, **kwargs):
        self.file_path = None
        super(self.__class__, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    @require_auth('admin')
    def open(self):
        # 获取监控的path
        self.file_path = self.get_argument('file_path', '')
        MonitorHandler.clients.append(self)
        thread = MyThread(target=file_monitor, args=('%s.log' % self.file_path, self))
        MonitorHandler.threads.append(thread)
        self.stream.set_nodelay(True)

        try:
            for t in MonitorHandler.threads:
                if t.is_alive():
                    continue
                t.setDaemon(True)
                t.start()

        except WebSocketClosedError:
            client_index = MonitorHandler.clients.index(self)
            MonitorHandler.threads[client_index].stop()
            MonitorHandler.clients.remove(self)
            MonitorHandler.threads.remove(MonitorHandler.threads[client_index])

        logger.debug("Websocket: Monitor client num: %s, thread num: %s" % (len(MonitorHandler.clients),
                                                                            len(MonitorHandler.threads)))

    def on_message(self, message):
        # 监控日志，发生变动发向客户端
        pass

    def on_close(self):
        # 客户端主动关闭
        # self.close()

        logger.debug("Websocket: Monitor client close request")
        try:
            client_index = MonitorHandler.clients.index(self)
            MonitorHandler.clients.remove(self)
            MonitorHandler.threads.remove(MonitorHandler.threads[client_index])
        except ValueError:
            pass


class WebTty(Tty):
    def __init__(self, *args, **kwargs):
        super(WebTty, self).__init__(*args, **kwargs)
        self.ws = None
        self.data = ''
        self.input_mode = False


class WebTerminalKillHandler(tornado.web.RequestHandler):
    @require_auth('admin')
    def get(self):
        ws_id = self.get_argument('id')
        Log.objects.filter(id=ws_id).update(is_finished=True)
        for ws in WebTerminalHandler.clients:
            if ws.id == int(ws_id):
                logger.debug("Kill log id %s" % ws_id)
                ws.log.save()
                ws.close()
        logger.debug('Websocket: web terminal client num: %s' % len(WebTerminalHandler.clients))


class ExecHandler(WebSocketHandler):
    clients = []
    tasks = []

    def __init__(self, *args, **kwargs):
        self.id = 0
        self.user = None
        self.role = None
        self.runner = None
        self.assets = []
        self.perm = {}
        self.remote_ip = ''
        super(ExecHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    @require_auth('user') # 为了绕过权限，被放弃2016-4-11
    def open_old(self):
        logger.debug('Websocket: Open exec request')
        role_name = self.get_argument('role', 'sb')
        self.remote_ip = self.request.remote_ip
        logger.debug('Web执行命令: 请求系统用户 %s' % role_name)
        self.role = get_object(PermRole, name=role_name)
        self.perm = get_group_user_perm(self.user)
        roles = self.perm.get('role').keys()
        if self.role not in roles:
            self.write_message('No perm that role %s' % role_name)
            self.close()
        self.assets = self.perm.get('role').get(self.role).get('asset')

        res = gen_resource({'user': self.user, 'asset': self.assets, 'role': self.role})
        self.runner = MyRunner(res)
        message = '有权限的主机: ' + ', '.join([asset.hostname for asset in self.assets])
        self.__class__.clients.append(self)
        self.write_message(message)

    @require_auth('user')
    def open(self):
        """
        新的修改权限 2016-4-11
        删除所有的权限认证，得到选中的主机列表，查询所有[{hostname,ip,port,password}],传递给MyRunner
        """

        logger.debug('Websocket: Open exec request')
        role_name = self.get_argument('role', 'sb')
        assets_name = self.get_argument('check_assets', None)

        if not assets_name:
            raise Exception('Please choice one host')
        self.remote_ip = self.request.remote_ip
        logger.debug('Web执行命令: 请求系统用户 %s' % role_name)

        res = []
        for ip in assets_name.split(':'):
            asset = Asset.objects.get(ip=ip)

            res.append({
                'hostname': asset.hostname,
                'ip' :      asset.ip,
                'password': asset.passwd,
                'port' :    asset.port,
                'username': asset.username
            })
        # print 'res=' ,res
        self.runner = MyRunner(res)
        message = '选中%s台主机: '%(assets_name.count(':')+1) + assets_name
        self.__class__.clients.append(self)
        self.write_message(message)

    def on_message(self, message):
        data = json.loads(message)
        pattern = data.get('pattern', '')
        command = data.get('command', '')
        asset_name_str = ''
        if pattern and command:
            for inv in self.runner.inventory.get_hosts(pattern=pattern):
                asset_name_str += '%s ' % inv.name
            self.write_message('匹配主机: ' + asset_name_str)
            self.write_message('<span style="color: yellow">Ansible> %s</span>\n\n' % command)
            self.__class__.tasks.append(MyThread(target=self.run_cmd, args=(command, pattern)))
            try:
                ExecLog(host=asset_name_str, cmd=command, user=self.user.username, remote_ip=self.remote_ip).save()
            except Exception, e:
                self.write_message('执行命令日志保存出错: ' + str(e))

        for t in self.__class__.tasks:
            if t.is_alive():
                continue
            try:
                t.setDaemon(True)
                t.start()
            except RuntimeError:
                pass

    def run_cmd(self, command, pattern):
        self.runner.run('shell', command, pattern=pattern)
        newline_pattern = re.compile(r'\n')
        for k, v in self.runner.results.items():
            for host, output in v.items():
                output = newline_pattern.sub('<br />', output)
                logger.debug(output)
                if k == 'ok':
                    header = "<span style='color: green'>[ %s => %s]</span>\n" % (host, 'Ok')
                else:
                    header = "<span style='color: red'>[ %s => %s]</span>\n" % (host, 'failed')
                self.write_message(header)
                self.write_message(output)

        self.write_message('\n~o~ Task finished ~o~\n')

    def on_close(self):
        logger.debug('关闭web_exec请求')


class WebTerminalHandler(tornado.websocket.WebSocketHandler):
    clients = []
    tasks = []

    def __init__(self, *args, **kwargs):
        self.term = None
        self.log_file_f = None
        self.log_time_f = None
        self.log = None
        self.id = 0
        self.user = None
        self.ssh = None
        self.channel = None
        super(WebTerminalHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    @require_auth('user')
    def open_bak(self):  # 原来的版本，为了绕过权限放弃。
        logger.debug('Websocket: Open request')
        role_name = self.get_argument('role', 'sb')
        asset_id = self.get_argument('id', 9999)
        asset = get_object(Asset, id=asset_id)
        if asset:
            roles = user_have_perm(self.user, asset)    # 跳转到jperm/perm_api :149
            logger.debug(roles)
            logger.debug('系统用户: %s' % role_name)
            login_role = ''
            for role in roles:
                if role.name == role_name:
                    login_role = role
                    break
            if not login_role:
                logger.warning('Websocket: Not that Role %s for Host: %s User: %s ' % (role_name, asset.hostname,
                                                                                       self.user.username))
                self.close()
                return
        else:
            logger.warning('Websocket: No that Host: %s User: %s ' % (asset_id, self.user.username))
            self.close()
            return
        logger.debug('Websocket: request web terminal Host: %s User: %s Role: %s' % (asset.hostname, self.user.username,
                                                                                     login_role.name))
        self.term = WebTty(self.user, asset, login_role, login_type='web')
        self.term.remote_ip = self.request.remote_ip
        self.ssh = self.term.get_connection()
        self.channel = self.ssh.invoke_shell(term='xterm')
        WebTerminalHandler.tasks.append(MyThread(target=self.forward_outbound))
        WebTerminalHandler.clients.append(self)

        for t in WebTerminalHandler.tasks:
            if t.is_alive():
                continue
            try:
                t.setDaemon(True)
                t.start()
            except RuntimeError:
                pass

    @require_auth('user')
    def open(self):  # 新的函数，绕过验证
        logger.debug('Websocket: Open request')
        role_name = self.get_argument('role', 'sb')
        asset_id = self.get_argument('id', 9999)
        print 'asset_id:', asset_id
        asset = get_object(Asset, id=asset_id)

        login_role = user_have_perm(self.user, asset)  # 跳转到jperm/perm_api :149, 被修改过，将传回一个可用的role
        self.term = WebTty(self.user, asset, login_role, login_type='web')
        self.term.remote_ip = self.request.remote_ip
        result = self.term.get_connection()
        if isinstance(result, tuple) and result[0] == 'fail':
            self.write_message(json.dumps({'data':result[1]}))
            raise Exception(result[1])

        self.ssh = result
        self.channel = self.ssh.invoke_shell(term='xterm')
        WebTerminalHandler.tasks.append(MyThread(target=self.forward_outbound))
        WebTerminalHandler.clients.append(self)

        for t in WebTerminalHandler.tasks:
            if t.is_alive():
                continue
            try:
                t.setDaemon(True)
                t.start()
            except RuntimeError:
                pass

    def on_message(self, message):
        data = json.loads(message)
        if not data:
            return

        if 'resize' in data.get('data'):
            self.channel.resize_pty(
                data.get('data').get('resize').get('cols', 80),
                data.get('data').get('resize').get('rows', 24)
            )
        elif data.get('data'):
            self.term.input_mode = True
            if str(data['data']) in ['\r', '\n', '\r\n']:
                if self.term.vim_flag:
                    match = self.term.ps1_pattern.search(self.term.vim_data)
                    if match:
                        self.term.vim_flag = False
                        vim_data = self.term.deal_command(self.term.vim_data)[0:200]
                        if len(data) > 0:
                            TtyLog(log=self.log, datetime=datetime.datetime.now(), cmd=vim_data).save()

                TtyLog(log=self.log, datetime=datetime.datetime.now(),
                       cmd=self.term.deal_command(self.term.data)[0:200]).save()
                self.term.vim_data = ''
                self.term.data = ''
                self.term.input_mode = False
            # print u'received data at:', dt.now()
            self.channel.send(data['data'])
        else:
            pass

    def on_close(self):
        logger.debug('Websocket: Close request')
        if self in WebTerminalHandler.clients:
            WebTerminalHandler.clients.remove(self)
        try:
            self.log_file_f.write('End time is %s' % datetime.datetime.now())
            self.log.is_finished = True
            self.log.end_time = datetime.datetime.now()
            self.log.save()
            self.log_time_f.close()
            self.ssh.close()
            self.close()
        except AttributeError:
            pass
        except Exception, e:
            print u'Error while: Websocket: Close request ! '
            print traceback.print_exc()

    def forward_outbound(self):
        self.log_file_f, self.log_time_f, self.log = self.term.get_log()
        self.id = self.log.id
        try:
            data = ''
            pre_timestamp = time.time()
            while True:
                r, w, e = select.select([self.channel, sys.stdin], [], [])
                if self.channel in r:
                    recv = self.channel.recv(1024)
                    if not len(recv):
                        return
                    data += recv
                    if self.term.vim_flag:
                        self.term.vim_data += recv
                    try:
                        self.write_message(json.dumps({'data': data}))
                        now_timestamp = time.time()
                        self.log_time_f.write('%s %s\n' % (round(now_timestamp-pre_timestamp, 4), len(data)))
                        self.log_file_f.write(data)
                        pre_timestamp = now_timestamp
                        self.log_file_f.flush()
                        self.log_time_f.flush()
                        if self.term.input_mode and not self.term.is_output(data):
                            self.term.data += data
                        data = ''
                    except UnicodeDecodeError:
                        pass
        except IndexError:
            pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/monitor', MonitorHandler),
            (r'/terminal', WebTerminalHandler),
            (r'/kill', WebTerminalKillHandler),
            (r'/exec', ExecHandler),
        ]

        setting = {
            'cookie_secret': 'DFksdfsasdfkasdfFKwlwfsdfsa1204mx',
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'debug': False,
        }

        tornado.web.Application.__init__(self, handlers, **setting)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port, options.host)
    # server.listen(options.port)
    processes_num = 15  # 5
    print u'processes_num = ', processes_num
    server.start(num_processes=processes_num)
    print "Run server on %s:%s" % (options.host, options.port)
    tornado.ioloop.IOLoop.instance().start()
