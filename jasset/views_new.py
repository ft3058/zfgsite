# coding:utf8
"""

"""
import socket
import string
from random import choice
from django.db.models import Q
from jasset.asset_api import *
from jasset.asset_scripts import *
from jumpserver.api import *
from jumpserver.models import Setting
from jasset.forms import AssetForm, IdcForm
from jasset.models import Asset, IDC, AssetGroup, AssetGroup1, DomainGroup
from util import get_random_str, write_log
from script_init_server import init_server, clear_asset
from script_copy_files import copy_file_to_server


from const import MAKE_DIR_PART, RSYNC_SCRIPT_PART
script_dir = '/root/scripts/tmpl'


@require_role('admin')
def biz_edit(request):
    header_title, path1, path2 = u'业务变更', u'资产管理', u'业务变更'
    asset_id = request.GET.get('id', '')
    asset = get_object(Asset, id=asset_id)

    # check out all tmpl files
    script_names = []
    for i in os.listdir(script_dir):
        if os.path.isfile(os.path.join(script_dir, i)):
            script_names.append(i)

    if request.method == 'POST':
        print  u'推送..'
        # return HttpResponseRedirect(reverse('idc_list'))
        return HttpResponse(u'yes')
    else:
        # idc_form = IdcForm(instance=idc)
        return my_render('jasset/biz_edit.html', locals(), request)


def load_script_content(request):
    script_name = request.GET.get('script_name', '')
    if not script_name:
        return HttpResponse('')
    script_path = os.path.join(script_dir, script_name)
    if not os.path.exists(script_path):
        return HttpResponse('')
    s = ''
    with open(script_path) as f:
        s = f.read()
    # s = s.replace('MAKE_DIR_PART', MAKE_DIR_PART).replace('RSYNC_SCRIPT_PART', RSYNC_SCRIPT_PART)
    return HttpResponse(s)


def add_new_tmpl_name(request):
    """just create a new tmpl file"""
    new_tmpl_name = request.GET.get('new_tmpl_name', '').strip()
    if not new_tmpl_name:
        return HttpResponse('')
    script_path = os.path.join(script_dir, new_tmpl_name)
    if not os.path.exists(script_path):
        with open(script_path, 'w') as f:
            f.write('')
        return HttpResponse(u'已经新建立一个空模板！')

    return HttpResponse(u'已经存在')

def del_tmpl_name(request):
    script_name = request.GET.get('script_name', '').strip()
    if not script_name:
        return HttpResponse('')
    script_path = os.path.join(script_dir, script_name)
    if not os.path.exists(script_path):
        return HttpResponse(u'模板不存在!')
    else:
        os.remove(script_path)
        return HttpResponse(u'删除成功!')


def update_tmpl_content(request):
    try:
        script_name = request.POST.get('script_name')
        tmpl_content = request.POST.get('tmpl_content')
        script_path = os.path.join(script_dir, script_name)
        # print tmpl_content
        # print '---', script_path, script_name
        with open(script_path, 'w') as f:
            f.write(tmpl_content.encode('utf8'))
        return HttpResponse("update successful !")
    except Exception, e:
        return HttpResponse(str(e))

def gen_target_content(request):
    """
    变量名
    YxdownPhoneAndroid=/home/yxdown/phone/android

    $yuming  sync.yxdown.cn
    $Rsync   YxdownPhoneAndroid
    $Rpath   /home/yxdown/phone/android
    """
    try:
        asset_id = request.POST.get('asset_id', '')
        script_name = request.POST.get('script_name', '')
        tmpl_content = request.POST.get('tmpl_content', '')

        asset = get_object(Asset, id=int(asset_id))
        if not asset:
            return HttpResponse('not found asset id :' + asset_id)
        yuming = 'sync.yxdown.cn'

        group1 = asset.group1.all()
        if not group1:
            return HttpResponse('***sub group is None!***')
        if not group1[0].module_path:
            return HttpResponse('***module_path is not set!***')

        path_str = group1[0].module_path
        pairs = path_str.split(',')
        names_list = []

        make_dir_part = ''
        rsync_script_part = ''
        for pair in pairs:
            modu_name1 = pair.split('=')[0].strip()
            path_name1 = pair.split('=')[-1].strip()
            names_list.append([modu_name1, path_name1])

            make_dir_part += MAKE_DIR_PART.replace('$Rpath', path_name1)
            rsync_script_part += RSYNC_SCRIPT_PART\
                .replace('$yuming', yuming)\
                .replace('$Rsync', modu_name1)\
                .replace('$Rpath', path_name1)

        target_content = tmpl_content.replace('MAKE_DIR_PART', make_dir_part).replace('RSYNC_SCRIPT_PART', rsync_script_part)
        return HttpResponse(target_content)
    except Exception, e:
        return HttpResponse('***' + str(e) + '***')

def get_ssh(host, port, username, password,timeout=10):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=host, port=int(port), username=username, password=password, timeout=timeout)
    return s


