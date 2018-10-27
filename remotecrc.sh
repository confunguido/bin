#!/bin/bash
remotedir=~/RemoteCRC
if [ ! -d $remotedir ]
then
   mkdir $remotedir
fi

if nmcli con show --active | grep -q ND_Campus
then
    echo "VPN CONNECTED"
else
    nmcli con up ND_Campus
fi

if nmcli con show --active | grep -q ND_Campus
then
    sshfs gcamargo@condorfe.crc.nd.edu:/afs/crc.nd.edu/user/g/gcamargo $remotedir
fi
