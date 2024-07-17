#! /bin/bash

# if no argument is provided, suppose there is only one pdf file here
ARG1=${1:-$(ls *.pdf)}

# suppose contents.txt file is here
python3 -c "from contents import Contents; Contents().write4CPDF()"
# Add bookmarks to the given pdf file
cpdf -add-bookmarks contents.bmk "$ARG1" -o "$ARG1"




