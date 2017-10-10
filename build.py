#!/bin/python3
import digitalocean
import time
import paramiko
from scp import SCPClient
import config
from os import system

system("cd david; cargo build --release --all; cd ..")

count = 30

manager = digitalocean.Manager(token=config.token)
keys = manager.get_all_sshkeys()

with open('servers.csv', 'w') as f:
    f.write('Machine #, IP Address\n')

droplets = []
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
    with open('servers.csv', 'a+') as f:
        f.write("%s,%s\n" % (idx, droplet.ip_address))

    k = paramiko.RSAKey.from_private_key_file("/home/david/.ssh/id_rsa")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=droplet.ip_address, username="root", pkey=k)
    i, o, e = c.exec_command("echo root:nuccdcpracticelab2017 | chpasswd")

    # David's virus 1
    c.exec_command("apt-get -y install debsums")

time.sleep(5)

for idx, droplet in enumerate(droplets):
    droplet.load()
    k = paramiko.RSAKey.from_private_key_file("/home/david/.ssh/id_rsa")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=droplet.ip_address, username="root", pkey=k)
    # David's virus 2
    c.exec_command("mv /bin/ls /realLS")
    scp = SCPClient(c.get_transport())
    scp.put('david/target/release/virus', '/var/virus')
    scp.put('david/target/release/virus', '/virus')
    scp.put('david/target/release/virus', '/var/virus')
    c.exec_command("mv /usr/bin/debsums /realDebsums")
    scp.put('david/target/release/debsums', '/usr/bin/debsums')
    scp.put('david/target/release/ls', '/bin/ls')
    scp.put('david/target/release/ls', '/usr/bin/ls')
    scp.put('david/target/release/ls', '/sbin/ls')
    scp.put('david/target/release/ls', '/usr/sbin/ls')
    c.exec_command("echo %s > /virusNum" % str(idx))
    c.exec_command("nohup /virus &")


time.sleep(20)
