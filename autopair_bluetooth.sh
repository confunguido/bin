#!/bin/bash
if [$1 -eq 1]
then
    bluetoothctl<<EOF
    connect 20:74:CF:0B:62:F8
EOF
else if [ $1 -eq 2 ]
then
    bluetoothctl<<EOF
    connect 00:11:67:11:1C:5C
EOF
fi

