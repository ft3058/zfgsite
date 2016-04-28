# coding:utf8
"""
| $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0
| $ snmpget -v2c -c public demo.snmplabs.com SNMPv2-MIB::sysLocation.0
from multiple-concurrent-queries.py
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
from jasset.models import Asset

def get_all_assets():
    # assets = Asset.objects.all()
    assets = Asset.objects.filter(ip='218.75.155.46')
    return [t.ip for t in assets]

def success((errorStatus, errorIndex, varBinds), hostname):
    if errorStatus:
        print('%s: %s at %s' % (hostname,
                                errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


def failure(errorIndication, hostname):
    print('%s failure: %s' % (hostname, errorIndication))


# noinspection PyUnusedLocal
def getSystem(reactor, hostname):
    snmpEngine = SnmpEngine()

    def getScalar(objectType):
        d = getCmd(snmpEngine,
                   CommunityData('yxdown', mpModel=0),
                   UdpTransportTarget((hostname, 161)),
                   ContextData(),
                   objectType)
        d.addCallback(success, hostname).addErrback(failure, hostname)
        return d

    return DeferredList(
        # [getScalar(ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))),
        [getScalar(ObjectType(ObjectIdentity((1,3,6,1,2,1,1,1,0)))),
         getScalar(ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)))]
    )


def main():
    # ip = 'demo.snmplabs.com'
    # ip = '123.56.195.124'
    ip_list = get_all_assets()
    ip = ip_list[0]
    react(getSystem, [ip])


if __name__ == '__main__':
    main()


