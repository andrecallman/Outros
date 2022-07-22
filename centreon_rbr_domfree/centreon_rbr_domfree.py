
# coding: utf-8
import sys
import requests
from lxml import html
import json


domain='andreantunes.com.br'
#url=rbr_url+domain
url='https://api.dev.name.com/v4/domains:search'
user='aaaaaaaaaaaaa'
passwd='*************'
data={
    'keyword':domain
}

page=json.loads(requests.post(url,auth=(user,passwd),data=json.dumps(data)).text)

print('Resultados para {}:'.format(domain))
print('----------------------------------------------')



for result in page['results']:
    if 'purchasable' in result and result['purchasable'] :
        msg='disponivel'
        print('O dominio {} está {}'.format(result['domainName'],msg))
    else:
        msg='indisponivel'
        print('O dominio {} está {}'.format(result['domainName'],msg))
