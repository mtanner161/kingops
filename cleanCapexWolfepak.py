import pandas as pd
import os

capexRaw = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\capexjan.csv"
)

numEntries = len(capexRaw)

dateList = []

for i in range(0, numEntries):
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Oct-20", "10/1/2020"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Dec-20", "12/1/2020"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Jan-21", "1/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Feb-21", "2/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Mar-21", "3/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Apr-21", "4/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "May-21", "5/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Jun-21", "6/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Jul-21", "7/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Aug-21", "8/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Sep-21", "9/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Oct-21", "10/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Nov-21", "11/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Dec-21", "12/1/2021"
    )
    capexRaw["Effective Date"] = capexRaw["Effective Date"].replace(
        "Jan-22", "1/1/2022"
    )
    print("yay")

capexRaw.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\loe.csv", index=False
)


print("yay")