def copy_files_and_restart_service(host, port, username, password, module_path_list, target_file_path):
    try:
        s = get_ssh(host, port, username, password)
        ssh = s.invoke_shell()

        # rm vhost
        cmd = '/bin/rm /usr/local/nginx/conf/vhost/*.conf \n'
        print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        print 'rm vhost conf complete..'
        write_log(ip=host, cmd=cmd, title='rm_vhost', result="succ")

        cmd = '/bin/cp /tmp/*.conf /usr/local/nginx/conf/vhost/ \n'
        print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        print 'rm /tmp/*.conf complete..'
        write_log(ip=host, cmd=cmd, title='rm_vhost', result="succ")

        # rm rsync.sh
        cmd = '/bin/rm /root/rsync.sh \n'
        print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        print 'rm rsync.sh complete..'
        write_log(ip=host, cmd=cmd, title='rm_rsync', result="succ")

        # rm module path files
        cmd = '/bin/rm -rf %s \n' % ' '.join(module_path_list)
        print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        print 'rm rsync.sh complete..'
        write_log(ip=host, cmd=cmd, title='rm_rsync', result="succ")

        # kill
        cmd = '/bin/killall -9 rsync \n'
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(1)
        print 'killall -9 rsync complete..'
        write_log(ip=host, cmd=cmd, title='kill rsync', result="succ")

        # copy tmp file to /root
        cmd = '/bin/cp %s /root \n' % target_file_path
        print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(0.5)
        print 'cp succ..'
        write_log(ip=host, cmd=cmd, title='copy_file', result="succ")

        cmd = 'service nginx restart \n'
        write_log(ip=host, cmd=cmd, title='copy_file', result="succ ")
        # print 'run CMD: ', cmd
        ssh.send(cmd)
        time.sleep(1)
        # print 'complete..'
        write_log(ip=host, cmd='', title='copy_file', result="copy complete .. ")
        s.close()
    except:
        try:
            s.close()
        except:
            pass


def push_target_content_to_host(request):
    try:
        asset_id = int(request.POST.get('asset_id', '99999'))
        script_name = request.POST.get('script_name', '')
        target_script_content = request.POST.get('target_script_content', '')

        if not script_name:
            return HttpResponse('*** script_name is empty ***')

        # 1.copy new file to server (/tmp dir)

        tmp_dir_name = ''.join([choice(string.letters) for x in range(3)])
        pp = '/tmp/'+ tmp_dir_name + '/'
        if not os.path.exists(pp):
            os.mkdir(pp)
        tmp_file = pp + script_name
        with open(tmp_file, 'w') as f:
            f.write(target_script_content.encode('utf8'))
        # time.sleep(3)
        # copy tmp file to remote server
        from script_copy_files import CopyThread
        ct = CopyThread()
        a = get_object(Asset, id=asset_id)

        # get some dir
        gp1_list = a.group1.all()
        module_path_list = []
        script_path = ''
        for gp1 in gp1_list:
            if gp1 and gp1.module_path:
                ppaths = gp1.module_path.split(',')
                for i in ppaths:
                    mod_path = i.split('=')[-1].strip()
                    if mod_path and mod_path not in module_path_list:
                        module_path_list.append(mod_path)
            if gp1 and gp1.script_path:
                script_path = gp1.script_path

        print 'module_path_list = ', module_path_list
        print 'script_path = ', script_path

        local_dir = pp
        remote_dir = '/tmp/'
        fname_list = [script_name, ]
        if script_path:
            # 需要将在数据库中配置好的路径[/var/serconf/nginx/yxdown.com/phone/android ]，
            # 转化成在jumpserver上的路径[/root/scripts/nginx/yxdown.com/phone/android ]
            jump_path = script_path.replace('/var/serconf', '/root/scripts')
            for ff in os.listdir(jump_path):
                if ff.endswith('.conf'):
                    fname_list.append(os.path.join(jump_path, ff))
        logged_user = request.user.username
        # print '====================================='
        # print a.ip, a.port, a.username, a.passwd, local_dir, remote_dir, fname_list, logged_user
        ct.set_params(a.ip, a.port, a.get_username(), a.passwd, local_dir, remote_dir, fname_list, logged_user)
        ct.start()
        ct.join()
        print 'copy succc...'

        # 2.delete old rsync.sh etc and restart ng
        remote_tmp_fname = remote_dir + script_name
        print 'remote_tmp_fname = ', remote_tmp_fname
        copy_files_and_restart_service(a.ip, a.port, a.get_username(), a.passwd, module_path_list, remote_tmp_fname)

        print 'all succ...'

        allfile = '/root/' + script_name + ', ' + ','.join(module_path_list) + ', /usr/local/nginx/conf/vhost/*.conf'
        return HttpResponse(u'推送完成（复制文件［%s］，删除文件［%s］，重启nginx） !' % (script_name, allfile))

    except Exception, e:
        return HttpResponse('Error:' + str(e))


@require_role('admin')
def biz_start(request)    :
    pass



