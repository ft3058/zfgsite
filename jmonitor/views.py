# coding:utf-8
import traceback
from django.db.models import Q
from jasset.asset_api import *
from jumpserver.api import *
from jumpserver.models import Setting
from jasset.forms import AssetForm, IdcForm
from jasset.models import Asset, IDC, AssetGroup, AssetGroup1, ASSET_TYPE, ASSET_STATUS, Domains
from jperm.perm_api import get_group_asset_perm, get_group_user_perm
from jperm.models import PermRuleDomain
from jlog.models import RsyncCheckLog
from rsync_util import *


# Create your views here.
@require_role('user')
def rsync_status_list(request):
    """
    asset list domain view
    """
    q = request.GET
    header_title, path1, path2 = u'查看Rsync状态', u'状态管理', u'查看状态'
    username = request.user.username
    user_perm = request.session['role_id']

    # -----------------------------------------------------
    path1 = q.get('path1', '')
    path2 = q.get('path2', '')
    path3 = q.get('path3', '')
    path4 = q.get('path4', '')
    path5 = q.get('path5', '')
    path6 = q.get('path6', '')
    path7 = q.get('path7', '')
    path8 = q.get('path8', '')
    module_name = q.get('module_name', '')

    path1_list = []
    path2_list = []
    path3_list = []
    path4_list = []
    path5_list = []
    path6_list = []
    path7_list = []
    path8_list = []
    module_name_all = []

    domain_list = Domains.objects.all()
    for d in domain_list:
        if d.path1 and d.path1 not in path1_list:
            path1_list.append(d.path1)
        if d.path2 and d.path2 not in path2_list:
            path2_list.append(d.path2)
        if d.path3 and d.path3 not in path3_list:
            path3_list.append(d.path3)
        if d.path4 and d.path4 not in path4_list:
            path4_list.append(d.path4)
        if d.path5 and d.path5 not in path5_list:
            path5_list.append(d.path5)
        if d.path6 and d.path6 not in path6_list:
            path6_list.append(d.path6)
        if d.path7 and d.path7 not in path7_list:
            path7_list.append(d.path7)
        if d.path8 and d.path8 not in path8_list:
            path8_list.append(d.path8)
        # add module
        if d.module_name and d.module_name not in module_name_all:
            module_name_all.append(d.module_name)

    print 'path1_list = ', path1_list
    print 'path2_list = ', path2_list
    print 'path3_list = ', path3_list

    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", False)
    group_id = request.GET.get("group_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if user_perm != 0:
        asset_find = Asset.objects.all()
    else:
        asset_id_all = []
        user = get_object(User, username=username)
        asset_perm = get_group_user_perm(user) if user else {'asset': ''}
        user_asset_perm = asset_perm['asset'].keys()
        for asset in user_asset_perm:
            asset_id_all.append(asset.id)
        asset_find = Asset.objects.filter(pk__in=asset_id_all)
        asset_group_all = list(asset_perm['asset_group'])

    domains_list = Domains.objects.all()

    if module_name:
        domains_list = domains_list.filter(module_name=module_name)
    if path1:
        domains_list = domains_list.filter(path1=path1)
    if path2:
        domains_list = domains_list.filter(path2=path2)
    if path3:
        domains_list = domains_list.filter(path3=path3)
    if path4:
        domains_list = domains_list.filter(path4=path4)
    if path5:
        domains_list = domains_list.filter(path5=path5)
    if path6:
        domains_list = domains_list.filter(path6=path6)
    if path7:
        domains_list = domains_list.filter(path7=path7)
    if path8:
        domains_list = domains_list.filter(path8=path8)

    asset_find = []
    for d in domains_list:
        asset_finds = d.asset_set.all()
        for a in asset_finds:
            asset_find.append(a)

    if keyword:
        '''
        asset_find = asset_find.filter(
            Q(hostname__contains=keyword) |
            Q(other_ip__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(remote_ip__contains=keyword) |
            Q(comment__contains=keyword) |
            Q(username__contains=keyword) |
            Q(group__name__contains=keyword) |
            Q(cpu__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(brand__contains=keyword) |
            Q(cabinet__contains=keyword) |
            Q(sn__contains=keyword) |
            Q(system_type__contains=keyword) |
            Q(system_version__contains=keyword))'''
        new_list = []
        print 'len: ', len(asset_find)
        for i in asset_find:
            print '----',  i.ip
            if keyword in i.hostname or keyword in i.ip:
                new_list.append(i)
        asset_find = new_list

    if export:
        if asset_id_all:
            asset_find = []
            for asset_id in asset_id_all:
                asset = get_object(Asset, id=asset_id)
                if asset:
                    asset_find.append(asset)
        s = write_excel(asset_find)
        if s[0]:
            file_name = s[1]
        smg = u'excel文件已生成，请点击下载!'
        return my_render('jasset/asset_excel_download.html', locals(), request)

    # ------------------------------get extra data----------------------------------------------------
    for at in asset_find:
        # find rsync log
        logs = list(RsyncCheckLog.objects.filter(remote_ip=at.ip).order_by('-id')[:1])
        if logs:
            at.last_dt = logs[0].datetime.strftime("%Y-%m-%d/%H:%M:%S")
            at.result_tag = logs[0].result_tag
            at.file_num = "<br/>".join([x.strip() for x in logs[0].file_num.split('|')])
        else:
            at.last_dt = 'Null'
            at.result_tag = 'Null'
            at.file_num = 'Null'


    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    # if user_perm != 0:
    return my_render('jmonitor/rsync_status_list.html', locals(), request)
    # else:
    #     return my_render('jasset/asset_cu_list.html', locals(), request)



@require_role("user")
def rsync_status_check(request):
    """
    check rsync status for assets
    """
    if request.method == 'POST':
        # asset_id_all = request.GET.get('asset_id_all', '')
        # arg =  287 name =  admin - check status
        asset_id_all = unicode(request.POST.get('asset_id_all', ''))
        name = unicode(request.user.username) + ' - ' + u'check status'
        print 'asset_id_all = ', asset_id_all, 'name = ', name
        # asset_ansible_update(asset_list, name)

        if not asset_id_all.strip():
            return HttpResponse(u'参数不正确!')

        asset_list = []
        asset_id_all = asset_id_all.split(',')
        for asset_id in asset_id_all:
            asset = get_object(Asset, id=asset_id)
            if asset:
                asset_list.append(asset)

        rc = RsyncCheck()

        # module_name = '391kComApk'
        rc.get_module_key_dict(IP, PORT, USERNAME, PASSWORD, setrepo=True)
        print u'read rsyncd.conf succ ... '
        # path = rc.module_path_dict.get(module_name)
        # print u'start fetch repo files..'
        # rc.fetch_repo_files(path)e

        for at in asset_list:
            rsync_log = RsyncCheckLog()
            rsync_log.user = unicode(request.user.username)
            rsync_log.host = at.hostname
            rsync_log.remote_ip = at.ip
            rsync_log.check_status = 'running'
            rsync_log.result_tag = u'检测中'
            rsync_log.save()

            log_id = rsync_log.pk
            print u'current log id: ', log_id

            try:
                print u'compareing ip: ', at.ip
                down_module_key_dict = rc.get_module_key_dict(at.ip, at.port, at.username, at.passwd)
                result_tag = u'正常'

                for k, path in down_module_key_dict.items():
                    msg = ''
                    rsync_log = get_object(RsyncCheckLog, pk=log_id)
                    if rsync_log:
                        print 'found a instance...'
                    else:
                        print 'not found a instance... '
                        continue

                    print '++++++++++++++++++++', k, path

                    try:
                        # exec cmd
                        cmd = LS_CMD_TMPL + path
                        # get all file for repo first
                        rc.fetch_repo_files(path)

                        file_not_exists, file_err_size, file_err_time, file_count, repo_file_count = rc.compare_files(at, k, cmd)
                        print 'not_exists count: ', len(file_not_exists)
                        print 'err_size count: ', len(file_err_size)
                        print 'err_time count: ', len(file_err_time)
                        print 'total file count: %d/%d' % (file_count, repo_file_count)
                        print 'file_not_exists = ', file_not_exists
                        print 'file_err_size = ', file_err_size
                        print 'file_err_time = ', file_err_time
                        if file_not_exists or file_err_size or file_err_time:
                            result_tag = u'错误'
                            print u'错误'
                            print
                            print
                        else:
                            print 'no error.....'


                        tmp = str(rsync_log.file_num) if rsync_log.file_num else ''
                        rsync_log.file_num = tmp + ' [path=%s %d/%d] |' % (path, file_count, repo_file_count)

                        # save the data
                        tmp = str(rsync_log.cmd) if rsync_log.cmd else ''
                        rsync_log.cmd = tmp + ' [cmd=(%s)] |' % cmd

                        tmp = str(rsync_log.file_not_exists) if rsync_log.file_not_exists else ''
                        rsync_log.file_not_exists = tmp + ' [path=(%s) %s] |' % (path, ','.join([f.fname for f in file_not_exists]))

                        tmp = str(rsync_log.file_err_size) if rsync_log.file_err_size else ''
                        rsync_log.file_err_size = tmp + ' [path=(%s) %s] |' % (path, ','.join([f.fname for f in file_err_size]))

                        tmp = str(rsync_log.file_err_time) if rsync_log.file_err_time else ''
                        rsync_log.file_err_time = tmp + ' [path=(%s) %s] |' % (path, ','.join([f.fname for f in file_err_time]))

                    except Exception, e1:
                        msg = str(e1)

                    if not msg:
                        msg = u'命令执行完成！'
                    rsync_log.result = msg
                    rsync_log.save()

                rsync_log.result_tag = result_tag
                rsync_log.check_status = 'finished'
                rsync_log.save()
            except Exception, e:
                err = u'检测中出错: %s, msg: %s' % (at.ip, str(e))
                rsync_log = get_object(RsyncCheckLog, pk=log_id)
                rsync_log.result_tag = u'检测异常'
                rsync_log.check_status = 'error'
                rsync_log.result = err
                rsync_log.save()

        return HttpResponse(u'批量更新成功!')
    return HttpResponse(u'批量更新成功!')


@require_role('admin')
def rsync_status_detail(request):
    """
    Asset detail view
    """
    header_title, path1, path2 = u'Rsync同步状态信息(最近一次检测)', u'Rsync管理', u'状态详情'
    asset_id = request.GET.get('id', '')
    asset = get_object(Asset, id=asset_id)
    # print 'asset username = ', asset.username
    # print 'asset passwd = ', asset.passwd None

    # perm_info = get_group_asset_perm(asset)
    # log = Log.objects.filter(host=asset.hostname)
    # find rsync log

    logs = list(RsyncCheckLog.objects.filter(remote_ip=asset.ip).order_by('-id')[:1])
    file_not_exists_list = []
    file_err_size_list = []
    file_err_time_list = []
    log_detail = 'No Error'
    file_num_list = []

    if logs:
        log = logs[0]
        # 1
        file_not_exists = log.file_not_exists

        if file_not_exists:
            paths = filter(None, [x.strip() for x in file_not_exists.split('|')])
            for path in paths:
                # ['[path=/a/b 1.txt,2.txt]', '[path=/c/d 8.bak,9.bak]']
                path = path.replace('[path=', '').replace(']', '')
                print '-path-', path
                path_head = path.split(' ')[0].replace('(', '').replace(')', '')
                path_tail = path.split(' ')[-1]
                for l in path_tail.split(','):
                    l = l.strip()
                    if l:
                        file_not_exists_list.append(os.path.join(path_head, l))

        # 2
        file_err_size = log.file_err_size
        if file_err_size:
            paths = filter(None, [x.strip() for x in file_err_size.split('|')])
            for path in paths:
                # ['[path=/a/b 1.txt,2.txt]', '[path=/c/d 8.bak,9.bak]']
                path = path.replace('[path=', '').replace(']', '')
                print '-path-', path
                path_head = path.split(' ')[0].replace('(', '').replace(')', '')
                path_tail = path.split(' ')[-1]
                for l in path_tail.split(','):
                    l = l.strip()
                    if l:
                        file_err_size_list.append(os.path.join(path_head, l))

        # 3
        file_err_time = log.file_err_time
        if file_err_time:
            paths = filter(None, [x.strip() for x in file_err_time.split('|')])
            for path in paths:
                # ['[path=/a/b 1.txt,2.txt]', '[path=/c/d 8.bak,9.bak]']
                path = path.replace('[path=', '').replace(']', '')
                print '-path-', path
                path_head = path.split(' ')[0].replace('(', '').replace(')', '')
                path_tail = path.split(' ')[-1]
                for l in path_tail.split(','):
                    l = l.strip()
                    if l:
                        file_err_time_list.append(os.path.join(path_head, l))
        log_detail = log.result
        # at.file_num = "<br/>".join([x.strip() for x in logs[0].file_num.split('|')])
        for x in [x.strip() for x in logs[0].file_num.split('|')]:
            x = x.replace('[path=', '').replace(']', '')
            file_num_list.append({'path': x.split(' ')[0], 'desc': x.split(' ')[-1]})

    file_not_exists_list_count = len(file_not_exists_list)
    file_err_size_list_count = len(file_err_size_list)
    file_err_time_list_count = len(file_err_time_list)
    return my_render('jmonitor/rsync_detail.html', locals(), request)