#!/usr/bin/python
"""
Challenge 11: Write an application that will:
Create an SSL terminated load balancer (Create self-signed certificate.)
Create a DNS record that should be pointed to the load balancer.
Create Three servers as nodes behind the LB.
Each server should have a CBS volume attached to it. (Size and type are irrelevant.)
All three servers should have a private Cloud Network shared between them.
Login information to all three servers returned in a readable format as the result of the script, including connection information.
"""

import pyrax
import os, time
import pyrax.exceptions as exc
import argparse

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
cnw = pyrax.cloud_networks
cbs = pyrax.cloud_blockstorage
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns

parser = argparse.ArgumentParser(description='Please run this script as python challenge11.py -c ssl_cert -k key_file')
parser.add_argument('-c','--ssl_cert', help='SSL certificate path')
parser.add_argument('-k','--key_file', help='Key file')

args = parser.parse_args()

if os.path.isfile(args.ssl_cert) == False:
    print 'SSL cert does not exist. Please enter proper path and run script again'
    exit(1)
else:
    print 'File %s exists' %args.ssl_cert
        

if os.path.isfile(args.key_file) == False:
    print 'Key file does not exist. Please enter proper path and run script again'
    exit(1)
else:
    print 'File %s exists' %args.key_file
    
def create_servers():
    network_name = "My_Network"
    network_ip = "192.168.0.0/24"
    new_net = cnw.create(network_name, cidr=network_ip)
    networks = new_net.get_server_networks(public=True, private=True)
    print "\nCloud Netorks has been setup\n"
    
  
    vols = []
    for i in xrange(0,3):
       vol = "storage"+str(i)
       vol = cbs.create(name=vol, size=100, volume_type="SATA")
       vols.append(vol)
    print "Cloud Block Storage created !!!!!\n"    
  #  print vols
   
    servers = []
    pas = []
    print "Now servers are getting created"
    for i in xrange(0,3):
        name = "server"+str(i)
        server = cs.servers.create(name, "c195ef3b-9195-4474-b6f7-16e5bd86acd0", "2", nics=networks)
        servers.append(server)
        pas.append(server.adminPass)
    
    for i in xrange(0,3):
        while servers[i].status != "ACTIVE":
            print "Waiting for servers to be active" 
            servers[0] = cs.servers.get(servers[0].id)
            servers[1] = cs.servers.get(servers[1].id)
            servers[2] = cs.servers.get(servers[2].id)
            time.sleep(15)
    
    ips = []    
    for i in xrange(0,3):
        ip = servers[i].networks["private"][0]
        print ip     
        ips.append(ip)
    print ips

    print "\nAttaching storage device to servers:"
    
    for i in xrange(0,3):
        vols[i].attach_to_instance(servers[i], mountpoint="/dev/xvdd")
        pyrax.utils.wait_until(vols[i], "status", "in-use", interval=3, attempts=0, verbose=True)
        print "Volume attachments: ", vols[i].attachments
        print "Attached to server %s moving on\n" % (i)
    
    print "Congrats !!!! Block storage are attached to all the servers"
        
    with open(args.ssl_cert,'r') as f:
     cert = f.read()

    with open(args.key_file,'r') as f:
     key = f.read()

    nodes = []
    for i in xrange(0,3):
         node = clb.Node(address=ips[i], port=80, condition="ENABLED")
         nodes.append(node)
    print "Nodes created. Creating load balancer\n"
    
    vip = clb.VirtualIP(type="PUBLIC")

    lb = clb.create("example_lb", port=80, protocol="HTTP",
        nodes=nodes, virtual_ips=[vip])

    while lb.status != 'ACTIVE':
      print "Waiting for load balancer to be active"        
      lb = clb.get(lb.id)
      time.sleep(10)        
    print "Load balancer created, adding SSL to it\n"

    lb.add_ssl_termination(
        securePort=443,
        enabled=True,
        secureTrafficOnly=False,
        certificate=cert,
        privatekey=key,
        )

    while lb.status != 'ACTIVE':
         lb = clb.get(lb.id)
         time.sleep(10)
    print "Congrats Load balancer is created with SSL\n"
    
    print "Load Balancer:", lb.name
    print "ID:", lb.id
    print "Status:", lb.status
    print "Nodes:", lb.nodes
    print "Virtual IPs:", lb.virtual_ips
    print "Algorithm:", lb.algorithm
    print "Protocol:", lb.protocol        
    print 
    
    print 
    ip = lb.virtual_ips[0].address
    
    try:
            dom = dns.create(name="dhruvilthakkar17.com", emailAddress="abc@example.edu",
                    ttl=900, comment="sample domain")
    except exc.DomainCreationFailed as e:
            print "Domain creation failed:", e
    print "Domain created:"
    print
    
    a_rec = {"type": "A",
            "name": "dhruvilthakkar17.com",
            "data": ip,
            "ttl": 6000}
    recs = dom.add_records([a_rec])
    print "Domain is created\n"
    print recs
    
    for i in xrange(0,3):
        print "Server Name: ",servers[i].name
        print "Admin Password: ", pas[i]
        print "Networks: ", servers[i].networks
        print
        
if __name__ == "__main__":
    create_servers()
