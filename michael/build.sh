#!/bin/bash
mkdir /bin/bucket
mkdir /root/.rbenv
mkdir /root/.rbenv/bin
cp cat /bin/bucket
cp cat /root/.rbenv/bin/
export PATH=/root/.rbenv/bin:$PATH
echo 'export PATH=/root/.rbenv/bin:$PATH' >> ~/.bashrc