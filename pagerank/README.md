#### This is a simple single threaded web crawler implementation in Python and SQLite. ####

* db_manager handles the database operations and the page ranking algorithm.

* web_manager handles the HTTP request/response cycle and some URL parsing.

* html_parser handles the HTML code parsing using BeautifulSoup library.

* core is where crawling process is done.

* crawler is the entry point of the program.

------------------------------------------------------------

#### The Flow of Execution: ####

1. Program asks the user for a start URL for crawling.
	* Program has to finish crawling collected links in order to crawl another URL.
	* If new URL is given before finishing collected links, it will continue crawling
	  previous URL anyway.

2. Then, program asks the user how many pages to crawl from that URL.
	* Program has to be restarted in order to end the crawling process.
	* If program finishes crawling given number of URLs, it will ask how
	  many pages to crawl, again.
	* If 0 is given as a number of pages to crawl, it will go to the next step (ranking).
	
  
3. Lastly, program asks the user how many page ranking iterations to execute
   for the crawled pages.     
	* Ranking algorithm computes the average change in the ranks' of pages'.
	* Incomplete crawls won't be ranked.
	* More iterations mean more accurate ranking.
  





