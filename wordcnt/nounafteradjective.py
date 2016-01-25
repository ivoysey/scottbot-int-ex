import sys
import os
import re
import string
import argparse
import itertools

from util import clean , fexists

## describe and parse arguments from the command line
parser = argparse.ArgumentParser(description="Count the number of times a "
                                 + "noun appears after an adjective in a "
                                 + "corpus of English text.")
parser.add_argument("filename",
                    help="path to the file with the corpus to analyze. " +
                         "by default, assumed to be plain text.",
                    type=fexists)
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
