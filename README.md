# CCDC Virus Lab

build.py contains the code for building the digitalocean droplets. 

down.py destroys all of the created digitalocean droplets. 

index.html and server.py are the monitoring webserver (server.py also relies on redis)

virus.py is an example virus

All the directories contain each individual's virus. 


## Lab

For this lab, the team wrote various pieces of malware and ran them on virtual servers. Participants were tasked with removing the malware. All **viruses** call out to the monitoring interface (currently hardcoded), allowing participants to track their progress.
