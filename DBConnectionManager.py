import sqlite3

class DBConnectionManager:

    def __init__(self):
        self.dbPath = "Museums.db"
        self.connection = sqlite3.connect(self.dbPath)


    def getDBConnection(self):
        return self.connection





