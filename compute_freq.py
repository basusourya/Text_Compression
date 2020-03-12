# -*- coding: utf-8 -*-

import string      # definitions of ascii printable chars
from collections import defaultdict     # fast counting

d = defaultdict(int)    # define dictionary for counting frequencies

#inp = input("Enter a sentence: ")
f = open("book1.txt", "r")
text = f.read()

# define text - see below for how to download from a url
#text = '''Lorem ipsum dolor sit amet,\tconsectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''

for ch in text:       # loop over each character 
    if ch in string.printable:     # is the character in the ascii/printable set?
        d[ch] += 1    #   if so, add 1 to that characters frequency counter

print(d)     

# print all frequencies; for key in d: d[key] gives the freq number
