#!/bin/bash
remotedir=~/RemoteCRC
if [ ! -d $remotedir ]
then
    echo "$remotedir doesn't exist, no need to unmount"
    exit
fi

if grep -qs $remotedir /proc/mounts
then
    sudo umount $remotedir
else
    echo " $remotedir not mounted"
fi

if grep -qs $remotedir /proc/mounts
then
    echo "cant remote, $remote dir still mounted"
else
    rm -r $remotedir
fi

