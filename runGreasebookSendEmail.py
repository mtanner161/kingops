## Import greasebook variables
from greasebookApi import (
    totalOilVolume,
    totalGasVolume,
    yesTotalOilVolume,
    yesTotalGasVolume,
    lastWeekTotalOilVolume,
    lastWeekTotalGasVolume,
    oilChangeDaily,
    gasChangeDaily,
    dateToday,
    yesDateString,
)

## Important packages needed
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

## create function to send email
def send_email(email_recipient, email_subject, email_message):
    email_sender = os.getenv("USERNAME_KING")
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_recipient
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_message, "plain"))

    totalProdFile = (
        r"C:\Users\MichaelTanner\Documents\code_doc\king\data\totalAssetsProduction.csv"
    )

    wellReportFile = (
        r"C:\Users\MichaelTanner\Documents\code_doc\king\data\yesterdayWellReport.csv"
    )

    ### OPENS EACH ATTACHMENTS

    with open(totalProdFile, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    with open(wellReportFile, "rb") as attachment:
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
        f"attachment; filename= wellAssetOverview.csv",
    )

    ## ATTACHES EACH FILE TO EMAIL
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
    "Oil production: "
    + str(round(yesTotalOilVolume, 1))
    + " bbl \n\n"
    + "Gas production: "
    + str(round(yesTotalGasVolume, 1))
    + " mcf \n\n"
    + "Change in oil production (previous day): "
    + str(oilChangeDaily)
    + " bbl\n\n"
    + "Change in gas production (previous day): "
    + str(gasChangeDaily)
    + " mcf"
    + "\n\n Brown Central Battery logging 450 MCF - great news"
    + "\n\n Working on v2.0 which includes a estimated daily oil production based on wells report vs. not report.  The other attachment is the first step to build out the core logic behind whether we want to flag a well as 0, not reported or reported."
    + "\n\nView the Dashboard in Teams (KOC Field Operations) PowerBi Mobile Application or here (if numbers are not updated, try again in 30 min or reply to this email): "
    + dashboardLink
)

## email subject
subject = "Daily Production Report KOP Assets - " + yesDateString
print(subject)

## Potenital users to send to
michaelTanner = os.getenv("MICHAEL_TANNER")
jayYoung = os.getenv("JAY_YOUNG")
rexGifford = os.getenv("REX_GIFFORD")
kellyDuncan = os.getenv("KELLY_DUNCAN")
chandlerKnox = os.getenv("CHANDLER_KNOX")
paulGerome = os.getenv("PAUL_GEROME")
jayEvans = os.getenv("JAY_EVANS")
stuTurley = os.getenv("STU_TURLEY")
allenSantos = os.getenv("ALLEN_SANTOS")
craigHaesly = os.getenv("CRAIG_HAESLY")
peterSnell = os.getenv("PETER_SNELL")
paulGraham = os.getenv("PAUL_GRAHAM")

### LIST TO SEND TO
send_email(
    michaelTanner,
    subject,
    message,
)


send_email(
    stuTurley,
    subject,
    message,
)

send_email(
    chandlerKnox,
    subject,
    message,
)


send_email(
    rexGifford,
    subject,
    message,
)

send_email(
    paulGerome,
    subject,
    message,
)

send_email(
    kellyDuncan,
    subject,
    message,
)


print("All Email's Sent")
