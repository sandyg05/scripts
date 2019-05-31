import web_manager as wm
import html_parser as hp
from urllib.error import HTTPError


websites = []


def crawl(crawler_database, start_url):

    crawler_database.connect_db()

    if crawler_database.check_db():  # Restarting the previous crawling process
        print("Restarting previous crawl process.")

    else:  # Starting a new crawling process from start_url

        website = wm.extract_root(start_url)

        if len(website) > 1:
            crawler_database.cursor.execute('INSERT OR IGNORE INTO Websites '
                                            '(url) VALUES ( ? )', (website,))

            crawler_database.cursor.execute('INSERT OR IGNORE INTO Pages '
                                            '(url, html, new_rank) '
                                            'VALUES ( ?, NULL, 1.0 )', (start_url,))

            crawler_database.connection.commit()

    # Getting the current website
    crawler_database.cursor.execute('''SELECT url FROM Websites''')

    for row in crawler_database.cursor:
        websites.append(str(row[0]))

    print(websites)

    crawl_counter = 0

    while True:  # Crawl Loop

        if crawl_counter < 1:
            crawl_counter = int(input('How many pages do you want to crawl? '))
            if crawl_counter == 0:
                break

        print("Crawling Iteration:", crawl_counter)
        crawl_counter -= 1

        # Getting a random row where HTML Code and error is NULL
        crawler_database.cursor.execute('SELECT id,url FROM Pages WHERE '
                                        'html is NULL and error is NULL '
                                        'ORDER BY RANDOM() LIMIT 1')

        row = crawler_database.cursor.fetchone()

        if row is None:  # Breaking the loop when there are no row
            print("All pages are retrieved.")
            break

        from_id = row[0]
        url = row[1]

        print("Crawling ->", "Page ID =", from_id, "| URL =", url, end=' ')

        # This query deletes all records which the current page points to.
        crawler_database.cursor.execute('DELETE from Links WHERE from_id=?', (from_id,))

        try:
            document = wm.open_url(url)

            if wm.get_http_status_code(document) != 200:  # Checking HTTP Status Code (200 means success)
                print("Error occured while loading the page: ",
                      wm.get_http_status_code(document))

                crawler_database.cursor.execute('UPDATE Pages SET error=? WHERE url=?',
                                                (wm.get_http_status_code(document), url))

            if 'text/html' != wm.get_http_content_type(document):  # Checking the Content-Type
                print("This URL is not an HTML file.")
                crawler_database.cursor.execute('DELETE FROM Pages WHERE url=?', (url,))
                crawler_database.cursor.execute('UPDATE Pages SET error=0 WHERE url=?', (url,))
                crawler_database.connection.commit()
                continue

            soup = hp.parse_html(document)  # Using BeautifulSoup to repair and parse HTML document
            html_code = str(soup)

        except HTTPError:
            print("Unable to retrieve or parse page")
            crawler_database.cursor.execute('UPDATE Pages SET error=-1 WHERE url=?', (url,))
            crawler_database.connection.commit()
            continue

        # Inserting the currently crawling page to Pages table with initial rank 1.0
        crawler_database.cursor.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank)'
                                        ' VALUES ( ?, NULL, 1.0 )', (url,))

        # Updating the currently crawling pages html field
        crawler_database.cursor.execute('UPDATE Pages SET html=? WHERE url=?', (html_code, url))
        crawler_database.connection.commit()

        a_tags = hp.get_tags(soup, "a")  # Getting all <a> tags because they are the links to other pages
        href_count = 0

        for tag in a_tags:
            href_attribute = hp.get_attribute(tag, "href")

            if not wm.does_exist(href_attribute):
                continue

            if wm.is_image(href_attribute):
                continue

            if href_attribute.endswith('/'):
                href_attribute = href_attribute[:-1]

            if wm.is_relative(href_attribute):
                href = wm.make_absolute(url, href_attribute)  # Making the absolute URL

            if href.find("#") > 1:
                pointer = href.find("#")
                href = href[:pointer]  # Cutting the fragment part in the URL

            is_found = False
            for website in websites:
                if href.startswith(website):  # If href is in the Websites, breaking the loop
                    is_found = True
                    break
            if not is_found:
                continue

            # Inserting the href to Pages table with initial rank 1.0
            crawler_database.cursor.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) '
                                            'VALUES ( ?, NULL, 1.0 )', (href,))
            href_count = href_count + 1
            crawler_database.connection.commit()

            # Getting the id of the href
            crawler_database.cursor.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (href,))
            row = crawler_database.cursor.fetchone()
            if row is None:
                print("Couldn't retrieve id of href ->", href)
                continue

            to_id = row[0]

            # Inserting from_id (currently crawling pages id) and to_id (href's id) to Links Table
            crawler_database.cursor.execute('INSERT OR IGNORE INTO Links (from_id, to_id) '
                                            'VALUES ( ?, ? )', (from_id, to_id))

        print("| links found =", href_count, "\n")

    crawler_database.disconnect_db()
