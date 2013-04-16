#!/usr/bin/env python
"""Challenge 2: Write a script that clones a server (takes an image and deploys the image as a new server"""

import pyrax
import os
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers
servers = cs.servers.list()
srv_dict = {}

print "Welcome to challenge 2. We are going to clone a server i.e create image of a server and than create a server from that image \n"

print "Select a server from which an image will be created."
for pos, srv in enumerate(servers):
    print "%s: %s" % (pos, srv.name)
    srv_dict[str(pos)] = srv.id
selection = None

while selection not in srv_dict:
    if selection is not None:
        print " -- Invalid choice"
    selection = raw_input("Enter the number for your choice: ")
    while selection == '':
        print "You must select one server"
        selection = raw_input("Please select one of the server: ")

server_id = srv_dict[selection]
print
nm = raw_input("Please enter a name for the image: ")
while nm == '':
    print "You must specify a name for the image"
    nm = raw_input("Please enter a name for the image. ")

img_id = cs.servers.create_image(server_id, nm)
print "Image '%s' is being created. Its ID is: %s \n" % (nm, img_id)

a = cs.images.list()
final = [img for img in cs.images.list() if nm in img.name][0]

while final.status != "ACTIVE":
 time.sleep(15)
 print "Please wait while the image is being build:"
 final = [img for img in cs.images.list() if nm in img.name][0]

print "\nThe image build is complete, now creating server from that image: \n"
name = 'from_'+nm
server = cs.servers.create(name,final.id,'3')
pas = server.adminPass
print 'Server is spun-up. Please wait for its network to be set up. \n'

while not server.networks:
    print "Please wait while networks are setup for server." 
    time.sleep(10)
    server = cs.servers.get(server.id)

print "#######################"
print "Here are logins for server %s" % (server.name)
print "ID:", server.id
print "Status:", server.status
print "Admin password:", pas
print server.networks
print "#######################"