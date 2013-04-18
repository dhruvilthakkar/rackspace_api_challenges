#!/usr/bin/python
"""Challenge 9: Write an application that when passed the arguments FQDN, image, and flavor it creates a server of the specified image and 
flavor with the same name as the fqdn, and creates a DNS entry for the fqdn pointing to the server's public IP. Worth 2 Points"""
import pyrax
import os
import sys
import time
import pyrax.exceptions as exc
import argparse

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
dns = pyrax.cloud_dns
dom = dns.list()

parser = argparse.ArgumentParser(description='Please run this script as python challenge9.py -d fqdn -i image -f flavor')
parser.add_argument('-d', '--fqdn', help='Domain name for which you want to create server and add DNS record',required=True)
parser.add_argument('-i','--image', help='Image id', default='03318d19-b6e6-4092-9b5c-4758ee0ada60')
parser.add_argument('-f', '--flavor', help='Flavor', default=2)
args = parser.parse_args()

fqdn = args.fqdn
id = args.image
flavor = args.flavor

print "Creating server with name %s image id %s and with flavor %d \n" % (fqdn, str(id), flavor)
pas = ""
created = cs.servers.create(fqdn, id, flavor)
pas = created.adminPass

while created.status != 'ACTIVE':
 print "Logins will be printed, please wait for server to be active:"
 time.sleep(15)
 created = cs.servers.get(created.id)

ip = created.networks["public"][0]
print "Public IP of server is ", ip

print ""
print "#######################"
print "Here are logins for the server which is created:"
print "ID:", created.id
print "Status:", created.status
print "Admin password:", pas
print ip 
print created.networks["private"][0]
print "#######################"

try:
    dom = dns.find(name=fqdn)
except exc.NotFound:
    answer = raw_input("\nThe domain '%s' was not found. Do you want to create "
            "it? [y/n]" % fqdn)
    if not answer.lower().startswith("y"):
        sys.exit()

try:
 dom = dns.create(name=fqdn, emailAddress="sample@example.edu",
 ttl=900, comment="sample domain")
except exc.DomainCreationFailed as e:
 print "Domain creation failed:", e
 print "Domain created:", dom

print "Domain created"
print "Adding records now"

a_rec = {"type": "A",
        "name": fqdn,
        "data": ip,
        "ttl": 6000}
mx_rec = {"type": "MX",
        "name": fqdn,
        "data": "mail."+fqdn,
        "priority": 50,
        "comment": "Backup mail server"}
recs = dom.add_records([a_rec, mx_rec])
print "\nRecords added. Here are the details:\n"
print recs


