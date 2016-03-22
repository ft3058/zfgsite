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


@require_role('admin')
def group_add(request):
    """
    Group add view
    添加资产组
    """
    header_title, path1, path2 = u'添加资产组', u'资产管理', u'添加资产组'
    asset_all = Asset.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '')
        asset_select = request.POST.getlist('asset_select', [])
        comment = request.POST.get('comment', '')

        try:
            if not name:
                emg = u'组名不能为空'
                raise ServerError(emg)

            asset_group_test = get_object(AssetGroup, name=name)
            if asset_group_test:
                emg = u"该组名 %s 已存在" % name
                raise ServerError(emg)

        except ServerError:
            pass

        else:
            db_add_group(name=name, comment=comment, asset_select=asset_select)
            smg = u"主机组 %s 添加成功" % name

    return my_render('jasset/group_add.html', locals(), request)


@require_role('admin')
def group1_add(request):
    """
    Group1 add view
    添加资产组
    """
    header_title, path1, path2 = u'添加资产组分组', u'资产管理', u'添加资产分组'
    group_id = request.GET.get('id', 0)
    if not group_id:
        return HttpResponse('group id is empty!')
    print 'group_id : ', group_id
    gp = get_object(AssetGroup, id=group_id)
    # asset_all = Asset.objects.all()
    asset_all = Asset.objects.filter(group=gp)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        asset_select = request.POST.getlist('asset_select', [])
        print 'added list:', ',,'.join(asset_select)
        comment = request.POST.get('comment', '')

        try:
            if not name:
                emg = u'组名不能为空'
                raise ServerError(emg)

            asset_group_test = get_object(AssetGroup1, name=name)
            if asset_group_test:
                emg = u"该组名 %s 已存在" % name
                raise ServerError(emg)

        except ServerError:
            pass

        else:
            db_add_group1(name=name, comment=comment, asset_select=asset_select, group=gp)
            smg = u"主机分组 %s 添加成功" % name

    return my_render('jasset/group1_add.html', locals(), request)


@require_role('admin')
def group1_edit(request):
    """
    Group1 add view
    modify资产组
    http://127.0.0.1:8000/jasset/group1/edit/?group1_id=7&gourp_id=15
    """
    header_title, path1, path2 = u'修改资产组分组', u'资产管理', u'修改资产分组'
    '''
    group_id = request.GET.get('id', 0)
    if not group_id:
        return HttpResponse('group_id is empty!')'''

    group1_id = request.GET.get('id', 0)
    if not group1_id:
        return HttpResponse('group1_id is empty!')

    group1 = get_object(AssetGroup1, id=group1_id)
    if not group1:
        return HttpResponse('not found group1!')
    group = group1.group  # get_object(AssetGroup, id=group_id)

    # available for select
    if group:
        asset_all = Asset.objects.filter(group=group)
    else:
        asset_all = Asset.objects.all()
    asset_exist = Asset.objects.filter(group=group, group1=group1)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        module_path = request.POST.get('module_path', '')
        asset_select = request.POST.getlist('asset_select', [])
        print 'added list:', ',,'.join(asset_select)
        comment = request.POST.get('comment', '')

        edit_group1 = None
        try:
            if not name:
                emg = u'组名不能为空'
                raise ServerError(emg)

            edit_group1 = get_object(AssetGroup1, name=name)
            if not edit_group1:
                edit_group1 = AssetGroup1(name=name, group=group, comment=comment, module_path=module_path)
                edit_group1.save()

        except ServerError:
            pass

        else:
            # db_add_group1(name=name, comment=comment, asset_select=asset_select, group=group)
            # group1.save()
            group1.name = name.strip()
            group1.group = group
            group1.comment = comment.strip()
            group1.module_path = module_path.strip()
            group1.save()

            # delete all group1 for every asset
            for at in asset_exist:
                at.group1.remove(group1)

            for asset_id in asset_select:
                group1_add_asset(edit_group1, asset_id)
            smg = u"主机分组 %s 修改成功" % name

    return my_render('jasset/group1_edit.html', locals(), request)


