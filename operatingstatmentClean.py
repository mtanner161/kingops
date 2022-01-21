##File to Clean the Operating Statment via Wolfpak
import os
import pandas as pd
import numpy as np
import requests

osRaw = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\combocurve\ComboCurve\operatingstatementOctober.csv"
)


fp = open("./king/combocurve/ComboCurve/cleanOperatingStatment.csv", "w")

fp.write("Date, Description, Value\n")

k = 0
date = np.zeros([len(osRaw.columns) - 4], dtype=str)

dummy = osRaw.iloc[1]

for i in range(3, len(dummy)):
    date[i - 2] = dummy.iloc[3:14]

for i in range(3, len(osRaw.columns)):
    date[k] = osRaw.iat[0, i]
    k = k + 1


for i in range(1, len(osRaw)):
    testValue = osRaw[i][4]

    if testValue == "nan":
        continue

    description = osRaw[i][3]

    value = []
    for j in range(3, len(osRaw.columns)):
        fp.write(date[j - 3], description, osRaw[i][j])


print("Hello World")
