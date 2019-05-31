import argparse
import logging
import os
import sys
import time
import pickle

import pandas as pd

import web_scraper
from word_mapper import WordMapper
import word_chainer

root = os.getcwd()
logging.basicConfig(format="[%(asctime)s] %(message)s",
                    datefmt="%d.%m.%Y %H:%M:%S",
                    level=logging.INFO)

parser = argparse.ArgumentParser(description="********** Markov Chain Pipeline in Python **********",
                                 prog="markov.py",
                                 usage="\nmarkov.py [scrape]"
                                       "\nmarkov.py [scan] [-o OUT]"
                                       "\nmarkov.py [chain] [-i IN] [-w WORD]")

parser.add_argument('mode', default="scan", help="script running mode [scrape, scan, chain]", type=str)
parser.add_argument('-o', '--output', default="mappings.pkl", help="mapping file's name to write", type=str)
parser.add_argument('-i', '--input', default="mappings.pkl", help="mapping file's name to read", type=str)
parser.add_argument('-w', '--word', default=10, help="how many words to chain", type=int)
parser.add_argument("-v, --version", action="version", version="%(prog)s 0.2")
args = parser.parse_args()


def main():
    if args.mode == "scan":
        if "books.csv" not in os.listdir(root) or "books" not in os.listdir(root):
            sys.exit("\nThere is no data to scan. Run the script with scrape mode first.")
        else:
            try:
                start = time.time()
                mapper = WordMapper()  # Creating the WordMapper object loads every word in the disk to ram.
                end = time.time()
                logging.info("{} words are loaded into memory in {} seconds.".format(mapper.word_count(),
                                                                                     (end - start)))

                mapper.map_words()  # This will create mappings for every word.
                prefixes, suffixes = WordMapper.stats()
                logging.info("{} words are mapped to {} suffixes.".format(prefixes, suffixes))

                os.chdir("..")
                with open(args.output, "wb") as output:
                    pickle.dump(mapper.word_mappings, output, pickle.HIGHEST_PROTOCOL)  # Saving the mappings.

                logging.info("Mappings written to {} in {}.".format(args.output, os.getcwd()))
            except KeyboardInterrupt:
                sys.exit(logging.error("Exiting current process."))

    elif args.mode == "scrape":
        if "books.csv" not in os.listdir(root):  # If books.csv doesn't exist, creating it first.
            logging.info("Writing books.csv ")
            top_book_urls = web_scraper.scrape()  # Getting the list of urls.
            df = web_scraper.to_df(top_book_urls)  # Adding them to df.
            web_scraper.save(df)  # Saving df to csv.
        else:  # If books.csv exists, but books directory doesn't exist.
            df_books = pd.read_csv("books.csv")

            if not os.path.exists(web_scraper.BOOKS_DIR):  # Creating the directory, if it doesn't exist.
                os.makedirs(web_scraper.BOOKS_DIR)

            count = 0
            for i in df_books.index:  # Iterating the .csv file and writing books to disk.
                if df_books.iloc[i, 0] + ".txt" in os.listdir(web_scraper.BOOKS_DIR):
                    logging.error("{} is already written to the disk.".format(df_books.iloc[i, 0]))
                else:
                    try:
                        try:
                            web_scraper.write_book(df_books.iloc[i, 1], df_books.iloc[i, 0])
                            count += 1
                        except TypeError:
                            logging.error("Unable to write {} to the disk.\n".format(df_books.iloc[i, 0]))
                    except KeyboardInterrupt:
                        logging.info("{} books written to the disk in the current process.\n".format(count))
                        sys.exit(logging.error("There are {} books in the disk.\n".
                                               format(sum(1 for _ in os.listdir(web_scraper.BOOKS_DIR)))))

    elif args.mode == "chain":
        try:
            with open(args.input, "rb") as input_file:
                mapping = pickle.load(input_file)
                chain = word_chainer.chain_words(mapping, args.word)
                print(chain)
        except FileNotFoundError:
            sys.exit(logging.error("File {} is not found in {}.".format(args.input, os.getcwd())))


if __name__ == "__main__":
    main()
