import os
import pandas as pd
import numpy as np
import json

rawKingHeaders = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\kingheaders.csv"
)

wellName = rawKingHeaders["Well Name"]
wellNumber = rawKingHeaders["Well Number"]
apiNumber = rawKingHeaders["API14"]

goodList = pd.DataFrame()
goodList = goodList.append(wellName)
goodList = goodList.append(wellNumber)
goodList = goodList.append(apiNumber)


print(type(wellNumber.iloc[5]))
print(wellNumber.iloc[5])

goodList.to_excel("welNameTest.xlsx", index=False)

print("yay")
