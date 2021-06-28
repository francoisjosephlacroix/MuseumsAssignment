from api.API import API
from api.CitiesTableAssembler import CitiesTableAssembler
from infrastructure.DBConnectionManager import DBConnectionManager
from api.MuseumTableAssembler import MuseumTableAssembler
from infrastructure.WikiTable import WikiTable


def main():
    print("Started collecting museum data")
    print("...")
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


if __name__ == '__main__':
    main()
