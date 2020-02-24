import pandas as pd


class WikiTable(pd.DataFrame):

    def persist(self, tableName, connection):
        self.to_sql(tableName, connection, if_exists='replace')

    def load(tableName, connection):
        sql_query = "SELECT * FROM {}".format(tableName)
        return WikiTable.copy(pd.read_sql(sql_query, connection))
