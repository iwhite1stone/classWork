import requests
import json
import pandas as pd
from sklearn import linear_model
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
#declaring the list for calls
#teamList = ['Arkansas','Texas','Alabama','Auburn','Missouri','Vanderbilt','Kentucky','Florida','Georgia']
teamList = ['Arkansas','Texas']
dfList = []
bearerToken = ""
def getSeasonStats():
    #build a dataframe from the API call for season stats
    dfAllTeamsStats = pd.DataFrame()
    for each in teamList:

        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + bearerToken
        }
        params = {
            'team': each
        }

        seasonResponse = requests.get('https://api.collegefootballdata.com/stats/season', params=params, headers=headers)
        seasonData = seasonResponse.json()

        dfTeamStats = pd.json_normalize(seasonData)
        dfTeamStats = dfTeamStats[dfTeamStats['season'] >= 2004]
        dfAllTeamsStats = pd.concat([dfAllTeamsStats, dfTeamStats])


    #dfAllTeamsStats['SeasonTeam'] = dfAllTeamsStats['season'].astype(str) + " " +  dfAllTeamsStats['team']
    dfAllTeamsStats = dfAllTeamsStats.pivot(index=['season','team'], columns='statName', values='statValue').reset_index().rename_axis(None)
    print(dfAllTeamsStats)

    dfAllTeamsStats = dfAllTeamsStats[['possessionTime','firstDowns','thirdDownConversions','netPassingYards','sacks','team','season']]
    return dfAllTeamsStats
def getTeamRecord():
    # build a dataframe from the API call for team record
    dfAllTeamsRecord = pd.DataFrame()
    for each in teamList:
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + bearerToken
        }
        params = {
            'team': each
        }
        recordResponse = requests.get('https://api.collegefootballdata.com/records', params=params, headers=headers)
        recordData = recordResponse.json()
        dfTeamRecord = pd.json_normalize(recordData)

        dfTeamRecord = dfTeamRecord[dfTeamRecord['year'] >= 2004]
        dfTeamRecord = dfTeamRecord[['year', 'total.games','total.wins','total.losses']]
        dfTeamRecord = dfTeamRecord.rename(columns={"year":"season", "total.games":"total games","total.wins":"wins","total.losses":"losses"})
        dfTeamRecord['team'] = each
        dfAllTeamsRecord = pd.concat([dfAllTeamsRecord,dfTeamRecord])

        #dfAllTeamsRecord['SeasonTeam'] = dfAllTeamsRecord['season'].astype(str) + " " + dfAllTeamsRecord['team']

    dfGroupTeamRecord = dfAllTeamsRecord.groupby(by=['team']).sum()

    return dfAllTeamsRecord
def findMostImportant(dfAllData):

    #dfAllData['winPercentage'] = dfAllData['wins']/dfAllData['total games']
    dfAllData = dfAllData.drop(columns=['wins','losses','total games','season','team'])
    dfAllData = dfAllData.dropna(axis='columns')
    x = dfAllData.drop('netPassingYards', axis = 1)
    y = dfAllData['netPassingYards']

    regr = linear_model.LinearRegression()
    regr.fit(x,y)

    x = sm.add_constant(x)  # adding a constant

    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)

    print_model = model.summary()
    print(print_model)
dfAllTeamsRecord = getTeamRecord()
dfAllTeamStats = getSeasonStats()
dfAllData = dfAllTeamsRecord.merge(dfAllTeamStats, how='inner',on=["season","team"])

# dfAllData = dfTeamStats
findMostImportant(dfAllData)

