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

# check if a string is an English noun
def noun (string):
    #TODO: use nltk here
    return string

# adds basic arguments to an argparser
def baseargs (p):
    p.add_argument("filename",
                    help="path to the file with the corpus to analyze. " +
                         "by default, assumed to be plain text.",
                    type=fexists)
    p.add_argument("-p" , "--pdf",
                    help="treat the file as PDF rather than plain text. the " +
                         "results may be different depending on the quality " +
                         "of the PDF. default is false. requires the package" +
                         " pdfrw.",
                    action="store_true",
                    default=False)
    p.add_argument("-g", "--gutenberg",
                    help="indicates that the file came from Project Gutenberg"+
                         ", in which case we ignore their header and footer."+
                         " this will only work when combined with the PDF " +
                         "option if we get a good parse. default is off.",
                    action="store_true",
                    default=False)

# this is https://gist.github.com/jmcarp/7105045. the standard docs for
# how to use pdfminer give an example of how to use it, but it's slightly
# busted. this is what the internet seems to have settled on for how to
# interpret that example into code that actually does something.

def pdf_to_text(pdfname):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams

    from cStringIO import StringIO

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = file(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text
