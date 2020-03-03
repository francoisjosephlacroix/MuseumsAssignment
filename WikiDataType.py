import enum


class WikiDataType(enum.Enum):
    CommonsMedia = 0
    GlobeCoordinates = 1
    Item = 2
    Property = 3
    String = 4
    MonolingualText = 5
    ExternalIdentifier = 6
    Quantity = 7
    Time = 8
    URL = 9
    MathematicalExpression = 10
    GeographicShape = 11
    MusicalNotation = 12
    TabularData = 13
    Lexemes = 14
    Forms = 15
    Senses = 16

class WikiDataTypeConverter:

    def convertStringToWikiDatatype(self, value):

        value = value.lower()

        if value == "commonsMedia":
            return WikiDataType.CommonsMedia
        elif value == "globe-coordinate":
            return WikiDataType.GlobeCoordinates
        elif value == "wikibase-item":
            return WikiDataType.Item
        elif value == "property":
            return WikiDataType.Property
        elif value == "string":
            return WikiDataType.String
        elif value == "monolingualtext":
            return WikiDataType.MonolingualText
        elif value == "external-id":
            return WikiDataType.ExternalIdentifier
        elif value == "quantity":
            return WikiDataType.Quantity
        elif value == "time":
            return WikiDataType.Time
        elif value == "url":
            return WikiDataType.URL
        elif value == "mathematical expression":
            return WikiDataType.MathematicalExpression
        elif value == "geographic shape":
            return WikiDataType.GeographicShape
        elif value == "musical notation":
            return WikiDataType.MusicalNotation
        elif value =="tabular data":
            return WikiDataType.TabularData
        elif value =="lexemes":
            return WikiDataType.Lexemes
        elif value =="forms":
            return WikiDataType.Forms
        elif value =="senses":
            return WikiDataType.Senses

        raise ValueError("Unknown data type: {}".format(value))
