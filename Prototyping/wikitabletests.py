import sqlite3

from infrastructure.WikiTable import WikiTable


dbPath = "Museums.db"
connection = sqlite3.connect(dbPath)

table = {'Client_Name':['John Smith', 'Bill Martin'],
         'Country_ID':[1,2],
         'Date': [14012019, 14012019]}


wikitable = WikiTable(table)


wikitable.persist("MuseumsAndCities", connection)


