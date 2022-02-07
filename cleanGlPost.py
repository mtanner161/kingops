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

folder_path = r"C:\Users\MichaelTanner\King Operating\KOC Field Operations - General\Daily Wolfepak GL Post Exports"
file_type = "\*csv"  # set to look for xlsx
files = glob.glob(folder_path + file_type)  # creates file path
maxFileLead = max(files, key=os.path.getctime)

glPostRaw = pd.read_csv(maxFileLead)

numEntires = len(glPostRaw)

loeBetter = pd.DataFrame()

for i in range(0, numEntires):
    row = glPostRaw.iloc[i]
    accountNumber = float(row["Account"])
    if accountNumber in range(9000, 9999):
        loeBetter = loeBetter.append(row)

print(len(loeBetter))

loeBetter.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\glexportjan.csv",
    index=False,
)

glExportMaster = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\glexportjan.csv"
)

dateTable = []
sourceCompanyTable = []
effectiveDateTable = []
amountTable = []

numEntires = len(glExportMaster)

for i in range(0, numEntires):
    row = glExportMaster.iloc[i]
    accountNumberNew = row["Account"]
    amountTotal = float(row["Amount"])

print("yay")
