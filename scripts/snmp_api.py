# coding:utf8
"""

"""
from pysnmp.entity.rfc3413.oneliner import cmdgen, ntforg
from pysnmp.proto.api import v2c


def get_server_info(addr, community_index, community_name, oid, port=161):
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
        cmdgen.CommunityData(community_index, community_name, 0),
        cmdgen.UdpTransportTarget((addr, port)), oid)
    print errorIndication
    print errorStatus
    print type(varBinds[0]), varBinds
    for i in varBinds:
        print '---', i
    # [ObjectType(ObjectIdentity(ObjectName('1.3.6.1.2.1.1.1.0')), DisplayString('Linux iZ25kr8h103Z 3.13.0-65-generic #106-Ubuntu SMP Fri Oct 2 22:08:27 UTC 2015 x86_64', subtypeSpec=ConstraintsIntersection(ConstraintsIntersection(ConstraintsIntersection(ConstraintsIntersection(), ValueSizeConstraint(0, 65535)), ValueSizeConstraint(0, 255)), ValueSizeConstraint(0, 255))))]


def get_cmd_val(addr, community_index, community_name, oid, port=161):
    """
    # '1.3.6.1.4.1.11.2.3.1.1.13'
    # '.1.3.6.1.4.1.2021.10.1.3.1'
    '1.3.6.1.2.1.1.1.0'
    """
    try:
        res = cmdgen.CommandGenerator().getCmd(
            cmdgen.CommunityData(community_index, community_name, 1),
            cmdgen.UdpTransportTarget((addr, port)), oid)
        return res
    except Exception, e:
        print u'get cmd error: %s' % str(e)
        return (str(e), )

def get_next_cmd_val(addr, community_index, community_name, oid, port=161):
    """
    # '1.3.6.1.4.1.11.2.3.1.1.13'
    # '.1.3.6.1.4.1.2021.10.1.3.1'
    '1.3.6.1.2.1.1.1.0'
    """
    try:
        res = cmdgen.CommandGenerator().nextCmd(
            cmdgen.CommunityData(community_index, community_name, 1),
            cmdgen.UdpTransportTarget((addr, port)), oid)
        return res
    except Exception, e:
        print u'get cmd error: %s' % str(e)
        return (str(e), )


def test_oids():
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().bulkCmd(
        # cmdgen.UsmUserData('my-user', 'my-authkey', 'my-privkey'),
        cmdgen.CommunityData('my-agent', S['name'], 0),
        cmdgen.UdpTransportTarget((S['ip'], 161)),
    0, 25, # nonRepeaters, maxRepetitions
    # (1,3,6,1,2,1,1)
        (1,3,6,1,2,1,1,1,0)
    # '.1.3.6.1.4.1.3495.1.3.1.7'
    )
    print errorIndication
    print errorStatus

    for varBindTableRow in varBinds:
        print varBindTableRow

    # [(ObjectName('1.3.6.1.2.1.1.1.0'), OctetString("'Linux my.domain.com 2.6.21 #2 Mon Mar 19 17:07:18 MSD 2006 i686'"))]
    # [(ObjectName('1.3.6.1.2.1.1.2.0'), ObjectIdentifier('1.3.6.1.4.1.8072.3.2.10'))]
    # [ skipped ]
    # [(ObjectName('1.3.6.1.2.1.1.9.1.4.9'), TimeTicks('17'))]


def get_cmd_info(oid):
    '''
    oid is str or tuple
    '''

    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('my-agent', S['name'], 0),
    cmdgen.UdpTransportTarget((S['ip'], 161)), oid)
    print '1 = ', errorIndication
    # None
    print '2 = ', errorStatus
    # 0
    print '3 = ', varBinds
    # [(ObjectName('1.3.6.1.2.1.1.1.0'), OctetString("'Linux my.domain.com 2.6.21 #2 Mon Mar 19 17:07:18 MSD 2006 i686'"))]


def trap_test():
    """
    danger
    """
    errorIndication, errorStatus, errorIndex, varBinds = ntforg.NotificationOriginator().sendNotification(
    cmdgen.UsmUserData('my-user', 'my-authkey', 'my-privkey'),
    cmdgen.UdpTransportTarget(('localhost', 162)),
    'trap',
    (('SNMPv2-MIB', 'coldStart'),),
    ((1,3,6,1,2,1,1,3,0), v2c.TimeTicks(44100))
    )
    print errorIndication
    print errorStatus
    
    
def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
    print 'sendRequestHandle =', sendRequestHandle
    print 'errorIndication =', errorIndication
    print 'errorStatus =', errorStatus
    print 'varBinds =', varBinds
    print 'cbCtx =', cbCtx
    print 'end....'


def test_asyn_cmd():
    asynCommandGenerator = cmdgen.AsynCommandGenerator()
    # This is a non-blocking call
    sendRequestHandle = asynCommandGenerator.asyncGetCmd(
        cmdgen.CommunityData('my-agent', S['name'], 0),
        # cmdgen.UsmUserData('my-user', 'my-authkey', 'my-privkey'),
        cmdgen.UdpTransportTarget((S['ip'], 161)), ((1,3,6,1,2,1,1,1,0),), (cbFun, None))
    print sendRequestHandle
    asynCommandGenerator.snmpEngine.transportDispatcher.runDispatcher()
    sendRequestHandle = 1
    errorIndication = None
    errorStatus = 0
    # varBinds = [(ObjectName('1.3.6.1.2.1.1.1.0'), OctetString("'Linux my.domain.com 2.6.21 #2 Mon Mar 19 17:07:18 MSD 2006 i686'"))]
    cbCtx = None
    print u'complete...'
   

if __name__ == '__main__':
    from const import S, OIDS
    # get_server_info()
    # test()
    # test_oids()
    oid = '1.3.6.1.2.1.1.1.0'
    oid = (1,3,6,1,2,1,1,1,0)
    # get_cmd_info(oid)

    addr = S['ip']
    community_name = S['name']
    community_index = 'my-agent'

    oid = OIDS['tcp_conn_count']
    # oid = OIDS['hrStorageIndex']

    get_server_info(addr, community_index, community_name, oid)
    errorIndication, errorStatus, errorIndex, varBinds = get_cmd_val(addr, community_index, community_name, oid)
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
    pass


