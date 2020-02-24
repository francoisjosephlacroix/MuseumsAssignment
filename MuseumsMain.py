from API import API
from CitiesTableAssembler import CitiesTableAssembler
from DBConnectionManager import DBConnectionManager
from MuseumTableAssembler import MuseumTableAssembler
from WikiTable import WikiTable

if __name__ == '__main__':
    api = API()
    dbConnectionManager = DBConnectionManager()

    museumListJson = api.getMuseumList()
    museumTableAssembler = MuseumTableAssembler()
    museumTable = museumTableAssembler.assembleTable(museumListJson)
    museumTable.persist("Museums", dbConnectionManager.getDBConnection())

    citiesTable = WikiTable(museumTable[['City', 'CityRef']])
    citiesTableAssembler = CitiesTableAssembler()
    citiesTable = citiesTableAssembler.assemble(citiesTable, api)
    citiesTable.persist("Cities", dbConnectionManager.getDBConnection())

    print(museumTable)
    print(citiesTable)
