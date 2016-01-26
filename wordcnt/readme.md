To use all the features of both scripts, one needs to install the following
python packages that aren't in the standard library, probably via *pip
install*. Both scripts provide some functionality or fail gracefully when
different things aren't present, though.
* progressbar
* nltk
* pdfminer


This directory contains my solutions for the two tasks involving processing
the text of "Alice in Wonderland". The files included are described below:

* **algo-toys/**

  some code in other languages that i wrote while thinking about the
  problems to figure out how i wanted to solve them. it's basically scratch
  work. nothing in here should be assumed to be correct or even to compile.

* **input/**

  the inputs from project gutenberg stored locally, both in plain text and
  PDF, and a text that i used for debugging both scripts.

* **answers.md**

  the answers to the specific concrete questions stated in the description.

* **assumptions.md**

  discussion of some of the assumptions i made in the process of
  implementing solutions to the given tasks, and some observations after
  solving them.

* **descr.txt**

  description of the tasks, from email conversation with scott


* **mostused.py**

  script that takes a text, possibly pdf and possibly from gutenberg, and
  computes the n most-used words in the text.

  help message provides details about interaction.

* **nounnearadjective.py**

  script that takes a text, possibly pdf and possibly from gutenberg, and a
  noun and computes the number of times that noun appears adjacent to an
  adjective.

  help message provides details about interaction.

* **readme.md**

  this file, which describes the other files

* **resources.md**

  a description of websites and other things that i read in the process of
  writing the two scripts to solve the tasks presented.


* **util.py**

  code that's used by both scripts, factored out into a utilities
  file. each function is documented interally and imported as needed in
  either place.
