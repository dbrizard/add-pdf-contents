# -*- coding: utf-8 -*-
"""
Small Python module to format the table of contents for inclusion in a 
PDF or DJVU file.

# Initial contents file formating

The input file 'contents.txt' must be formated this way:

- number of spaces at the beginning of the line indicates the level;
- the number at the end of the line indicates the page;
- (blank lines are ignored);

Output defaults to 'contents.bmk'.


One liner, provided the contents is written in 'contents.txt':
> from contents import Contents
>  Contents().write4PDFTK()


# Use of output contents file

## DJVU files

Use the two following commands:

> djvused -e print-outline book.djvu
> djvused -s -e 'set-outline contents.bmk' book.djvu


## PDF files

First, get the metadata of the PDF file:
> pdftk file.pdf dump_data > metadata.txt

Then, modify the metadata file by including contents.bmk after the line containing
the keyword "NumberOfPages:".

Finally, updade the PDf metadata:
> pdftk file.pdf update_info metadata.txt output newfile.pdf



Created on Thu Aug 20 13:20:10 2020

@author: dbrizard
"""

import os
import subprocess as sbp
import glob

import warnings



class Contents(object):
    """
    
    """
    
    def __init__(self, fname='contents.txt', pagesep=' ', indent=' ', debug=False):
        """
        
        :param str fname: file name
        :param str pagesep: page number separator
        :param str indent: indentation (level) separator
        :param bool debug: print lines for debugging purpose
        """
        
        with open(fname, 'r') as f:
            text = f.readlines()
        
        self.text = text # [xx.strip() for xx in text]
        self.pagesep = pagesep
        self.indent = indent
        
        
        self.detectOffsetOpen()
        self.treatLines(debug=debug)
    
    
    def detectOffsetOpen(self):
        """Automatic detection of page number offset, written as first line.
        Also scans first line for 'open' or 'close' keyword for bookmarks
        
        Warning: 'close' option must be BEFORE 'offset' option
        
        """
        fline = self.text[0]
        if "open" in fline.lower():
            self.Open = True
            print("Open bookmarks option detected in first line.")
            fline = fline.replace("open", "")
        elif "close" in fline.lower():
            self.Open = False
            print("Close bookmarks option detected in first line.")
            fline = fline.replace("close","")
            
        if "offset" in fline:
            # remove trailing \n
            fline.rstrip()
            ind = fline.rfind(self.pagesep)
            self.offset = int( fline[ind+len(self.pagesep):] )
            print("Offset detected in first line: %i"%self.offset)

        else:
            self.offset = None
            
        if hasattr(self, "Open") or "offset" in fline.lower():
            # remove offset line
            self.text.pop(0)            
    
    
    def arbitrateOffset(self, offset):
        """
        
        :param int offset: offset given while calling write4XXX method
        """
        if offset is None and self.offset is not None:
            final_offset = self.offset
        elif offset is not None and self.offset is None:
            final_offset = offset
        elif offset is not None and self.offset is not None:
            final_offset = self.offset
        elif offset is None and self.offset is None:
            final_offset = 0
        
        return final_offset        
    
    
    def treatLines(self, debug=False):
        """Read each line and get title, level (indentation) and page number
        
        :param bool debug: print lines for debugging purpose
        """
        level = []
        title = []
        page = []
        for ll in self.text:
            #---Remove trailing \n---
            lll = ll.rstrip()
            if debug:
                print(lll)
                
            if not len(lll)==0:
                #---Count number of leading sep---
                ni = len(lll) - len(lll.lstrip(self.indent))
                
                #---Get page number---
                ind = lll.rfind(self.pagesep)
                pagenumb = lll[ind+len(self.pagesep):]
                
                #---Get title---
                ttl = lll[:ind]

                nonumber = False
                try:
                    page.append(int(pagenumb))
                    fail = True
                except ValueError:
                    print("No page number: %s"%lll)
                    nonumber = True
                
                if not nonumber:
                    level.append(ni+1)
                    title.append(ttl.strip())
        
        self.level = level
        self.page = page
        self.title = title
    
    
    def write4PDFTK(self, fname='contents.bmk', offset=0):
        """
        
        :param str fname: output filename
        :param int offset: page number offset
        """
        offset = self.arbitrateOffset(offset)
        with open(fname, 'w') as f:
            for tt, ll, pp in zip(self.title, self.level, self.page):
                pp = pp + offset
                f.write('BookmarkBegin\n')
                f.write('BookmarkTitle: %s\n'%tt)
                f.write('BookmarkLevel: %i\n'%ll)
                f.write('BookmarkPageNumber: %i\n'%pp)
    
    
    def write4CPDF(self, fname='contents.bmk', offset=0, Open=True):
        """
        
        :param str fname: output filename
        :param int offset: page number offset
        :param bool Open: children visible or not when pdf file loaded.
        """
        if hasattr(self, "Open"):
            Open = self.Open
            
        offset = self.arbitrateOffset(offset)
        with open(fname, 'w') as f:
            for tt, ll, pp in zip(self.title, self.level, self.page):
                pp = pp + offset
                if '"' in tt:
                    print('/!\ found illegal " character in string in:')
                    print(tt)                    
                if Open:
                    line = '%i "%s" %i open\n'%(ll-1, tt, pp)
                else:
                    line = '%i "%s" %i\n'%(ll-1, tt, pp)
                f.write(line)
            
    
    def write4DJVU(self, fname='contents.bmk', offset=0):
        """
        
        :param str fname: output filename
        :param int offset: page number offset
        """
        offset = self.arbitrateOffset(offset)
        n = len(self.title)
        with open(fname, 'w') as f:
            f.write('(bookmarks\n')
            for ii, (tt, ll, pp) in enumerate(zip(self.title, self.level, self.page)):
                pp = pp + offset
                if ii<n-1:
                    if self.level[ii+1]==self.level[ii]:
                        # next is the same level
                        f.write('("%s" "#%i")\n'%(tt, pp))
                    elif self.level[ii+1]>self.level[ii]:
                        # there will be sublevels, keep parenthesis open
                        f.write('("%s" "#%i"\n'%(tt, pp))
                    elif self.level[ii+1]<self.level[ii]:
                        # no more sublevels, close parentheses
                        n_close = self.level[ii]-self.level[ii+1] +1
                        f.write('("%s" "#%i"'%(tt, pp)+' )'*n_close +'\n')
                else:
                    n_close = ll + 1
                    f.write('("%s" "#%i"'%(tt, pp)+' )'*n_close +'\n')


        
