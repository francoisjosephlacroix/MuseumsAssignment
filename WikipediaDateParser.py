from datetime import datetime


class WikipediaDateParser():

    def parse(stringDate):

        # Remove + at beginning
        stringDate = stringDate[1:]

        month = stringDate[5:7]
        day = stringDate[8:10]

        if (month == "00"):
            stringDate = stringDate[:5] + "01" + stringDate[7:]
        if (day == "00"):
            stringDate = stringDate[:8] + "01" + stringDate[10:]

        return datetime.strptime(stringDate, '%Y-%m-%dT%H:%M:%SZ')

