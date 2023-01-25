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

budgetRawFile = pd.read_excel(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\afe\thurman23v\thurman23vAfeOg.xlsx")

masterMatchFile = pd.read_excel(
    r".\kingops\data\afe\welldriveWolfepakMatch.xlsx")

actualWellCostWolfepak = pd.read_excel(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\afe\thurman23v\thurman23vActualSpend.xlsx")

welldriveBudgetAccounts = masterMatchFile["Code WellDrive"].tolist()
wolfepakActualAccounts = masterMatchFile["Code WolfePak"].tolist()
wolfepakActualDesc = masterMatchFile["Description WolfePak"].tolist()

actualAccountCodeList = actualWellCostWolfepak["Account"].tolist()
actualAccountDescList = actualWellCostWolfepak["{Account Desc}"].tolist()
actualCostList = actualWellCostWolfepak["Amount"].tolist()

outputData = []
currentAccountCodes = []

fp = open(r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\afe\thurman23v\thurman23vAfeActualVarience.csv", "w")

headerString = "Account,Account Description,AFE Budget,Actual Spend,Varience\n"
fp.write(headerString)

for i in range(0, len(budgetRawFile)):
    # Budget row
    rowAfeBudgetRaw = budgetRawFile.iloc[i]
    afeBudgetAccountCode = rowAfeBudgetRaw["Account"]
    afeBudgetCost = rowAfeBudgetRaw["Cost"]

    indexBudget = welldriveBudgetAccounts.index(afeBudgetAccountCode)
    actualAccountCode = wolfepakActualAccounts[indexBudget]
    accountActualOccurrences = [j for j, x in enumerate(
        actualAccountCodeList) if x == actualAccountCode]

    if accountActualOccurrences == []:
        actualCostClean = 0
    else:
        actualCostClean = 0
        for m in range(0, len(accountActualOccurrences)):
            actualCostClean += actualCostList[accountActualOccurrences[m]]

    indexDesc = wolfepakActualAccounts.index(actualAccountCode)

    outputData.append([actualAccountCode, wolfepakActualDesc[indexDesc],
                      afeBudgetCost, actualCostClean])

    currentAccountCodes.append(actualAccountCode)

for k in range(0, len(actualAccountCodeList)):
    if actualAccountCodeList[k] not in currentAccountCodes:
        outputData.append(
            [actualAccountCodeList[k], actualAccountDescList[k], 0, actualCostList[k]])

outputData.sort(key=lambda x: x[0])
counter = 0

tom = 1

while tom == 1:
    account = outputData[counter][0]
    occurences = [j for j, x in enumerate(outputData) if x[0] == account]
    budgetCost = 0
    for m in range(0, len(occurences)):
        budgetCost += outputData[occurences[m]][2]

    actualCost = 0
    for m in range(0, len(occurences)):
        actualCost += outputData[occurences[m]][3]

    counter = occurences[len(occurences) - 1] + 1

    junk = 1

    varience = budgetCost - actualCost

    description = str(outputData[counter][1])
    betterDesc = description.replace(",", "")
    printString = (
        str(account)
        + ","
        + str(betterDesc)
        + ","
        + str(budgetCost)
        + ","
        + str(actualCost)
        + ","
        + str(varience)
        + "\n"
    )

    if counter == len(outputData) - 1:
        tom = 0

    fp.write(printString)

fp.close()


print("yay")
