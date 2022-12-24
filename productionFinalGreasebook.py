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


# 30 Day Or Full? If False - only looking at last 30 days and appending.
fullProductionPull = False
numberOfDaysToPull = 30

fileName = (
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\totalAssetsProduction.csv"
)

load_dotenv()  # load ENV

# adding the Master Battery List for Analysis
masterBatteryList = pd.read_csv(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\masterBatteryList.csv"
)

# set some date variables we will need later
dateToday = dt.datetime.today()
todayYear = dateToday.strftime("%Y")
todayMonth = dateToday.strftime("%m")
todayDay = dateToday.strftime("%d")
dateYes = dateToday - timedelta(days=1)
yesDayString = dateYes.strftime("%d")

# Set production interval based on boolen
if fullProductionPull == True:
    productionInterval = "&start=2021-05-01&end="
else:
    dateThirtyDays = dateToday - timedelta(days=numberOfDaysToPull)
    dateThirtyDaysYear = dateThirtyDays.strftime("%Y")
    dateThirtyDaysMonth = dateThirtyDays.strftime("%m")
    dateThirtyDaysDay = dateThirtyDays.strftime("%d")
    productionInterval = (
        "&start="
        + dateThirtyDaysYear
        + "-"
        + dateThirtyDaysMonth
        + "-"
        + dateThirtyDaysDay
        + "&end="
    )

# Master API call to Greasebooks
url = (
    "https://integration.greasebook.com/api/v1/batteries/daily-production?apiKey="
    + str(os.getenv("GREASEBOOK_API_KEY"))
    + productionInterval
    + todayYear
    + "-"
    + todayMonth
    + "-"
    + todayDay
)

# make the API call
response = requests.request(
    "GET",
    url,
)

responseCode = response.status_code  # sets response code to the current state

# parse as json string
results = response.json()
# setting to length of results
numEntries = len(results)

if responseCode == 200:
    print("Status Code is 200")
    print(str(numEntries) + " entries read")
else:
    print("The Status Code: " + str(response.status_code))

# checks if we need to pull all the data or just last specificed
if fullProductionPull == False:
    # Opening Master CSV for total asset production
    totalAssetProduction = pd.read_csv(fileName)
else:
    headerList = [
        "Date",
        "Client",
        "Battery Name",
        "Oil Volume",
        "Gas Volume",
        "Water Volume",
        "Last 7 Day Oil Average",
        "Last 14 Day Oil Average",
        "Last 7 Day Gas Average",
        "Last 14 Day Gas Average",
    ]
    totalAssetProduction = pd.DataFrame(
        0, index=np.arange(numEntries - 1), columns=headerList
    )

# a bunch of variables the below loop needs
wellIdList = []
wellNameList = []
runningTotalOil = []
runningTotalGas = []
numberOfDaysBattery = []
wellOilVolumeTwoDayAgo = np.zeros([200], dtype=object)
wellGasVolumeTwoDayAgo = np.zeros([200], dtype=object)
avgOilList = []
avgGasList = []
last14DayListOil = []
last14DayListGas = []
fourteenDayOilData = np.zeros([200, 14], dtype=float)
sevenDayOilData = np.zeros([200, 7], dtype=float)
fourteenDayGasData = np.zeros([200, 14], dtype=float)
sevenDayGasData = np.zeros([200, 7], dtype=float)
batteryIdCounterFourteen = np.zeros([200], dtype=int)
batteryIdCounterSeven = np.zeros([200], dtype=int)
rollingFourteenDayPerWellOil = np.zeros([200], dtype=float)
rollingFourteenDayPerWellGas = np.zeros([200], dtype=float)
gotDayData = np.full([200], False)
totalOilVolume = 0
totalGasVolume = 0
totalWaterVolume = 0
yesTotalOilVolume = 0
yesTotalGasVolume = 0
yesTotalWaterVolume = 0
twoDayOilVolume = 0
twoDayGasVolume = 0
threeDayOilVolume = 0
threeDayGasVolume = 0
lastWeekTotalOilVolume = 0
lastWeekTotalGasVolume = 0

# Convert all dates to str for comparison rollup
todayYear = int(dateToday.strftime("%Y"))
todayMonth = int(dateToday.strftime("%m"))
todayDay = int(dateToday.strftime("%d"))

dateYesterday = dateToday - timedelta(days=1)
dateTwoDaysAgo = dateToday - timedelta(days=2)
dateThreeDaysAgo = dateToday - timedelta(days=3)
dateLastWeek = dateToday - timedelta(days=8)

