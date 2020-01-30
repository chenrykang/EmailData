#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:19:42 2020

@author: christopherkang


I would like you to solution this challenge:
 
1)      Upload the attached file
2)      Create data frames on python
a.       Let the user pick the template(s) to consider (it could be more that one à check box)  
 
3)      Produce an exportable (as a .csv file) report online with the following output –related to the template selected by the user :
a.       Sent
b.      Delivered (number of emails delivered)
c.       Delivery rate (b/a)
d.      Open rate (= number of emails opened divided by b)
e.       Click rate (= number of emails clicked divided by b)
 
Additional requirements:
-          The report should display the results by year and by month for 2018 and 2019.
-          The web app should be accessible online via either Heroku, AWS or, Google Cloud by the time of our interview.
-          The code should be uploaded either on Gitlab or Github

"""

import pandas as pd
from datetime import datetime

class Data():

    def readData(self):

        csv = "data_test_JAN24_2020.csv"
        data = pd.read_csv(csv)
        data = data.dropna() #drop any rows with nan (no values)
        return data
    
    def editCells(self, df, slideDic):

        li = ['sent', 'delivered', 'delRate', 'openRate', 'clickRate']

        data = df.copy(deep=True)

        for i, slideTup in enumerate(slideDic.values()):
            data = data[data[li[i]].between(float(slideTup[0]), float(slideTup[1]))]

        return data
    
    def getSlideValues(self, df):

        minDic = {}
        maxDic = {}

        for columnName in df.columns.values.tolist():
            if columnName != 'date' and columnName != 'template':
                minDic[columnName] = df[columnName].min()
                maxDic[columnName] = df[columnName].max()

        return (minDic, maxDic)

    def parseData(self, data):
        sentLi = []
        deliveredLi = []
        delRateLi = []
        openRateLi = []
        clickRateLi = []
        dateLi = []
        templateLi = []

        for index, row in data.iterrows():
            
            #parse df
            sent = int(row[0].split('|')[6])
            rejects = int(row[0].split('|')[5])
            delivered = sent-rejects
            opened = int(row[0].split('|')[11])
            clicked = int(row[0].split('|')[10])
            date = row[0].split('|')[9]
            date = datetime.strptime(date, "%m/%d/%Y %H:%M")
            template = row[0].split('|')[8]
            
            if sent > 0:
                delRate = int((delivered/sent))*100
            else:
                delRate = -1
            if delivered > 0:
                openRate = int((opened/delivered))*100
                clickRate = int((clicked/delivered))*100
            else:
                openRate = -1
                clickRate = -1
                
            
            #append attributes to lists
            sentLi.append(sent)
            deliveredLi.append(delivered)
            delRateLi.append(delRate)
            openRateLi.append(openRate)
            clickRateLi.append(clickRate)
            dateLi.append(date)
            templateLi.append(template)


        data.insert(1, 'date', dateLi)
        data.insert(2, 'sent', sentLi)
        data.insert(3, 'delivered', deliveredLi)
        data.insert(4, 'delRate', delRateLi)
        data.insert(5, 'openRate', openRateLi)
        data.insert(6, 'clickRate', clickRateLi)
        data.insert(7, 'template', templateLi)

        data.drop(data.columns[[0]], axis=1, inplace=True)

        data = data[(data['date'] > '12-31-2017 23:59:59') & (data['date'] <= '2019-12-31 23:59:59')]

        data = data.sort_values(by='date', ascending = False)

        return data
    

























