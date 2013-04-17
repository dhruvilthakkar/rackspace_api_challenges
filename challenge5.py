#!/usr/bin/python
"""Challenge 5: Write a script that creates a Cloud Database instance. 
This instance should contain at least one database, and the database should have at least one user that can connect to it. Worth 1 Point"""
import pyrax
import os
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cdb = pyrax.cloud_databases

instance_name = pyrax.utils.random_name(8)

flavors = cdb.list_flavors()
nm = raw_input("Enter a name for your new database instance: ")
print
print "Available Flavors:"
for pos, flavor in enumerate(flavors):
    print "%s: %s, %s" % (pos, flavor.name, flavor.ram)

flav = int(raw_input("Select a Flavor for your new instance: "))
try:
    selected = flavors[flav]
except IndexError:
    print "Invalid selection; exiting."
    sys.exit()

print
sz = int(raw_input("Enter the volume size in GB (1-50): "))

print "Creating a database instance with name %s flavor %d and size %d GB" % (nm, flav, sz)

instance = cdb.create(nm, flavor=selected, volume=sz)
id=instance.id

print type(instance.status)
while instance.status != "ACTIVE":
 print "Please wait while the instance is being build:"
 time.sleep(15)
 instance = cdb.get(id)

print "\nInstance is build, here are the details:"
print "Instance Name:", instance.name
print "Instance ID:", instance.id
print "Instance Status:", instance.status

print "\nInstance is created, lets create database"

name = raw_input("Please enter the name of the database: ")
while name == '':
    print "Please enter some name for database"
    name = raw_input("Please enter the name of the database: ")
db = instance.create_database(name)
print "Database %s is created" %(db.name)
#print db

username = raw_input("Instance is created, database is created, please enter a username: ")
while username == '':
    print "Please enter a valid username "
    username = raw_input("Instance is created, database is created, please enter a username: ")
user = instance.create_user(name=username,password="q1w2e3r4",database_names=db)
print "User %s is created for database" %(username)

dbs = instance.list_databases()
users = instance.list_users()
print dbs
print users





