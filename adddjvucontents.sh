#! /bin/bash

# if no argument is provided, suppose there is only one DJVU file here
ARG1=${1:-$(ls *.djvu)}

# suppose contents.txt file is here
python3 -c "from contents import Contents; Contents().write4DJVU()"
# Add bookmarks to the given djvu file
djvused -s -e 'set-outline contents.bmk' "$ARG1"
