from bs4 import BeautifulSoup

from WikiTable import WikiTable


class MuseumTableAssembler:

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
