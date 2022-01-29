import pandas as pd
import os

glPostRaw = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\glpostjan.csv"
)
capexRaw = pd.read_csv(r"C:\Users\MichaelTanner\Documents\code_doc\king\data\loe.csv")
capexRaw = capexRaw.drop("Category_Name", 1)
capexRaw = capexRaw.drop("Client", 1)
capexRaw = capexRaw.drop("Effective Date", 1)
capexRaw = capexRaw.drop("Total", 1)

numEntires = len(glPostRaw)

for i in range(0, numEntires):
    row = glPostRaw.iloc[i]
    accountNumber = float(row["Account"])
    if accountNumber < 9000:
        glPostRaw = glPostRaw.drop(i, 0)


print("yay")
