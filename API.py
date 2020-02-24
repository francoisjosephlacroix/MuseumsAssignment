import requests


class API:

    def __init__(self):
        pass


    def getMuseumList(self):
        museumsRequest = requests.get(
            'https://en.wikipedia.org/w/api.php?action=parse&page=List_of_most_visited_museums&prop=text&format=json')

        page_content = museumsRequest.json()

        return page_content


    def getWikibaseItemFromArticleName(self, articleName):
        wikibaseIdURL = "https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&titles={}&props=descriptions&languages=en&format=json".format(
            articleName)
        wikibaseRequest = requests.get(wikibaseIdURL)
        wikibaseJson = wikibaseRequest.json()
        wikibaseEntities = wikibaseJson['entities']
        wikibaseItem = list(wikibaseEntities)[0]

        return wikibaseItem

    def getRedirect(self, cityRef):
        pageIdURL = "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={}&format=json".format(
            cityRef)
        pageIdRequest = requests.get(pageIdURL)
        pageIdJson = pageIdRequest.json()
        pages = pageIdJson["query"]['pages']
        pageId = list(pages)[0]
        redirectUrl = "https://en.wikipedia.org/w/api.php?action=query&format=json&pageids={}&redirects".format(
            pageId)
        redirectRequest = requests.get(redirectUrl)
        redirectJson = redirectRequest.json()
        redirectsTo = redirectJson["query"]['redirects'][0]['to']
        formattedRedirect = redirectsTo.replace(' ', '_')
        return formattedRedirect


    def getPopulationData(self, id):
        populationRequest = requests.get(
            "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&format=json".format(id))
        populationJson = populationRequest.json()
        entities = populationJson["entities"]
        entity = entities[list(entities)[0]]
        claims = entity["claims"]
        populationData = claims["P1082"]
        return populationData




