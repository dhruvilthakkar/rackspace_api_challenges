#!/usr/bin/python
"""Challenge 13: Write an application that nukes everything in your Cloud Account. It should:
Delete all Cloud Servers
Delete all Custom Images
Delete all Cloud Files Containers and Objects
Delete all Databases
Delete all Networks
Delete all CBS Volumes"""

import pyrax
import os,time

creds_file = os.path.expanduser("/Users/dhru4670/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
cnw = pyrax.cloud_networks
cbs = pyrax.cloud_blockstorage
cdb = pyrax.cloud_databases
cf = pyrax.cloudfiles

def delete_servers():
    print "\nDeleting servers:"
    servers = cs.servers.list()
    if not servers:
        print 'No servers exists'
        return
    for server in servers:
        while server.status != 'ACTIVE':
            print 'Waiting for the servers %s to be active' %(server.name)
            time.sleep(10)
            server = cs.servers.get(server.id)    
        print 'Deleting server',server.name
        server.delete()    

def delete_images():    
    print '\nDeleting images'
    all_images = cs.images.list()
    images = [img for img in all_images if hasattr(img, "server")]
    if not images:
        print 'No image exists'
        return
    for image in images:        
        while image.status != 'ACTIVE':
            print 'Waiting for the image %s to be active:' %image.name
            time.sleep(10)
            image = cs.images.get(image.id)
    print 'Deleting image', image.name
    cs.images.delete(image.id)    

def delete_networks():
    print '\nDeleting cloud networks:'
    networks = cnw.list()
    for network in networks:
        if network.id != '00000000-0000-0000-0000-000000000000' and network.id !='11111111-1111-1111-1111-111111111111':
            print 'Deleting network:',network.id
            network.delete() 
            
def delete_blockstorage():
    print '\nDeleting cloud block storage:'
    vols = cbs.findall()
    if not vols:
        print 'No block storage exist'
        return
    for vol in vols:
        print 'Deleting volume',vol.name
        vol.delete()            

def delete_database():
    print '\nDeleting cloud database:'
    dbs = cdb.list()
    if not dbs:
        print 'No database exist'
        return
    for db in dbs:
        while db.status != 'ACTIVE':
            print 'Waiting for the instance %s to be active:' %db.name
            time.sleep(10)
            db = cdb.get(db.id)
        print 'Deleting volume',db.name
        db.delete()

def delete_files():
    print '\nDeleting cloud files:'
    conts = cf.get_all_containers()
    if not conts:
        print 'There are no containers'
        return
    for cont in conts:
        print 'Deleting container',cont
        cont.delete_all_objects()
        cont.delete()
            
                        
if __name__ == "__main__":
    delete_images()
    delete_servers()
    delete_networks()   
    delete_blockstorage()
    delete_database()
    delete_files()     