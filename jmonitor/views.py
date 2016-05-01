# coding:utf-8
import traceback
from datetime import datetime as dt
from datetime import timedelta
from django.db.models import Q
from jasset.asset_api import *
from jumpserver.api import *
from jumpserver.models import Setting
from jasset.forms import AssetForm, IdcForm
from jasset.models import Asset, IDC, AssetGroup, AssetGroup1, ASSET_TYPE, ASSET_STATUS, Domains
from jperm.perm_api import get_group_asset_perm, get_group_user_perm
from jperm.models import PermRuleDomain
from jlog.models import RsyncCheckLog, CustomLog
from jmonitor.models import TcpConnCount, DiskSize
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

    module_name = q.get('module_name', '')
    module_name_list = []
    path_name_list = []
    filtered_assets = []
    selected_group1 = None

    group1_list = AssetGroup1.objects.all()
    for gp1 in group1_list:
        if gp1.module_path and isinstance(gp1.module_path, basestring):
            path_str = gp1.module_path
            pairs = path_str.split(',')
            for pair in pairs:
                modu_name1 = pair.split('=')[0].strip()
                path_name1 = pair.split('=')[-1].strip()
                if modu_name1 not in module_name_list:
                    module_name_list.append([modu_name1, gp1])
                if path_name1 not in path_name_list:
                    path_name_list.append([path_name1, gp1])
                if module_name == modu_name1:
                    selected_group1 = gp1

    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", False)
    group_id = request.GET.get("group_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if module_name:
        asset_find = Asset.objects.filter(group1=selected_group1)
    else:
        asset_find = Asset.objects.exclude(group1__isnull=True)


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
        for i in asset_find:
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
    new_list = []
    for k1, k2 in module_name_list:
        new_list.append({'k1': k1, 'k2': k2.name})
    module_name_list = new_list

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
        module_name = request.POST.get('module_name', '').strip()
        name = unicode(request.user.username) + ' - ' + u'check status'
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

        for at in asset_list:
            rsync_log = RsyncCheckLog()
            rsync_log.user = unicode(request.user.username)
            rsync_log.host = at.hostname
            rsync_log.remote_ip = at.ip
            rsync_log.check_status = 'running'
            rsync_log.result_tag = u'检测中'
            rsync_log.save()

            log_id = rsync_log.pk

            try:
                result_tag = u'正常'
                # down_module_key_dict = rc.get_module_key_dict(at.ip, at.port, at.username, at.passwd)
                gp1_list = at.group1.all()
                path_list = []
                for gp1 in gp1_list:
                    if gp1 and gp1.module_path:
                        path_str = gp1.module_path
                        pairs = path_str.split(',')
                        for pair in pairs:
                            modu_name1 = pair.split('=')[0].strip()
                            path_name1 = pair.split('=')[-1].strip()
                            if path_name1 and path_name1 not in path_list:
                                # check all module name if module_name is ''
                                if not module_name:
                                    path_list.append([modu_name1, path_name1])
                                else:
                                    if module_name == modu_name1:
                                        path_list.append([modu_name1, path_name1])

                for k, path in path_list:
                    msg = ''
                    rsync_log = get_object(RsyncCheckLog, pk=log_id)
                    if rsync_log:
                        pass
                    else:
                        continue

                    try:
                        # exec cmd
                        cmd = LS_CMD_TMPL + path
                        # get all file for repo first
                        rc.fetch_repo_files(path)

                        file_not_exists, file_err_size, file_err_time, file_count, repo_file_count = rc.compare_files(at, k, cmd)
                        # print 'not_exists count: ', len(file_not_exists)
                        # print 'err_size count: ', len(file_err_size)
                        # print 'err_time count: ', len(file_err_time)
                        # print 'total file count: %d/%d' % (file_count, repo_file_count)
                        # print 'file_not_exists = ', file_not_exists
                        # print 'file_err_size = ', file_err_size
                        # print 'file_err_time = ', file_err_time
                        if file_not_exists or file_err_size or file_err_time:
                            result_tag = u'错误'

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
                        result_tag = u'检测异常'

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


@require_role('user')
def oplog_status(request):
    """
    show all logs
    """

    header_title, path1, path2 = u'操作日志', u'状态监控', u'日志查看'
    username = request.user.username
    users = User.objects.all()

    find_type = request.GET.get('findtype', '')
    find_user = request.GET.get('finduser', '')
    result = request.GET.get('result', '')
    findip = request.GET.get('findip', '')

    if findip:
        find_log_list = list(CustomLog.objects.filter(ip=findip).order_by('-datetime')[:50])
        return my_render('jmonitor/oplog_status.html', locals(), request)

    if find_type or find_user: # 搜索 初始化
        if result in ['success', 'fail']:
            find_log_list = list(CustomLog.objects.filter(user=find_user, title=find_type, result=result).order_by('-datetime')[:50])
        else:
            find_log_list = list(CustomLog.objects.filter(user=find_user, title=find_type).order_by('-datetime')[:100])
    else:
        # 默认搜索登陆用户后50个成功的
        find_log_list = list(CustomLog.objects.filter(user=username, result='fail').order_by('-datetime')[:50])
    return my_render('jmonitor/oplog_status.html', locals(), request)


def get_asset_group_tree(request):
    tree = []
    groups = AssetGroup.objects.all()
    for g in groups:
        g1s = AssetGroup1.objects.filter(group=g)
        g1_asset_list = []
        all_ass_num_in_group = 0
        for g1 in g1s:
            ass_list = Asset.objects.filter(group1=g1)
            if ass_list:
                g1s_ass_list = []
                for a in ass_list:
                    g1s_ass_list.append({'text': u'资产 : ' + a.ip})
                g1_asset_list.append({'text': u'分组 : ' + g1.name + u' [%d]' % len(g1s_ass_list), 'nodes': g1s_ass_list})
                all_ass_num_in_group += len(g1s_ass_list)
            else:
                g1_asset_list.append({'text': u'分组 : ' + g1.name + u' [0]'})

        if g1_asset_list:
            tree.append({'text': u'资产组 : ' + g.name + u' [%d]' % all_ass_num_in_group, 'nodes': g1_asset_list})
        else:
            tree.append({'text': u'资产组 : ' + g.name + u' [0]'})

    return HttpResponse(json.dumps(tree), content_type="application/json")


@require_role('admin')
def graph_index(request):

    path1, path2 = u'状态监控', u'graph'
    # s = TcpConnCount.objects.filter().order_by('-cdt')[500]
    # data_list = ", ".join([str(x.cnt) for x in s])

    return my_render('jmonitor/graph_index.html', locals(), request)


@require_role('admin')
def get_graph_html(request):
  try:
    G = request.GET
    # y = dt.now() - timedelta(days=1)

    t = G['t']
    if t == 'asset':
        t1 = G['t1']
        ip = G['ip'].split(':')[-1].strip()

        if t1 == 'tcp':
            title = u'TCP连接数 - ' + ip
            container_tcp_id = 'container_' + 'tcp_conn_' + ip.replace('.', '_')

            objs = TcpConnCount.objects.filter(ip=ip).order_by('-cdt')[0:288*2]
            data_list = ", ".join([str(x.cnt) for x in objs])

            y = dt.now() - timedelta(minutes=5*len(objs))
            milli_seconds = 5*len(objs) * 60 * 1000
            date_start_list = ', '.join([str(x) for x in [y.year, y.month, y.day, y.hour, y.minute, y.second]])

            return my_render('jmonitor/data_tcp_conn_count.html', locals(), request)

        elif t1 == 'disk_usage':
            title = u'磁盘空间 /home - ' + ip
            container_disk_id = 'container_' + 'disk_' + ip.replace('.', '_')

            objs = DiskSize.objects.filter(ip=ip).order_by('-cdt')[0:288*2]

            y = dt.now() - timedelta(minutes=5*len(objs))
            milli_seconds = 5*len(objs) * 60 * 1000
            date_start_list = ', '.join([str(x) for x in [y.year, y.month, y.day, y.hour, y.minute, y.second]])

            data_list1 = []
            data_list2 = []
            for x in objs:
                data_list1.append(str(x.total))
                data_list2.append(str(x.used))
            data_list1 = ', '.join(data_list1)
            data_list2 = ', '.join(data_list2)

            return my_render('jmonitor/data_disk_size.html', locals(), request)

        elif t1 == 'ifdata':
            title = u'流量 - ' + ip
            container_ifdata_id = 'container_' + 'ifdata_' + ip.replace('.', '_')

            objs = DiskSize.objects.filter(ip=ip).order_by('-cdt')[0:288*2]

            y = dt.now() - timedelta(minutes=5*len(objs))
            milli_seconds = 5*len(objs) * 60 * 1000
            date_start_list = ', '.join([str(x) for x in [y.year, y.month, y.day, y.hour, y.minute, y.second]])

            data_list1 = []
            data_list2 = []
            for x in objs:
                data_list1.append(str(x.total))
                data_list2.append(str(x.used))
            data_list1 = ', '.join(data_list1)
            data_list2 = ', '.join(data_list2)

            return my_render('jmonitor/data_disk_size.html', locals(), request)
        else:
            return HttpResponse('No data')

    else:
        return HttpResponse('Empty graph')
  except Exception, e:
      print u'error: %s' % str(e)
      return HttpResponse(str(e))