yesYear = int(dateYesterday.strftime("%Y"))
yesMonth = int(dateYesterday.strftime("%m"))
yesDay = int(dateYesterday.strftime("%d"))

twoDayYear = int(dateTwoDaysAgo.strftime("%Y"))
twoDayMonth = int(dateTwoDaysAgo.strftime("%m"))
twoDayDay = int(dateTwoDaysAgo.strftime("%d"))

threeDayYear = int(dateThreeDaysAgo.strftime("%Y"))
threeDayMonth = int(dateThreeDaysAgo.strftime("%m"))
threeDayDay = int(dateThreeDaysAgo.strftime("%d"))

lastWeekYear = int(dateLastWeek.strftime("%Y"))
lastWeekMonth = int(dateLastWeek.strftime("%m"))
lastWeekDay = int(dateLastWeek.strftime("%d"))

# if not pulling all of production - then just get the list of dates to parse
if fullProductionPull == False:
    listOfDates = totalAssetProduction["Date"].to_list()  # gets list of dates
    # finds out what date is last
    lastRow = totalAssetProduction.iloc[len(totalAssetProduction) - 1]
    dateOfLastRow = lastRow["Date"]
    splitDate = re.split("/", str(dateOfLastRow))  # splits date correct
    day = int(splitDate[1])  # gets the correct day
    month = int(splitDate[0])  # gets the correct month
    year = int(splitDate[2])  # gets the correct
    referenceTime15Day = dt.date(year, month, day) - \
        timedelta(days=15)  # creates a reference time
    dateOfInterest = referenceTime15Day.strftime(
        "%#m/%#d/%Y")  # converts to string
    startingIndex = listOfDates.index(
        dateOfInterest)  # create index surrounding
else:
    startingIndex = 0
    referenceTime15Day = dt.date(2021, 5, 1)

# Gets list of Battery id's that are clean for printing
listOfBatteryIds = masterBatteryList["Id"].tolist()
goodBatteryNames = masterBatteryList["Pretty Battery Name"].tolist()
pumperNames = masterBatteryList["Pumper"].tolist()

j = 0

priorDay = -999

initalSizeOfTotalAssetProduction = len(totalAssetProduction)

