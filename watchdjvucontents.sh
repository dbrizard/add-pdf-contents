#! /bin/bash

while true; do inotifywait -e modify contents.txt 2>/dev/null ; date; adddjvucontents.sh "$1" ; done
