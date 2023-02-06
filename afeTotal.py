# Import packages needed
from ast import keyword
from http import client
from posixpath import split
from time import strftime
from black import out
import requests
import os
from datetime import date, datetime, timedelta
import datetime as dt
import glob
import re
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from openpyxl import Workbook

nameOfWell = "porter33v"

pathOfDailyReport = '.\\kingops\\data\\afe' + '\\' + nameOfWell + "\\" + "daily"
pathOfAfe = r".\kingops\data\afe" + "\\" + nameOfWell

plannedCostFile = pathOfAfe + "\\" + nameOfWell + "planned.xlsx"
plannedCostDepth = pd.read_excel(plannedCostFile)

masterMatchFile = pd.read_excel(
    r".\kingops\data\afe\welldriveWolfepakMatch.xlsx")

pathOfMasterFile = pathOfAfe + "\\" + "fullreport.xlsx"

masterAfe = pd.read_excel(pathOfMasterFile)

welldriveBudgetAccounts = masterMatchFile["Code WellDrive"].tolist()
wolfepakActualAccounts = masterMatchFile["Code WolfePak"].tolist()
wellEzAccounts = masterMatchFile["Code Wellez"].tolist()

costItemListClean = []

totalCostAllFile = []
totalDateAllFile = []
totalDepthAllFile = []
totalCumulativeCost = []

dailyItemCostFileName = pathOfAfe + "\\" + nameOfWell + "dailyItemCost.csv"
dailyItemCostFp = open(dailyItemCostFileName, "w")

daysVsDepthFileName = pathOfAfe + "\\" + nameOfWell + "daysvsdepth.csv"
daysVsDepthFp = open(daysVsDepthFileName, "w")

headerString = "Date, Account Number, Depth, Daily Cost Estimate, Description\n"
dailyItemCostFp.write(headerString)

headerString = "Date, Days, Hours, Planned Depth, Planned Cost, Daily, Daily Cost Estimated, Actual Depth, Cumulative Cost\n"
daysVsDepthFp.write(headerString)

masterAfe = masterAfe.fillna(0)

timeStampList = masterAfe["textbox51"].tolist()
timeStampCleanList = list(set(timeStampList))

timeStampCleanList = [str(i) for i in timeStampCleanList]

timeStampCleanList.sort(key=lambda date: datetime.strptime(
    date, '%Y-%m-%d %H:%M:%S'))

dateCleanList = []
daysList = []
days = 0
totalDailyCost = 0
cumulativeCost = 0
foundStartDate = 0

for i in range(0, len(timeStampCleanList)):
    dt = datetime.strptime(timeStampCleanList[i], '%Y-%m-%d %H:%M:%S')
    dateCleanList.append(dt.strftime("%m/%d/%Y"))
    daysList.append(days)
    days = days + 1

measuredDepthList = masterAfe["Textbox8.1"].tolist()
measuredDepthListClean = list(set(measuredDepthList))

mergedDaysDateList = list(zip(daysList, dateCleanList))


for i in range(0, len(masterAfe)):
    row = masterAfe.iloc[i]
    date = row[0]
    if i == 0:
        lastDate = date
    dateClean = date.strftime("%m/%d/%Y")
    cost = row[115]
    description = row[113]
    if description == 0:
        description = ""
    cleanDescription = description[5:]
    cleanDescription = cleanDescription.replace(",", "")
    measuredDepth = row[70]

    account = row[114]
    accountClean = int(abs(account))
    if accountClean > 0 and cost != 0:
        accountIndex = wellEzAccounts.index(accountClean)
        wolfepakAccount = wolfepakActualAccounts[accountIndex]
        string = (
            dateClean
            + ","
            + str(wolfepakAccount)
            + ","
            + str(measuredDepth)
            + ","
            + str(cost)
            + ","
            + str(cleanDescription)
            + "\n"
        )

        dailyItemCostFp.write(string)

    if foundStartDate == 0 and measuredDepth > 0:
        foundStartDate = 1
        day = 0

    if date == lastDate:
        totalDailyCost = totalDailyCost + cost
    else:
        cumulativeCost = cumulativeCost + totalDailyCost
        if foundStartDate == 1:
            row = plannedCostDepth.iloc[day]
            lastDateClean = lastDate.strftime("%m/%d/%Y")
            outputString = (
                lastDateClean
                + ","
                + str(day)
                + ","
                + str(row["HOURS"])
                + ","
                + str(row["PLAN DEPTH"])
                + ","
                + str(row["PLAN COST"] * -1)
                + ","
                + str(row["DAILY"] * -1)
                + ","
                + str(totalDailyCost * -1)
                + ","
                + str(lastMeasuredDepth)
                + ","
                + str(cumulativeCost * -1)
                + "\n"
            )
            daysVsDepthFp.write(outputString)
            day = day + 1

        totalDailyCost = cost

    lastDate = date
    lastMeasuredDepth = measuredDepth

cumulativeCost = cumulativeCost + totalDailyCost
row = plannedCostDepth.iloc[day]
lastDateClean = lastDate.strftime("%m/%d/%Y")
outputString = (
    lastDateClean
    + ","
    + str(day)
    + ","
    + str(row["HOURS"])
    + ","
    + str(row["PLAN DEPTH"])
    + ","
    + str(row["PLAN COST"] * -1)
    + ","
    + str(row["DAILY"] * -1)
    + ","
    + str(totalDailyCost * -1)
    + ","
    + str(lastMeasuredDepth)
    + ","
    + str(cumulativeCost * -1)
    + "\n"
)

daysVsDepthFp.write(outputString)

for i in range(day + 1, len(plannedCostDepth)):
    row = plannedCostDepth.iloc[i]
    outputString = (
        ""
        + ","
        + str(i)
        + ","
        + str(row["HOURS"])
        + ","
        + str(row["PLAN DEPTH"])
        + ","
        + str(row["PLAN COST"] * -1)
        + ","
        + str(row["DAILY"] * -1)
        + ","
        + ""
        + ","
        + ""
        + ","
        + ""
        + "\n"
    )

    daysVsDepthFp.write(outputString)

dailyItemCostFp.close()
daysVsDepthFp.close()


print("yay")
