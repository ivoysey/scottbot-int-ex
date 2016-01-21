# take a file and figure out the four most used words.
import sys
## import nltk
import re

## import argparse ## TODO use this to make argument parsing cleaner once
                   ## you get the NLTK stuff worked out


## this function takes a word and gives a canonical syntax for it--so
## removes punctionation, normalizes case, etc.
##
## TODO: looking at the contents of the keyset this generates this is
## probably harder than i think; i bet nltk has a function to do it.
def clean (s):
    return s.lower()

if len (sys.argv) == 1 :
    ## currently assuming that we get exactly one arg, which is a path to
    ## the corpus file
    print 'please provide one argument, a path to the file that you want to traverse'
else:
    try:
        f = open(sys.argv[1], 'r')
        d = dict()
        for line in f:
            words = line.split()
            for word in words:
                clean_word = clean(word)
                if clean_word in d:
                    d[clean_word] += 1
                else:
                    d[clean_word] = 1
        f.close()
        print d

    except ValueError:
        print 'Please supply integer arguments'
    except IOError:
        print 'Please supply a path to a real file'
