# Cleaning custom daily allocation reports from Greasebook
# Developed by Michael Tanner

# import required packages
import os
import glob
import json
import pandas as pd
import numpy as np
import re
import smtplib
from datetime import date, datetime
import datetime as dt


# IMPORTANT - SET DATE TO CORRECT VALUES
todayDate = "1/25/2022"
yesDate = "1/24/2022"
lastWeekDate = "1/19/2022"
lastMonthDate = "12/25/2021"


# finds source folder
folder_path = r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Clients\King Operating\Finance - Reservoir\Daily Production Data"
file_type = "\*xlsx"  # set to look for xlsx
files = glob.glob(folder_path + file_type)  # creates file path
maxFileLead = max(files, key=os.path.getctime)  # gets latest file path
# get raw CSV download maxFileLead
rawProduction = pd.read_excel(maxFileLead)

# setting the headers
rawProduction = rawProduction.iloc[1:, :]
rawProduction.columns = rawProduction.iloc[0]
rawProduction = rawProduction[1:]

# opening a file pointer and setting to write mode
fp = open(r"C:\Users\MichaelTanner\Documents\code_doc\king\data\kellyAssets.csv", "w")

# set the header values
headerString = "Date," + "Lease," + "Field," + "Well Name," + "Oil," + "Gas\n"

# write the header
fp.write(headerString)

# clean the "Lease" colmun so it spilts into Lease, Field and Well Name
for i in range(0, len(rawProduction)):
    row = rawProduction.iloc[i]
    leaseName = row["Lease"]
    if row["Date"] == "Totals":
        break
    splitString = re.split("-|–", leaseName)
    if len(splitString) == 3:
        outputString = (
            row["Date"]
            + ","
            + splitString[0]
            + ","
            + splitString[1]
            + ","
            + splitString[2]
            + ","
            + row["Oil"]
            + ","
            + row["Gas"]
            + "\n"
        )
    else:
        outputString = (
            row["Date"]
            + ","
            + splitString[0]
            + ","
            + splitString[1]
            + ","
            + "No Well Name"
            + ","
            + row["Oil"]
            + ","
            + row["Gas"]
            + "\n"
        )
    # replace with Pretty Area Names
    outputString = outputString.replace("Peak", "East Texas")
    outputString = outputString.replace("CWS", "South Texas")
    outputString = outputString.replace("Otex", "Gulf Coast")

    # write the string
    fp.write(outputString)

fp.close()

cleanKellyAsset = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\kellyAssets.csv"
)

oilSum = 0
oilSumYes = 0
oilSumWeek = 0
oilSumMonth = 0
gasSum = 0
gasSumYes = 0
gasSumWeek = 0
gasSumMonth = 0

# gets todays sum
for i in range(0, len(cleanKellyAsset)):
    if cleanKellyAsset.iloc[i, 0] == todayDate:
        gasSum = gasSum + float(cleanKellyAsset.iloc[i, 5])
        oilSum = oilSum + float(cleanKellyAsset.iloc[i, 4])
    else:
        continue

for i in range(0, len(cleanKellyAsset)):
    if cleanKellyAsset.iloc[i, 0] == lastMonthDate:
        gasSumMonth = gasSumMonth + float(cleanKellyAsset.iloc[i, 5])
        oilSumMonth = oilSumMonth + float(cleanKellyAsset.iloc[i, 4])
    else:
        continue

for i in range(0, len(cleanKellyAsset)):
    if cleanKellyAsset.iloc[i, 0] == lastWeekDate:
        gasSumWeek = gasSumWeek + float(cleanKellyAsset.iloc[i, 5])
        oilSumWeek = oilSumWeek + float(cleanKellyAsset.iloc[i, 4])
    else:
        continue


print(round(oilSum, 2))
print(round(gasSum, 2))
print(round(oilSumYes, 2))
print(round(gasSumYes, 2))
print(round(oilSum - oilSumYes, 2))
print(round(gasSum - gasSumYes, 2))

dashboardLink = "https://app.powerbi.com/view?r=eyJrIjoiM2U5OTYxOWYtOTEyMS00M2YxLWE0NTktMDFjZjcwNzlmMjg3IiwidCI6IjA1MTM5NTUzLWVlOTAtNDdhZi1iNmY3LTU0ZDk2OTc4ZTQ5ZSJ9&pageName=ReportSectionb8f3ed9f3c4313759775"


from mailer import Mailer

mail = Mailer(email="operations.king@gmail.com", password="Bigshow1637%")

mail.send(
    receiver="mtanner@kingoperating.com, kduncan@kingoperating.com, pgerome@kingoperating.com",
    subject="Daily Production Report UPDATE: 1/25/2021 - ETX, STX and Gulf Coast",
    message="Oil production: "
    + str(oilSum)
    + " bbl. \n\n"
    + "Gas production: "
    + str(gasSum)
    + " mcf \n\n"
    + "Change in oil production (previous day): "
    + str(oilSum - oilSumYes)
    + " bbl\n\n"
    + "Change in gas production (previous day): "
    + str(gasSum - gasSumYes)
    + " mcf"
    + "\n\nView the Dashboard here (if numbers are not updated, try again in 30 min or email Michael): "
    + dashboardLink,
)


print("done")