@require_role('admin') # /asset/clear_asset/ 清理主机
def asset_clear_asset(request):
    if request.method == 'POST':
        ip = request.POST.get('ip', '')
        if ip:
            try:
                asset = Asset.objects.get(ip=ip)
                text = clear_asset(asset.ip, asset.port, asset.username, asset.passwd, request.user.username)
                return HttpResponse(json.dumps({'error':'0','info': text}), content_type="application/json")
                # return my_render(request.META.get('HTTP_REFERER','/'), "<script>alert('a');</script>", request)
            except Asset.DoesNotExist:
                return HttpResponse(json.dumps({'error':'1','info':'不存在的主机资源'}), content_type="application/json")
            except paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException:
                return HttpResponse(json.dumps({'error':'1','info':'认证失败 (可能错误:密码错误)'}), content_type="application/json")
            except socket.error:
                return HttpResponse(json.dumps({'error':'1','info':'端口可能出错'}), content_type="application/json")
            except:
                return HttpResponse(json.dumps({'error':'1','info':'未知错误,请查看日志,并提交给管理员'}), content_type="application/json")

@require_role('admin')
def dmgroup_list(request):
    """
    list asset group
    列出资产组
    """
    header_title, path1, path2 = u'查看资产组', u'资产管理', u'查看域名组'
    keyword = request.GET.get('keyword', '')
    domain_group_list = DomainGroup.objects.all()
    '''
    domain_id = request.GET.get('id')
    if domain_id:
        asset_group_list = asset_group_list.filter(id=group_id)
    if keyword:
        asset_group_list = asset_group_list.filter(Q(name__contains=keyword) | Q(comment__contains=keyword))
    '''
    # asset_group_list, p, asset_groups, page_range, current_page, show_first, show_end = pages(asset_group_list, request)
    domain_group_list, p, asset_groups, page_range, current_page, show_first, show_end = pages(domain_group_list, request)
    return my_render('jasset/dmgroup_list.html', locals(), request)

@require_role('admin')
def dmgroup_add(request):
    header_title, path1, path2 = u'资产管理', u'域名组管理', u'添加域名组'
    # asset_all = Asset.objects.all()
    # this asset repr assetgroup
    asset_all = AssetGroup.objects.all()

    if request.method == 'POST':
        P = request.POST
        name = P.get('name', '')
        asset_select = P.getlist('asset_select', [])
        comment = request.POST.get('comment', '')

        try:
            if not name:
                emg = u'域名不能为空'
                raise ServerError(emg)

            domain_group_test = get_object(DomainGroup, name=name)
            if domain_group_test:
                emg = u"域名 %s 已存在" % name
                raise ServerError(emg)

        except ServerError:
            pass

        else:
            db_add_dmgroup(name=name, comment=comment, asset_select=asset_select)
            smg = u"主机组 %s 添加成功" % name
            return my_render('jasset/dmgroup_add.html', locals(), request)

    return my_render('jasset/dmgroup_add.html', locals(), request)


def dmgroup_edit(request):
    header_title, path1, path2 = u'资产管理', u'域名组管理', u'编辑域名组'

    if request.method == 'GET':
        dmgroup_id = request.GET.get('id')
        dmgroup = DomainGroup.objects.get(id=dmgroup_id)
        # this asset repr assetgroup
        finds = AssetGroup.objects.all()
        asset_all = []
        asset_select = []

        for i in finds:
            if i.domain_group and i.domain_group.name == dmgroup.name:
                asset_select.append(i)
            else:
                asset_all.append(i)
        return my_render('jasset/dmgroup_edit.html', locals(), request)

    elif request.method == 'POST':
        P = request.POST
        name = P.get('name', '')
        asset_select = P.getlist('asset_select', [])
        comment = request.POST.get('comment', '')
        dmgroup = DomainGroup.objects.get(name=name)
        # remove dmgroup from each group
        for gp in AssetGroup.objects.filter(domain_group=dmgroup):
            # gp = AssetGroup.objects.get(id=groupid)
            gp.domain_group = None
            gp.save()
        dmgroup.comment = comment
        dmgroup.save()
        db_edit_dmgroup(name=name, comment=comment, asset_select=asset_select)
        smg = u"主机组 %s 修改成功" % name
        return my_render('jasset/dmgroup_edit.html', locals(), request)


@require_role('admin')
def dmgroup_del(request):
    dmgroup_ids = request.GET.get('id', '')
    dmgroup_ids = dmgroup_ids.split(',')

    if dmgroup_ids:
        for _id in dmgroup_ids:
            DomainGroup.objects.filter(id=_id).delete()
            '''
            # delete group1
            group1_list = AssetGroup1.objects.filter(group__id=group_id)
            for gp1 in group1_list:
                # remove gp1 from asset first
                for ast in Asset.objects.filter(group1=gp1):
                    ast.group1.filter(id=gp1.id).delete()
                    print u'remove group1[%d] from asset[%d]' % (gp1.id, ast.id)
                gp1.delete()
                print u'AssetGroup1 [id=%d] is deleted!' % gp1.id
            '''
        return HttpResponse(u'删除成功')
    else:
        return HttpResponse(u'not exists this dmgroup_ids id: %s' % dmgroup_ids)
