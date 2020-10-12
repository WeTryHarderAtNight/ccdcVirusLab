#!/usr/bin/python3

import requests
import sys

ip_address = sys.argv[1]

for identifier in range(0,30):
	for name in range(0,5):
		response = requests.get("http://{0}:8080/api/submit?id={1}&virusName={2}".format(ip_address,identifier,name))
		print("Machine:{0} - Virus:{1} - {2}".format(identifier,name,response))