@require_role('admin')
def group_edit(request):
    """
    Group edit view
    编辑资产组
    """
    header_title, path1, path2 = u'编辑主机组', u'资产管理', u'编辑主机组'
    group_id = request.GET.get('id', '')
    group = get_object(AssetGroup, id=group_id)

    asset_all = Asset.objects.all()
    asset_select = Asset.objects.filter(group=group)
    asset_no_select = [a for a in asset_all if a not in asset_select]

    if request.method == 'POST':
        name = request.POST.get('name', '')
        asset_select = request.POST.getlist('asset_select', [])
        comment = request.POST.get('comment', '')

        try:
            if not name:
                emg = u'组名不能为空'
                raise ServerError(emg)

            if group.name != name:
                asset_group_test = get_object(AssetGroup, name=name)
                if asset_group_test:
                    emg = u"该组名 %s 已存在" % name
                    raise ServerError(emg)

        except ServerError:
            pass

        else:
            group.asset_set.clear()
            db_update_group(id=group_id, name=name, comment=comment, asset_select=asset_select)
            smg = u"主机组 %s 添加成功" % name

        return HttpResponseRedirect(reverse('asset_group_list'))

    return my_render('jasset/group_edit.html', locals(), request)


@require_role('admin')
def group_list(request):
    """
    list asset group
    列出资产组
    """
    header_title, path1, path2 = u'查看资产组', u'资产管理', u'查看资产组'
    keyword = request.GET.get('keyword', '')
    asset_group_list = AssetGroup.objects.all()
    group_id = request.GET.get('id')
    if group_id:
        asset_group_list = asset_group_list.filter(id=group_id)
    if keyword:
        asset_group_list = asset_group_list.filter(Q(name__contains=keyword) | Q(comment__contains=keyword))

    asset_group_list, p, asset_groups, page_range, current_page, show_first, show_end = pages(asset_group_list, request)
    return my_render('jasset/group_list.html', locals(), request)


@require_role('admin')
def group1_list(request):
    """
    list asset group
    列出资产分组
    """
    header_title, path1, path2 = u'查看资产分组', u'资产管理', u'查看资产分组'
    keyword = request.GET.get('keyword', '')
    asset_group_list = AssetGroup1.objects.all()
    group_id = request.GET.get('id')
    if group_id:
        asset_group_list = asset_group_list.filter(id=group_id)
    if keyword:
        asset_group_list = asset_group_list.filter(Q(name__contains=keyword) | Q(comment__contains=keyword))

    asset_group_list, p, asset_groups, page_range, current_page, show_first, show_end = pages(asset_group_list, request)
    return my_render('jasset/group1_list.html', locals(), request)


@require_role('admin')
def domain_group_list(request):
    """ show all domain """
    header_title, path1, path2 = u'查看所有域', u'域管理', u'查看域'
    keyword = request.GET.get('keyword', '')
    # asset_group_list = AssetGroup.objects.all()
    domain_list = Domains.objects.all()
    domain_id = request.GET.get('id')
    if domain_id:
        domain_list = domain_list.filter(id=domain_id)
    if keyword:
        domain_list = domain_list.filter(Q(module_name__contains=keyword) | Q(comment__contains=keyword))

    domain_list, p, domains, page_range, current_page, show_first, show_end = pages(domain_list, request)
    return my_render('jasset/domain_group_list.html', locals(), request)


@require_role('admin')
def group_del(request):
    """
    Group delete view
    删除主机组
    """
    group_ids = request.GET.get('id', '')
    group_id_list = group_ids.split(',')

    for group_id in group_id_list:
        AssetGroup.objects.filter(id=group_id).delete()
        # delete group1
        group1_list = AssetGroup1.objects.filter(group__id=group_id)
        for gp1 in group1_list:
            # remove gp1 from asset first
            for ast in Asset.objects.filter(group1=gp1):
                ast.group1.filter(id=gp1.id).delete()
                print u'remove group1[%d] from asset[%d]' % (gp1.id, ast.id)
            gp1.delete()
            print u'AssetGroup1 [id=%d] is deleted!' % gp1.id
    return HttpResponse(u'删除成功')