# MASTER loop that goes through each of the items in the response
for currentRow in range(numEntries - 1, 0, -1):
    row = results[currentRow]  # get row i in results
    keys = list(row.items())  # pull out the headers

    # set some intial variables for core logic
    oilDataExist = False
    gasDataExist = False
    waterDataExist = False
    oilVolumeClean = 0
    gasVolumeClean = 0
    waterVolumeClean = 0

    # Loops through each exposed API variable. 5If it exisits - get to correct variable
    for idx, key in enumerate(keys):
        if key[0] == "batteryId":
            batteryId = row["batteryId"]
        elif key[0] == "batteryName":
            batteryName = row["batteryName"]
        elif key[0] == "date":
            date = row["date"]
        # if reported, set to True, otherwise leave false
        elif key[0] == "oil":
            oilDataExist = True
            oilVolumeRaw = row["oil"]
            if oilVolumeRaw == "":  # if "" means it not reported
                oilVolumeClean = 0
            else:
                oilVolumeClean = oilVolumeRaw
        elif key[0] == "mcf":  # same as oil
            gasDataExist = True
            gasVolumeRaw = row["mcf"]
            if gasVolumeRaw == "":
                gasVolumeClean = 0
            else:
                gasVolumeClean = gasVolumeRaw
        elif key[0] == "water":  # same as oil
            waterDataExist = True
            waterVolumeRaw = row["water"]
            if waterVolumeRaw == "":
                waterVolumeClean = 0
            else:
                waterVolumeClean = waterVolumeRaw

    # spliting date correctly
    splitDate = re.split("T", date)
    splitDate2 = re.split("-", splitDate[0])
    year = int(splitDate2[0])
    month = int(splitDate2[1])
    day = int(splitDate2[2])

    if priorDay == day or priorDay == -999:
        newDay = False
    else:
        newDay = True

    # CORE LOGIC BEGINS FOR MASTER LOOP

    # checks to see if last day had an entry for every well - if not fixes it to include
    if newDay == True:
        for counter in range(0, len(wellIdList)):
            if gotDayData[counter] != True:
                fourteenDayOilData[counter][batteryIdCounterFourteen[counter]] = 0
                fourteenDayGasData[counter][batteryIdCounterFourteen[counter]] = 0
                sevenDayOilData[counter][batteryIdCounterSeven[counter]] = 0
                sevenDayGasData[counter][batteryIdCounterSeven[counter]] = 0
                lastFourteenDayTotalOil = sum(
                    fourteenDayOilData[counter]) / (14)
                lastFourteenDayTotalGas = sum(
                    fourteenDayGasData[counter]) / (14)
                rollingFourteenDayPerWellOil[counter] = lastFourteenDayTotalOil
                rollingFourteenDayPerWellGas[counter] = lastFourteenDayTotalGas
                if year == twoDayYear and month == twoDayMonth and day == twoDayDay:
                    wellOilVolumeTwoDayAgo[counter] = "No Data Reported"
                    wellGasVolumeTwoDayAgo[counter] = "No Data Reported"
                if batteryIdCounterFourteen[counter] < 13:
                    batteryIdCounterFourteen[counter] = batteryIdCounterFourteen[counter] + 1
                else:
                    batteryIdCounterFourteen[counter] = 0
                if batteryIdCounterSeven[counter] < 6:
                    batteryIdCounterSeven[counter] = batteryIdCounterSeven[counter] + 1
                else:
                    batteryIdCounterSeven[counter] = 0

    # resets gotDayData to False as we loop the current day
    if newDay == True:
        gotDayData = np.full((200), False)
        newDay = False

    # Colorado set MCF to zero
    if batteryId == 25381 or batteryId == 25382:
        gasVolumeClean = 0

    if batteryId in wellIdList:  # builds a list of all battery ID's with data
        index = wellIdList.index(batteryId)
        # running total of oil/gas and number of reporeted days for each reponse
        runningTotalOil[index] = runningTotalOil[index] + oilVolumeClean
        runningTotalGas[index] = runningTotalGas[index] + gasVolumeClean
        numberOfDaysBattery[index] = numberOfDaysBattery[index] + 1

        if newDay == False:
            gotDayData[index] = True

        # 14 day running average code
        fourteenDayOilData[index][batteryIdCounterFourteen[index]
                                  ] = oilVolumeClean
        fourteenDayGasData[index][batteryIdCounterFourteen[index]
                                  ] = gasVolumeClean
        lastFourteenDayTotalOil = sum(fourteenDayOilData[index]) / (14)
        lastFourteenDayTotalGas = sum(fourteenDayGasData[index]) / (14)
        if batteryIdCounterFourteen[index] < 13:
            batteryIdCounterFourteen[index] = batteryIdCounterFourteen[index] + 1
        else:
            batteryIdCounterFourteen[index] = 0

        # seven day running average code
        sevenDayOilData[index][batteryIdCounterSeven[index]] = oilVolumeClean
        sevenDayGasData[index][batteryIdCounterSeven[index]] = gasVolumeClean
        lastSevenDayTotalOil = sum(sevenDayOilData[index]) / (7)
        lastSevenDayTotalGas = sum(sevenDayGasData[index]) / (7)

        if batteryIdCounterSeven[index] < 6:
            batteryIdCounterSeven[index] = batteryIdCounterSeven[index] + 1
        else:
            batteryIdCounterSeven[index] = 0
    else:  # if batteryId is not in list, then add to list and roll up
        wellIdList.append(batteryId)
        index = wellIdList.index(batteryId)
        runningTotalOil.insert(index, oilVolumeClean)
        runningTotalGas.insert(index, gasVolumeClean)
        numberOfDaysBattery.insert(index, 1)
        wellNameList.insert(index, batteryName)
        lastSevenDayTotalOil = oilVolumeClean
        lastFourteenDayTotalOil = oilVolumeClean
        lastSevenDayTotalGas = gasVolumeClean
        lastFourteenDayTotalGas = gasVolumeClean
        if newDay == False or currentRow == (numEntries - 1):
            gotDayData[index] = True

    # Summing today, yesterday and last week oil gas and water
    if year == todayYear and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolumeClean
        totalGasVolume = totalGasVolume + gasVolumeClean
        totalWaterVolume = totalWaterVolume + waterVolumeClean

    rollingFourteenDayPerWellOil[index] = lastFourteenDayTotalOil
    rollingFourteenDayPerWellGas[index] = lastFourteenDayTotalGas

    # Checks to see if the parsed day is equal to two days ago - adds oil/gas volume to counter
    if year == twoDayYear and month == twoDayMonth and day == twoDayDay:
        twoDayOilVolume = twoDayOilVolume + oilVolumeClean
        twoDayGasVolume = twoDayGasVolume + gasVolumeClean

        # for two day ago - checks if batteryId is in wellIdList
        if batteryId in wellIdList:  # if yes, does data exisit and logs correct boolean
            if oilDataExist == True:
                wellOilVolumeTwoDayAgo[index] = oilVolumeClean
            else:
                wellOilVolumeTwoDayAgo[index] = "No Data Reported"
            if gasDataExist == True:
                wellGasVolumeTwoDayAgo[index] = gasVolumeClean
            else:
                wellGasVolumeTwoDayAgo[index] = "No Data Reported"

    # Checks to see if the parsed day is equal to yesterday days ago - adds oil/gas volume to counter
    if year == yesYear and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolumeClean
        yesTotalGasVolume = yesTotalGasVolume + gasVolumeClean

    # Checks to see if the parsed day is equal to three days ago - adds oil/gas volume to counter
    if year == threeDayYear and month == threeDayMonth and day == threeDayDay:
        threeDayOilVolume = threeDayOilVolume + oilVolumeClean
        threeDayGasVolume = threeDayGasVolume + gasVolumeClean

    # Checks to see if the parsed day is equal to last week - adds oil/gas volume to counter
    if year == lastWeekYear and month == lastWeekMonth and day == lastWeekDay:
        lastWeekTotalOilVolume = lastWeekTotalOilVolume + oilVolumeClean
        lastWeekTotalGasVolume = lastWeekTotalGasVolume + gasVolumeClean

    # Splits battery name up
    splitString = re.split("-|–", batteryName)
    # sets client name to client name from ETX/STX and GCT
    clientName = splitString[0]
    # if field name exisits - add the batteryName
    if len(splitString) >= 3:
        batteryNameBetter = splitString[1]
        for i in range(2, len(splitString)):
            batteryNameBetter = batteryNameBetter + "-" + splitString[i]
    else:
        batteryNameBetter = splitString[1]

    index = listOfBatteryIds.index(batteryId)
    goodBatteryNameWrite = goodBatteryNames[index]

    # cleaning up the strings for outputing
    batteryNameBetter = batteryNameBetter.replace(" ", "")
    clientName = clientName.replace(" ", "")
    dateString = str(month) + "/" + str(day) + "/" + str(year)

    # grabs current time
    currentTime = dt.date(year, month, day)

    # switches clinet names to more easily viewable items
    if currentTime >= referenceTime15Day:
        if clientName == "CWS":
            clientName = "South Texas"
        elif clientName == "Peak":
            clientName = "East Texas"
        elif clientName == "Otex":
            clientName = "Gulf Coast"
        elif clientName == "Midcon":
            clientName = "Midcon"
        elif clientName == "Wellman":
            clientName = "Permian Basin"
        elif clientName == "Wellington":
            clientName = "Colorado"

        # creates a newRow
        newRow = [
            dateString,
            clientName,
            goodBatteryNameWrite,
            str(oilVolumeClean),
            str(gasVolumeClean),
            str(waterVolumeClean),
            str(lastSevenDayTotalOil),
            str(lastFourteenDayTotalOil),
            str(lastSevenDayTotalGas),
            str(lastFourteenDayTotalGas),
        ]
        # STARTING HERE WITH IF STATEMENT
        if (startingIndex + j) > (initalSizeOfTotalAssetProduction - 1):
            totalAssetProduction.loc[startingIndex + j] = newRow
        else:
            totalAssetProduction.iloc[startingIndex + j] = newRow

        j = j + 1

    priorDay = day

