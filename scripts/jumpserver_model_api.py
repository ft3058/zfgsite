# coding:utf8
"""

"""

import os, sys
from twisted.internet.defer import DeferredList
from twisted.internet.task import react
from pysnmp.hlapi.twisted import *

proj_path = "/data/www/yxyw/jump"
try:
    from local_vars import *
except: pass
print 'proj_path:', proj_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jumpserver.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# from juser.models import User
from jasset.models import IpInfo, Asset

def get_all_assets():
    from jasset.models import Asset
    assets = Asset.objects.all()
    # assets = Asset.objects.filter(ip='218.75.155.46')
    return assets

def get_all_assets_ip():
    from jasset.models import Asset
    assets = Asset.objects.all()
    # assets = Asset.objects.filter(ip='218.75.155.46')
    return [t.ip for t in assets]


if __name__ == '__main__':
    ip_list = get_all_assets_ip()
    print ip_list


