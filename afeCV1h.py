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

fileName = pd.read_csv(r".\kingops\data\afe\kinga199cv1h\1.9.2023.csv")
fileNameExcel = pd.read_excel(
    r".\kingops\data\afe\kinga199cv1h\1.1.2023test.xlsx")

costItemListClean = []

fileName = fileName.fillna(0)
dateList = fileName["textbox58"].tolist()
costList = fileName["textbox13.1"].tolist()
costItemList = fileName["textbox34"].tolist()
totalMeasuredDepthList = fileName["Textbox8.1"].tolist()
trueVerticalDepthList = fileName["Textbox10.1"].tolist()
# getting total / measured depth
totalMeasuredDepth = totalMeasuredDepthList[0]
trueVerticalDepth = trueVerticalDepthList[0]
trueVerticalDepthClean = int(trueVerticalDepth.replace(",", ""))
totalMeasuredDepthClean = int(totalMeasuredDepth.replace(",", ""))

for i in range(0, len(costItemList)):
    itemString = costItemList[i]
    if itemString == 0:
        itemString = ""
    cleanString = itemString[5:]
    costItemListClean.append(cleanString)

costListClean = list(dict.fromkeys(costList))

columns = fileName.columns
print(columns)
print(type(costItemList[3]))
totalDailyCost = sum(costListClean)
dateOfAfe = dateList[0]


print("yay")
