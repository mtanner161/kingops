import os.path
import glob
import pandas as pd

## Gets Latest File in Lead Data Folder

# sets folder path
folder_path = r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Allen Dropbox\# King Operating\Daily Lead Data"
file_type = "\*csv"  # sets file type to csv
files = glob.glob(folder_path + file_type)  # creates file path
maxFileLead = max(
    files, key=os.path.getctime
)  # gets latest from that path and t4hat type of file

## Gets Latest File in Cash Data Folder
folder_path = r"C:\Users\MichaelTanner\OneDrive - Sandstone Group\Allen Dropbox\# King Operating\Daily Cash Data"
file_type = "\*csv"  # sets file type to csv
files = glob.glob(folder_path + file_type)  # creates file path
maxFileCash = max(
    files, key=os.path.getctime
)  # gets latest from that path and t4hat type of file

leadFile = pd.read_csv(maxFileLead)
cashFile = pd.read_csv(maxFileCash)

leadFile.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\leads.csv", index=False
)
cashFile.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\cash.csv", index=False
)


print("yay")
