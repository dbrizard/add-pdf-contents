#! /bin/bash

# suppose contents.txt file is here
python3 -c "from contents import Contents; Contents().write4DJVU()"
# Add bookmarks to the given djvu file
djvused -s -e 'set-outline contents.bmk' "$1"
