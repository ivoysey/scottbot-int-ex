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
def clean (s):
    ## ignore strings containing at least one digit or URL artifacts
    digits = re.compile('.*\d+.*|http')
    if (digits.match(s)):
        return None
    else :
        # otherwise, remove punctuation except hyphens and normalize case
        s = s.translate(None, string.punctuation.replace("-", ""))
        s = s.lower()
        return s

def incr (word, d):
    if word in d:
        d[word] += 1
    else:
        d[word] = 1

# sort a list of pairs in decreasing order by the second component
def sortpl (l):
    return sorted(l, reverse=True, key=lambda x : x[1])

def biggest (k , items):
    ## abort if the query makes no sense
    if k > len(items):
        raise Exception('trying to compute the ' + str(k) +
                        'most used words, but there are only ' + str(len(d)) +
                        ' unique words in the corpus')

    ## otherwise, grab the first k entries, then traverse the rest of the
    ## items updating as we go to find the biggest k
    so_far = sortpl(items[:k])

    for elem in items[k:]:
        so_far.append(elem)
        so_far = (sortpl(so_far))[:k]

    return so_far

## TODO: this is the number of words i want to find; take it as an
## argument, but it's up here so i don't hard-code it later.
k = 4

if len (sys.argv) == 1 :
    ## currently assuming that we get exactly one arg, which is a path to
    ## the corpus file
    print 'please provide one argument, a path to the file that you want to traverse'
else:
    # open the file from the command line arguments or bail if we can't
    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print 'Please supply a path to a real file'

    # traverse the whole file, adding canonical forms of valid words into a
    # dictionary counting the number of appearances
    d = dict()
    for line in f:
        ## get rid of ASCII em and en dashes before breaking into words, so
        ## each half is its own word
        line = (line.replace("---", " ")).replace("--", " ")

        for word in line.split():
            clean_word = clean(word)
            if clean_word == None:
                #ignore words that don't parse
                continue
            else:
                # add or update words that do parse
                incr(clean_word,d)

    # all the interesting data is in the dict now, so free this up
    f.close()

    ## TODO: finish using this to debug the string parsing stuff
    # for k, v in d.items():
    #     print k, '|->', v
    # print 'unique words: ', len(d)

    # travese the dictionary to find the k most frequently used words, where
    # k is taken on the command line but defaults to four.

    print "the four most-used words are: "
    for key , val in biggest(k,d.items()):
        print ('\t"' + key + '", which was used '
               + (str(val))
               + ' time' + ("" if val == 1 else "s"))
