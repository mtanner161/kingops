## Import packages needed
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

debugMode = True  ## Set to False to Add Colorado, set to True to Debug and not add

import chandlerAssetRollUp  # Runs chandler asset

load_dotenv()  # load ENV

folder_path = r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Clients\King Operating\Finance - Reservoir\Daily Production Data\Colorado"
file_type = "\*xlsx"  # set to look for xlsx
files = glob.glob(folder_path + file_type)  # creates file path
maxFileLead = max(files, key=os.path.getctime)

dailyColorado = pd.read_excel(maxFileLead)


dailyColoradoClean = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\coloradoAssets.csv"
)

dailyChandlerAsset = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\chandlerAssetsDaily.csv"
)

##adding the Master Battery List for Analysis
masterBatteryList = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\masterBatteryList.csv"
)

# check date on Colorado
dailyColoradoDate = dailyColorado.iloc[0, 7]
print(dailyColoradoDate)

# set some date variables we will need later
dateToday = dt.datetime.today()
todayYear = dateToday.strftime("%Y")
todayMonth = dateToday.strftime("%m")
todayDay = dateToday.strftime("%d")
dateYes = dateToday - timedelta(days=1)
yesDayString = dateYes.strftime("%d")

# set ETX/STX and GCT API url
url = (
    "https://integration.greasebook.com/api/v1/batteries/daily-production?apiKey="
    + os.getenv("GREASEBOOK_API_KEY")
    + "&start=2021-05-01&end="
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


# print response code, should = 200
print(response.status_code)
# parse as json string
results = response.json()
# setting to length of results
numEntries = len(results)

## Opening Master CSV for total asset production
totalAssetProductionFp = open(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\totalAssetsProduction.csv",
    "w",
)
# write the header string for master file
headerString = (
    "Date,"
    + "Client,"
    + "Battery Name ,"
    + "Oil Volume,"
    + "Gas Volume,"
    + "Water Volume\n"
)

totalAssetProductionFp.write(headerString)  # write the header string
# a bunch of variables the below loop needs
noOilList = []
noGasList = []
totalOilVolume = 0
totalGasVolume = 0
totalWaterVolume = 0
yesTotalOilVolume = 0
yesTotalGasVolume = 0
yesTotalWaterVolume = 0
twoDayOilVolume = 0
twoDayGasVolume = 0
lastWeekTotalOilVolume = 0
lastWeekTotalGasVolume = 0

## Convert all dates to str for comparison rollup
todayYear = int(dateToday.strftime("%Y"))
todayMonth = int(dateToday.strftime("%m"))
todayDay = int(dateToday.strftime("%d"))

dateYesterday = dateToday - timedelta(days=1)
dateTwoDaysAgo = dateToday - timedelta(days=2)
dateLastWeek = dateToday - timedelta(days=7)

yesYear = int(dateYesterday.strftime("%Y"))
yesMonth = int(dateYesterday.strftime("%m"))
yesDay = int(dateYesterday.strftime("%d"))

twoDayYear = int(dateTwoDaysAgo.strftime("%Y"))
twoDayMonth = int(dateTwoDaysAgo.strftime("%m"))
twoDayDay = int(dateTwoDaysAgo.strftime("%d"))

lastWeekYear = int(dateLastWeek.strftime("%Y"))
lastWeekMonth = int(dateLastWeek.strftime("%m"))
lastWeekDay = int(dateLastWeek.strftime("%d"))


## BEGIN CODE FOR ETX STX and GCT

# master loop for greasebook API
for i in range(0, numEntries):
    row = results[i]  # get row i in results
    keys = list(row.items())  # pull out the headers
    # set each volume to empty string
    oilVolume = ""
    gasVolume = ""
    waterVolume = ""

    # Loops through each exposed API variable. If it exisits - get to correct variable
    for idx, key in enumerate(keys):
        if key[0] == "batteryId":
            batteryId = row["batteryId"]
        elif key[0] == "batteryName":
            batteryName = row["batteryName"]
        elif key[0] == "date":
            date = row["date"]
        elif key[0] == "oil":
            oilVolume = row["oil"]
        elif key[0] == "mcf":
            gasVolume = row["mcf"]
        elif key[0] == "water":
            waterVolume = row["water"]
    # if empty, replace with 0 for printing
    if oilVolume == "":
        oilVolume = 0
    if gasVolume == "":
        gasVolume = 0
    if waterVolume == "":
        waterVolume = 0
    # spliting date correctly
    splitDate = re.split("T", date)
    splitDate2 = re.split("-", splitDate[0])
    year = splitDate2[0]
    month = int(splitDate2[1])
    day = int(splitDate2[2])

    #### in progress
    if year == str(yesYear) and month == yesMonth and day == yesDay and oilVolume == 0:
        noOilList.append(batteryName)

    if year == str(yesYear) and month == yesMonth and day == yesDay and gasVolume == 0:
        noGasList.append(batteryName)

    ## Summing today, yesterday and last week oil gas and water
    if year == str(todayYear) and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolume
        totalGasVolume = totalGasVolume + gasVolume
        totalWaterVolume = totalWaterVolume + waterVolume

    if year == str(yesYear) and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolume
        yesTotalGasVolume = yesTotalGasVolume + gasVolume

    if year == str(twoDayYear) and month == twoDayMonth and day == twoDayDay:
        twoDayOilVolume = twoDayOilVolume + oilVolume
        twoDayGasVolume = twoDayGasVolume + gasVolume

    if year == str(lastWeekYear) and month == lastWeekMonth and day == lastWeekDay:
        lastWeekTotalOilVolume = lastWeekTotalOilVolume + oilVolume
        lastWeekTotalGasVolume = lastWeekTotalGasVolume + gasVolume

    ## Splits battery name up
    splitString = re.split("-|–", batteryName)
    clientName = splitString[0]  # sets client name to client name from ETX/STX and GCT
    # if field name exisits - add the batteryName
    if len(splitString) >= 3:
        batteryNameBetter = splitString[1]
        for i in range(2, len(splitString)):
            batteryNameBetter = batteryNameBetter + "-" + splitString[i]
    else:
        batteryNameBetter = splitString[1]

    # cleaning up the strings for outputing
    batteryNameBetter = batteryNameBetter.replace(" ", "")
    clientName = clientName.replace(" ", "")
    dateString = str(month) + "/" + str(day) + "/" + str(year)
    # create outstring for first row of total assets
    outputString = (
        dateString
        + ","
        + clientName
        + ","
        + batteryNameBetter
        + ","
        + str(oilVolume)
        + ","
        + str(gasVolume)
        + ","
        + str(waterVolume)
        + "\n"
    )
    # replace with client offical names
    outputString = outputString.replace("Peak", "KOEAS")
    outputString = outputString.replace("CWS", "KOSOU")
    outputString = outputString.replace("Otex", "KOGCT")
    outputString = outputString.replace("Midcon", "KOAND")
    outputString = outputString.replace("Wellman", "KOPRM")

    totalAssetProductionFp.write(outputString)

###### COLORADO CODE BEGINS
## I reuse variables for oilVolume etc for ease

clientName = "WELOP"  ## Changes client name to WELOP

# create a nice yesterday date string
yesDateString = str(yesMonth) + "/" + str(yesDay) + "/" + str(yesYear)

# get lastest Colorado Data from specific folder and set to correct values
northBatteryGas = dailyColorado.iloc[5, 2]
northBatteryWater = dailyColorado.iloc[4, 2]
northBatteryOil = dailyColorado.iloc[3, 2]
northBatteryWellCount = dailyColorado.iloc[2, 2]
southBatteryGas = dailyColorado.iloc[5, 5]
southBatteryWater = dailyColorado.iloc[4, 5]
southBatteryOil = dailyColorado.iloc[3, 5]
southBatteryWellCount = dailyColorado.iloc[2, 5]

# creating lists for each north and south battery
northList = []
southList = []
northList.append(yesDateString)  ## set each time
southList.append(yesDateString)
northList.append(clientName)
southList.append(clientName)

# adding the new variables to correct list
northList.append("North")
northList.append(northBatteryOil)
northList.append(northBatteryGas)
northList.append(northBatteryWater)
southList.append("South")
southList.append(southBatteryOil)
southList.append(southBatteryGas)
southList.append(southBatteryWater)

if debugMode == False:
    # adding the new data to the clean Colorado table for next day run
    dailyColoradoClean.loc[len(dailyColoradoClean.index)] = northList
    dailyColoradoClean.loc[len(dailyColoradoClean.index)] = southList


## Master Loop for Colorado Assets
for i in range(0, len(dailyColoradoClean)):
    # sets correct variables for calculations (resttting some)
    row = dailyColoradoClean.iloc[i]
    date = row["Date"]
    batteryName = row["Battery Name"]
    oilVolume = row["Oil Volume"]
    gasVolume = row["Gas Volume"]
    waterVolume = row["Water Volume"]
    splitDate = re.split("/", date)
    day = int(splitDate[1])
    month = int(splitDate[0])
    year = int(splitDate[2])
    # test for date and sums
    if year == todayYear and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolume
        totalGasVolume = totalGasVolume + gasVolume
        totalWaterVolume = totalWaterVolume + waterVolume

    if year == yesYear and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolume
        yesTotalGasVolume = yesTotalGasVolume + gasVolume
        yesTotalWaterVolume = yesTotalWaterVolume + waterVolume

    if year == twoDayYear and month == twoDayMonth and day == twoDayDay:
        twoDayOilVolume = twoDayOilVolume + oilVolume
        twoDayGasVolume = twoDayGasVolume + gasVolume

    if year == lastWeekYear and month == lastWeekMonth and day == lastWeekDay:
        lastWeekTotalOilVolume = lastWeekTotalOilVolume + oilVolume
        lastWeekTotalGasVolume = lastWeekTotalGasVolume + gasVolume

    # write the output string
    outputString = (
        date
        + ","
        + clientName
        + ","
        + batteryName
        + ","
        + str(oilVolume)
        + ","
        + str(gasVolume)
        + ","
        + str(waterVolume)
        + "\n"
    )

    totalAssetProductionFp.write(outputString)


# writes to clean CSV
dailyColoradoClean.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\coloradoAssets.csv",
    index=False,
)

