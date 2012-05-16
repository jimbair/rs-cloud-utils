#!/usr/bin/python -tt
# Below, please configure your Rackspace Cloud Files information.
username = 'your_username_here'
apiKey = 'yourapigoeshere1234567'

# You shouldn't have to change this.
backupContainer = 'cloudsites'

# For our DB backups
# Just an example of how to de-duplicate entries
db1 = '10.20.30.1'
db2 = 'my-other-db.dc01.superhax.net'

# Edit the following tuple of tuples to add the collection of Databases
# you wish to backup. This must be done as we cannot dump all DBs with
# MySQL dump, and you generally tie one DB per cloud site.
#
# Follows dbDump format:
# User, pass, db, host
databases = [ ( '123456_wordpress', 'l33tp4ssW0Rd', '123456_wpdb', db1 ),
              ( '123456_phpbb', 'l33tp4ssW0Rd', '123456_phpbbdb', db1 ),
              ( '123456_personal', 'l33tp4ssW0Rd', '123456_mydb', db2 ),
              ( '123456_testing', 'l33tp4ssW0Rd', '123456_testdb', db2 ),
              ( '123456_dev', 'l33tp4ssW0Rd', '123456_devdb', db2 )
            ]
