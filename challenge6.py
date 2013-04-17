#!/usr/bin/python
"""
Challenge 6: Write a script that creates a CDN-enabled container in Cloud Files. Worth 1 Point
"""
import pyrax
import os
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

name = raw_input("Enter the name of the container: ")
while name == '':
    name = raw_input("Please enter a valid name of container: ")

print "\nCreating container with name %s \n" %(name)
cont = cf.create_container(name)
print "Container:", cont
print "Before Making Public"
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri

cont.make_public(ttl=1200)

cont = cf.get_container(name)
print cont
print "After Making Public"
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri

#f = cf.list_containers()
#f1 = cf.get_all_containers()

#print f
#print f1
