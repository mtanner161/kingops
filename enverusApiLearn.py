from enverus_developer_api import DeveloperAPIv3
from dotenv import load_dotenv
import os

load_dotenv()  # load ENV

key = DeveloperAPIv3(secret_key=os.getenv("ENVERUS_API"))

for row in key.query("wells", county="REEVES", deleteddate="null"):
    print(row)

print("yay")
