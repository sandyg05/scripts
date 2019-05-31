import logging
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
import os


BOOKS_DIR = os.path.join(os.getcwd(), "books")
BASE_URL = "https://www.gutenberg.org/browse/scores/top"

logging.basicConfig(format="[%(asctime)s] %(message)s",
                    datefmt="%d.%m.%Y %H:%M:%S",
                    level=logging.DEBUG)


def scrape_letter():
    pass
    # TODO Function which scrapes english books from the given letter.


def parse_page(url):
    """
    Returns a list of ols in the given url.
    :param url: The base URL of top 100 books.
    :return: Every single ol in the page.
    """
    html = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    logging.debug("Parsing the URL {} ".format(url))
    return soup.find_all("ol")


def get_book_links(books_lists):
    """
    Returns a list of URLs extracted from the ols without duplicates.
    :param books_lists: List of ols in the page.
    :return: List of tuple pairs of book names and urls.
    """
    ol_urls = []

    for ol in books_lists:
        books = ol.find_all("li")
        # Getting the a.text and hrefs of every book for storing.
        book_urls = [(book.a.text, "https://www.gutenberg.org" + book.a.get("href"))
                     for book in books
                     if book.a.get("href").startswith("/ebooks")]
        ol_urls.extend(book_urls)

    logging.debug("{} book links (with duplicates) are extracted from the URL {} ".format(len(set(ol_urls)), BASE_URL))

    return ol_urls


def scrape():
    """
    Automates the url extraction process.
    :return: The list of book names and their URLs in tuples.
    """
    books_lists = parse_page(BASE_URL)
    urls = get_book_links(books_lists)

    return sorted(urls)


def to_df(urls):
    """
    Creates a pandas dataframe from the books and urls pairs.
    :param urls: List of book, url pairs.
    :return: Books and urls in a dataframe.
    """

    columns = ["book", "url"]
    df_books = pd.DataFrame(columns=columns)

    df_books["book"] = [url[0] for url in urls]
    df_books["url"] = [url[1] for url in urls]

    df_books.drop_duplicates(subset="url", inplace=True)
    df_books.reset_index(drop=True, inplace=True)
    df_books["book"] = df_books["book"].apply(lambda s: s[:s.rfind("(")])  # Cutting the number at the end

    logging.debug("{} unique books are loaded to the dataframe.".format(df_books.shape[0]))
    return df_books


def save(df):
    """
    Creates a .csv file in the current directory from the given books dataframe.
    :param df: Pandas dataframe with books and their URLs.
    """
    df.to_csv("books.csv", index=False)
    logging.debug("{} saved to the current directory.".format("books.csv"))


def open_book(book_url):
    """
    Opens the book and returns Plain Text UTF-8 form from the given URL.
    :param book_url: URL of a book.
    :return: Plain Text UTF-8 form of the book.
    """

    book_html = urlopen(book_url)
    book_soup = BeautifulSoup(book_html, "html.parser")

    book_plain_text_url = [link.get("href").strip("/")
                           for link in book_soup.find_all("a", href=True)
                           if link.text == "Plain Text UTF-8"]

    if book_plain_text_url:
        logging.debug("Opening {} ".format(book_soup.find("title").text.strip(" - Free Ebook")))
        text = urlopen("https://" + book_plain_text_url[0]).read().decode("utf-8")
        return text
    else:
        return None


def write_book(book_url, book_name):
    """
    Writing the plain text of book to the disk.
    :param book_url: URL of a book.
    :param book_name: Name of the book.
    """
    book_text = open_book(book_url)
    book_path = os.path.join(BOOKS_DIR, book_name)

    with open(book_path + ".txt", mode="w", encoding="utf-8") as f:
        logging.debug("Writing {} to the disk.\n".format(book_name))
        f.write(book_text)
