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

#fileName = pd.read_csv(r".\kingops\data\afe\kinga199cv1h\1.9.2023.csv")


pathCv1hAfe = r".\kingops\data\afe\kinga199cv1h"
folderList = os.listdir(pathCv1hAfe)


costItemListClean = []


totalCostAllFile = []
totalDateAllFile = []
totalDepthAllFile = []

for name in folderList:
    fullPathFileName = pathCv1hAfe + "\\" + name
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
            totalDailyCost = totalDailyCost + float(item)
        else:
            totalDailyCost = totalDailyCost + item

    #totalDailyCost = sum(float(costListClean))
    dateOfAfe = dateList[0]

    totalCostAllFile.append(totalDailyCost)
    totalDateAllFile.append(dateOfAfe)
    totalDepthAllFile.append(totalMeasuredDepthClean)


print("yay")
