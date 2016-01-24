# take a file and figure out the four most used words.
import sys
# import nltk
import re
import string
from collections import OrderedDict

## import argparse ## TODO use this to make argument parsing cleaner once
                   ## you get the NLTK stuff worked out

## this function takes a word and gives a canonical syntax for it--so
## removes punctionation, normalizes case, etc.
##
## TODO: looking at the contents of the keyset this generates this is
## probably harder than i think; i bet nltk has a function to do it.
def clean (s):
    ## ignore strings containing at least one digit or URL artifacts
    digits = re.compile('.*\d+.*|http')
    if (digits.match(s)):
        return None
    else :
        # otherwise, remove punctuation except hyphens  and normalize case
        s = s.translate(None, string.punctuation.replace("-", ""))
        s = s.lower()
        return s

if len (sys.argv) == 1 :
    ## currently assuming that we get exactly one arg, which is a path to
    ## the corpus file
    print 'please provide one argument, a path to the file that you want to traverse'
else:
    try:
        f = open(sys.argv[1], 'r')
        d = dict()
        for line in f:
            ## get rid of ASCII em and en dashes
            line = (line.replace("---", " ")).replace("--", " ")

            for word in line.split():
                clean_word = clean(word)
                if clean_word == None:
                    #ignore words that don't parse
                    continue
                else:
                    # add or update words that do parse
                    if clean_word in d:
                        d[clean_word] += 1
                    else:
                        d[clean_word] = 1

        # all the interesting data is in the dict now, so free this up
        f.close()

        # for k, v in d.items():
        #     print k, '|->', v
        # print 'unique words: ', len(d)

        # sort the dictionary by value in the standard way
        od = OrderedDict(sorted(d.items(), reverse=True, key=lambda t: t[1]))
        print "the four most used words are: "
        for k , v in (od.items())[:4]:
            print '\t"' + k + '", which was used ' + (str(v)) + ' times'


    except IOError:
        print 'Please supply a path to a real file'
