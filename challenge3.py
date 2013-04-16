#!/usr/bin/python

""" Challenge 3: Write a script that accepts a directory as an argument as well as a container name. The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). 
The script should handle errors appropriately. (Check for invalid paths, etc.) Worth 2 Points """

import pyrax
import os
import time
import argparse
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

parser = argparse.ArgumentParser(description='Please run this script as python challenge3.py -f folder_path -c container_name')
parser.add_argument('-f', '--file', help='Complete path of folder', required=True)
parser.add_argument('-c', '--container', help='Container name', required=True)

args = parser.parse_args()

path = args.file
cont = args.container

while not os.path.exists(path):
 print "Directory doesn't exist"
 path = raw_input('Please enter the exact directory path which you want to upload: ')

try:
 cont = cf.get_container(cont)
 print "Container exists, uploading file to container: " + cont.name
except pyrax.exceptions.NoSuchContainer:
 print "Container does not exist, creating container " + cont
 cont = cf.create_container(cont)

print "Uploading files from directory " + path +" to container "

upload_key, total_bytes = cf.upload_folder(path, container=cont)

print "Total bytes to upload:", total_bytes
uploaded = 0
while uploaded < total_bytes:
 uploaded = cf.get_uploaded(upload_key)
 print "Progress: %4.2f%%" % ((uploaded * 100.0) / total_bytes)
 time.sleep(5)

print "Uploaded contents from directory "+ path+ " to container "+ cont.name
