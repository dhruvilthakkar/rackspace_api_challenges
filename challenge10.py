#!/usr/bin/python
"""
Challenge 10: Write an application that will:
- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
- Create a load balancer
- Add the 2 new servers to the LB
- Set up LB monitor and custom error page. 
- Create a DNS record based on a FQDN for the LB VIP. 
- Write the error page html to a file in cloud files for backup.
Whew! That one is worth 8 points!
"""

import pyrax
import os
import argparse, time
import pyrax.exceptions as exc
import pyrax.utils as utils


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns
cf = pyrax.cloudfiles


parser = argparse.ArgumentParser(description='Please run this script as python challenge10.py -s ssh_public_key_path -i image_id -d domain')    
parser.add_argument('-i', '--image', default='03318d19-b6e6-4092-9b5c-4758ee0ada60')
parser.add_argument('-f', '--flavor', type=int, default=2, help="Flavor ID to build server with", choices=range(2,9))
parser.add_argument('-s', '--ssh', help='File path of public ssh key', required=True)
parser.add_argument('-d', '--domain', help='Enter domain for which you want to create reqord', required=True)

args = parser.parse_args()

if os.path.isfile(args.ssh) == False:
    print "SSH key file does not exist"
    exit(1)
else:    
    print "File %s exists" %args.ssh

with open(args.ssh,'r') as f:
    read_data = f.read()    
    
files = {"/root/.ssh/authorized_keys": read_data}    
    
pas = []
print args
i = 0
servers=[]

for i in xrange(0,2):
    name = 'web'+ str(i)
    server = cs.servers.create(name, args.image, args.flavor, files=files)
    pas.append(server.adminPass)
    servers.append(server)

print "Servers are spun up. It might take some time for networks to be set up for servers"

for i in xrange(0,2):
    while not servers[i].networks:
        print "Waiting for networks to set up:"
        time.sleep(15)
        servers[i] = cs.servers.get(servers[i].id)
    
public = []
private = []
node = []
for i in xrange(0,2):
    public.append(servers[i].networks["public"][0])
    private.append(servers[i].networks["private"][0])
print public
print private    

print "\nServers are created. Now creating loadbalancer:\n"
node1 = clb.Node(address=private[0], port=80, condition="ENABLED")
node2 = clb.Node(address=private[1], port=80, condition="ENABLED")

vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create("web_lb", port=80, protocol="HTTP", nodes=[node1, node2], virtual_ips=[vip])

print "\nLoad balancer created. Here are the details:"
print "Load Balancer ID:",lb.id
print "Load balancer name:",lb.name
print "Load Balancer status:",lb.status
print "Nodes:",lb.nodes
print "Virtual IPs:", lb.virtual_ips
print "Algorithm:", lb.algorithm
print "Protocol:", lb.protocol
print 
while lb.status != 'ACTIVE':
    lb = clb.get(lb.id)
    time.sleep(10)
    print "Waiting for load balancer to go active"
lb.add_health_monitor(type='CONNECT', delay = 10, timeout=10, attemptsBeforeDeactivation=3)
print "Here is load balancer's health monitor"
print lb.get_health_monitor()
print
html = "<html><body>Sorry, we are performing maintenance. Please try after some time</body></html>"
ip = lb.virtual_ips[0].address
print "Load balancers Public IP is: ",ip

try:
        dom = dns.create(name=args.domain, emailAddress="abc@example.edu",
                ttl=900, comment="sample domain")
except exc.DomainCreationFailed as e:
        print "Domain creation failed:", e
print "Domain created:", args.domain
print "Adding records:"

a_rec = {"type": "A",
        "name": args.domain,
        "data": ip,
        "ttl": 6000}
recs = dom.add_records([a_rec])
print "\nRecords added. Here are the details:\n"
print recs

print "\nCreating container in cloud files and storing backup file in it"
cont = cf.create_container("web_backup")
print "\n Container created with name web_backup"
with utils.SelfDeletingTempfile() as tmpname:
    with open(tmpname, "w") as tmp:
        tmp.write(html)
    nm = os.path.basename(tmpname)
    print
    print "Uploading file. File name is: %s" % nm
    cf.upload_file(cont, tmpname, content_type="text/text") 
obj = cont.get_object(nm)
print
print "Stored Object:", obj