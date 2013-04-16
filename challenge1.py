#!/usr/bin/env python

"""Challenge 1: Write a script that builds three 512 MB Cloud Servers that following a similar naming convention. 
(ie., web1, web2, web3) and returns the IP and login credentials for each server. Use any image you want. Worth 1 point"""

import pyrax
import os
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers
servername = "web"
image = '03318d19-b6e6-4092-9b5c-4758ee0ada60'
i_d = 2
pas = []
servers = []

print "Welcome to challenge 1 creating 3 servers and displaying logins for them \n"

for i in xrange(0,3):
    name = servername + str(i)
    server = cs.servers.create(name, image, i_d)
    servers.append(server)
    pas.append(server.adminPass)

print "Servers are spun up. It might take some time for networks to be setup and server to be ACTIVE. Please be patient \n"
   
for i in xrange(0,3):
    while not servers[i].networks:
        print "Waiting for networks to be setup"
        servers[i] = cs.servers.get(servers[i].id)
        time.sleep(15) 

print "\nGreat. Networks are setup. Here are the logins \n"

for i in xrange(0,3):
    print "#######################"
    print "Here are logins for server %s" % (servers[i].name)
    print "ID:", servers[i].id
    print "Status:", servers[i].status
    print "Admin password:", pas[0]
    print servers[i].networks
    print "#######################"
