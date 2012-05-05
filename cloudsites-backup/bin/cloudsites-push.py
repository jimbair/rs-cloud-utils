#!/usr/bin/python -tt
# cloudsites-rotate.py - A simple script to login to our Rackspace Cloud Files
# and rotate our backups for Rackspace Cloud Sites.

import os
import sys

# We need to make sure we have these locally.
import cloudfiles

# Get our personal info
from config import *

prog = sys.argv[0]

uploaded = False

# This is a work-around for this issue:
# https://github.com/rackspace/python-cloudfiles/issues/34
#
# How many times you wish to re-try until giving up.
from ssl import SSLError
loopNumber, maxLoopNumber = 0, 5

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
ourContainer = conn.get_container(backupContainer)

# Upload our file.
while loopNumber < maxLoopNumber and not uploaded:
    try:
        msg = "INFO: Uploading %s to %s..." % (filename, backupContainer)
        sys.stdout.write(msg)
        sys.stdout.flush()
        ourBackup = ourContainer.create_object(filename)
        ourBackup.load_from_filename(localFile)
        sys.stdout.write('done.\n')
        sys.stdout.flush()
        uploaded = True
    except SSLError:
        loopNumber += 1
        msg = "failed.\n"
        msg += "ERROR: Upload of %s failed.\n" % (filename,)
        msg += "INFO: Retry #%d beginning.\n" % (loopNumber,)
        sys.stdout.write(msg)
        sys.stdout.flush()

# All done.
sys.exit(0)