#### BEGIN MidCon and Permian Data Pull

# loops over Midcon and Wellman table
for i in range(0, len(dailyChandlerAsset)):
    row = dailyChandlerAsset.iloc[i]  # gets the first row
    date = row["Date"]  # gets correct date
    clientName = row["Client"]  # set client name correctly
    batteryName = row["Battery Name"]  # set correct battery name
    oilVolume = row["Oil Volume"]  # gets oil volume
    gasVolume = row["Gas Volume"]  # gets gas volume
    waterVolume = row["Water Volume"]  # gets water volume
    splitDate = re.split("-", str(date))  # splits date correct
    day = int(splitDate[2])  # gets the correct day
    month = int(splitDate[1])  # gets the correct month
    year = int(splitDate[0])  # gets the correct

    if year == todayYear and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolume
        totalGasVolume = totalGasVolume + gasVolume
        totalWaterVolume = totalWaterVolume + waterVolume

    if year == yesYear and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolume
        yesTotalGasVolume = yesTotalGasVolume + gasVolume
        yesTotalWaterVolume = yesTotalWaterVolume + waterVolume

    if year == twoDayYear and month == twoDayMonth and day == twoDayDay:
        twoDayOilVolume = twoDayOilVolume + oilVolume
        twoDayGasVolume = twoDayGasVolume + gasVolume

    if year == lastWeekYear and month == lastWeekMonth and day == lastWeekDay:
        lastWeekTotalOilVolume = lastWeekTotalOilVolume + oilVolume
        lastWeekTotalGasVolume = lastWeekTotalGasVolume + gasVolume

    # writes the output string
    outputString = (
        str(date)
        + ","
        + clientName
        + ","
        + str(batteryName)
        + ","
        + str(oilVolume)
        + ","
        + str(gasVolume)
        + ","
        + str(waterVolume)
        + "\n"
    )

    totalAssetProductionFp.write(outputString)  # physically write the string

