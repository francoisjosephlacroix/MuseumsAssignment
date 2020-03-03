from bs4 import BeautifulSoup

import WikipediaDateParser
from WikiDataType import WikiDataType, WikiDataTypeConverter
from WikiReferenceValidator import WikiReferenceValidator
from WikiTable import WikiTable





class MuseumTableAssembler:

    def __init__(self):
        self.wikiDataTypeConverter = WikiDataTypeConverter()

    def assembleTable(self, page_content):
        page_html = page_content["parse"]["text"]["*"]
        soup = BeautifulSoup(page_html)

        self.soupTable = soup.find('table', {'class': 'wikitable sortable'})
        self.columns = ['MuseumName', 'MuseumNameRef', 'City', 'CityRef', 'VisitorsPerYear', 'ReferenceYear']
        self.museumNames = []
        self.museumNamesRef = []
        self.cities = []
        self.citiesRef = []
        self.nbVisitors = []
        self.referenceYears = []
        self.contents = {}

        self.buildContents()
        self.pdTable = WikiTable(self.contents, columns=self.columns)

        return self.pdTable

    def buildContents(self):
        rows = self.soupTable.find_all('tr')
        del rows[0]

        for row in rows:
            self.buildRow(row)

        self.contents[self.columns[0]] = self.museumNames
        self.contents[self.columns[1]] = self.museumNamesRef
        self.contents[self.columns[2]] = self.cities
        self.contents[self.columns[3]] = self.citiesRef
        self.contents[self.columns[4]] = self.nbVisitors
        self.contents[self.columns[5]] = self.referenceYears

    def buildRow(self, row):
        # Find all columns in this row
        data = row.find_all('td')

        # Extract data and metadata from each column
        museumNameData = data[0].find('a', href=True, recursive=False)
        cityData = data[1].find('a', href=True, recursive=False)
        visitorsData = data[2].getText()

        # Remove <sup> tag
        data[3].find('sup').decompose()
        referenceYearData = data[3].getText()

        # Assign data to correct column
        museumName = museumNameData.getText()
        self.museumNames.append(museumName)
        museumNameRef = museumNameData["href"]

        isReferenceValid = WikiReferenceValidator.isReferenceValid(museumNameRef)
        if(not isReferenceValid):
            museumNameRef = ""

        self.museumNamesRef.append(museumNameRef)

        city = cityData.getText()
        self.cities.append(city)
        cityRef = cityData["href"]
        self.citiesRef.append(cityRef)

        visitorsData = visitorsData.replace(',', '')
        nbVisitorsForMuseum = eval(visitorsData)
        self.nbVisitors.append(nbVisitorsForMuseum)

        referenceYear = int(referenceYearData)
        self.referenceYears.append(referenceYear)

    def addMuseumProperties(self, table, properties, api):

        for index, row in table.iterrows():

            museumRef = row["MuseumNameRef"]
            museumRef = museumRef.replace("/wiki/","")
            print("museumRef", museumRef)

            if(museumRef == ""):
                continue

            wikibaseItem = api.getWikibaseItemFromArticleName(museumRef)
            print("wikibaseItem",wikibaseItem)

            #If article doesn't exist, check for redirects
            if(wikibaseItem == "-1"):
                redirect = api.getRedirect(museumRef)
                print("Redirect", redirect)
                wikibaseItem = api.getWikibaseItemFromArticleName(redirect)
                print("New wikibaseItem", wikibaseItem)


            museumDataJson = api.getWikiDataForWikibaseItem(wikibaseItem)

            propertiesJson = museumDataJson["entities"][wikibaseItem]["claims"]

            for key, value in properties.items():

                try:
                    property = propertiesJson[key]
                    feature = self.extractFeatureFromProperty(property, key, value, api)

                    for propertyName, propertyValue in feature.items():
                        if propertyName not in table:
                            table[propertyName] = ""

                        table.at[index, propertyName] = propertyValue

                except:
                    pass



    def extractFeatureFromProperty(self, json, key, propertyName, api):
        property = json[0]
        mainsnak = property["mainsnak"]
        datatype = mainsnak["datatype"]

        wikiDataType = self.wikiDataTypeConverter.convertStringToWikiDatatype(datatype)

        if wikiDataType == WikiDataType.GlobeCoordinates:
            value = mainsnak["datavalue"]["value"]
            latitude = value["latitude"]
            longitude = value["longitude"]
            altitude = value["altitude"]

            propertyValue = {"latitude": latitude, "longitude": longitude, "altitude": altitude}
            return propertyValue

        elif wikiDataType == WikiDataType.Item:

            wikibaseId = mainsnak["datavalue"]["value"]["id"]
            wikibaseIdJson = api.getWikiDataForWikibaseItem(wikibaseId)

            aliases = wikibaseIdJson["entities"][wikibaseId]["aliases"]

            if "en" in aliases:
                enAliases = aliases["en"]
                alias = enAliases[0]["value"]

            else:
                #If no english name, just take the first alias in any language
                alias = list(aliases)[0][0]["value"]

            return {propertyName: alias}

        elif wikiDataType == WikiDataType.ExternalIdentifier:

            id = mainsnak["datavalue"]["value"]

            return {propertyName: id}

        elif wikiDataType == WikiDataType.Time:

            stringDate = mainsnak["datavalue"]["value"]["time"]

            date = WikipediaDateParser.parse(stringDate)
            formattedDateString = date.strftime("%Y-%m-%dT%H:%M:%SZ")
            return {propertyName: formattedDateString}


