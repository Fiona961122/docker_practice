import sqlite3

CREATE_TABLE = "CREATE TABLE entity (name TEXT PRIMARY KEY, count INT DEFAULT 1)"
SELECT = "SELECT * FROM entity ORDER BY count DESC"
UPSERT = "INSERT INTO entity(name) VALUES (?) ON CONFLICT(name) DO UPDATE SET count=count+1"


class DatabaseConnection(object):

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename, check_same_thread=False)

    def create_schema(self):
        try:
            self.connection.execute(CREATE_TABLE)
        except sqlite3.OperationalError:
            print("Warning: 'entity' table was already created, ignoring...")

    def get(self):
        cursor = self.connection.execute(SELECT)
        return cursor.fetchall()

    def add(self, name):
        self.connection.execute(UPSERT, (name,))
        self.connection.commit()


if __name__ == '__main__':
    connection = DatabaseConnection('test.sqlite')
    connection.create_schema()
    connection.add('jane')
    print(connection.get())
