# take a file and figure out the four most used words.
import sys
import re
import string
import argparse

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


# assume that k makes sense relative to items.
## computes the k most-occuring
# pairs in a list of pairs, where the second component is a number. assumes
# that 0 <= k <= |items|.
def biggest (k , items):
    ## grab the first k entries, then traverse the rest of the items
    ## updating as we go to find the biggest k
    so_far = sortpl(items[:k])

    for elem in items[k:]:
        so_far.append(elem)
        so_far = (sortpl(so_far))[:k]

    return so_far

## check while parsing the arguments that the number given is a nat. zero
## is ok, oddly enough!
def nat (string) :
    value = int(string)
    if value < 0:
        msg = "%r is not a natural number" % string
        raise argparse.ArgumentTypeError(msg)
    return value

#####################

## describe and parse arguments from the command line
parser = argparse.ArgumentParser(description="Count the n most-used words in a corpus of English text")
parser.add_argument("filename", help="path to the plain text file with the corpus to analyze")
parser.add_argument("-n" , "--number",
                    help="number of most frequently used words to compute. defaults to 4.",
                    type=nat,
                    default=4)
parser.add_argument("-p" , "--pdf",
                    help="treat the file as PDF rather than plain text. the results may be different depending on the quality of the PDF. default is false.",
                    action="store_true",
                    default=False)
args = parser.parse_args()

# open the file from the command line arguments or bail if we can't
try:
    f = open(args.filename, 'r')
except IOError:
    print 'Please supply a path to a real file'

if args.pdf == True:
    print "aw crap"
    exit(1)

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

## abort if the query makes no sense. note that we can't check this stuff
## until we build the dictionary, because whether or not the argument
## args.number is sensible depends on the number of unique words.
if args.number > len(d):
    raise Exception('trying to compute the ' + str(args.number) +
                    'most used words, but there are only ' + str(len(d)) +
                    ' unique words in the corpus')

print ("the " + str(args.number) + " most-used word" +
       (" is" if args.number == 1 else "s are") +
       ":")
for key , val in biggest(args.number, d.items()):
    print ('\t"' + key + '", which was used '
           + (str(val))
           + ' time' + ("" if val == 1 else "s"))