# creates an running average
for i in range(0, len(wellIdList)):
    avgOilList.insert(i, runningTotalOil[i] / numberOfDaysBattery[i])
    avgGasList.insert(i, runningTotalGas[i] / numberOfDaysBattery[i])

fpReported = open(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\yesterdayWellReport.csv", "w"
)
headerString = "Battery ID,Battery Name,Oil Production,14-day Oil Average,Gas Production,14-day Gas Average\n"
fpReported.write(headerString)

for i in range(0, len(wellIdList)):
    if i < len(rollingFourteenDayPerWellOil) and i < len(rollingFourteenDayPerWellGas):
        outputString = (
            str(wellIdList[i])
            + ","
            + wellNameList[i]
            + ","
            + str(wellOilVolumeTwoDayAgo[i])
            + ","
            + str(rollingFourteenDayPerWellOil[i])
            + ","
            + str(wellGasVolumeTwoDayAgo[i])
            + ","
            + str(rollingFourteenDayPerWellGas[i])
            + "\n"
        )
    else:
        outputString = (
            str(wellIdList[i])
            + ","
            + wellNameList[i]
            + ","
            + "-"
            + ","
            + str(avgOilList[i])
            + ","
            + "-"
            + ","
            + str(avgGasList[i])
            + "\n"
        )

    fpReported.write(outputString)

