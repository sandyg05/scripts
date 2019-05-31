import sqlite3


class CrawlerDatabase:

    def __init__(self, db_name):
        """
        When the CrawlerDatabase is initialized, the necessary tables are created, if they don't exist
        """

        self._db_name = db_name
        self.connection = sqlite3.connect(db_name + ".sqlite")
        self.cursor = self.connection.cursor()

        # All of the unique urls are stored in the Pages table

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pages
                        (id INTEGER PRIMARY KEY, 
                         url TEXT UNIQUE,
                         error INTEGER)''')

        # Links table is a junction table for representing the many to many relationship between links
        # from_id is the pointing url and to_id is the pointed url

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Links
                            (from_id INTEGER, 
                             to_id INTEGER)''')

        # Websites is the table for storing unique host names

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Websites 
                            (url TEXT UNIQUE)''')

        self.cursor.close()
        self.connection.close()

    def connect_db(self):
        # Connects to db
        self.connection = sqlite3.connect(self._db_name + ".sqlite")
        self.cursor = self.connection.cursor()

    def disconnect_db(self):
        # Disconnects from db
        self.cursor.close()
        self.connection.close()

    def check_db(self):
        # Checks the crawler had started a crawling process before with this database
        self.cursor.execute('SELECT id,url FROM Pages WHERE error is NULL ORDER BY RANDOM() LIMIT 1')
        row = self.cursor.fetchone()

        return row is not None
