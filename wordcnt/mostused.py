import re
import argparse
import itertools

from util import clean , baseargs , incr , sortpl , opentext , ctrlc

# deal with ctrl-c cleanly
signal.signal(signal.SIGINT,ctrlc)

# computes the k most-occuring pairs in a list of pairs, where the second
# component is a number. assumes that 0 <= k <= |items|.n
def biggest (k , items):
    ## grab the first k entries, sort them to set up loop invariant
    so_far = sortpl(items[:k])

    # traverse the rest of the items updating as we go
    for elem in items[k:]:
        so_far.append(elem)
        so_far = (sortpl(so_far))[:k]

    return so_far

# check while parsing the arguments that the number given is a nat.
def nat (string) :
    value = int(string)
    if value < 0:
        msg = "%r is not a natural number" % string
        raise argparse.ArgumentTypeError(msg)
    return value

#####################

## describe and parse arguments from the command line
parser = argparse.ArgumentParser(description="Count the n most-used words in" +
                                 "a corpus of English text.")
baseargs (parser)
parser.add_argument("-n" , "--number",
                    help="number of most frequently used words to compute. "
                          + "defaults to 4.",
                    type=nat,
                    default=4)
args = parser.parse_args()
txtsrc = opentext (args.pdf , args.gutenberg , args.filename)

# traverse the whole file, adding canonical forms of valid words into a
# dictionary counting the number of appearances.
d = dict()
for line in txtsrc:
    # get rid of ASCII em and en dashes
    line = (line.replace("---", " ")).replace("--", " ")

    for word in line.split():
        clean_word = clean(word)
        if clean_word == None:
            #ignore words that don't parse
            continue
        else:
            # add or update words that do parse
            incr(clean_word,d)

# if we're not reading from a PDF, we have to close the file handle once
# we're done counting all the words. the other three settings close
# themselves.
if not (args.pdf or args.gutenberg):
    txtsrc.close()

# abort if the query makes no sense. note that we can't check this until we
# build the dictionary: it depends on the number of unique words.
if args.number > len(d):
    raise Exception('trying to compute the ' + str(args.number) +
                    ' most used words, but there are only ' + str(len(d)) +
                    ' unique words in the corpus')

# otherwise compute and print out the answer
print ("the " + str(args.number) + " most-used word" +
       (" is" if args.number == 1 else "s are") +
       ":")
for key , val in biggest(args.number, d.items()):
    print ('\t"' + key + '", which was used '
           + (str(val))
           + ' time' + ("" if val == 1 else "s"))
