from ast import keyword
from time import strftime
import requests
import os
from datetime import date, datetime, timedelta
import datetime as dt
import re
from dotenv import load_dotenv

load_dotenv()

dateToday = dt.datetime.today()
todayYear = dateToday.strftime("%Y")
todayMonth = dateToday.strftime("%m")
todayDay = dateToday.strftime("%d")

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

response = requests.request(
    "GET",
    url,
)

print(response.status_code)

results = response.json()

numEntries = len(results)

fp = open(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\kellyAssetsBetter.csv", "w"
)

headerString = (
    "Battery ID," + "Battery Name," + "Date," + "Oil Volume," + "Gas Volume\n"
)

fp.write(headerString)

dateYesterday = dateToday - timedelta(days=1)
dateLastWeek = dateToday - timedelta(days=7)
totalOilVolume = 0
totalGasVolume = 0
yesTotalOilVolume = 0
yesTotalGasVolume = 0
lastWeekTotalOilVolume = 0
lastWeekTotalGasVolume = 0

todayYear = dateToday.strftime("%Y")
todayMonth = dateToday.strftime("%m")
todayDay = dateToday.strftime("%d")

yesYear = dateYesterday.strftime("%Y")
yesMonth = dateYesterday.strftime("%m")
yesDay = dateYesterday.strftime("%d")

lastWeekYear = dateLastWeek.strftime("%Y")
lastWeekMonth = dateLastWeek.strftime("%m")
lastWeekDay = dateLastWeek.strftime("%d")

for i in range(0, numEntries):

    row = results[i]
    keys = list(row.items())

    oilVolume = ""
    gasVolume = ""

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

    if oilVolume == "":
        oilVolume = 0
    if gasVolume == "":
        gasVolume = 0

    splitDate = re.split("T", date)
    splitDate2 = re.split("-", splitDate[0])
    year = splitDate2[0]
    month = splitDate2[1]
    day = splitDate2[2]

    if year == todayYear and month == todayMonth and day == todayDay:
        totalOilVolume = totalOilVolume + oilVolume
        totalGasVolume = totalGasVolume + gasVolume

    if year == yesYear and month == yesMonth and day == yesDay:
        yesTotalOilVolume = yesTotalOilVolume + oilVolume
        yesTotalGasVolume = yesTotalGasVolume + gasVolume

    if year == lastWeekYear and month == lastWeekMonth and day == lastWeekDay:
        lastWeekTotalOilVolume = lastWeekTotalOilVolume + oilVolume
        lastWeekTotalGasVolume = lastWeekTotalGasVolume + gasVolume

    outputString = (
        str(batteryId)
        + ","
        + batteryName
        + ","
        + date
        + ","
        + str(oilVolume)
        + ","
        + str(gasVolume)
        + "\n"
    )

    outputString = outputString.replace("Peak", "East Texas")
    outputString = outputString.replace("CWS", "South Texas")
    outputString = outputString.replace("Otex", "Gulf Coast")

    fp.write(outputString)

fp.close()

oilChangeDaily = round(totalOilVolume - yesTotalOilVolume, 2)
gasChangeDaily = round(totalGasVolume - yesTotalGasVolume, 2)
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

fp = open(r"C:\Users\MichaelTanner\Documents\code_doc\king\data\oilgaschange.csv", "w")

headerString = "Daily Oil Change,Daily Gas Change, 7-day Oil Percent Change, 7-day Gas Percent Change\n"
fp.write(headerString)
outputString = (
    str(oilChangeDaily)
    + ","
    + str(gasChangeDaily)
    + ","
    + str(oilSevenDayPercent)
    + ","
    + str(gasSevenDayPercent)
)
fp.write(outputString)
fp.close()


print("Done")
