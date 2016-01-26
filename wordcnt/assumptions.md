most used words
===============

the task statement leaves a few questions unanswered. in order to get a
well-defined program, i've made a few assumptions.

 - "words" should be treated modulo things like punctuation and
   capitalization. so "QUEEN" and "queen" and "Queen!" should all be
   treated as the same word appearing in different contexts.

   words that are hyphenated, like "jury-box", are perfectly good words by
   themselves. so that word appears once in the Alice text and doesn't
   increase the counts for the words "jury" or "box"

   words that have more than one hyphen glyph between them are different
   words, because it's the standard ASCII-ification of em and en dashes. so
   "he gamboled---that is to say walked--in" produces eight distinct words
   not six.

   non-sense words to write down sounds people make that maybe aren't
   language, like "PLEUGH!" for spitting, but might not appear in a
   dictionary are fine words for this question.

 - "alice in wonderland" refers to the actual text of the book, not the
   metatext of a particular printing, such as copyright statements, project
   gutenburg text, tables of contents, or chapter headings. so that means
   that any operations on "alice in wonderland" shouldn't take into account
   the

 - it's not clear if the version of the text is specifically the project
   gutenburg edition, or even more specifically the PDF of the project
   gutenburg edition. the latter introduces some new complications, because
   you have to use some tool to extract the strings from the PDF as strings
   in data before doing anything with it.

   i'm actually curious to see how either choice effects the set of words
   you get out. my guess is that it won't effect the four that appear the
   largest number of times, but it will change the lower-frequency ones
   somewhat.

   the tool to convert PDF to txt is also an interesting choice. pdftotext
   is the standard unix tool; languages may have built-in ones that provide
   a more portable program

 - there's a little bit of non-determinism in the words that you output. it
   might be the case that the 20 most used words are all used exactly 5
   times, for example, so if you're computing the four most used words
   which ones do you pick? this is the maximal-but-not-maximum problem.

   in this case, i give no guarantees


after working through the solution, here are some thoughts about the answer:

 - looking at the results, for alice, you get stuff like "the", "and", "to"
   and "a". it' be easy programmatically to remove a list of words from the
   results to get only "interesting words" and take something on the
   command line to swap in different ignore lists or similar.

 - it's pretty hard to curate a list of things to ignore; that's a big
   design decision that i'm not sure how i would make and would want to
   talk to people with. really depends on what the tool would be used
   for.

 - apostophies also end up being oddly semantic to figure out if you can
   remove them. so "''tis" should normalize to "'tis" probably because it's
   a front-contraction at the beginning of a nested quote. but "'where's"
   and "i'm" all get non-deterministic fast. instead, we just normalize out
   all apostrophies.

 - in general, i think NLTK is too big a hammer for the "most frequently
   used words" task.

   it does have a built-in function FreqDist which answers exactly the
   question posed, and the sample code for that is in chapter 1 of the NLTK
   book. but. for this application i think it's over kill. you still need
   to filter out the words that have punctuation in them and clean up the
   output, so you don't save that much programming effort.

   it takes a long time, too. i did a little profiling of this, and my
   solutions about ten times faster. just loading the nltk module takes a
   long time.

   i'm fairly sure that they're investing the time to sort the entire
   dictionary of unique words and counts; that makes sense if you expect to
   make a lot of queries against it for different things over a long
   running program, but doesn't make as much sense for just one query of a
   fixed sized. this is a hard design decision to make, though, and it's
   possible that the better choice would be to stick with something that's
   simpler to write and less hand-rolled even though it's slower.


"alice" near adjectives
=======================

similarly, i made some assumptions about this question statement:

 - the uestion says "how often does alice appear on either side of an
   adjective". i'm going to interpret that to mean "how many times does
   .. ".

   the other reasonable interpretation is "what percentage of times that a
   noun appears on either side of an adjective is that noun alice?" which
   is a very different task that's a lot more computationally intensive,
   because tagging is hard. this is bad enough, even only needing to tag
   some words; to do that you need to tag every single word in the text and
   then post-process the list. the post-processing is linear; the tagging
   is not.

 - nltk is absolutely the right tool here; i have no idea how to do POS
   tagging and you can't get around it to complete this task, so it's well
   worth the overhead.