@require_role('admin')
def group1_del(request):
    """
    Group delete view
    删除主机fen组
    """
    try:
        group1_ids = request.GET.get('id', '')
        group1_id_list = group1_ids.split(',')
        for group1_id in group1_id_list:
            AssetGroup1.objects.filter(id=int(group1_id)).delete()
        print 'delete succ..'
    except Exception, e:
        print 'delete group1 delete error: %s' % str(e)
    return HttpResponse(u'删除成功')


def asset_add_post(request):
    try:
        if not request.method == 'POST':
            return HttpResponse('only receive post data')
        q = request.POST
        ip = q['ip'].strip()
        port = int(q['port'].strip())
        username = q['account'].strip()
        password = q['password'].strip()
        check_code = q['checkCode'].strip()

        obj = Asset()
        obj.ip = ip
        obj.hostname = ip
        obj.port = port
        obj.username = username
        # obj.password = password
        obj.passwd = password
        password_encode = CRYPTOR.encrypt(password)
        obj.password = password_encode

        obj.check_code = check_code
        obj.save()
        return HttpResponse('success')
    except Exception, e:
        print str(e)
        print traceback.print_exc()
        return HttpResponse('Error: %s' % str(e))


@require_role('admin')
def domain_add(request):
    """
    domain add view
    添加资产组
    """
    header_title, path1, path2 = u'添加资产Domain', u'资产管理', u'添加Domain'

    asset_all = Asset.objects.all()

    if request.method == 'POST':
        module_name = request.POST.get('module_name', '').strip()
        full_path = request.POST.get('full_path', '').strip()
        domain_host = request.POST.get('domain_host', '').strip()
        port = request.POST.get('port', '').strip()
        asset_select = request.POST.getlist('asset_select', [])
        print 'added list:', ',,'.join(asset_select)

        comment = request.POST.get('comment', '')

        try:
            if not module_name:
                emg = u'模块名不能为空'
                raise ServerError(emg)
            if not full_path:
                emg = u'路径不能为空'
                raise ServerError(emg)
            if not domain_host:
                emg = u'主机名不能为空'
                raise ServerError(emg)
            if not port:
                emg = u'端口'
                raise ServerError(emg)

            if not asset_select:
                emg = u'Server List不能为空'
                raise ServerError(emg)

            dom = get_object(Domains, module_name=module_name)
            if dom:
                emg = u"该模块名 %s 已存在" % module_name
                raise ServerError(emg)

        except ServerError:
            pass

        else:
            # db_add_group1(name=name, comment=comment, asset_select=asset_select, group=gp)
            o = Domains()
            o.module_name = module_name
            o.full_path = full_path
            o.domain_host = domain_host
            o.port = int(port)
            o.comment = comment
            paths = filter(None, full_path.split('/'))  # [1:]
            for n, i in enumerate(paths):
                exec "o.path%d = '%s'" % (n+1, i)
            o.save()
            print 'save domains succ!!!!!!'

            o = Domains.objects.get(module_name=module_name)
            for asset_id in asset_select:
                # asset_select is asset id
                print 'process asset_id: ', asset_id
                asset = get_object(Asset, pk=asset_id)
                if asset:
                    # add method is changed
                    # asset.domain = o
                    # asset.save()
                    asset.domains.add(o)
                    asset.save()
                    print 'add to %s: %s' % (asset.ip, str(o))

            smg = u"%s 添加成功" % module_name

    return my_render('jasset/domain_add.html', locals(), request)


