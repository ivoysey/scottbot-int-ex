import os
import re
import string
import argparse

# takes a word and gives a canonical syntax for it--so removes
# punctionation, normalizes case, etc.
def clean (s):
    # ignore strings containing at least one digit or URL artifacts
    digits = re.compile('.*\d+.*|http')
    if (digits.match(s)):
        return None

    # otherwise, remove punctuation except hyphens
    s = s.translate(None, re.sub("-", '',string.punctuation))

    # if that was everything, abort
    if s == "":
        return None

    # otherwise, return lower case
    return s.lower()

# check if a name points to an existant file
def fexists (string):
    if not (os.path.isfile(string)):
        msg = "%r is not a valid file" % string
        raise argparse.ArgumentTypeError(msg)
    return string
