#!/usr/bin/python -tt
# Simple script to take a list of databases and their 
# credentials and dump them to a local file.

import os
import sys

from commands import getstatusoutput

# Get our personal info
from config import *

def usage(prog):
    msg = "%s - program to backup MySQL databases.\n\n" % (prog,)
    msg += "Usage:\n"
    msg += "%s [DIRECTORY]\n" % (prog,)
    return msg


def dbDump(username, password, database, hostname):
    """
    A basic wrapper for mysqldump to dump our databases when
    given the required items.
    """

    command = "mysqldump -u %s -p%s %s -h %s" % ( username, password, database, hostname )

    # Run mysqldump, make sure it exists cleaning, and return the output.
    ec, out = getstatusoutput(command)
    if ec:
        msg = "ERROR: MySQL dump of %s failed.\n" % (database,)
        sys.stderr.write(msg)
        sys.exit(1)

    return out


# MAIN
def main():

    # Our program name
    prog = os.path.basename(sys.argv[0])

    # We need two args (one for prog name, one for directory)
    if len(sys.argv) != 2:
        msg = "ERROR: Directory not provided.\n"
        msg += usage(prog)
        sys.stderr.write(msg)
        sys.exit(1)

    dumpDir = sys.argv[1]

    # Make sure directory exists.
    if not os.path.isdir(dumpDir):
        msg = "ERROR: Directory not found.\n"
        msg += usage(prog)
        sys.stderr.write(msg)
        sys.exit(1)

    # For tuple in tuples, backup each database.
    for creds in databases:
        username = creds[0]
        password = creds[1]
        database = creds[2]
        hostname = creds[3]
        filename = '%s.sql' % (database,)

        # Combine folder and filename, resolving any symlinks.
        dumpFile = os.path.realpath(os.path.join(dumpDir, filename))

        # Don't overwrite existing files.
        if os.path.isfile(dumpFile):
            msg = "ERROR: %s already exists.\n" % (dumpFile,)
            sys.stderr.write(msg)
            sys.exit(1)

        # Do the deed
        msg = "INFO: Dumping %s..." % (database,)
        sys.stdout.write(msg)
        sys.stdout.flush()
        textObj = dbDump(username, password, database, hostname)
        f = open(dumpFile, 'w')
        f.write(textObj)
        f.close()
        sys.stdout.write('done.\n')
        
        # A basic check to make sure we closed our file correctly.
        if not f.closed:
            msg = "ERROR: Unable to write our database backup to %s\n" % (dumpFile)
            sys.stderr.write(msg)
            sys.exit(1)

# Run if called directly.
if __name__ == '__main__':
    main()
    sys.exit(0)