fpReported.close()

notReportedListOil = []
notReportedListGas = []
pumperNotReportedList = []

for i in range(0, len(wellIdList)):
    if wellOilVolumeTwoDayAgo[i] == "No Data Reported" and rollingFourteenDayPerWellOil[i] > 0:
        index = listOfBatteryIds.index(wellIdList[i])
        goodBatteryNameWrite = goodBatteryNames[index]
        notReportedListOil.append(goodBatteryNameWrite)
        pumperName = pumperNames[index]
        if pumperName not in pumperNotReportedList:
            pumperNotReportedList.append(pumperName)
    if wellGasVolumeTwoDayAgo[i] == "No Data Reported" and rollingFourteenDayPerWellGas[i] > 0:
        index = listOfBatteryIds.index(wellIdList[i])
        goodBatteryNameWrite = goodBatteryNames[index]
        notReportedListGas.append(goodBatteryNameWrite)
        pumperName = pumperNames[index]
        if pumperName not in pumperNotReportedList:
            pumperNotReportedList.append(pumperName)

# Oil and gas daily change numbers
oilChangeDaily = round((twoDayOilVolume - threeDayOilVolume), 2)
gasChangeDaily = round((twoDayGasVolume - threeDayGasVolume), 2)
oilSevenDayPercent = round(
    (twoDayOilVolume - lastWeekTotalOilVolume) / lastWeekTotalOilVolume, 1
)
gasSevenDayPercent = round(
    (twoDayGasVolume - lastWeekTotalGasVolume) / lastWeekTotalGasVolume, 1
)

if oilChangeDaily > 0:
    increaseDecreaseOil = "Increase"
else:
    increaseDecreaseOil = "Decline"

if gasChangeDaily > 0:
    increaseDecreaseGas = "Increase"
else:
    increaseDecreaseGas = "Decline"

totalAssetProduction.to_csv(
    fileName,
    index=False,
)

# Opens Oil Change File for daily specific percent change calculations
oilGasCustomNumbersFp = open(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\oilgascustomnumbers.csv",
    "w",
)

headerString = "Daily Oil Change,Daily Gas Change, 7-day Oil Percent Change, 7-day Gas Percent Change, Two Day Ago Oil Volume, Two Day Ago Gas Volume, Increase/Decrease Oil, Increase/Decrease Gas\n"

oilGasCustomNumbersFp.write(headerString)

outputString = (
    str(oilChangeDaily)
    + ","
    + str(gasChangeDaily)
    + ","
    + str(oilSevenDayPercent)
    + ","
    + str(gasSevenDayPercent)
    + ","
    + str(twoDayOilVolume)
    + ","
    + str(twoDayGasVolume)
    + ","
    + increaseDecreaseOil
    + ","
    + increaseDecreaseGas
)

oilGasCustomNumbersFp.write(outputString)
oilGasCustomNumbersFp.close()

# print out the volumes for data check while model is running
print("Today Oil Volume: " + str(totalOilVolume))
print("Today Gas Volume: " + str(totalGasVolume))
print("Yesterday Oil Volume: " + str(yesTotalOilVolume))
print("Yesterday Gas Volume: " + str(yesTotalGasVolume))
print("Two Day Ago Oil Volume: " + str(twoDayOilVolume))
print("Two Day Ago Gas Volume: " + str(twoDayGasVolume))
print("Three Day Ago Oil Volume: " + str(threeDayOilVolume))
print("Three Day Ago Gas Volume: " + str(threeDayGasVolume))
print("Last Week Oil Volume: " + str(lastWeekTotalOilVolume))
print("Last Week Gas Volume: " + str(lastWeekTotalGasVolume))
print("Daily Change Oil Volume: " + str(oilChangeDaily))
print("Daily Change Gas Volume: " + str(gasChangeDaily))
print("Percent Oil Volume: " + str(oilSevenDayPercent))
print("Percent Gas Volume: " + str(gasSevenDayPercent))


print("Done Rolling Up Production")
