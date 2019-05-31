import sqlite3


class CrawlerDatabase:

    def __init__(self, db_name):
        """
        Factory method for creating a database with given name.
        If database exists with the given name, crawler won't overwrite data.
        :param db_name: Name of the sqlite file. (string)
        """

        self._db_name = db_name
        self.connection = sqlite3.connect(db_name + ".sqlite")
        self.cursor = self.connection.cursor()

        # Creating tables for the database

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pages
                        (id INTEGER PRIMARY KEY, 
                         url TEXT UNIQUE, 
                         html TEXT,
                         error INTEGER, 
                         old_rank REAL, 
                         new_rank REAL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Links
                            (from_id INTEGER, 
                             to_id INTEGER)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Websites 
                            (url TEXT UNIQUE)''')

        self.disconnect_db()

    def connect_db(self):
        """
        Connects to the database.
        :return: Doesn't return anything but connection will be kept.
        """

        self.connection = sqlite3.connect(self._db_name + ".sqlite")
        self.cursor = self.connection.cursor()

    def disconnect_db(self):
        """
        Closes the connection to the database.
        :return: Doesn't return anything.
        """
        self.cursor.close()
        self.connection.close()

    def check_db(self):
        """
        Checks the crawler had started a crawling process before with this database.
        :return: A random incomplete row from Pages table.
        """

        self.cursor.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
        row = self.cursor.fetchone()

        return row is not None

    def get_from_ids(self):
        """
        Gets every page id that is pointing to another page, once.
        :return: A list of page ids pointing to another page.
        """
        from_ids = []

        self.cursor.execute('''SELECT DISTINCT from_id FROM Links''')
        for row in self.cursor:
            from_ids.append(row[0])

        return from_ids

    def rank_pages(self):
        """
        Ranks the pages.
        :return: Doesn't return anything.
        """

        self.connect_db()  # Connects to database.

        pages_pointing = self.get_from_ids()  # List of ids pointing to another page.
        pages_pointed = []  # List of ids pointed by another page.
        links = []  # List of every combination of pointing and pointed ids.

        self.cursor.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
        for row in self.cursor:
            from_id = row[0]
            to_id = row[1]

            if from_id == to_id:
                continue

            if from_id not in pages_pointing:
                continue

            if to_id not in pages_pointing:
                continue

            links.append(row)

            if to_id not in pages_pointed:
                pages_pointed.append(to_id)

        actual_ranks = {}  # page : new_rank mappings from database.

        for page in pages_pointing:
            self.cursor.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (page,))
            row = self.cursor.fetchone()
            actual_ranks[page] = row[0]

        iterations = input('How many iterations do you want to rank pages? ')

        if len(actual_ranks) < 1:  # There are no pages to rank.
            print("There are no pages to rank. Quitting ranking process...")
            quit()

        for iteration in range(int(iterations)):  # The page ranking loop

            new_ranks = {}  # page : 0.0 mappings.
            total_rank = 0.0  # Total of the new_ranks.

            for (page, old_rank) in list(actual_ranks.items()):

                total_rank = total_rank + old_rank  # Getting the total of the ranks.
                new_ranks[page] = 0.0  # Setting all ranks to 0.

            for (page, old_rank) in list(actual_ranks.items()):

                give_ids = []

                for (from_id, to_id) in links:
                    if from_id != page:
                        continue

                    if to_id not in pages_pointed:
                        continue

                    give_ids.append(to_id)

                if len(give_ids) < 1:
                    continue

                amount = old_rank / len(give_ids)

                for item in give_ids:
                    new_ranks[item] = new_ranks[item] + amount

            new_total_rank = 0
            for (page, next_rank) in list(new_ranks.items()):
                new_total_rank = new_total_rank + next_rank

            result = (total_rank - new_total_rank) / len(new_ranks)

            for rank in new_ranks:
                new_ranks[rank] = new_ranks[rank] + result

            new_total_rank = 0
            for (page, next_rank) in list(new_ranks.items()):
                new_total_rank = new_total_rank + next_rank

            total_difference = 0
            for (page, old_rank) in list(actual_ranks.items()):
                new_rank = new_ranks[page]
                difference = abs(old_rank - new_rank)  # Average change from old rank to new rank.
                total_difference = total_difference + difference

            average_difference = total_difference / len(actual_ranks)
            print("Ranking Iteration", iteration + 1, "\nAverage Difference ->", average_difference, "\n")

            actual_ranks = new_ranks

        print("\nID - Rank pairs from the database:\n", list(actual_ranks.items()))

        self.cursor.execute('''UPDATE Pages SET old_rank=new_rank''')

        for (item, new_rank) in list(actual_ranks.items()):  # Writing new ranks to Pages table.
            self.cursor.execute('''UPDATE Pages SET new_rank=? WHERE id=?''', (new_rank, item))

        self.connection.commit()
        self.disconnect_db()

    def reset_ranks(self):
        """
        Resets all the ranks of pages to 1.0.
        :return: Doesn't return anything.
        """

        self.connect_db()  # Connects to database.

        self.cursor.execute('''UPDATE Pages SET new_rank=1.0, old_rank=0.0''')  # Resetting all ranks.

        self.connection.commit()
        self.disconnect_db()

        print("All page ranks are reset.")

    def show_stats(self):
        """
        Displays pages in a order from with most inbound links to least.
        :return: Doesn't return anything.
        """

        self.connect_db()  # Connects to database.

        self.cursor.execute('''SELECT COUNT(from_id) AS links, old_rank, new_rank, id, url  
                                FROM Pages JOIN Links ON Pages.id = Links.to_id
                                WHERE html IS NOT NULL
                                GROUP BY id ORDER BY links DESC''')

        print("\n\nInbound Links | Old Rank | New Rank | ID | URL (From pages with most inbound links to least)\n")

        crawl_count = 0
        for row in self.cursor:
            print(row)
            crawl_count += 1
        print("\nDatabase Summary: ", crawl_count, 'completed crawls.\n')

        self.disconnect_db()
