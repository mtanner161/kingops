import json

import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
from numpy import int64
import pandas as pd

config = {
    "endpoint": "https://kingtest.documents.azure.com:443/",
    "primarykey": "M51cErUG6aJAzHOfkk9vO74w4Rt1FOfAp1mabqUoqL46O4JVdvCQ2PdoF96Bqq9HYIywze8ElfmhBRU77VU1aA==",
}

client = cosmos_client.CosmosClient(
    url=config["endpoint"], credential={"masterKey": config["primarykey"]}
)

# Download and read csv file
df = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\combocurve\ComboCurve\cleanEconOneLiner.csv"
)
# Reset index - creates a column called 'index'
df = df.reset_index()
# Rename that new column 'id'
# Cosmos DB needs one column named 'id'.
df = df.rename(columns={"index": "id"})
# Convert the id column to a string - this is a document database.
df["id"] = df["id"].astype(str)

database_link = "dbs/" + "combo"

collection_link = database_link + "/colls/" + "combocurve"

# Write rows of a pandas DataFrame as items to the Database Container
for i in range(0, df.shape[0]):
    # create a dictionary for the selected row
    data_dict = int(str(df.iloc[i, :]))
    # convert the dictionary to a json object.
    data_dict = json.dumps(data_dict)
    insert_data = client.UpsertItem(collection_link, json.loads(data_dict))


print("Records inserted successfully.")
