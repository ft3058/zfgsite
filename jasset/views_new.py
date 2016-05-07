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
from jasset.models import Asset, IDC, AssetGroup, AssetGroup1, ASSET_TYPE, ASSET_STATUS, Domains
from jperm.perm_api import get_group_asset_perm, get_group_user_perm
from jperm.models import PermRuleDomain
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


def push_target_content_to_host(request):
    try:
        asset_id = int(request.POST.get('asset_id', '99999'))
        script_name = request.POST.get('script_name', '')
        target_script_content = request.POST.get('target_script_content', '')

        if not script_name:
            return HttpResponse('*** script_name is empty ***')

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
        local_dir = pp
        remote_dir = '/root/'
        fname_list = [script_name, ]
        logged_user = request.user.username
        # print '====================================='
        # print a.ip, a.port, a.username, a.passwd, local_dir, remote_dir, fname_list, logged_user
        ct.set_params(a.ip, a.port, a.username, a.passwd, local_dir, remote_dir, fname_list, logged_user)
        ct.start()
        ct.join()

        return HttpResponse('write succ: ' + tmp_file)


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


