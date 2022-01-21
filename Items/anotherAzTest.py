from azure.cosmos import CosmosClient
import azure.cosmos.cosmos_client as cosmos_client
import os

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

database_name = "testDatabase"
database = client.get_database_client(database_name)
container_name = "products"
container = database.get_container_client(container_name)

for i in range(1, 10):
    container.upsert_item(
        {
            "id": "item{0}".format(i),
            "productName": "Widget",
            "productModel": "Model {0}".format(i),
        }
    )

print("I did it")

something = container.upsert_item()
