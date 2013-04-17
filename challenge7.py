#!/usr/bin/python
"""
Challenge 7: Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer. Worth 3 Points
"""
import pyrax
import os
import time 

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
clb = pyrax.cloud_loadbalancers

cs = pyrax.cloudservers
servername = "web"
image = '03318d19-b6e6-4092-9b5c-4758ee0ada60'
i_d = 2
pas = []
servers = []

print "Welcome to challenge 7 creating 2 servers and adding it to a load balancer \n"

for i in xrange(0,2):
    name = servername + str(i)
    server = cs.servers.create(name, image, i_d)
    servers.append(server)
    pas.append(server.adminPass)

print "Servers are spun up. It might take some time for networks to be setup and server to be ACTIVE. Please be patient \n"
   
for i in xrange(0,2):
    while not servers[i].networks:
        print "Waiting for networks to be setup"
        servers[i] = cs.servers.get(servers[i].id)
        time.sleep(15) 

print "\nGreat. Networks are setup. Here are the logins \n"

for i in xrange(0,2):
    print "#######################"
    print "Here are logins for server %s" % (servers[i].name)
    print "ID:", servers[i].id
    print "Status:", servers[i].status
    print "Admin password:", pas[i]
    print servers[i].networks
    print "#######################"
    print

print "Lets add the two servers to a load balancer now: "    
node1 = clb.Node(address=servers[0].networks['private'][0], port=80, condition="ENABLED")
node2 = clb.Node(address=servers[1].networks['private'][0], port=80, condition="ENABLED")

vip = clb.VirtualIP(type="PUBLIC")

lb = clb.create("example_lb", port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])

print "\nLoad balancer created. Here are the details:"
print "Load Balancer ID:",lb.id
print "Load balancer name:",lb.name
print "Load Balancer status:",lb.status
print "Nodes:",lb.nodes
print "Virtual IPs:", lb.virtual_ips
print "Algorithm:", lb.algorithm
print "Protocol:", lb.protocol
print 