#### This is a markov chain pipeline implementation used on Project Gutenberg books. ####

* web_scraper.py scrapes books from https://www.gutenberg.org/browse/scores/top and writes them to disk, until KeyboardInterrupt or there is no book left.

* scanner.py generates words from every book in the disk.

* word_mapper.py has a singleton. The singleton instance stores generated words in memory then creates the markov model.

* word_chainer.py randomly chains words from the created model.

* markov.py controls the pipeline.


  





