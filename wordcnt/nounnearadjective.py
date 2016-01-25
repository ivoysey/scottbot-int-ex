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
baseargs(parser, "nicer output if you have progressbar installed.")
parser.add_argument("noun", help="the noun for which to search", type=noun)
args = parser.parse_args()

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
# the target noun, keeping track of those that are adjectives
ctxid = nltk.text.ContextIndex(nltk.word_tokenize(corpus))

if args.verbose:
    print "created context index"

common = ctxid.common_contexts([args.noun.lower()])
if args.verbose:
    print "created common contexts"

# this can take a long time, i think just because tagging is hard.
iterob = ctxid.common_contexts([args.noun.lower()])
if args.verbose:
    print "tagging contexts"
    try:
        import progressbar
        bar = progressbar.ProgressBar(widgets=[progressbar.Bar(),
                                           ' (', progressbar.ETA(), ') ',])
        iterob = bar(iterob)
    except ImportError:
        pass

start = re.compile('START')
end = re.compile('END')

# given a pair (w,t), if t is JJ, increment d[w]
def incr_if_jj(d, word):
    # skip the tags that nltk introduces for position in a context
    if( not(start.search(word) or end.search(word))):
        tagged = nltk.pos_tag([word])
        if tagged[0][1] == "JJ":
            incr (tagged[0][0], d)

# tag everything and mark down when it's an adjective in a dictionary
d = dict()
for x , y in iterob:
    incr_if_jj (d , x)
    incr_if_jj (d , y)

# compute the number of occurances and print it out, with more information
# if verbose is set
if args.verbose:
    print d
    sys.stdout.write('total number of occurances: ')
print (sum(d.values()))
