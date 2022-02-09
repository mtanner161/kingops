## Import packages needed
from ast import keyword
from http import client
from time import strftime
import requests
import os
from datetime import date, datetime, timedelta
import datetime as dt
import re
from dotenv import load_dotenv
import pandas as pd

load_dotenv()  # load ENV

# read in prodouctions files
dailyColorado = pd.read_excel(
    r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Clients\King Operating\Finance - Reservoir\Daily Production Data\WMSSU Daily Operations Report Febr. 8, 2022.xlsx"
)
dailyColoradoClean = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\coloradoAssets.csv"
)

# check date on Colorado
dailyColoradoDate = dailyColorado.iloc[0, 7]
print(dailyColoradoDate)

# set some date variables we will need later
dateToday = dt.datetime.today()
todayYear = dateToday.strftime("%Y")
todayMonth = dateToday.strftime("%m")
todayDay = dateToday.strftime("%d")

# set ETX/STX and GCT API url
url = (
    "https://integration.greasebook.com/api/v1/batteries/daily-production?apiKey="
    + os.getenv("GREASEBOOK_API_KEY")
    + "&start=2021-01-01&end="
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
fp = open(
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

fp.write(headerString)  # write the header string
# a bunch of variables the below loop needs
dateYesterday = dateToday - timedelta(days=1)
dateLastWeek = dateToday - timedelta(days=7)
totalOilVolume = 0
totalGasVolume = 0
totalWaterVolume = 0
yesTotalOilVolume = 0
yesTotalGasVolume = 0
yesTotalWaterVolume = 0
lastWeekTotalOilVolume = 0
lastWeekTotalGasVolume = 0

## Convert all dates to str for comparison rollup
todayYear = dateToday.strftime("%Y")
todayMonth = dateToday.strftime("%m")
todayDay = dateToday.strftime("%d")

yesYear = dateYesterday.strftime("%Y")
yesMonth = dateYesterday.strftime("%m")
yesDay = dateYesterday.strftime("%d")

lastWeekYear = dateLastWeek.strftime("%Y")
lastWeekMonth = dateLastWeek.strftime("%m")
lastWeekDay = dateLastWeek.strftime("%d")

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
    month = splitDate2[1]
    day = splitDate2[2]

    ## Summing today, yesterday and last week oil gas and water
    if year == todayYear and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolume
        totalGasVolume = totalGasVolume + gasVolume
        totalWaterVolume = totalWaterVolume + waterVolume

    if year == yesYear and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolume
        yesTotalGasVolume = yesTotalGasVolume + gasVolume

    if year == lastWeekYear and month == lastWeekMonth and day == lastWeekDay:
        lastWeekTotalOilVolume = lastWeekTotalOilVolume + oilVolume
        lastWeekTotalGasVolume = lastWeekTotalGasVolume + gasVolume

    ## Splits battery name up
    splitString = re.split("-|–", batteryName)
    clientName = splitString[0]  # sets client name to client name from ETX/STX and GCT
    # if field name exisits - add the batteryName
    if len(splitString) == 3:
        batteryNameBetter = splitString[1] + "-" + splitString[2]
    else:
        batteryNameBetter = splitString[1]

    # cleaning up the strings for outputing
    batteryNameBetter = batteryNameBetter.replace(" ", "")
    clientName = clientName.replace(" ", "")
    dateString = month + "/" + day + "/" + year
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

    fp.write(outputString)

###### COLORADO CODE BEGINS
## I reuse variables for oilVolume etc for ease

clientName = "WELOP"  ## Changes client name to WELOP

## Master Loop for Colorado Assets
for i in range(0, len(dailyColoradoClean)):
    # sets correct variables for calculations (resttting some)
    row = dailyColoradoClean.iloc[i]
    date = row["Date"]
    batteryName = row["Battery"]
    oilVolume = row["Oil Volume"]
    gasVolume = row["Gas Volume"]
    waterVolume = row["Water Volume"]
    splitDate = re.split("/", date)
    day = splitDate[1]
    month = splitDate[0]
    year = splitDate[2]
    # test for date and sums
    if year == todayYear and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolume
        totalGasVolume = totalGasVolume + gasVolume
        totalWaterVolume = totalWaterVolume + waterVolume

    if year == yesYear and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolume
        yesTotalGasVolume = yesTotalGasVolume + gasVolume
        yesTotalWaterVolume = yesTotalWaterVolume + waterVolume

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

    fp.write(outputString)

# create a nice yesterday date string
yesDateString = yesMonth + "/" + yesDay + "/" + yesYear

# get lastest Colorado Data from specific folder and set to correct values
northBatteryGas = dailyColorado.iloc[5, 2]
northBatteryWater = dailyColorado.iloc[4, 2]
northBatteryOil = dailyColorado.iloc[3, 2]
northBatteryWellCount = dailyColorado.iloc[2, 2]
southBatteryGas = dailyColorado.iloc[5, 5]
southBatteryWater = dailyColorado.iloc[4, 5]
southBatteryOil = dailyColorado.iloc[3, 5]
southBatteryWellCount = dailyColorado.iloc[2, 5]

# add Colorado total oil/gas/water to totals for all assets
totalOilVolume = totalOilVolume + northBatteryOil + southBatteryOil
totalGasVolume = totalGasVolume + northBatteryGas + southBatteryGas
totalWaterVolume = totalWaterVolume + northBatteryWater + southBatteryWater

# creating lists for each north and south battery
northList = []
southList = []
northList.append(yesDateString)  ## set each time
southList.append(yesDateString)

# adding the new variables to correct list
northList.append("North")
northList.append(northBatteryOil)
northList.append(northBatteryGas)
northList.append(northBatteryWater)
southList.append("South")
southList.append(southBatteryOil)
southList.append(southBatteryGas)
southList.append(southBatteryWater)

# adding the new data to the clean Colorado table for next day run
dailyColoradoClean.loc[len(dailyColoradoClean.index)] = northList
dailyColoradoClean.loc[len(dailyColoradoClean.index)] = southList

## Writes the South Battery
outputString = (
    yesDateString
    + ","
    + clientName
    + ","
    + "South"
    + ","
    + str(southBatteryOil)
    + ","
    + str(southBatteryGas)
    + ","
    + str(southBatteryWater)
    + "\n"
)

fp.write(outputString)  # write the string

# Writes the North Battery
outputString = (
    yesDateString
    + ","
    + clientName
    + ","
    + "North"
    + ","
    + str(northBatteryOil)
    + ","
    + str(northBatteryGas)
    + ","
    + str(northBatteryWater)
    + "\n"
)

fp.write(outputString)  # writes the string
fp.close()  # close the final asset table

#### These are extra steps

# Calculates variables needed to daily analysis numbers
lenColorado = len(dailyColoradoClean)
yesColoradoOil1 = dailyColoradoClean.iloc[lenColorado - 1, 2]
yesColoradoGas1 = dailyColoradoClean.iloc[lenColorado - 1, 3]
yesColoradoWater1 = dailyColoradoClean.iloc[lenColorado - 1, 4]
yesColoradoOil2 = dailyColoradoClean.iloc[lenColorado - 2, 2]
yesColoradoGas2 = dailyColoradoClean.iloc[lenColorado - 2, 3]
yesColoradoWater2 = dailyColoradoClean.iloc[lenColorado - 2, 4]

yesTotalOilVolume = yesTotalOilVolume + yesColoradoOil1 + yesColoradoOil2
yesTotalGasVolume = yesTotalGasVolume + yesColoradoGas1 + yesColoradoGas2
yesTotalWaterVolume = yesTotalWaterVolume + yesColoradoWater1 + yesColoradoWater2

## export the Colorado Asset table
dailyColoradoClean.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\coloradoAssets.csv",
    index=False,
)


oilChangeDaily = round(totalOilVolume - yesTotalOilVolume, 2)
gasChangeDaily = round(totalGasVolume - yesTotalGasVolume, 2)
waterChangeDaily = round(totalWaterVolume - yesTotalWaterVolume, 2)
oilSevenDayPercent = (totalOilVolume - lastWeekTotalOilVolume) / lastWeekTotalOilVolume
gasSevenDayPercent = (totalGasVolume - lastWeekTotalGasVolume) / lastWeekTotalGasVolume

print("Today Oil Volume: " + str(totalOilVolume))
print("Today Gas Volume: " + str(totalGasVolume))
print("Yesterday Oil Volume: " + str(yesTotalOilVolume))
print("Yesterday Gas Volume: " + str(yesTotalGasVolume))
print("Last Week Oil Volume: " + str(lastWeekTotalOilVolume))
print("Last Week Gas Volume: " + str(lastWeekTotalGasVolume))
print("Daily Change Oil Volume: " + str(oilChangeDaily))
print("Daily Change Gas Volume: " + str(gasChangeDaily))
print("Percent Oil Volume: " + str(oilSevenDayPercent))
print("Percent Gas Volume: " + str(gasSevenDayPercent))

## Opens Oil Change File for daily specific calculations
fp = open(r"C:\Users\MichaelTanner\Documents\code_doc\king\data\oilgaschange.csv", "w")

headerString = "Daily Oil Change,Daily Gas Change,Daily Water Change, 7-day Oil Percent Change, 7-day Gas Percent Change\n"
fp.write(headerString)
outputString = (
    str(oilChangeDaily)
    + ","
    + str(gasChangeDaily)
    + ","
    + str(waterChangeDaily)
    + ","
    + str(oilSevenDayPercent)
    + ","
    + str(gasSevenDayPercent)
)
fp.write(outputString)
fp.close()


print("Done - Yay")
