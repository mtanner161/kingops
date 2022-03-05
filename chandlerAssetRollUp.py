from ast import keyword
from http import client
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

df = pd.concat(
    pd.read_excel(
        r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Allen Dropbox\# King Operating\Daily Production Data Files\chandlerAssetsDailyUpdateBETTER.xlsx",
        sheet_name=None,
    ),
    ignore_index=True,
)

df.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\chandlerAssetsDaily.csv",
    index=False,
)

print("Completed Midcon and Wellman Rollup")
