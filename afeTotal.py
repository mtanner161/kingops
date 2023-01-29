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

headerString = "Date, Account Number, Depth, Daily Cost Estimate, Description\n"
dailyItemCostFp.write(headerString)

masterAfe = masterAfe.fillna(0)

for i in range(0, len(masterAfe)):
    row = masterAfe.iloc[i]
    date = row[0]
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
    if accountClean == 9217:
        junk = 1
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
            + str(cost * -1)
            + ","
            + str(cleanDescription)
            + "\n"
        )

        dailyItemCostFp.write(string)

    junk = 1

dailyItemCostFp.close()

print("yay")
