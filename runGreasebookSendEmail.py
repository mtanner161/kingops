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

    filename = (
        r"C:\Users\MichaelTanner\Documents\code_doc\king\data\totalAssetsProduction.csv"
    )

    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= totalAssetProduction.csv",
    )

    msg.attach(part)
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


dashboardLink = os.getenv("DASHBOARD_URL")

message = (
    "Oil production: "
    + str(yesTotalOilVolume)
    + " bbl. \n\n"
    + "Gas production: "
    + str(yesTotalGasVolume)
    + " mcf \n\n"
    + "Change in oil production (previous day): "
    + str(oilChangeDaily)
    + " bbl\n\n"
    + "Change in gas production (previous day): "
    + str(gasChangeDaily)
    + " mcf"
    + "\n\nView the Dashboard in Teams (KOC Field Operations) or here (if numbers are not updated, try again in 30 min or email Michael): "
    + dashboardLink
)

subject = "Daily Production Report All Assets TEST - " + todayDateString
michaelTanner = os.getenv("MICHAEL_TANNER")
jayYoung = os.getenv("JAY_YOUNG")
rexGifford = os.getenv("REX_GIFFORD")
kellyDuncan = os.getenv("KELLY_DUNCAN")
chandlerKnox = os.getenv("CHANDLER_KNOX")
paulGerome = os.getenv("PAUL_GEROME")
jayEvans = os.getenv("JAY_EVANS")

print(subject)

send_email(
    michaelTanner,
    subject,
    message,
)

send_email(
    chandlerKnox,
    subject,
    message,
)

send_email(
    jayEvans,
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
