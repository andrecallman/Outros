import requests


url = 'http://192.168.50.91:8080/api/v1/dags/example_bash_operator/tasks'
url = 'http://airflow.integration.cloud.bionexo.com.br/api/experimental/dags/plannexo_integration_company_104/dag_runs'
username = 'admin'
password = 'a123456@'

username='andre.antunes@bionexo.com'
password = 'cwbjj214m*'

headers = {
    'Content-Type': 'application/json',
}

# response = requests.get(url=url, headers=headers,auth=(username,password)).json()
response = requests.get(url=url, headers=headers,auth=(username,password))

print(response.text)
# for task in response['tasks']:
#     print(task['task_id'])