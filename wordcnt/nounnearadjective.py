import string
import re
import argparse
import signal
import sys
from util import clean , baseargs , opentext , ctrlc , incr

# deal with ctrl-c cleanly
signal.signal(signal.SIGINT,ctrlc)

# make sure we have nltk installed before doing anything else
try:
    import nltk
except ImportError:
    print "looking for adjectives near nouns requires that you install nltk"
    exit(1)

# check if a string is an English noun
def noun (string):
    tag = nltk.pos_tag([string])
    if not(tag[0][1] == 'NN' or tag[0][1] == 'NNP'):
        msg = "%r is not a noun according to nltk" % string
        raise argparse.ArgumentTypeError(msg)
    return string

# describe and parse arguments from the command line
parser = argparse.ArgumentParser(description="Count the number of times a "
                                 + "noun appears after an adjective in a "
                                 + "corpus of English text.")
baseargs(parser)
parser.add_argument("noun", help="the noun for which to search", type=noun)
args = parser.parse_args()

## todo: how many times am i actually traversing this in each of the four
## different arg cases?

txtsrc = opentext (args.pdf, args.gutenberg, args.filename)

# dump the corpus into a string so nltk can tokenize it
corpus = ""
for line in txtsrc:
    corpus = corpus + (line.lower())
if not (args.pdf or args.gutenberg):
    txtsrc.close()

if args.verbose:
    print "read in text"

# tokenizing and making a context index are fairly cheap; tagging is
# expensive. we build the index first, then only tag words that are near
# the target noun, keeping track of those that are adjectives (marked with
# JJ).
ctxid = nltk.text.ContextIndex(nltk.word_tokenize(corpus))

if args.verbose:
    print "created context index"

## todo: make incr take an optional predicate argument that defaults to
## \_.true

# given a pair (w,t), if t is JJ, increment d[w]
def incr_if_jj(d, word):
    tagged = nltk.pos_tag([word])
    if tagged[0][1] == "JJ":
        incr (tagged[0][0], d)

common = ctxid.common_contexts([args.noun.lower()])
if args.verbose:
    print "created common contexts"

d = dict()
# todo: filter out "*START*" , "*END*"? or will nltk treat those like
# sentinels

# this can take a long time for big texts, just because tagging is hard.
if args.verbose:
    sys.stdout.write("tagging contexts")
    sys.stdout.flush()

for x , y in ctxid.common_contexts([args.noun.lower()]):
    if args.verbose:
        sys.stdout.write(".")
        sys.stdout.flush()
    incr_if_jj (d , x)
    incr_if_jj (d , y)
if args.verbose:
    print

sum = 0
for k , v in d.items():
    sum += v

if args.verbose:
    print d
    print 'total number of occurances: ' + str(sum)
else:
    print sum



# question says "how often does alice appear on either side of an
# adjective". i'm going to interpret that to mean "how many times does
# .. ". the other interpretation is "what percentage of times that a noun
# appears on either side of an adjective is that noun alice?" which is a
# different task. maybe write another script to do that, but that thing is
# going to take a super long time to run. this is bad enough, even only
# needing to tag some words; to do that you need to tag every single word
# in the text and then post-process the list. the post-processing is
# linear; the tagging is not.
