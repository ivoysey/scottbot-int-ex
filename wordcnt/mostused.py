import re
import argparse
import itertools

from util import clean , fexists

# increment a value in a dictionary or set it to 1 if it's not there.
def incr (word, d):
    if word in d:
        d[word] += 1
    else:
        d[word] = 1

# sort a list of pairs in decreasing order by the second component
def sortpl (l):
    return sorted(l, reverse=True, key=lambda x : x[1])

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
parser.add_argument("filename",
                    help="path to the file with the corpus to analyze. " +
                         "by default, assumed to be plain text.",
                    type=fexists)
parser.add_argument("-n" , "--number",
                    help="number of most frequently used words to compute. "
                          + "defaults to 4.",
                    type=nat,
                    default=4)
parser.add_argument("-p" , "--pdf",
                    help="treat the file as PDF rather than plain text. the " +
                         "results may be different depending on the quality " +
                         "of the PDF. default is false. requires the package" +
                         " pdfrw.",
                    action="store_true",
                    default=False)

parser.add_argument("-g", "--gutenberg",
                    help="indicates that the file came from Project Gutenberg"+
                         ", in which case we ignore their header and footer."+
                         " this will only work when combined with the PDF " +
                         "option if we get a good parse. default is off.",
                    action="store_true",
                    default=False)
args = parser.parse_args()

# get the text of the corpus from either a plain text or PDF file
if args.pdf:
    try:
        from util import pdf_to_text
    except ImportError:
        print 'reading from a PDF file requires that you install pdfminer'
        exit(1)
    corpus = (pdf_to_text(args.filename)).split("\n")
else:
    corpus = open(args.filename, 'r')

# optionally ignore project gutenberg headers if you can find them
if args.gutenberg:
    header = re.compile('START\s+OF\s+THIS\s+PROJECT\s+GUTENBERG\s+EBOOK')
    footer = re.compile('END\s+OF\s+THIS\s+PROJECT\s+GUTENBERG\s+EBOOK')

    drop = itertools.dropwhile(lambda x: not(bool(header.search(x))), corpus)
    take = itertools.takewhile(lambda x: not(bool(footer.search(x))), drop)

    ## skip the first line, which still has the header in it
    take.next()

    txtsrc = take
else:
    txtsrc = corpus


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
# we're done counting all the words
if args.pdf == False:
    corpus.close()

# abort if the query makes no sense. note that we can't check this stuff
# until we build the dictionary because it depends on the number of unique
# words.
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
