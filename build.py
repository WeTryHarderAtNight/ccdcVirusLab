#!/bin/python3
import digitalocean
import time
import paramiko
from scp import SCPClient
import config
from os import system
from typing import Tuple

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

def initDroplet(tuple):
    idx = tuple[0]
    ip = tuple[1]

    def waitUntilCompletion(a: Tuple) -> None:
        print(a[1].readlines())
        print(a[2].readlines())


    k = paramiko.RSAKey.from_private_key_file("/home/david/.ssh/id_rsa")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=ip, username="root", pkey=k)
    scp = SCPClient(c.get_transport())
    waitUntilCompletion(c.exec_command("echo root:nuccdcpracticelab2017 | chpasswd"))

    # general setup
    c.exec_command("hostname %s" % str(idx))
    waitUntilCompletion(c.exec_command("echo %s > /virusNum" % str(idx)))
    waitUntilCompletion(c.exec_command("DEBIAN_FRONTEND=noninteractive apt-get update; DEBIAN_FRONTEND=noninteractive apt-get install -y debsums curl build-essential make python-pip cargo"))

    # Isaac's virus 1
    waitUntilCompletion(c.exec_command("pip install pyinstaller setproctitle requests"))

    time.sleep(5)

    # David's virus 2
    c.exec_command("mv /bin/ls /realLS")
    scp.put('david/', '/root/david/', recursive=True)
    waitUntilCompletion(c.exec_command('cd /root/david/; cargo build --all'))
    c.exec_command('cp /root/david/target/debug/virus /var/virus')
    c.exec_command('cp /root/david/target/debug/virus /virus')
    c.exec_command('cp /root/david/target/debug/virus /var/virus')
    c.exec_command("mv /usr/bin/debsums /realDebsums")
    c.exec_command('cp /root/david/target/debug/debsums /usr/bin/debsums')
    c.exec_command('cp /root/david/target/debug/ls /bin/ls')
    c.exec_command('cp /root/david/target/debug/ls /usr/bin/ls')
    c.exec_command('cp /root/david/target/debug/ls /sbin/ls')
    c.exec_command('cp /root/david/target/debug/ls /usr/sbin/ls')

    # Alex's virus 2
    scp.put("alex/GLaDOS/", "/root/glados/", recursive=True)
    waitUntilCompletion(c.exec_command("cd /root/glados/; make; make install"))
    # c.exec_command("rm -rf /root/glados") TODO

    # Isaac's virus 2
    scp.put('isaac/', '/root/isaac/', recursive=True)
    time.sleep(1)
    waitUntilCompletion(c.exec_command('cd /root/isaac; /root/isaac/build.sh'))
    waitUntilCompletion(c.exec_command('cp /root/isaac/not_ntpd /usr/bin/not_ntpd'))
    c.exec_command('nohup /usr/bin/not_ntpd %s &' % str(idx))
    # c.exec_command("rm -rf /root/isaac") TODO

    # Michael's virus 2
    scp.put('michael/', '/root/michael/', recursive=True)
    waitUntilCompletion(c.exec_command('cd /root/michael; chmod +x build.sh; ./build.sh'))
    c.exec_command('nohup cat /virusNum &')
    # c.exec_command("rm -rf /root/michael") TODO

    # Victor's virus 2
    scp.put('victor/', '/root/victor/', recursive=True)
    waitUntilCompletion(c.exec_command('cd /root/victor; chmod +x build.sh; ./build.sh'))
    c.exec_command('nohup /root/victor/\[systemdeamond\] &')
    # TODO

    print('Done with %s' % idx)

tuples = []
for idx, droplet in enumerate(droplets):
    print('Starting droplet...')
    droplet.load()
    print(droplet.ip_address)
    with open('servers.csv', 'a+') as f:
        f.write("%s,%s\n" % (idx, droplet.ip_address))
    tuples.append((idx, droplet.ip_address))

time.sleep(5)

print('Started!')

from multiprocessing import Pool

try:
    p = Pool(30)
    p.map(initDroplet, tuples)
finally:
    for idx, ip in tuples:
        k = paramiko.RSAKey.from_private_key_file("/home/david/.ssh/id_rsa")
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname=ip, username="root", pkey=k)
        c.exec_command("nohup ls / &")

time.sleep(20)
