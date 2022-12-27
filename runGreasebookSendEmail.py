# Import greasebook variables

from productionFinalGreasebook import (
    dateToday,
    yesTotalOilVolume,
    yesTotalGasVolume,
    oilChangeDaily,
    gasChangeDaily,
    twoDayGasVolume,
    twoDayOilVolume,
    notReportedListOil,
    notReportedListGas,
    dateTwoDaysAgo,
    pumperNotReportedList,
    listOfBatteryIds,
    goodBatteryNames,
    pumperNames
)

# Important packages needed
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd


# Load the .env
load_dotenv()
# create today's string
todayDateString = dateToday.strftime("%m/%d/%Y")
twoDayAgoDateString = dateTwoDaysAgo.strftime("%m/%d/%Y")

# create function to send email


def send_email(email_recipient, email_subject, email_message):
    email_sender = os.getenv("USERNAME_KING")
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_recipient
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_message, "plain"))

    productionFileGood = (r".\kingops\data\totalAssetsProduction.csv")
    oilGasReportedFile = (r".\kingops\data\yesterdayWellReport.csv")

    # OPENS EACH ATTACHMENTS

    with open(productionFileGood, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    with open(oilGasReportedFile, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        partTwo = MIMEBase("application", "octet-stream")
        partTwo.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    encoders.encode_base64(partTwo)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= totalAssetProduction.csv",
    )
    partTwo.add_header(
        "Content-Disposition",
        f"attachment; filename= twoDayAgoWellReport.csv",
    )

    # ATTACHES EACH FILE TO EMAIL
    msg.attach(part)
    msg.attach(partTwo)

    text = msg.as_string()

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.ehlo()
        server.starttls()
        server.login(os.getenv("USERNAME_KING"), os.getenv("PASSWORD_KING"))
        server.sendmail(email_sender, email_recipient, text)
        print("email sent")
        server.quit()
    except:
        print("SMPT server connection error")

    return True


## import links
dashboardLink = os.getenv("DASHBOARD_URL")
wellList = os.getenv("MASTER_BATTERY_LIST")

# Body of the email mesasge
message = (
    "2-day Ago Oil production: "
    + str(round(twoDayOilVolume, 1))
    + " bbl \n\n"
    + "2-day Ago Gas production: "
    + str(round(twoDayGasVolume, 1))
    + " mcf \n\n"
    + "Change in oil production (previous day): "
    + str(oilChangeDaily)
    + " bbl\n\n"
    + "Change in gas production (previous day): "
    + str(gasChangeDaily)
    + " mcf"
    + "\n\nView the Dashboard in Teams (KOC Field Operations) PowerBi Mobile Application or here (if numbers are not updated, try again in 30 min or reply to this email): "
    + dashboardLink
)

message = message + "\n\n" + "Not Reported List by Pumper Route" + \
    "\n" + "----------------------------------------------------" + "\n"


# loops over notReportedList and orgainzes by pumper for easy viewing
for i in range(0, len(pumperNotReportedList)):
    pumper = pumperNotReportedList[i]
    message = message + "Pumper Name: " + pumperNotReportedList[i]
    for j in range(0, len(notReportedListOil)):
        name = notReportedListOil[j]
        index = goodBatteryNames.index(name)
        if pumperNames[index] == pumper:
            message = message + "\n    " + name
    for m in range(0, len(notReportedListGas)):
        name = notReportedListGas[m]
        index = goodBatteryNames.index(name)
        if pumperNames[index] == pumper:
            if name not in notReportedListOil:
                message = message + "\n    " + name
    message = message + "\n"

# email subject
subject = "Daily Production Report KOP Assets - " + twoDayAgoDateString
print(subject)

# Potenital users to send to
michaelTanner = os.getenv("MICHAEL_TANNER")
jayYoung = os.getenv("JAY_YOUNG")
rexGifford = os.getenv("REX_GIFFORD")
chandlerKnox = os.getenv("CHANDLER_KNOX")
paulGerome = os.getenv("PAUL_GEROME")
craigHaesly = os.getenv("CRAIG_HAESLY")
peterSnell = os.getenv("PETER_SNELL")
garretStacey = os.getenv("GARRET_STACEY")
grahamPatterson = os.getenv("GRAHAM_PATTERSON")

# LIST TO SEND TO
send_email(
    michaelTanner,
    subject,
    message,
)

send_email(
    garretStacey,
    subject,
    message,
)


send_email(
    chandlerKnox,
    subject,
    message,
)

send_email(
    peterSnell,
    subject,
    message,
)

send_email(
    grahamPatterson,
    subject,
    message,
)

print("All Email's Sent")
