#!/bin/bash
sudo mkdir /bin/bucket
mkdir ~/.rbenv/bin
cp cat /bin/bucket
cp cat ~/rbenv/bin
export PATH=/home/`whoami`/.rbenv/bin:$PATH
