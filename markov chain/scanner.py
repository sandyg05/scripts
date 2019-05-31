import os
from string import punctuation
import logging

logging.basicConfig(format="[%(asctime)s] %(message)s",
                    datefmt="%d.%m.%Y %H:%M:%S",
                    level=logging.DEBUG)


def trim_book(file):
    """
    Cuts the boilerplate header and footer in the books.
    :param file: File form of the book.
    :return: String form of the book without header and footer.
    """
    text = file.read()
    text = text[text.find("*** START OF THIS PROJECT GUTENBERG EBOOK"):text.find("*** END OF THIS PROJECT GUTENBERG "
                                                                                 "EBOOK")]
    return text


def get_words(file):
    """
    Generating words inside the book.
    :param file: File form of the book.
    :return: Words inside the book.
    """
    with open(file, encoding="utf-8") as book_file:
        logging.debug("Generating words from {} ".format(file))
        text = trim_book(book_file)  # Getting rid of header and footer.

    word_count = 0

    for word in text.split():
        word = "".join(char for char in word if char not in punctuation)  # Deleting punctuations
        yield word
        word_count += 1

    logging.debug("{} words extracted from {} ".format(word_count, file))


def scan():
    """
    Generating words from every book in the directory.
    """
    os.chdir("books")

    for book in os.listdir(os.getcwd()):
        yield from get_words(book)  # This line consumes generators one by one and works like a one big generator.
