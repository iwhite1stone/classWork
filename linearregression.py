# -*- coding: utf-8 -*-
"""linearRegression

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FDxn8uRVsuRy9FNda3ZS4iQg_DLmuBCk
"""

from google.colab import files
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# uploaded = files.upload()
# dfTeamData = pd.read_csv(io.BytesIO(uploaded['AllTeams.csv']))
#Get data from GitHub
dfTeamData = pd.read_csv('https://raw.githubusercontent.com/iwhite1stone/classWork/main/AllTeams.csv')
dfTeamData = pd.pivot_table(dfTeamData,values='statValue',columns='statName',index='season', aggfunc=np.sum).reset_index()
print(dfTeamData)
#Set variables for correlation
xColumn = 'passingTDs'
yColumn = 'firstDowns'
x = dfTeamData[xColumn]
y = dfTeamData[yColumn]
s = dfTeamData['season']
plt.scatter(x,y)
#Add trendline
plt.ylabel(yColumn)
plt.xlabel(xColumn)
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x,p(x),"r--")
#Show graph
plt.show()

"""# New Section"""
