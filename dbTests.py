import sqlite3
import pandas as pd

from WikiTable import WikiTable

dbPath = "Museums.db"
connection = sqlite3.connect(dbPath)

# cursor = connection.cursor()
#
# table = {'Client_Name':['John Smith','Bill Martin'],
#          'Country_ID':[1,2],
#          'Date': [14012019, 14012019]}
#
# pdTable = pd.DataFrame(table)
#
# print(pdTable)
#
# pdTable.to_sql('CLIENTS', connection, if_exists='replace', index=False)
# # connection.commit()
#
# #
# # cursor.execute('''CREATE TABLE CLIENTS
# #              ([generated_id] INTEGER PRIMARY KEY,[Client_Name] text, [Country_ID] integer, [Date] date)''')
# #
#
# test = cursor.execute("SELECT * FROM CLIENTS")


test = WikiTable.load("Museums", connection)

print(test)



