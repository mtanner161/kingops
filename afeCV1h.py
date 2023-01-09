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

fileName = pd.read_csv(r".\kingops\data\afe\kinga199cv1h\1.1.2023.csv")
fileNameExcel = pd.read_excel(
    r".\kingops\data\afe\kinga199cv1h\1.1.2023test.xlsx")

dateList = fileName["textbox58"].tolist()
costList = fileName["textbox13.0"].tolist()
costItemList = fileName["textbox34"].tolist()
columns = fileName.columns
print(columns)
print(type(costList[21]))
dateOfAfe = dateList[0]


print("yay")
