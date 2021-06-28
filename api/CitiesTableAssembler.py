from datetime import timedelta
from domain.WikipediaDateParser import WikipediaDateParser
from utils.constants import DATE_QUALIFIER


class CitiesTableAssembler:

    def assemble(self, citiesTable, api):
        self.citiesTable = citiesTable

        self.cityWikibaseIds = {}

        self.addWikibaseIds(api)
        self.addPopulation(api)

        self.citiesTable.drop_duplicates(inplace=True)
        self.citiesTable.reset_index(inplace=True, drop=True)

        return self.citiesTable

    def addWikibaseIds(self, api):
        self.citiesTable["WikibaseId"] = ""

        for index, row in self.citiesTable.iterrows():
            cityRefOriginal = row['CityRef']
            cityRef = cityRefOriginal.replace('/wiki/', '')

            if cityRefOriginal not in self.cityWikibaseIds:
                wikibaseItem = api.getWikibaseItemFromArticleName(cityRef)

                if wikibaseItem == "-1":
                    redirectsTo = api.getRedirect(cityRef)
                    wikibaseItem = api.getWikibaseItemFromArticleName(redirectsTo)

                self.cityWikibaseIds[cityRefOriginal] = wikibaseItem

            wikibaseId = self.cityWikibaseIds[row["CityRef"]]
            self.citiesTable.at[index, "WikibaseId"] = wikibaseId

    def addPopulation(self, api):
        self.citiesTable["Population"] = ""
        populationDict = {}

        for id in self.cityWikibaseIds.values():
            populationData = api.getPopulationData(id)

            preferredData = None
            newestData = None
            newestDate = WikipediaDateParser.parse('+0001-01-01T00:00:00Z')
            highestPopulation = 0
            preferredFound = False

            for data in populationData:
                if data.get("rank", "") == "preferred":
                    preferredData = data
                    preferredFound = True

                currentPopulationString = data.get("mainsnak", {}).get("datavalue", {}).get("value", {})\
                    .get("amount", "")
                currentPopulation = eval(currentPopulationString)

                if (currentPopulation > highestPopulation):
                    highestPopulation = currentPopulation

                # Check if date is more recent than newest
                dates = data.get("qualifiers", {}).get(DATE_QUALIFIER)
                if dates is None:
                    continue

                date = list(dates)[0]
                stringDate = date.get("datavalue", {}).get("value", {}).get("time", '')
                currentDate = WikipediaDateParser.parse(stringDate)
                dateDelta = newestDate - currentDate

                emptyDelta = timedelta()
                if (dateDelta < emptyDelta):
                    newestDate = currentDate
                    newestData = data

                elif (dateDelta == emptyDelta):
                    newestPopulationString = newestData.get("mainsnak", {}).get("datavalue", {}).get("value", {})\
                        .get("amount", "")
                    newestPopulation = eval(newestPopulationString)

                    if (currentPopulation > newestPopulation):
                        newestDate = currentDate
                        newestData = data

            if preferredFound:
                populationString = preferredData.get("mainsnak", {}).get("datavalue", {}).get("value", {})\
                    .get("amount", "")
                population = eval(populationString)
            else:
                if (newestData is not None):
                    populationString = newestData.get("mainsnak", {}).get("datavalue", {}).get("value", {}) \
                        .get("amount", "")
                    population = eval(populationString)
                else:
                    population = highestPopulation

            populationDict[id] = population

        for index, row in self.citiesTable.iterrows():
            population = populationDict[self.citiesTable.at[index, "WikibaseId"]]
            self.citiesTable.at[index, "Population"] = population
