#! /bin/bash

# suppose contents.txt file is here
python3 -c "from contents import Contents; Contents().write4CPDF()"
# Add bookmarks to the given pdf file
cpdf -add-bookmarks contents.bmk "$1" -o "$1"
