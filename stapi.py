import requests
import json


def seriesNameSwitch(value):
    if value == 'Star Trek: The Animated Series':
        return 'TAS'
    elif value == 'Star Trek: Deep Space Nine':
        return 'DS9'
    elif value == 'Star Trek: Enterprise':
        return 'ENT'
    elif value == 'Star Trek: Discovery':
        return 'DISC'
    elif value == 'Star Trek: The Next Generation':
        return 'TNG'
    elif value == 'Star Trek: The Original Series':
        return 'TOS'
    elif value == 'Star Trek: Voyager':
        return 'VOY'
    else:
        raise ValueError('**SERIES NAME NOT DEFINED**')


seasonSearchUrl = 'http://stapi.co/api/v1/rest/season/search'
seasonQueryUrl = 'http://stapi.co/api/v1/rest/season?uid='

response = requests.get(seasonSearchUrl)
# r.encoding = 'UTF-8'
print('RAW URL:= ' + response.url)
print('RAW RESPONSE:= ' + str(response.status_code))
# print('RAW TEXT:= ' + str(rJson))
responseJson_dict = json.loads(response.text)
print(json.dumps(responseJson_dict, indent=4, sort_keys=True))

# print(responseJson_dict['seasons'][0]['series']['title'])

with open('startrekdata.csv', 'w') as csvFile:

    csvFile.write('Series' + '\t' + 'Episode Title' + '\t' + 'Season #' + '\t' + 'Episode #' + '\t' + 'Star Date' + '\t' + 'Air Date' + '\r\n')

    seasonsArray = responseJson_dict['seasons']
    for season in seasonsArray:
        # print(season['series']['title'] + ", Season " + str(season['seasonNumber']))
        seriesName = seriesNameSwitch(season['series']['title'])
        seasonUid = season['uid']
        # print(seasonUid)
        # print(requests.get(seasonQueryUrl + seasonUid).url)
        getSeasons = requests.get(seasonQueryUrl + seasonUid)
        season_dict = json.loads(getSeasons.text)
        episodesArray = season_dict['season']['episodes']
        # print(episodesArray)
        for episode in episodesArray:
            episodeTitle = episode['title']
            episodeNumber = episode['episodeNumber']
            seasonNumber = str(episode['seasonNumber'])
            starDate = episode['stardateFrom']
            airDate = episode['usAirDate']
            csvFile.write(seriesName + '\t' + episodeTitle + '\t' + seasonNumber + '\t' + str(episodeNumber) + '\t' + str(starDate) + '\t' + str(airDate) + '\r\n')
print('DATA PROCESSING COMPLETE')
