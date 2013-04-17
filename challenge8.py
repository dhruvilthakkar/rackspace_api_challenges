#!/usr/bin/python
import pyrax
import os
import argparse
import pyrax.exceptions as exc

"""Challenge 8: Write a script that will create a static webpage served out of Cloud Files. The script must create a new container, cdn enable it, 
enable it to serve an index file, create an index file object, upload the object to the container, and create a CNAME record pointing to the CDN URL of the container. Worth 3 Points
"""

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

parser = argparse.ArgumentParser(description='Please run this script as python container_name domain_name')
parser.add_argument('-c', '--container', help='Container name')
parser.add_argument('-f', '--fqdn', help='FQDN domain name')
args = parser.parse_args()
print "Creating container with name %s"%(args.container)

cont = cf.create_container(args.container)
cont.make_public(ttl=1200)

cont = cf.get_container(args.container)

print "cdn_uri: ", cont.cdn_uri
print "cdn_streaming_uri: ", cont.cdn_streaming_uri
cname = cont.cdn_uri[7:]
#print cname
text = "This is test index.html from Dhruvil Thakkar"
obj = cf.store_object(cont, "index.html", text)
print "Stored Object Name in container: ", obj.name
print "Size of the file is: ", obj.total_bytes

record = args.container + "." + args.fqdn

print "\nAdding record for subdomain %s" %(record)
cname_rec = {"type": "CNAME",
         "name": record,
         "data": cname,
         "ttl": 6000
         }

dom = dns.find(name=args.fqdn)
recs = dom.add_records([cname_rec])
print "\nRecord for subdomain is added. Here are the details\n"
print recs