import core
import db_manager as dm


def init_database(db_name):
    database = dm.CrawlerDatabase(db_name)
    return database


def crawl(database, start_url):
    core.crawl(database, start_url)
    database.show_stats()


def rank(database):
    database.rank_pages()
    database.show_stats()


def run():
    starting_page = input("Which page do you want crawl? ")
    db = init_database("crawl_db")
    crawl(db, starting_page)
    rank(db)


if __name__ == "__main__":
    run()
