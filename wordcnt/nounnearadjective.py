import string
import re
import argparse
import signal
import sys
from util import clean , baseargs , opentext , ctrlc

# deal with ctrl-c cleanly
signal.signal(signal.SIGINT,ctrlc)

# make sure we have nltk installed before doing anything else
try:
    import nltk
except ImportError:
    print "looking for adjectives requires that you install nltk"

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
    corpus = corpus + line

if not (args.pdf or args.gutenberg):
    txtsrc.close()

# tokenizing and making a context index are fairly cheap; tagging is
# expensive. we build the index first, then only tag words that are near
# the target noun, keeping track of those that are adjectives (marked with
# JJ)
d = dict()
ctxid = nltk.text.ContextIndex(nltk.word_tokenize(corpus))
for x , y in ctxid.common_contexts([args.noun]):
    print nltk.pos_tag([x,y])
