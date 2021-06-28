import pandas as pd


class WikiTable(pd.DataFrame):

    def __init__(self, fromDataFrame=None, *args, **kwrds):
        if fromDataFrame is not None:
            super().__init__(fromDataFrame)
        else:
            super().__init__(*args, **kwrds)

    def persist(self, tableName, connection):
        self.to_sql(tableName, connection, if_exists='replace')

    @staticmethod
    def load(tableName, connection):
        sqlQuery = f"SELECT * FROM {tableName}"
        dfFromSQL = pd.read_sql(sqlQuery, connection)
        try:
            dfFromSQL.drop(columns="index", inplace=True)
        except:
            pass
        wikitable = WikiTable(fromDataFrame=dfFromSQL)
        return wikitable
