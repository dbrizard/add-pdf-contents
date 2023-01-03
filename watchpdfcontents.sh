#! /bin/bash

while true; do inotifywait -e modify contents.txt 2>/dev/null ; date; addpdfcontents.sh "$1" ; done
