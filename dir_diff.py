#!/usr/bin/env python3

import sys
import os

def dir_listing(dir: str):
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path(dir)) for f in fn]

print("Comparing the two directories...")
file_lists = []
if len(sys.argv) != 3:
    print("Prints all files in directory 1 that aren't in directory 2")
    print("usage: dir_diff.py dir1 dir2")
    exit()

file_lists.append(os.listdir(sys.argv[1]))
file_lists.append(os.listdir(sys.argv[2]))

missing_files = set(file_lists[0]) - set(file_lists[1])

for f in missing_files:
    print("In %s and not in %s: %s " % (sys.argv[1], sys.argv[2], f))

if len(missing_files) == 0:
    print("No files are in %s and not in %s" % (sys.argv[1], sys.argv[2]))


