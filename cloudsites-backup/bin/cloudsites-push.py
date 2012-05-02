#!/usr/bin/python -tt
# cloudsites-rotate.py - A simple script to login to our Rackspace Cloud Files
# and rotate our backups for Rackspace Cloud Sites.

import os
import sys

# We need to make sure we have these locally.
import cloudfiles

# Get our personal info
from cloudsites-config import *

prog = sys.argv[0]

def usage():
    msg = "%s - Script to upload CloudSites backups.\n" % (prog,)
    msg += "Usage: %s [FILE]\n" % (prog,)
    sys.stdout.write(msg)
    sys.exit(1)

# Make sure we are given ONE file to upload
if len(sys.argv) != 2:
    usage()

# The file to upload.
localFile = sys.argv[1]

# Make sure the file exists
if not os.path.isfile(localFile):
    usage()

# Remove the path when naming it on Cloud Files
filename = os.path.basename(localFile)

# Connect to Rackspace Cloud Files with our API
conn = cloudfiles.get_connection(username, apiKey)

# Get our container object for where we plan to back everything up to.
containers = conn.get_all_containers()
for container in containers:
    if container.name == backupContainer:
        ourContainer = container
        break

msg = "INFO: Uploadng %s to %s..." % (filename, backupContainer)
sys.stdout.write(msg)
sys.stdout.flush()
ourBackup = ourContainer.create_object(filename)
ourBackup.load_from_filename(localFile)
sys.stdout.write('done.\n')

# All done.
sys.exit(0)
