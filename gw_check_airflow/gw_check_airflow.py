import requests


url = 'http://192.168.50.91:8080/api/v1/dags/example_bash_operator/tasks'
username = 'admin'
password = 'a123456@'

username='andre.antunes@bionexo.com'
password = '*******'

headers = {
    'Content-Type': 'application/json',
}

# response = requests.get(url=url, headers=headers,auth=(username,password)).json()
response = requests.get(url=url, headers=headers,auth=(username,password))

print(response.text)
# for task in response['tasks']:
#     print(task['task_id'])
