#! /bin/bash

# Automatic indentation with spaces of text file containing the table of contents
# (TOC) of a pdf document. Indentation proportional to TOC depth. 


# Note: improved thanks to the book "Learning bash shell", Newham & Rosenblatt 
usage="usage: autoindentcontents.sh [-d] file.txt"

while getopts ":d" opt; do
    case $opt in
        d  ) # remove dots 
             sed -i -E 's/\.\.+//g' $2
             sed -i -E 's/(\. +)+/    /g' $2 ;;
        \? ) echo $usage
             exit 1 ;;
    esac
done

shift $(($OPTIND - 1))

if [ -z "$@" ]; then
    echo "No file given"
    echo $usage
    exit 1
fi

# level 0: do nothing
# level 1: add one space
sed -z -i -E 's/\n([0-9A-Z]+\.[0-9]+\s)/\n \1/g' $1
# level 2: add two spaces
sed -z -i -E 's/\n([0-9A-Z]+\.[0-9]+.[0-9]+\s)/\n  \1/g' $1
# levels 3 & 4
sed -z -i -E 's/\n([0-9A-Z]+\.[0-9]+.[0-9]+.[0-9]+\s)/\n   \1/g' $1
sed -z -i -E 's/\n([0-9A-Z]+\.[0-9]+.[0-9]+.[0-9]+.[0-9]+\s)/\n    \1/g' $1

