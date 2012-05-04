#!/usr/bin/python -tt
# cloudsites-rotate.py - A simple script to login to our Rackspace Cloud Files
# and rotate our backups for Rackspace Cloud Sites.

import sys

# We need to make sure we have these locally.
import cloudfiles

# Get our personal info
from config import *

# More required information
rotationTypes = ('weekly', 'daily' )
ourBackups, dates = [], []

# This lets our rotationTypes be dynamic
maxDateNum = len(rotationTypes) + 1

# Build our dict for or rotation types for count later.
rotationCount = {}
for ourType in rotationTypes:
    rotationCount[ourType] = 0

# Connect to Rackspace Cloud Files with our API
conn = cloudfiles.get_connection(username, apiKey)

# Get our container object for where we plan to back everything up to.
ourContainer = conn.get_container(backupContainer)

# Get all of the files in our container.
ourObjects = ourContainer.get_objects()
for obj in ourObjects:
    # Pull the name from the cloudfiles object object (yo dawg)
    ourFile = str(obj.name)
    ourFile = '.'.join(ourFile.split('.')[:-1])
    if ourFile not in ourBackups:
        ourBackups.append(ourFile)

# Now, figure out what day's files need removed.
for ourFile in ourBackups:
    date = int(ourFile.split('_')[1])
    if date not in dates:
        dates.append(date)

# At most, we should have 3 dates present:
# Either two daily and a weekly, or two 
# weekly and a daily.
if len(dates) > maxDateNum:
    msg = "ERROR: More than 3 days of files found.\n"
    msg += "Please manually audit your backups and try again.\n"
    # Would be nice to add --force ability like rdiff-backup
    sys.stdout.write(msg)
    sys.exit(1)

# Figure out if we have to clean up daily or weekly backups.
for ourFile in ourBackups:
    for ourType in rotationTypes:
        if ourType in ourFile:
            rotationCount[ourType] += 1

# Find the largest key in our dict
backupType = sorted(rotationCount, key=rotationCount.get, reverse=True)[0]

# If our key is less than two, nothing to backup.
if rotationCount[backupType] < 2:
    sys.stdout.write("INFO: Nothing to rotate. Exiting.\n")
    sys.exit(0)
elif rotationCount[backupType] > 2:
    msg = "ERROR: More than two days found for rotation.\n"
    msg += "Please manually audit your backups and try again.\n"
    # Would be nice to add --force ability like rdiff-backup
    sys.stdout.write(msg)
    sys.exit(1)

# Remove invalid backup types (daily vs weekly)
for ourFile in ourBackups:
    if backupType not in ourFile:
        ourBackups.remove(ourFile)

# Now figure out which of the two is older.
dateCheck = {}
for ourFile in ourBackups:
    date = ourFile.split('_')[1]
    dateCheck[ourFile] = date

# The lower number is the old backup
oldBackup = sorted(dateCheck, key=dateCheck.get, reverse=False)[0]

# Remove the old objects
for obj in ourObjects:
    if oldBackup in obj.name:
        print "Purging old backup", obj
        ourContainer.delete_object(obj.name)

sys.exit(0) 
