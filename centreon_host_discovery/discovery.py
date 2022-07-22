import re
import socket
from icmplib import ping 

ipranges = '192.168.50.60-61,192.168.50.4-4,192.168.50.90-100'
ip_list = []
hosts_alive = []
hosts_info = {}
protocols_ports = {
    'ssh':  ['22/tcp','1022/tcp','2200/tcp','22000/tcp','2222/tcp'],
    'rdp':  ['3389/tcp'],
    'snmp': ['161/udp']
}


def convert_iprange_to_list(iprange):
    index = 0
    for iprange in ipranges.split(','):
        if not re.match("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)-(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",iprange):
            print('IP {} (position #{}) is not valid IP range. Use \"192.168.1.1-254\" format instead.'.format(iprange,index + 1))
            exit()
        prefix = '.'.join(iprange.split('-')[0].split('.')[:3])
        start = int(iprange.split('-')[0].split('.')[3])
        end = int(iprange.split('-')[1])

        for ip in range(start,end + 1):
            ip_list.append('{}.{}'.format(prefix,ip))

        index+=1

    return ip_list

def test_port(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOCK_DGRAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip,port))
    if result == 0:
        return True
    return False



for ip in  convert_iprange_to_list(ipranges):
    print('Testing ping on {}'.format(ip))
    result = ping(ip, count=1,interval=0.2,timeout=0.3)
    if result.is_alive:
        hosts_alive.append(result)




for host in hosts_alive:
    ip = host.address
    hosts_info[ip] = []
    for protocol in protocols_ports.keys():
        for port in protocols_ports[protocol]:
            result = test_port(ip,int(port.split('/')[0]))
            print('{}: port[{}] = {}'.format(ip,port,result))
            # if result:
                  #hosts_info[ip].append({'protocol':protocol,'port':port})
            hosts_info[ip].append({'protocol':protocol,'port':port,'status':result})



print(hosts_info)