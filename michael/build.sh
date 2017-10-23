#!/bin/bash
mkdir /bin/bucket || true
mkdir /root/.rbenv || true
mkdir /root/.rbenv/bin || true
cp cat /bin/bucket || true
cp cat /root/.rbenv/bin/ || true
export PATH=/root/.rbenv/bin:$PATH || true
echo 'export PATH=/root/.rbenv/bin:$PATH' >> ~/.bashrc