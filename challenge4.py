#!/usr/bin/python

"""Challenge 4: Write a script that uses Cloud DNS to create a new A record when passed a FQDN and IP address as arguments. Worth 1 Point"""

import pyrax, os, sys, argparse
import pyrax.exceptions as exc

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns

parser = argparse.ArgumentParser(description='Please run this script as python challenge4.py -f fqdn_name -i ip_address')
parser.add_argument('-f', '--fqdn',help='FQDN domain name', required=True)
parser.add_argument('-i', '--ip', help='IP address', required=True)
args=parser.parse_args()

fqdn = args.fqdn
ip = args.ip

dom = dns.list()

print "You have entered domain : "+fqdn
print "The IP addres you entered is : "+ str(ip)

try:
    dom = dns.find(name=fqdn)
except exc.NotFound:
    answer = raw_input("The domain '%s' was not found. Do you want to create "
            "it? [y/n]" % fqdn)
    if not answer.lower().startswith("y"):
        sys.exit()

    try:
        dom = dns.create(name=fqdn, emailAddress="sample@example.edu",
                ttl=900, comment="sample domain")
    except exc.DomainCreationFailed as e:
        print "Domain creation failed:", e
    print "Domain created:", dom
    print "Adding records\n"


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
print recs

