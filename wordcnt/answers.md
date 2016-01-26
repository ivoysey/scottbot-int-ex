most used words
===============

a little unsurprisingly, the four most used words in this text of "alice in
wonderland", ignoring the project gutenberg headers and footers, are "the",
"and", "to", and "a".

in the text version that gutenberg offers (11.txt), the counts that back up
these claims are given by

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
