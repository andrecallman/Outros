from paramiko import SSHClient
import paramiko


ssh = SSHClient()

ssh.connect(hostname='172.17.1.56',username='teletex',password='t3letX2010!')

print(ssh)
