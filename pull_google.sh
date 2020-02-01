#!/bin/bash

if [ $1 = "pull" ]; then
    echo "pull"
    rclone sync -P --update --filter-from ~/.filter_gdrive -v GoogleDrive:  ~/GoogleDrive --dry-run
elif [ $1 = "push" ]; then
    echo "push"
    rclone sync -P --update --filter-from ~/.filter_gdrive -v ~/GoogleDrive  GoogleDrive: --dry-run
else
    echo "invalid inpu, only push and pull allowed"
fi
