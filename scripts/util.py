# coding:utf8
"""

"""

def parse_tcp_conn_count(res, ip, dic):
    hostname = ip
    errorIndication, errorStatus, errorIndex, varBinds = res
    print '+++', errorIndication, errorStatus, errorIndex, varBinds
    if errorStatus:
        print('%s: %s at %s' % (hostname,
                                errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        '''
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
            '''
        # SNMPv2-SMI::mib-2.6.9.0 = 1415
        # SNMPv2-SMI::mib-2.6.9.0 = 1400
        s = varBinds[0].prettyPrint()
        print 's = ', s
        return int(s.split('=')[-1].strip())


def success(res, ip, dic):
    if dic['name'] == 'tcp_conn_count':
        return parse_tcp_conn_count(res, ip, dic)



def failure(errorIndication, hostname):
    print('%s failure: %s' % (hostname, errorIndication))


