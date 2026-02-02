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
Put the Shell scripts (`.sh` files) in an accessible folder, such as in `~/bin/`

In case you only have PDFTK, the second part of the script has to be modified to use PDFTK instead of CPDF.

# Usage
## Write the contents of the pdf/djvu file
First, you have to manually write in a text file (e.g. `contents.txt`) the contents of the pdf file you want to put bookmarks in:

* one line per bookmark;
* blank lines are ignored;
* the page number must be at the end of the line, seperated by a whitespace (other separator possible, not tested yet);
* **indentation is functional**: the depth of the bookmark is proportional to the number of whitespaces at the beginning of the line;
* page offsets in the form `+10` or `-8` on separate lines;
* if you use CPDF, the caracter `"` is reserved and connot be used (see generated file `contents.bmk`).

For better readability, you can use STL syntax highlighting in your text editor to better render the `contents.txt` file: numbers will be highlighted.

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

# The shell scripts
The shell script `addpdfcontents.sh` allows, in one line, to directly add the bookmarks in a pdf file with CPDF, provided the `contents.txt` file is in the current directory.
```
addpdfcontents.sh file.pdf
```

The shell script `adddjvucontents.sh` does the same on djvu files, using `djvused`.

The thrid shell script, `watchpdfcontents.sh`, allows to add the bookmarks in the pdf file each time the file `contents.txt` is modified. This can be useful to see the resulting pdf file while typing the contents file. 

Last, the `autoindentcontents.sh` script performs automatic indentation of a text file containing the table of contents:

- works only for "1.2.3 Subection title"-like TOC;
- also has a `-d` option to remove lines of dots ("........" often present between title and page number).


# Other similar tools

- [pdfoutline](https://github.com/yutayamamoto/pdfoutline) is very similar. It relies on `ghostscript` to add the outline to the pdf. *I did not find this tool when I developped the present one*. __Very slow__ but page number offset can be given anywhere in the contents file (this functionality is now also available). Can also significantly increase the size of the pdf (*I have to find out why and in which cases precisely*);
- [pdfoutliner](https://github.com/pnlng/pdfoutliner) seems a good option (not tested, only recently discovered), relies on `pdftk`;
- [simple-PDF-outline-adder](https://github.com/OpossumDaemon/simple-PDF-outline-adder) also uses `ghostscript`. The main drawback is that the outline text file must have, on each line, the page numbers BEFORE the title text; 
- [pdfoutline](https://github.com/eugmes/pdfoutline) is Haskell based and requires the level of each entry to be written explicitly (and is not determined from indentation of the text file);
- [doc-tools-toc](https://github.com/dalanicolai/doc-tools-toc) is a tool to manage table of contents (TOC) of pdf and djvu files with Emacs.

## See also

- [QuickOutline](https://github.com/ririv/QuickOutline) has a GUI and seems to be very powerful (automatically creates the outline from the OCR of the outline);
- [HandyOutliner](https://handyoutlinerfo.sourceforge.net/) also treats PDF and DJVU files, GUI based. 

