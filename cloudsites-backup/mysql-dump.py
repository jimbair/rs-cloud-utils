#!/usr/bin/python -tt
# Simple script to take a list of databases and their 
# credentials and dump them to a local file.

import os
import sys

from commands import getstatusoutput

# Just an example of how to de-duplicate entries
db1 = '10.20.30.1'
db2 = 'my-other-db.dc01.superhax.net'

# Edit the following tuple of tuples to add the collection of Databases
# you wish to backup. This must be done as we cannot dump all DBs with
# MySQL dump, and you generally tie one DB per cloud site.
#
# Follows dbDump format:
# User, pass, db, host
databases = (
            ( '123456_wordpress', 'l33tp4ssW0Rd', '123456_wpdb', db1 ),
            ( '123456_phpbb', 'l33tp4ssW0Rd', '123456_phpbbdb', db1 ),
            ( '123456_personal', 'l33tp4ssW0Rd', '123456_mydb', db2 ),
            ( '123456_testing', 'l33tp4ssW0Rd', '123456_testdb', db2 ),
            ( '123456_dev', 'l33tp4ssW0Rd', '123456_devdb', db2 )
            )

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
    prog = sys.argv[0]

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
        if dumpDir.endswith('/'):
            dumpfile = "%s%s.sql" % (dumpDir, database)
        else:
            dumpfile = "%s/%s.sql" % (dumpDir, database)

        # Don't overwrite existing files.
        if os.path.isfile(dumpfile):
            msg = "ERROR: %s already exists.\n" % (dumpfile,)
            sys.stderr.write(msg)
            sys.exit(1)

        # Do the deed
        msg = "Dumping %s..." % (database,)
        sys.stdout.write(msg)
        sys.stdout.flush()
        textObj = dbDump(username, password, database, hostname)
        f = open(dumpfile, 'w')
        f.write(textObj)
        f.close()
        sys.stdout.write('done.\n')
        
        # A basic check to make sure we closed our file correctly.
        if not f.closed:
            msg = "ERROR: Unable to write our database backup to %s\n" % (dumpfile)
            sys.stderr.write(msg)
            sys.exit(1)

# Run if called directly.
if __name__ == '__main__':
    main()
    sys.exit(0)
