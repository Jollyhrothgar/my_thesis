#!/usr/bin/env python

import argparse
import sys
import re
from subprocess import call

# This will never change, so no need to keep it as a free
# parameter.
THESIS_NAME = 'thesis.tex'
def load_thesis(filename):
    '''
    Loads thesis into an array one line at a time.
    Returns handle pointing to the array.
    '''
    thesis_lines = []
    with open(filename,'r') as f:
        thesis_lines = f.readlines()
    print THESIS_NAME,'had',len(thesis_lines),'lines'
    return thesis_lines


def main():
    parser = argparse.ArgumentParser(description="Compile Single or Multiple Chapters of my thesis")
    parser.add_argument("--clean",help="execute make clean before build",action="store_true")
    parser.add_argument("-d","--draft",help="add to compile in draft mode", action="store_true")
    parser.add_argument("-c","--chapter",nargs="*",help="The chapter number(s) you want to build, separated by a space")
    parser.add_argument("--nobuild",help="do not execute the build",action="store_true")
    args = parser.parse_args()
    
    build_whole_thesis = False
    chapters = args.chapter
    # if not called, chapters is None
    if not chapters:
        build_whole_thesis = True
    # chapters invoked, but not defined, length is zero
    elif len(chapters) == 0:
        build_whole_thesis = True
    # we have a defined array with chapter numbers
    else:
        build_whole_thesis = False

    # Convert any chapters to produce to numbers
    chap_keep_nums = []
    if not build_whole_thesis:
        for ch in chapters:
            chap_keep_nums.append(int(ch))

    thesis_lines = load_thesis(THESIS_NAME)
    output_thesis = []
    for line in thesis_lines:
        line = line.rstrip("\n");
        matches = re.search(r"(%\s*)?(\\input\{\s*(\d+)_\S+\.tex\s*\})",line)
        skip = re.search(r"\\chapter\{Chapter \d\}",line)
        if skip:
            continue
        out_line = line
        if matches:
            chapter_keep = int(matches.group(3))
            if build_whole_thesis and matches.group(1) == '%':
                out_line = line[1:]
                output_thesis.append(out_line)
                continue
            elif not build_whole_thesis:
                if chapter_keep not in chap_keep_nums and matches.group(1) != '%':
                    out_line = "%"+line;
                    print out_line
                    output_thesis.append(out_line)
                    place_holder = "\chapter{Chapter %s}"%chapter_keep
                    output_thesis.append(place_holder)
                    continue
                elif chapter_keep not in chap_keep_nums and matches.group(1) == '%':
                    output_thesis.append(out_line)
                    place_holder = "\chapter{Chapter %s}"%chapter_keep
                    output_thesis.append(place_holder)
                    continue

                if chapter_keep in chap_keep_nums and matches.group(1) == '%':
                    out_line = line[1:]
                    print out_line
                    output_thesis.append(out_line)
                    continue
        output_thesis.append(out_line)
    with open('thesis.tex','w') as out_file:
        for line in output_thesis:
            out_file.write("%s\n"%line)

    if args.clean:
        call(["make","clean"])
    if args.nobuild:
        return 0
    if args.draft:
        call(["make","draft"])
        return 0
    else:
        call(["make"])
        return 0
    
    return 0
if __name__ == '__main__':
    sys.exit(main())

