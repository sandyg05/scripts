import requests
import crawler
from database import CrawlerDatabase
import argparse
import time

# Defining the command line args
parser = argparse.ArgumentParser(description="Crawler for assessment",
                                 prog="main.py",
                                 usage="main.py [url]")

parser.add_argument('url', nargs="?", default='https://www.debenhams.com', help="url to start crawling")
args = parser.parse_args()

websites = []
start = args.url
cd = CrawlerDatabase('crawler')


def crawl(crawler_database, start_url):

    crawler_database.connect_db()

    if crawler_database.check_db():
        print("Restarting previous crawl process.")
    else:  # Starting a new crawling process from start_url
        website = start_url

        crawler_database.cursor.execute('INSERT OR IGNORE INTO Websites '
                                        '(url) VALUES ( ? )', (website, ))

        crawler_database.cursor.execute('INSERT OR IGNORE INTO Pages '
                                        '(url) VALUES ( ? )', (start_url, ))

        crawler_database.connection.commit()

    # Getting the current website
    crawler_database.cursor.execute('''SELECT url FROM Websites''')

    for row in crawler_database.cursor:
        websites.append(str(row[0]))

    print(websites)

    crawl_counter = 0

    try:
        while True:  # Crawl Loop

            if crawl_counter < 1:
                crawl_counter = int(input('How many pages do you want to crawl? '))
                if crawl_counter == 0:
                    break

            print("Crawling Iteration:", crawl_counter)
            crawl_counter -= 1

            # Getting a random row where  error is null
            crawler_database.cursor.execute('SELECT id,url FROM Pages WHERE '
                                            'error is NULL ORDER BY RANDOM() LIMIT 1')

            row = crawler_database.cursor.fetchone()

            if row is None:
                print("All pages are scraped.")
                break

            from_id = row[0]
            url = row[1]

            print("Crawling ->", "Page ID =", from_id, "| URL =", url, end=' ')

            crawler_database.cursor.execute('DELETE from Links WHERE from_id=?', (from_id, ))

            try:
                res = requests.get(url)
                status = res.status_code
                if status != 200:
                    print("Error occured while loading the page: {}".format(status))

                    crawler_database.cursor.execute('UPDATE Pages SET error=? WHERE url=?',
                                                    (status, url))

                if 'text/html' not in res.headers['Content-Type']:
                    print("This URL is not an HTML file.")
                    crawler_database.cursor.execute('DELETE FROM Pages WHERE url=?', (url, ))
                    crawler_database.cursor.execute('UPDATE Pages SET error=0 WHERE url=?', (url, ))
                    crawler_database.connection.commit()
                    continue

            except requests.exceptions.HTTPError:
                print("Unable to retrieve or parse page")
                crawler_database.cursor.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ))
                crawler_database.connection.commit()
                continue  # Going back for scraping another page

            # Inserting the currently crawling page to Pages table with initial rank 1.0
            crawler_database.cursor.execute('INSERT OR IGNORE INTO Pages (url) VALUES ( ? )', (url, ))

            links = crawler.get_links(url)

            for link in links:
                crawler_database.cursor.execute('INSERT OR IGNORE INTO Pages (url) VALUES ( ? )', (link, ))

                crawler_database.cursor.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (link, ))
                row = crawler_database.cursor.fetchone()
                if row is None:
                    print("Couldn't retrieve id of href ->", url)
                    continue

                to_id = row[0]

                # Inserting from_id (currently crawling pages id) and to_id (href's id) to Links Table
                crawler_database.cursor.execute('INSERT OR IGNORE INTO Links (from_id, to_id) '
                                                'VALUES ( ?, ? )', (from_id, to_id))

            crawler_database.connection.commit()

            print('\n {} links found.'.format(len(links)))
            print('\nSleeping for 2 seconds...\n')
            time.sleep(2)

    except KeyboardInterrupt:
        print('\n\nExiting crawler...')
    finally:
        crawler_database.disconnect_db()


if __name__ == '__main__':
    print('Start crawling at {}'.format(start))
    crawl(cd, start)
