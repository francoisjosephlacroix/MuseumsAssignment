import pandas as pd


class WikiTable(pd.DataFrame):

    def __init__(self, fromdataframe=None, *args, **kwrds):
        if fromdataframe is not None:
            super().__init__(fromdataframe)
        else:
            super().__init__(*args, **kwrds)

    def persist(self, tableName, connection):
        self.to_sql(tableName, connection, if_exists='replace')

    def load(tableName, connection):
        sql_query = "SELECT * FROM {}".format(tableName)
        pdDataframe = pd.read_sql(sql_query, connection)
        try:
            pdDataframe.drop(columns="index", inplace=True)
        except:
            pass
        wikitable = WikiTable(fromdataframe=pdDataframe)
        return wikitable
