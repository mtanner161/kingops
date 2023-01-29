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

nameOfWell = "kinga199cv2h"

pathOfDailyReport = '.\\kingops\\data\\afe' + '\\' + nameOfWell + "\\" + "daily"
pathOfAfe = r".\kingops\data\afe" + "\\" + nameOfWell
folderList = os.listdir(pathOfDailyReport)
plannedCostFile = pathOfAfe + "\\" + nameOfWell + "planned.xlsx"
plannedCostDepth = pd.read_excel(plannedCostFile)
masterMatchFile = pd.read_excel(
    r".\kingops\data\afe\welldriveWolfepakMatch.xlsx")

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

headerString = "Date, Account Number, Daily Cost Estimate, Description\n"
dailyItemCostFp.write(headerString)

for name in folderList:
    fullPathFileName = pathOfDailyReport + "\\" + name
    data = pd.read_csv(fullPathFileName)
    data = data.fillna(0)
    dateList = data["textbox58"].tolist()
    dateOfEstimatedCost = dateList[0]
    costEstimatedList = data["textbox13.1"].tolist()
    accountEstimatedList = data["textbox37"].tolist()
    costEstimatedCostList = data["textbox38"].tolist()
    descriptionEstimatedList = data["textbox34"].tolist()

    totalMeasuredDepthList = data["Textbox8.1"].tolist()
    trueVerticalDepthList = data["Textbox10.1"].tolist()

    for j in range(0, len(costEstimatedCostList)):
        itemCost = costEstimatedCostList[j]
        if itemCost != 0:
            itemCostCleanStepOne = itemCost.replace(",", "")
            itemCostCleanStepTwo = itemCostCleanStepOne.replace("$", "")
            itemCostClean = float(itemCostCleanStepTwo)
        else:
            itemCostClean = ""
        wellEzAccount = accountEstimatedList[j]
        wellEzAccountClean = int(abs(wellEzAccount))
        wellEzDescription = descriptionEstimatedList[j]

        if wellEzAccountClean > 0:
            accountIndex = wellEzAccounts.index(wellEzAccountClean)
            wolfepakAccount = wolfepakActualAccounts[accountIndex]
            string = (
                str(dateOfEstimatedCost)
                + ","
                + str(wolfepakAccount)
                + ","
                + str(itemCostClean)
                + ","
                + str(wellEzDescription)
                + "\n"
            )

            dailyItemCostFp.write(string)

# getting total / measured depth
    totalMeasuredDepth = totalMeasuredDepthList[0]
    if type(totalMeasuredDepth) == float or type(totalMeasuredDepth) == int:
        totalMeasuredDepthClean = totalMeasuredDepth
    else:
        totalMeasuredDepthClean = float(totalMeasuredDepth.replace(",", ""))

    for i in range(0, len(descriptionEstimatedList)):
        itemString = descriptionEstimatedList[i]
        if itemString == 0:
            itemString = ""
        cleanString = itemString[5:]
        costItemListClean.append(cleanString)

    costListClean = list(dict.fromkeys(costEstimatedList))
    totalDailyCost = 0

    for j in range(0, len(costListClean)):
        item = costListClean[j]
        if type(item) == str:
            item = item.replace(",", "")
            item = item.replace("$", "")
            item = item.replace("(", "")
            item = item.replace(")", "")
            totalDailyCost = totalDailyCost + float(item)
        else:
            totalDailyCost = totalDailyCost + item

    # totalDailyCost = sum(float(costListClean))
    dateOfAfe = dateList[0]

    totalCostAllFile.append(totalDailyCost)
    totalDateAllFile.append(dateOfAfe)
    totalDepthAllFile.append(totalMeasuredDepthClean)

# sort the data by date earliest to latest
sortedData = []

for i in range(0, len(totalDateAllFile)):
    date = totalDateAllFile[i]
    cost = totalCostAllFile[i]
    depth = totalDepthAllFile[i]
    sortedData.append([date, cost, depth])

runningCostList = []
runningTotalCost = 0

sortedData.sort(key=lambda michael: datetime.strptime(michael[0], '%m/%d/%Y'))

sortedRunningCostList = []

# sorts of the the running cost list
for i in range(0, len(sortedData)):
    sortedRunningCostList.append(sortedData[i][1])

for i in sortedRunningCostList:
    runningTotalCost += i
    runningCostList.append(runningTotalCost)

pathOfActual = pathOfAfe + "\\" + nameOfWell + "Actual.csv"

# begins writing to csv master file
fp = open(pathOfActual, "w")

# write and print header
header = "Date, Days, Hours, Planned Depth, Planned Cost, Daily, Actual Cost, Actual Depth, Cumulative Cost\n"
fp.write(header)

for i in range(0, len(plannedCostDepth)):
    plannedDays = plannedCostDepth["DAYS"][i]
    plannedCost = plannedCostDepth["PLAN COST"][i] * -1
    plannedDepth = plannedCostDepth["PLAN DEPTH"][i]
    hours = plannedCostDepth["HOURS"][i]
    dailyCost = plannedCostDepth["DAILY"][i] * -1

    if i < len(sortedData):
        actualDate = sortedData[i][0]
        actualCost = sortedData[i][1]
        actualDepth = sortedData[i][2]
        cumulativeCost = runningCostList[i] * -1
    else:
        actualDate = ""
        actualCost = ""
        actualDepth = ""
        cumulativeCost = ""

    if actualDepth == 0 and i != 0:
        actualDepth = lastActualDepth

    outputString = (
        str(actualDate)
        + ","
        + str(plannedDays)
        + ","
        + str(hours)
        + ","
        + str(plannedDepth)
        + ","
        + str(plannedCost)
        + ","
        + str(dailyCost)
        + ","
        + str(actualCost)
        + ","
        + str(actualDepth)
        + ","
        + str(cumulativeCost)
        + "\n"
    )

    fp.write(outputString)

    lastActualDepth = actualDepth

dailyItemCostFp.close()
fp.close()

print("yay")
