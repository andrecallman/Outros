# coding: utf8
from encodings.utf_8 import encode
import psutil
import json
import re

output = {'data':[]}

def get_disks(ignore=None):
    partitions = []
    for partition in psutil.disk_partitions():
        partitions.append('{};{};{}'.format(partition.device,partition.fstype,partition.mountpoint))

    if ignore:
        regex = re.compile(ignore)
        partitions = [i for i in partitions if not regex.search(i)]
        
    
    for partition in partitions:
        device,fs,mountpoint = partition.split(';')
        part = {
            'device': re.sub(r':\\', r'', device),
            'fs'    : fs,
            'mountpoint': re.sub(r'\\', r'', mountpoint)
        }
        output['data'].append(part)

    return output



def get_interfaces():
    interfaces = psutil.net_if_addrs()
    
    for interface in interfaces:
        interf = {}
        interf['name'] = interface.encode().decode()
        interf['speed'] = psutil.net_if_stats()[interface].speed
        output['data'].append(interf)
    return output

def get_services(ignore=None):
    windows_native_services = ["AxInstSV","SensrSvc","AeLookupSvc","AppHostSvc","AppIDSvc","Appinfo","ALG","AppMgmt"
        ,"aspnet_state","BITS","BFE","BDESVC","wbengine","bthserv","PeerDistSvc","CertPropSvc"
        ,"NfsClnt","KeyIso","EventSystem","COMSysApp","Browser","VaultSvc","CryptSvc","DcomLaunch"
        ,"UxSms","Dhcp","DPS","WdiServiceHost","WdiSystemHost","defragsvc","TrkWks","MSDTC"
        ,"Dnscache","EFS","EapHost","Fax","fdPHost","FDResPub","gpsvc","hkmsvc","HomeGroupListener"
        ,"HomeGroupProvider","hidserv","IISADMIN","IKEEXT","CISVC","UI0Detect","SharedAccess"
        ,"iphlpsvc","PolicyAgent","KtmRm","lltdsvc","LPDSVC","Mcx2Svc","MSMQ","MSMQTriggers"
        ,"clr_optimization_v2.0.50727","ftpsvc","MSiSCSI","swprv","MMCSS","NetMsmqActivator"
        ,"NetPipeActivator","NetTcpActivator","NetTcpPortSharing","Netlogon","napagent","Netman"
        ,"netprofm","NlaSvc","nsi","CscService","WPCSvc","PNRPsvc","p2psvc","p2pimsvc","pla"
        ,"PlugPlay","IPBusEnum","PNRPAutoReg","WPDBusEnum","Power","Spooler","wercplsupport"
        ,"PcaSvc","ProtectedStorage","QWAVE","RasAuto","RasMan","SessionEnv","TermService"
        ,"UmRdpService","RpcSs","RpcLocator","RemoteRegistry","iprip","RemoteAccess","RpcEptMapper"
        ,"SeaPort","seclogon","SstpSvc","SamSs","wscsvc","LanmanServer","ShellHWDetection","simptcp"
        ,"SCardSvr","SCPolicySvc","SNMP","SNMPTRAP","sppsvc","sppuinotify","SSDPSRV","StorSvc"
        ,"SysMain","SENS","TabletInputService","Schedule","lmhosts","TapiSrv","TlntSvr","Themes"
        ,"THREADORDER","TBS","upnphost","ProfSvc","vds","VSS","WMSVC","WebClient","AudioSrv"
        ,"AudioEndpointBuilder","SDRSVC","WbioSrvc","idsvc","WcsPlugInService","wcncsvc"
        ,"WinDefend","wudfsvc","WerSvc","Wecsvc","EventLog","MpsSvc","FontCache","StiSvc","msiserver"
        ,"fsssvc","Winmgmt","ehRecvr","ehSched","WMPNetworkSvc","TrustedInstaller","FontCache3.0.0.0"
        ,"WAS","WinRM","WSearch","W32Time","wuauserv","WinHttpAutoProxySvc","dot3svc","Wlansvc","wmiApSrv"
        ,"LanmanWorkstation","W3SVC","WwanSvc"
        ]
    services = psutil.win_service_iter()
    svcs = []
    for service in services:
        svc = psutil.win_service_get(service.name())
        if not svc.name() in windows_native_services and svc.status() == 'running':
            svcs.append('{};{};{}'.format(svc.name(),svc.display_name(),svc.status()))

    if ignore:
        regex = re.compile(ignore)
        svcs = [i for i in svcs if not regex.search(i)]
        
    for service in svcs:
        #print(service)
        name,descr,status = service.split(';')
        svc = {
            'name': name,
            'description' : descr.encode().decode(),
            'status': status
        }
        output['data'].append(svc)

    return output








print(json.dumps(get_disks(ignore='C'),indent=4))
#print(get_disks())
#output = get_interfaces()
#output = get_cpu()
# print(json.dumps(output,indent=4,ensure_ascii=False))
#print(json.dumps(get_services(ignore='WpnUserService_af591|UserDataSvc_af591'),indent=4,ensure_ascii=False))

# print(get_disks(ignore='D'))
# print(get_disks(ignore='C'))
