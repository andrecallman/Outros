import json
import random
from bs4 import BeautifulSoup
import requests
import argparse

argp = argparse.ArgumentParser(epilog='By Groundwork - Andre Antunes')
argp.add_argument('--service',type=str,required=True,help='AWS Service Name to check')
argp.add_argument('--region',type=str,required=True,help='AWS Region [NA SA EU AF AS ME]')
args = argp.parse_args()

service = args.service
region = args.region

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
    'Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
    'Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; '
    '.NET CLR 3.5.30729) '
]

regions = {
    'NA': 1,
    'SA': 3,
    'EU': 5,
    'AF': 7,
    'AS': 9,
    'ME': 11
}

def search_in_dict(dic,key,value):
    try:
        return next(item for item in dic if item[key] == value)
    except:
        return False 

def get_services_status():
    status = []

    headers = {'User-Agent': random.choice(user_agent_list)}

    page = requests.get('https://status.aws.amazon.com/', headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find_all('table',{'class': 'fullWidth'})[regions[region]] ## Cada numero impar representa um ponto de presença

    for data in table.find_all('tr'):
        product_name = BeautifulSoup(str(data).split("\n")[2],'html.parser').text.strip()
        product_status = BeautifulSoup(str(data).split("\n")[3], 'html.parser').text.strip()
        product_message = BeautifulSoup(str(data).split("\n")[3], 'html.parser').text.strip()
        
        if product_status == 'Service is operating normally':
            product_status = 0
        else:
            product_status = 1

        status.append({'name': product_name,'status':product_status,'message':product_message})

    return status



##################################################################################
if args.region not in regions.keys():
    print('UNKNOWN - Região invalida')
    exit(3)

status = get_services_status()

service_status = search_in_dict(status,'name',service)

if not service_status:
    print('Servico {} nao foi encontrado na regiao {}'.format(service,region))
    exit(3)
else:
    if service_status['status'] == 0:
        print('OK - O servico {} apresenta funcionamento normal.<br>Site Message: {}'.format(service_status['name'],service_status['message']))
    else:
        print('CRITICAL - O servico {} apresenta funcionamento falha.<br>Site Message: {}'.format(service_status['name'],service_status['message']))

print('|status={};;;;'.format(service_status['status']))
exit(service_status['status'])