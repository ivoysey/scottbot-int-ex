most used words
===============

a little unsurprisingly, the four most used words in this text of "alice in
wonderland", ignoring the project gutenberg headers and footers, are "the",
"and", "to", and "a".

in the text version that gutenberg offers, the counts that back up these
claims are given by

```
iev@leibniz wordcnt % python mostused.py -g input/11.txt
the, 1639
and, 866
to, 725
a, 631
```

the PDF version differs slightly in the counts,

```
iev@leibniz wordcnt % python mostused.py -pg input/11-pdf.pdf
the, 1638
and, 847
to, 721
a, 632
```

but produces the same answers. the variation may be because the texts are
actually slightly different even though p.g. offers them as the same
version, or because it's hard to parse text out of a PDF perfectly and some
things aren't parsing correctly by the library.


"alice" near adjectives
=======================

"alice" appears next to 9 different adjectives in the text. more
interestingly, the adjectives that are used to describe alice are: "poor",
"little", "foolish".

this program takes a lot longer to run, about fifteen minutes on the full
"alice" text depending on other system use, and pretty all the time is
spent in calls to nltk for tagging. here the results don't seem to differ
between parsing out the PDF or using the plain text file, probably because
there are fewer adjectives in the text so there are fewer chances to mess
up parsing them.



processing the text version (with the verbose flag, to get more output than
just "9"):

```
iev@leibniz wordcnt % python ./nounnearadjective.py -gv input/11.txt alice
read in text
created context index
created common contexts
tagging contexts
|#############################################################| (Time: 0:14:58)
{'poor': 5, 'little': 3, 'foolish': 1}
total number of occurances: 9
iev@leibniz wordcnt %
```
and the pdf (again with the verbose flag):
```
iev@leibniz wordcnt % python ./nounnearadjective.py -gpv input/11-pdf.pdf alice
read in text
created context index
created common contexts
tagging contexts
|#############################################################| (Time: 0:14:32)
{'poor': 5, 'little': 3, 'foolish': 1}
total number of occurances: 9
iev@leibniz wordcnt %
```