@require_role('admin')
def asset_add(request):
    """
    Asset add view
    添加资产
    """
    header_title, path1, path2 = u'添加资产', u'资产管理', u'添加资产'
    asset_group_all = AssetGroup.objects.all()
    af = AssetForm()
    default_setting = get_object(Setting, name='default')
    default_port = default_setting.field2 if default_setting else ''
    if request.method == 'POST':
        af_post = AssetForm(request.POST)
        ip = request.POST.get('ip', '')
        hostname = request.POST.get('hostname', '')
        is_active = True if request.POST.get('is_active') == '1' else False
        use_default_auth = request.POST.get('use_default_auth', '')
        try:
            if Asset.objects.filter(hostname=unicode(hostname)):
                error = u'该主机名 %s 已存在!' % hostname
                raise ServerError(error)

        except ServerError:
            pass
        else:
            if af_post.is_valid():
                asset_save = af_post.save(commit=False)
                if not use_default_auth:
                    password = request.POST.get('password', '')
                    password_encode = CRYPTOR.encrypt(password)
                    asset_save.password = password_encode
                if not ip:
                    asset_save.ip = hostname
                asset_save.is_active = True if is_active else False
                asset_save.save()
                af_post.save_m2m()

                msg = u'主机 %s 添加成功' % hostname
            else:
                esg = u'主机 %s 添加失败' % hostname

    return my_render('jasset/asset_add.html', locals(), request)


@require_role('admin')
def asset_add_batch(request):
    header_title, path1, path2 = u'添加资产', u'资产管理', u'批量添加'
    return my_render('jasset/asset_add_batch.html', locals(), request)


@require_role('admin')
def asset_del(request):
    """
    del a asset
    删除主机
    """
    asset_id = request.GET.get('id', '')
    if asset_id:
        Asset.objects.filter(id=asset_id).delete()

    if request.method == 'POST':
        asset_batch = request.GET.get('arg', '')
        asset_id_all = str(request.POST.get('asset_id_all', ''))

        if asset_batch:
            for asset_id in asset_id_all.split(','):
                asset = get_object(Asset, id=asset_id)
                asset.delete()

    return HttpResponse(u'删除成功')


@require_role(role='super')
def asset_edit(request):
    """
    edit a asset
    修改主机
    """
    header_title, path1, path2 = u'修改资产', u'资产管理', u'修改资产'

    asset_id = request.GET.get('id', '')
    username = request.user.username
    asset = get_object(Asset, id=asset_id)
    if asset:
        password_old = asset.password
    # asset_old = copy_model_instance(asset)
    af = AssetForm(instance=asset)
    if request.method == 'POST':
        af_post = AssetForm(request.POST, instance=asset)
        ip = request.POST.get('ip', '')
        hostname = request.POST.get('hostname', '')
        password = request.POST.get('password', '')
        is_active = True if request.POST.get('is_active') == '1' else False
        use_default_auth = request.POST.get('use_default_auth', '')
        try:
            asset_test = get_object(Asset, hostname=hostname)
            if asset_test and asset_id != unicode(asset_test.id):
                emg = u'该主机名 %s 已存在!' % hostname
                raise ServerError(emg)
        except ServerError:
            pass
        else:
            if af_post.is_valid():
                af_save = af_post.save(commit=False)
                if use_default_auth:
                    af_save.username = ''
                    af_save.password = ''
                    af_save.port = None
                else:
                    if password:
                        af_save.passwd = password
                        password_encode = CRYPTOR.encrypt(password)
                        af_save.password = password_encode
                    else:
                        af_save.password = password_old
                af_save.is_active = True if is_active else False
                af_save.save()
                af_post.save_m2m()
                # asset_new = get_object(Asset, id=asset_id)
                # asset_diff_one(asset_old, asset_new)
                info = asset_diff(af_post.__dict__.get('initial'), request.POST)
                db_asset_alert(asset, username, info)

                smg = u'主机 %s 修改成功' % ip
            else:
                emg = u'主机 %s 修改失败' % ip
                return my_render('jasset/error.html', locals(), request)
            return HttpResponseRedirect(reverse('asset_detail')+'?id=%s' % asset_id)

    return my_render('jasset/asset_edit.html', locals(), request)


