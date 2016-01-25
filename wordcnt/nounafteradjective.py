import string
import argparse

from util import clean , noun , baseargs

## describe and parse arguments from the command line
parser = argparse.ArgumentParser(description="Count the number of times a "
                                 + "noun appears after an adjective in a "
                                 + "corpus of English text.")
baseargs (parser)
parser.add_argument("noun", help="the noun for which to search", type=noun)
args = parser.parse_args()
