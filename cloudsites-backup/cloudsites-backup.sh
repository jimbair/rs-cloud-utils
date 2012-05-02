#!/bin/sh
# A small shell script to backup all of your Cloud Sites local files.
# Separeated from DB dumps and removing old files for clarity.

# Our customer number for Rackspace Cloud sites.
# This # is in front of DBs, db users, and in your /mnt/ target.
custNum='123456'

# Separate with spaces if needed - most users will only need one.
# Only tested against single controller so far.
storage='stor1-wc1-dfw1-fake'

# Day of the week to flag as weekly - example: Monday
weekly='Sunday'

# The rest of this you shouldn't have to touch! Do so with caution.
today=$(date +%A)
if [ -z "${today}" ]; then
    echo "Unable to find today's date."
    exit 1
fi

if [ "${weekly}" == "${today}" ]; then
    prefix='weekly'
else
    prefix='daily'
fi

# Our program name
prog=$(basename $0)

# Let's get started
echo "${prog} started on $(date)"

# Loop it, in case we have multiple storage arrays
for i in $storage; do

    # Where all of our website files should reside.
    ourPath="/mnt/${i}/${custNum}"

    # Make sure our folder is there.
    if [ ! -d "${ourPath}" ]; then
        echo "FAILURE: ${ourPath} is missing."
        exit 1
    fi

    # Make sure we have the libs we need.
    # PHP libs to push updates (soon to be replaced by Python)
    cfBackup="${ourPath}/bin/cloudfiles-push.py"
    if [ ! -s "${cfBackup}" ]; then
         echo "FAILURE: Unable to source our Cloudfiles Push script."
         exit 1
    fi

    # Dump our databases to filesystem before tarring everything up)
    dbBackup="${ourPath}/bin/mysql-dump.py"
    if [ ! -s "${dbBackup}" ]; then
        echo "FAILURE: Unable to find our DB backup script."
        exit 1
    fi

    # Needed to delete old backups.
    cfRotate="${ourPath}/bin/cloudfiles-rotate.py"
    if [ ! -s "${dbBackup}" ]; then
        echo "FAILURE: Unable to find our Cloudfiles Rotation script."
        exit 1
    fi

    # Backup our databases and check for a clean exit
    ${dbBackup} ${ourPath}
    if [ $? -ne 0 ]; then
        echo "FAILURE: Our databases failed to backup without error."
        exit 1
    fi

    # Set the date and name for the backup files
    # Format is daily_20120501_123456_stor1-wc1-dfw1.tar.gz.*
    backupName="${prefix}_$(date +%Y%m%d)_${custNum}_${i}.tar.gz."

    # Our tarball(s) containing all of our files.
    fullBack="${ourPath}/${backupName}"

    # Backup Site - no verbosity as it's in cron. Also, Cloud Files is limited to 5GB, so split tar as needed.
    tar -czpf /dev/stdout ${ourPath} | split -d -b 5000m - ${fullBack}
    if [ $? -ne 0 ]; then
        echo "FAILURE: Our command 'tar -czpf /dev/stdout ${ourPath}' then split failed."
        exit 1
    fi

    # Upload our files to cloud files.
    for tarball in ${fullBack}*; do
        ${cfBackup} ${tarball}
        if [ $? -ne 0 ]; then
            echo "FAILURE: Our command 'php ${cfBackup} ${tarball}' failed."
            exit 1
        fi
    done

    # After your backup has been uploaded, remove the tar ball and SQL dumps from the filesystem.
    rm -f ${fullBack}* ${ourPath}/${custNum}_*.sql
    if [ $? -ne 0 ]; then
        echo "FAILURE: Removing backup files failed."
        exit 1
    fi

done

# All done
echo "${prog} ompleted on $(date)"
exit 0
