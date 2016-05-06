# coding: utf-8

from __future__ import division

from jumpserver.api import *
from jumpserver.models import Setting


@require_role('admin')
def auth_setting(request):
    header_title, path1 = '项目设置', '设置'
    setting_default = get_object(Setting, name='default')

    if request.method == "POST":
        setting_raw = request.POST.get('setting', '')
        if setting_raw == 'default':
            username = request.POST.get('username', '')
            port = request.POST.get('port', '')
            password = request.POST.get('password', '')
            private_key = request.POST.get('key', '')

            if '' in [username, port]:
                return HttpResponse('所填内容不能为空, 且密码和私钥填一个')
            else:
                private_key_dir = os.path.join(BASE_DIR, 'keys', 'default')
                private_key_path = os.path.join(private_key_dir, 'admin_user.pem')
                mkdir(private_key_dir)

                if private_key:
                    with open(private_key_path, 'w') as f:
                            f.write(private_key)
                    os.chmod(private_key_path, 0600)

                if setting_default:
                    if password:
                        password_encode = CRYPTOR.encrypt(password)
                    else:
                        password_encode = password
                    Setting.objects.filter(name='default').update(field1=username, field2=port,
                                                                  field3=password_encode,
                                                                  field4=private_key_path)

                else:
                    password_encode = CRYPTOR.encrypt(password)
                    setting_r = Setting(name='default', field1=username, field2=port,
                                        field3=password_encode,
                                        field4=private_key_path).save()

            msg = "设置成功"
    return my_render('jset/auth_setting.html', locals(), request)


@require_role('admin')
def tmpl_setting(request):
    pass