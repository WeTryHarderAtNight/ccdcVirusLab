import os
import requests
import time
from sys import argv

def taunt():
    #os.system('wall "Taunt..."')
    pass

def update():
    requests.get('http://monitor.daviddworken.com:8080/api/submit?id=%s&virusName=0' % argv[1])

while True:
    taunt()
    update()
    time.sleep(5)