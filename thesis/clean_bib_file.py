#!/usr/bin/env python
import os, re, sys
#import argparse
def clean(fileName):
    remove_keys = ['abstract', 'doi', 'isbn', 'mendeley-groups', 'keywords',
    'file', 'issn', 'annote']
    blind_keys = ['url']
    try:
        with open(fileName, 'r') as bibf:
            with open(fileName+'.tmp','w') as cleanf:
                 lines = bibf.readlines()
                 for line in lines:
                     if re.search('author',line):
                         print line
                     if re.search('^'+'|'.join(blind_keys),line):
                         cleanf.write('%%%%' + line)
                     elif not re.search('^'+'|'.join(remove_keys),line):
                         #print line
                         cleanf.write(line)
                 cleanf.close()
                 os.remove(fileName)
                 os.rename(fileName + '.tmp', fileName)
        return 0
    except:
        print 'couldn\'t open',fileName
        return 1

def main():
    args = sys.argv[1:]    
    if len(args) != 1:     
        print 'Supply the script with the *.bib file'
        return 1           
    else:                  
        fileName = args[0]
        print 'cleaning    :',fileName
        return clean(fileName)
                           
if __name__ == '__main__':
    sys.exit(main())       