def addPDFtoc(pdffile=None):
    """
    
    """
    warnings.warn("This is not working yet..")
    #---GET PDF FILE---
    if pdffile is None:
        pdflist = glob.glob("*.pdf")
        if not len(pdflist)==0:
            if len(pdflist)>1:
                print("Several PDF files...")
                print(pdflist)
            pdffile = pdflist[0]
            print() 
        else:
            print("/!\ no pdf files in the folder...")
            
    
    #---GET META DATA---
    sbp.call(['pdftk %s dump_data meta.txt'%pdffile])
    
    #---SUPPOSE CONTENTS.BMK IS HERE---
    Contents().writePDFcontents()
    with open("contents.bmk") as f:
        cont = f.read()
    
    #---MODIFY META.TXT---
    with open('meta.txt', 'r') as f:
        meta = f.readlines()
    
    # find line with "NumberOfPages"
    for ii, ll in enumerate(meta[:20]):
        if 'NumberOfPages' in ll:
            ind = ii
    
    # write new meta.txt file
    meta.insert(ind, cont)
    meta2 = "".join(meta)
    # https://stackoverflow.com/questions/10507230/insert-line-at-middle-of-file-with-python
    with open("meta2.txt", 'r') as f:
        f.write(meta2)
    
    #---ADD CONTENTS TO PDF FILE---
    sbp.call(['pdftk', pdffile, 'update_info meta2.txt output test.pdf'])
        
    
        
    

if __name__=='__main__':
    #%% TEST CONTENTS
    C = Contents('contents.txt', debug=True)
    C.write4CPDF('cont_cpdf.bmk')
    C.write4PDFTK('cont_pdftk.bmk')
    C.write4DJVU('cont_djvu.bmk')
    

    
    #%%TEST ADDPDFTOC---
    if False:
        print("TTTTTTTTTTTTTT")
        addPDFtoc() # XXX not finished at all
    
