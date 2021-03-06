#!/bin/bash

if [ $1 = "pull" ]; then
    echo "pull"
    rclone sync --create-empty-src-dirs -P --update --filter-from ~/.filter_dropbox  -v Dropbox:  ~/Dropbox $2
elif [ $1 = "push" ]; then
    echo "push"
    rclone sync -P --update --filter-from ~/.filter_dropbox -v ~/Dropbox  Dropbox: $2
else
    echo "invalid input, only push and pull allowed"
fi