totalAssetProductionFp.close()  # close the final asset table

## Oil and gas daily change numbers
oilChangeDaily = round((yesTotalOilVolume - twoDayOilVolume), 2)
gasChangeDaily = round((yesTotalGasVolume - twoDayGasVolume), 2)
oilSevenDayPercent = round(
    (yesTotalOilVolume - lastWeekTotalOilVolume) / lastWeekTotalOilVolume, 1
)
gasSevenDayPercent = round(
    (yesTotalGasVolume - lastWeekTotalGasVolume) / lastWeekTotalGasVolume, 1
)

if oilChangeDaily > 0:
    increaseDecreaseOil = "Increase"
else:
    increaseDecreaseOil = "Decline"

if gasChangeDaily > 0:
    increaseDecreaseGas = "Increase"
else:
    increaseDecreaseGas = "Decline"

# print out the volumes for data check while model is running
print("Today Oil Volume: " + str(totalOilVolume))
print("Today Gas Volume: " + str(totalGasVolume))
print("Yesterday Oil Volume: " + str(yesTotalOilVolume))
print("Yesterday Gas Volume: " + str(yesTotalGasVolume))
print("Two Day Ago Oil Volume: " + str(twoDayOilVolume))
print("Two Day Ago Gas Volume: " + str(twoDayGasVolume))
print("Last Week Oil Volume: " + str(lastWeekTotalOilVolume))
print("Last Week Gas Volume: " + str(lastWeekTotalGasVolume))
print("Daily Change Oil Volume: " + str(oilChangeDaily))
print("Daily Change Gas Volume: " + str(gasChangeDaily))
print("Percent Oil Volume: " + str(oilSevenDayPercent))
print("Percent Gas Volume: " + str(gasSevenDayPercent))

## Opens Oil Change File for daily specific percent change calculations
totalAssetProductionFp = open(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\oilgascustomnumbers.csv", "w"
)

headerString = "Daily Oil Change,Daily Gas Change, 7-day Oil Percent Change, 7-day Gas Percent Change, Two Day Ago Oil Volume, Two Day Ago Gas Volume, Increase/Decrease Oil, Increase/Decrease Gas\n"

totalAssetProductionFp.write(headerString)

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
totalAssetProductionFp.write(outputString)
totalAssetProductionFp.close()


print("Done Rolling Up Production")