@require_role('user')
def asset_list(request):
    """
    asset list view
    """
    header_title, path1, path2 = u'查看资产', u'资产管理', u'查看资产'
    username = request.user.username
    user_perm = request.session['role_id']
    idc_all = IDC.objects.filter()
    asset_group_all = AssetGroup.objects.all()
    asset_types = ASSET_TYPE
    asset_status = ASSET_STATUS
    idc_name = request.GET.get('idc', '')
    group_name = request.GET.get('group', '')
    group1_name = request.GET.get('group1', '')
    asset_type = request.GET.get('asset_type', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", False)
    group_id = request.GET.get("group_id", '')
    group1_id = request.GET.get("group1_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if group_id:
        group = get_object(AssetGroup, id=group_id)
        if group:
            asset_find = Asset.objects.filter(group=group).order_by('-date_added')
            # find sub group (group1) in this group
            asset_group_all1 = AssetGroup1.objects.filter(group=group)

    elif group1_id:
        group1 = get_object(AssetGroup1, id=group1_id)
        if group1:
            asset_find = Asset.objects.filter(group1=group1).order_by('-date_added')
            # find sub group (group1) in this group
            asset_group_all1 = AssetGroup1.objects.filter(id=group1_id)

    elif idc_id:
        idc = get_object(IDC, id=idc_id)
        if idc:
            asset_find = Asset.objects.filter(idc=idc).order_by('-date_added')
    else:
        # SU user
        if user_perm != 0:
            asset_find = Asset.objects.all().order_by('-date_added')
        else:
            # CU user
            asset_id_all = []
            user = get_object(User, username=username)
            asset_perm = get_group_user_perm(user) if user else {'asset': ''}
            user_asset_perm = asset_perm['asset'].keys()
            for asset in user_asset_perm:
                asset_id_all.append(asset.id)

            # find from domains
            # domains_obj = user.domains.all()
            rule_domains_list = PermRuleDomain.objects.filter(user=user)
            print 'len rule_domains_list: ', len(rule_domains_list)

            for rule_dm in rule_domains_list:
                domains = rule_dm.domains.all()
                for dm in domains:
                    print '---domains= ', dm
                    asset_list1 = Asset.objects.filter(domains=dm).order_by('-date_added')
                    for st in asset_list1:
                        print '++++st.id = ', st.id
                        if st.id not in asset_id_all:
                            asset_id_all.append(st.id)

            # Item.objects.filter(Q(creator=owner) | Q(moderated=False))
            # asset_find = Asset.objects.filter(pk__in=asset_id_all)  old
            asset_find = Asset.objects.filter(pk__in=asset_id_all).order_by('-date_added')
            asset_group_all = list(asset_perm['asset_group'])

    if idc_name:
        asset_find = asset_find.filter(idc__name__contains=idc_name).order_by('-date_added')

    if group_name:
        asset_find = asset_find.filter(group__name__contains=group_name).order_by('-date_added')
        gp = get_object(AssetGroup, name=group_name)
        asset_group_all1 = AssetGroup1.objects.filter(group=gp)

    if group1_name:
        # asset_find = asset_find.filter(group1__name__contains=group1_name)
        asset_find = asset_find.filter(group1__name=group1_name).order_by('-date_added')

    if asset_type:
        asset_find = asset_find.filter(asset_type__contains=asset_type).order_by('-date_added')

    if status:
        asset_find = asset_find.filter(status__contains=status).order_by('-date_added')

    if keyword:
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
            Q(system_version__contains=keyword)).order_by('-date_added')

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

    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    if user_perm != 0:
        return my_render('jasset/asset_list.html', locals(), request)
    else:
        return my_render('jasset/asset_cu_list.html', locals(), request)


@require_role('user')
def asset_list_domain(request):
    """
    asset list domain view
    """
    q = request.GET
    header_title, path1, path2 = u'查看资产', u'资产管理', u'查看资产(域管理)'
    username = request.user.username
    user_perm = request.session['role_id']

    # -----------------------------------------------------
    module_name = q.get('module_name', '')
    path1 = q.get('path1', '')
    path2 = q.get('path2', '')
    path3 = q.get('path3', '')
    path4 = q.get('path4', '')
    path5 = q.get('path5', '')
    path6 = q.get('path6', '')
    path7 = q.get('path7', '')
    path8 = q.get('path8', '')

    path1_list = []
    path2_list = []
    path3_list = []
    path4_list = []
    path5_list = []
    path6_list = []
    path7_list = []
    path8_list = []
    module_name_list = []

    domain_list = Domains.objects.all()
    for d in domain_list:
        if d.module_name not in module_name_list:
            module_name_list.append(d.module_name)

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

    assets_list, p, assets, page_range, current_page, show_first, show_end = pages(asset_find, request)
    # if user_perm != 0:
    return my_render('jasset/asset_list_domain.html', locals(), request)
    # else:
    #     return my_render('jasset/asset_cu_list.html', locals(), request)








@require_role('admin')
def asset_edit_batch(request):
    af = AssetForm()
    name = request.user.username
    asset_group_all = AssetGroup.objects.all()

    if request.method == 'POST':
        q = request.POST
        env = q.get('env', '')
        idc_id = q.get('idc', '')
        port = q.get('port', '')
        use_default_auth = q.get('use_default_auth', '')
        username = q.get('username', '')
        password = q.get('password', '')
        group = q.getlist('group', [])
        cabinet = q.get('cabinet', '')
        comment = q.get('comment', '')
        asset_id_all = unicode(request.GET.get('asset_id_all', ''))
        asset_id_all = asset_id_all.split(',')
        for asset_id in asset_id_all:
            alert_list = []
            asset = get_object(Asset, id=asset_id)
            if asset:
                if env:
                    if asset.env != env:
                        asset.env = env
                        alert_list.append([u'运行环境', asset.env, env])
                if idc_id:
                    idc = get_object(IDC, id=idc_id)
                    name_old = asset.idc.name if asset.idc else u''
                    if idc and idc.name != name_old:
                        asset.idc = idc
                        alert_list.append([u'机房', name_old, idc.name])
                if port:
                    if unicode(asset.port) != port:
                        asset.port = port
                        alert_list.append([u'端口号', asset.port, port])

                if use_default_auth:
                    if use_default_auth == 'default':
                        asset.use_default_auth = 1
                        asset.username = ''
                        asset.password = ''
                        alert_list.append([u'使用默认管理账号', asset.use_default_auth, u'默认'])
                    elif use_default_auth == 'user_passwd':
                        asset.use_default_auth = 0
                        asset.username = username
                        asset.passwd = password  # added
                        password_encode = CRYPTOR.encrypt(password)
                        asset.password = password_encode
                        alert_list.append([u'使用默认管理账号', asset.use_default_auth, username])
                if group:
                    group_new, group_old, group_new_name, group_old_name = [], asset.group.all(), [], []
                    for group_id in group:
                        g = get_object(AssetGroup, id=group_id)
                        if g:
                            group_new.append(g)
                    if not set(group_new) < set(group_old):
                        group_instance = list(set(group_new) | set(group_old))
                        for g in group_instance:
                            group_new_name.append(g.name)
                        for g in group_old:
                            group_old_name.append(g.name)
                        asset.group = group_instance
                        alert_list.append([u'主机组', ','.join(group_old_name), ','.join(group_new_name)])
                if cabinet:
                    if asset.cabinet != cabinet:
                        asset.cabinet = cabinet
                        alert_list.append([u'机柜号', asset.cabinet, cabinet])
                if comment:
                    if asset.comment != comment:
                        asset.comment = comment
                        alert_list.append([u'备注', asset.comment, comment])
                asset.save()

            if alert_list:
                recode_name = unicode(name) + ' - ' + u'批量'
                AssetRecord.objects.create(asset=asset, username=recode_name, content=alert_list)
        return my_render('jasset/asset_update_status.html', locals(), request)

    return my_render('jasset/asset_edit_batch.html', locals(), request)


@require_role('admin')
def asset_detail(request):
    """
    Asset detail view
    """
    header_title, path1, path2 = u'主机详细信息', u'资产管理', u'主机详情'
    asset_id = request.GET.get('id', '')
    asset = get_object(Asset, id=asset_id)
    # print 'asset username = ', asset.username
    # print 'asset passwd = ', asset.passwd None

    perm_info = get_group_asset_perm(asset)
    log = Log.objects.filter(host=asset.hostname)
    if perm_info:
        user_perm = []
        for perm, value in perm_info.items():
            if perm == 'user':
                for user, role_dic in value.items():
                    user_perm.append([user, role_dic.get('role', '')])
            elif perm == 'user_group' or perm == 'rule':
                user_group_perm = value
    print perm_info

    asset_record = AssetRecord.objects.filter(asset=asset).order_by('-alert_time')

    return my_render('jasset/asset_detail.html', locals(), request)


@require_role('admin')
def asset_update(request):
    """
    Asset update host info via ansible view
    """
    asset_id = request.GET.get('id', '')
    asset = get_object(Asset, id=asset_id)
    name = request.user.username
    if not asset:
        return HttpResponseRedirect(reverse('asset_detail')+'?id=%s' % asset_id)
    else:
        asset_ansible_update([asset], name)
    return HttpResponseRedirect(reverse('asset_detail')+'?id=%s' % asset_id)


@require_role('admin')
def asset_update_batch(request):
    if request.method == 'POST':
        arg = request.GET.get('arg', '')
        name = unicode(request.user.username) + ' - ' + u'自动更新'
        if arg == 'all':
            asset_list = Asset.objects.all()
        else:
            asset_list = []
            asset_id_all = unicode(request.POST.get('asset_id_all', ''))
            asset_id_all = asset_id_all.split(',')
            for asset_id in asset_id_all:
                asset = get_object(Asset, id=asset_id)
                if asset:
                    asset_list.append(asset)
        asset_ansible_update(asset_list, name)
        return HttpResponse(u'批量更新成功!')
    return HttpResponse(u'批量更新成功!')


@require_role('admin')
def idc_add(request):
    """
    IDC add view
    """
    header_title, path1, path2 = u'添加IDC', u'资产管理', u'添加IDC'
    if request.method == 'POST':
        idc_form = IdcForm(request.POST)
        if idc_form.is_valid():
            idc_name = idc_form.cleaned_data['name']

            if IDC.objects.filter(name=idc_name):
                emg = u'添加失败, 此IDC %s 已存在!' % idc_name
                return my_render('jasset/idc_add.html', locals(), request)
            else:
                idc_form.save()
                smg = u'IDC: %s添加成功' % idc_name
            return HttpResponseRedirect(reverse('idc_list'))
    else:
        idc_form = IdcForm()
    return my_render('jasset/idc_add.html', locals(), request)


@require_role('admin')
def idc_list(request):
    """
    IDC list view
    """
    header_title, path1, path2 = u'查看IDC', u'资产管理', u'查看IDC'
    posts = IDC.objects.all()
    keyword = request.GET.get('keyword', '')
    if keyword:
        posts = IDC.objects.filter(Q(name__contains=keyword) | Q(comment__contains=keyword))
    else:
        posts = IDC.objects.exclude(name='ALL').order_by('id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(posts, request)
    return my_render('jasset/idc_list.html', locals(), request)


@require_role('admin')
def idc_edit(request):
    """
    IDC edit view
    """
    header_title, path1, path2 = u'编辑IDC', u'资产管理', u'编辑IDC'
    idc_id = request.GET.get('id', '')
    idc = get_object(IDC, id=idc_id)
    if request.method == 'POST':
        idc_form = IdcForm(request.POST, instance=idc)
        if idc_form.is_valid():
            idc_form.save()
            return HttpResponseRedirect(reverse('idc_list'))
    else:
        idc_form = IdcForm(instance=idc)
        return my_render('jasset/idc_edit.html', locals(), request)


@require_role('admin')
def idc_del(request):
    """
    IDC delete view
    """
    idc_ids = request.GET.get('id', '')
    idc_id_list = idc_ids.split(',')

    for idc_id in idc_id_list:
        IDC.objects.filter(id=idc_id).delete()

    return HttpResponseRedirect(reverse('idc_list'))


@require_role('admin')
def asset_upload(request):
    """
    Upload asset excel file view
    """
    if request.method == 'POST':
        excel_file = request.FILES.get('file_name', '')
        ret = excel_to_db(excel_file)
        if ret:
            smg = u'批量添加成功'
        else:
            emg = u'批量添加失败,请检查格式.'
    return my_render('jasset/asset_add_batch.html', locals(), request)
