# Import packages needed
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
import numpy as np

afeRawFile = pd.read_excel(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\afe\thurman23v\thurman23vAfeOg.xlsx")

masterMatchFile = pd.read_excel(
    r".\kingops\data\afe\welldriveWolfepakMatch.xlsx")

actualWellCostWolfepak = pd.read_excel(
    r"C:\Users\mtanner\OneDrive - King Operating\Documents 1\code\kingops\data\afe\thurman23v\thurman23vActualSpend.xlsx")

welldriveAccounts = masterMatchFile["Code WellDrive"].tolist()
wolfepakAccounts = masterMatchFile["Code WolfePak"].tolist()

for i in range(0, len(afeRawFile)):
    rowAfeRaw = afeRawFile.iloc[i]
    afeAccountCode = rowAfeRaw["Account"]
    afeCost = rowAfeRaw["Cost"]

    rowAfeActual = actualWellCostWolfepak.iloc[i]
    actualAccountCode = rowAfeActual["Account"]
    actualCost = rowAfeActual["Amount"]
    actualDescription = rowAfeActual["{Account Desc}"]


print("yay")
