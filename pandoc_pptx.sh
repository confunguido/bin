#!/bin/bash
base_filename=$(basename "$1")
dirname_file=$(dirname "$1")
filename=$(echo "$base_filename" | cut -f 1 -d '.')
ext_name="${base_filename##*.}"

if [ $ext_name == 'org' ]
then
    # echo $ext_name
    # echo $filename
    # echo $dirname_file
    echo "pandoc $1 -o $dirname_file/$filename.pptx"
    pandoc $1 -o $dirname_file/$filename.pptx
fi
