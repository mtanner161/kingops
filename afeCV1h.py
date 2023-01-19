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


pathOfDailyReport = r".\kingops\data\afe\kinga199cv2h"
folderList = os.listdir(pathOfDailyReport)
plannedCostDepth = pd.read_excel(
    r".\kingops\data\afe\kinga199cv2hplanned.xlsx")

costItemListClean = []

totalCostAllFile = []
totalDateAllFile = []
totalDepthAllFile = []
totalCumulativeCost = []

for name in folderList:
    fullPathFileName = pathOfDailyReport + "\\" + name
    data = pd.read_csv(fullPathFileName)
    data = data.fillna(0)
    dateList = data["textbox58"].tolist()
    costList = data["textbox13.1"].tolist()
    costItemList = data["textbox34"].tolist()
    totalMeasuredDepthList = data["Textbox8.1"].tolist()
    trueVerticalDepthList = data["Textbox10.1"].tolist()
# getting total / measured depth
    totalMeasuredDepth = totalMeasuredDepthList[0]
    if type(totalMeasuredDepth) == float or type(totalMeasuredDepth) == int:
        totalMeasuredDepthClean = totalMeasuredDepth
    else:
        totalMeasuredDepthClean = float(totalMeasuredDepth.replace(",", ""))

    for i in range(0, len(costItemList)):
        itemString = costItemList[i]
        if itemString == 0:
            itemString = ""
        cleanString = itemString[5:]
        costItemListClean.append(cleanString)

    costListClean = list(dict.fromkeys(costList))
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

for i in totalCostAllFile:
    runningTotalCost += i
    runningCostList.append(runningTotalCost)


sortedData.sort(key=lambda michael: datetime.strptime(michael[0], '%m/%d/%Y'))

# begins writing to csv master file
fp = open(r".\kingops\data\afe\final\kinga199cv2hActual.csv", "w")

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

fp.close()

print("yay")
