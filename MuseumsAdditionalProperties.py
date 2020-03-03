from API import API
from CitiesTableAssembler import CitiesTableAssembler
from DBConnectionManager import DBConnectionManager
from MuseumTableAssembler import MuseumTableAssembler
from WikiTable import WikiTable
import json


def main():
    print("Started collecting additional museum data")
    print("...")

    api = API()
    dbConnectionManager = DBConnectionManager()

    museumTableAssembler = MuseumTableAssembler()
    museumTable = WikiTable.load("Museums", dbConnectionManager.getDBConnection())

    print(museumTable)

    properties_configuration = "properties_configuration.json"
    with open(properties_configuration, 'r') as propertiesFile:
        propertiesJson = json.load(propertiesFile)
        print(propertiesJson)
        for property in propertiesJson:
            print("{}: {}".format(property, propertiesJson[property]))

    museumTableAssembler.addMuseumProperties(museumTable, propertiesJson, api)

    museumTable.persist("Museums", dbConnectionManager.getDBConnection())


if __name__ == '__main__':
    main()


