# Cleaning custom daily allocation reports from Greasebook
# Developed by Michael Tanner

# import required packages
import os
import glob
import json
from time import strptime
import pandas as pd
import numpy as np
import re
import smtplib
from datetime import date, datetime
import datetime as dt


# IMPORTANT - SET DATE TO CORRECT VALUES
todayDate = "1/26/2022"
yesDate = "1/25/2022"
lastWeekDate = "1/20/2022"
lastMonthDate = "12/26/2021"

newDate = datetime.strptime(todayDate, "%m/%d/%Y")
print(newDate)


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
    if cleanKellyAsset.iloc[i, 0] == yesDate:
        gasSumYes = gasSumYes + float(cleanKellyAsset.iloc[i, 5])
        oilSumYes = oilSumYes + float(cleanKellyAsset.iloc[i, 4])
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


oilChangeDaily = round(oilSum - oilSumYes, 2)
gasChangeDaily = round(gasSum - gasSumYes, 2)
oilSevenDayPercent = (oilSum - oilSumWeek) / oilSumWeek
gasSevenDayPercent = (gasSum - gasSumWeek) / gasSumWeek

print("Daily Oil Prod: " + str(round(oilSum, 2)))
print("Daily Gas Prod: " + str(round(gasSum, 2)))
print("Yes Oil Prod: " + str(round(oilSumYes, 2)))
print("Yes Gas Prod: " + str(round(gasSumYes, 2)))
print("Change Daily Oil Prod: " + str(round(oilSum - oilSumYes, 2)))
print("Change Daily Gas Prod: " + str(round(gasSum - gasSumYes, 2)))
print(oilSevenDayPercent)
print(gasSevenDayPercent)

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


dashboardLink = "https://app.powerbi.com/view?r=eyJrIjoiM2U5OTYxOWYtOTEyMS00M2YxLWE0NTktMDFjZjcwNzlmMjg3IiwidCI6IjA1MTM5NTUzLWVlOTAtNDdhZi1iNmY3LTU0ZDk2OTc4ZTQ5ZSJ9&pageName=ReportSectionb8f3ed9f3c4313759775"


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from dotenv import load_dotenv

load_dotenv()

nameTest = os.getenv("USERNAME_KING")
print(nameTest)


def send_email(email_recipient, email_subject, email_message):
    email_sender = os.getenv("USERNAME_KING")
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_recipient
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_message))

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.ehlo()
        server.starttls()
        server.login(os.getenv("USERNAME_KING"), os.getenv("PASSWORD_KING"))
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        print("email sent")
        server.quit()
    except:
        print("SMPT server connection error")

    return True


message = (
    "Oil production: "
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
    + dashboardLink
)

subject = "Daily Production Report East/South and Gulf Coast Texas Assets - 1/26/2021"

send_email(
    "mtanner@kingoperating.com",
    subject,
    message,
)

send_email(
    "pgerome@kingoperating.com",
    subject,
    message,
)

send_email(
    "kduncan@kingoperating.com",
    subject,
    message,
)


print("done")
