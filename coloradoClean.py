from email import header
from operator import index
import pandas as pd
import os
from datetime import date, datetime, timedelta
import datetime as dt

dailyColorado = pd.read_excel(
    r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Clients\King Operating\Finance - Reservoir\Daily Production Data\WMSSU Daily Operations Report Febr. 6, 2022.xlsx"
)
dailyColoradoClean = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\coloradoAssets.csv"
)


dateToday = dt.datetime.today()
print(str(dateToday))
dateYesterday = dateToday - timedelta(days=1)
dateYesString = dateYesterday.strftime("%m/%d/%Y")

northList = []
southList = []

northList.append(dateToday)  ## set each time
southList.append(dateToday)  ## set each time

northBatteryGas = dailyColorado.iloc[5, 2]
northBatteryWater = dailyColorado.iloc[4, 2]
northBatteryOil = dailyColorado.iloc[3, 2]
northBatteryWellCount = dailyColorado.iloc[2, 2]

northList.append("North")
northList.append(northBatteryOil)
northList.append(northBatteryGas)
northList.append(northBatteryWater)

southBatteryGas = dailyColorado.iloc[5, 5]
southBatteryWater = dailyColorado.iloc[4, 5]
southBatteryOil = dailyColorado.iloc[3, 5]
southBatteryWellCount = dailyColorado.iloc[2, 5]

southList.append("South")
southList.append(southBatteryOil)
southList.append(southBatteryGas)
southList.append(southBatteryWater)

print(northBatteryOil)
print(northBatteryWater)
print(northBatteryGas)
print(southBatteryOil)
print(southBatteryWater)
print(southBatteryGas)


dailyColoradoClean.loc[len(dailyColoradoClean.index)] = northList
dailyColoradoClean.loc[len(dailyColoradoClean.index)] = southList


dailyColoradoClean.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\coloradoAssets.csv",
    index=False,
)


print("yay")
