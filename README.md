Add bookmarks/outline to PDF or DJVU files to better scroll through its contents.

These small tools simplify the addititon of bookmarks/contents to PDF or DJVU files.

# Installation
## Python module
Put the Python module `contents.py` somewhere in your python path. Or modify the python path to tell where to find the module.

## PDF manipulating tool
Install either [CPDF](https://community.coherentpdf.com/) or [PDFTK](https://www.pdflabs.com/tools/pdftk-server/).

## DJVU tool
Make sure you have `djvused` installed (via [DjVuLibre](http://djvu.sourceforge.net/index.html)).

## Shell script
Put the Shell script `addpdfcontents.sh` in an accessible folder, such as in `~/bin/`

In case you only have PDFTK, the second part of the script has to be modified to use PDFTK instead of CPDF.

# Usage
## Write the contents of the pdf/djvu file
First, you have to manually write the contents of the pdf file you want to put bookmarks in:

* one line per bookmark;
* blank lines are ignored;
* the page number must be at the end of the line, seperated by a whitespace (other separator possible, not tested yet);
* **indentation is functional**: the depth of the bookmark is proportional to the number of whitespaces at the beginning of the line;
* if you use CPDF, the caracter `"` is reserved and connot be used (see generated file `contents.bmk`).

## Convert  `contents.txt` into `contents.bmk`
The Python module `contents.py` converts the contents of the pdf file into a format enabling the addition  of bookmarks in the pdf with the chosen tool (CPDF or PDFTK). By default, it searches the `contents.txt` file and writes a `contents.bmk` file.

The simplest line is therefore, in a Python terminal:
```
from contents import Contents
Contents().write4CPDF()
```

See the Python module for the following options:

* page number offset;
* open bookmarks or not (CPDF);
* debug option in case writing the `contents.bmk` file fails.

## Add the bookmarks to the file
This now takes place in 
a terminal.

### With CPDF:
```
cpdf -add-bookmarks contents.bmk in.pdf -o out.pdf
```

### With PDFTK
First, get the metadata of the PDF file:
```
pdftk file.pdf dump_data > metadata.txt
```

Then, modify the metadata file by including `contents.bmk` after the line containing the keyword `NumberOfPages:`.

Finally, updade the PDF metadata:
```
pdftk file.pdf update_info metadata.txt output newfile.pdf
```

### With DJVU files
Use the two following commands:
```
djvused -e print-outline book.djvu
djvused -s -e 'set-outline contents.bmk' book.djvu
```

# The shell scrip `addpdfcontents.sh`
The shell scrit allows, in on line, to directly add the bookmarks in a pdf file with CPDF, provided the `contents.txt` file is written.
```
addpdfcontents.sh file.pdf
```

**Warning**: the script is not yet robust to some special characters in the file name.

