## CASAFARI Python Developer Assessment Task 1

### Requirements

* [**Python 3.7**](https://www.python.org/downloads/)

* [**SQLite**](https://www.sqlite.org/index.html) is for storing the urls.

* [**Visual C++ Build Tools**](https://visualstudio.microsoft.com/visual-cpp-build-tools/) is for reppy because it is not pure Python.

### Packages

Use pip or any package manager to get those packages.

* sqlite3

* bs4

* requests

* reppy (needs C++ build tools for compiling)

### Usage

You can run main.py from command line with a url argument. If you don't pass the url argument, it will start from https://www.debenhams.com.

It creates an .sqlite file in the current working directory and stores the urls in that database.

The script sends a request to the initial url and collects the links. After collecting the links, the script creates a robots.txt parser and checks the collected links are allowed for scraping. If they are allowed for scraping, stores them in the database.

Repeats the process for every 2 seconds for the stored links until user quits or there are no links left.

If you want to start a new crawling process of another website, delete or rename the .sqlite file.