import digitalocean
import time
import paramiko
from scp import SCPClient
import config

count = 25

manager = digitalocean.Manager(token=config.token)
keys = manager.get_all_sshkeys()

droplets = []
try:
    for i in range(count):
        print(i)
        droplet = digitalocean.Droplet(token=config.token,
                                       name='ccdc',
                                       region='nyc1',
                                       image='ubuntu-16-04-x64',
                                       size_slug='512mb',
                                       ssh_keys=keys,
                                       backups=False)
        droplet.create()
        droplets.append(droplet)

    time.sleep(60)

    for idx, droplet in enumerate(droplets):
        print('Starting droplet...')
        droplet.load()
        print(droplet.ip_address)

        k = paramiko.RSAKey.from_private_key_file("/home/david/.ssh/id_rsa")
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname=droplet.ip_address, username="root", pkey=k)
        i, o, e = c.exec_command("echo root:nuccdcpracticelab2017 | chpasswd")

        scp = SCPClient(c.get_transport())
        scp.put('virus.py', '/virus.py')

        i, o, e = c.exec_command("nohup python3 /virus.py %s &" % idx)
        print('Done with droplet')

    time.sleep(20)
    for droplet in droplets:
        droplet.destroy()
finally:
    for droplet in droplets:
        try:
            droplet.destroy()
        except:
            pass