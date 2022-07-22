# coding: utf-8
import sys
import json
import re
import random
import argparse
from bs4 import BeautifulSoup
import requests

ap = argparse.ArgumentParser(description='Coleta de dados do site www.downdetector.com.br',
                             epilog='by Andre Antunes (andreluisantunes@gmail.com)')
ap.add_argument('-s', '--site', required=True, help='Site a ser verificado')
args = ap.parse_args()
empresa = args.site

# Lista de agentes de conexão ao site. Para evitar bloqueios é utilizado agente randomico
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

# Preparação da conexao com o site do downdetector
headers = {'User-Agent': random.choice(user_agent_list)}
page = requests.post('https://downdetector.com.br/fora-do-ar/{0}/'.format(empresa), headers=headers)

if page.status_code == 404:
    print('Empresa nao encontrada')
    exit(3)
page = page.text

# Leituda de informaçoes da pagina 
soup = BeautifulSoup(page, 'html.parser')
titulo = str(soup('title')[0]).split('não')[0].replace('<title>', '')
script = soup.findAll('script')[17]

# Leituda da informacao principal que indica problema ou disponibilidade do site
arr_status = str(soup.findAll('div', {'class': 'entry-title'})[0]).splitlines()
patern1 = r'.*Relatórios de usuários indicam potenciais problemas.*'
patern2 = r'.*Relatórios de usuários indicam problemas.*'

if bool(re.match(patern1, ''.join(arr_status))):
    status = 'WARNING'
    exit_code = 1
elif bool(re.match(patern2, ''.join(arr_status))):
    status = 'CRITICAL'
    exit_code = 2
else:
    status = 'OK'
    exit_code = 0

# Tratamento dos dados coletados do javascript da pagina
dados = []
valores = []

for line in str(script).split('\n'):
    regex = r".*{ x:.*"

    if bool(re.match(regex, line)):
        dados.append(line)

for dado in dados:
    dado = dado.strip()[:-1]
    dado = dado.replace('\'', '"')
    dado = dado.replace('x', '"x"')
    dado = dado.replace('y', '"y"')

    dado = json.loads(dado)

    valores.append(dado)

# Definicao dos resultados coletados na pagina
reclamacoes = valores[95]['y']
baseline = valores[191]['y']

# Exibicao dos dados ao usuario
print('Empresa: {1} <br>Baseline: {2} <br>Reclamacoes: {3} | baseline={2}, reclamacoes={3}'.format(status, titulo,
                                                                                                   baseline,
                                                                                                   reclamacoes))

# Codigo de saida do Centreon/Nagios
exit(exit_code)
requests.post()
