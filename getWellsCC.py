# import packages
from combocurve_api_v1 import ServiceAccount, ComboCurveAuth
from combocurve_api_v1.pagination import get_next_page_url
import requests
import numpy as np
import json
import pandas as pd
from requests.models import Response
from dotenv import load_dotenv
import os

load_dotenv()

# connect to service account
service_account = ServiceAccount.from_file(os.getenv("API_SEC_CODE_LIVE"))
api_key = os.getenv("API_KEY_PASS_LIVE")  # set API Key from enviroment variable
# specific Python ComboCurve authentication
combocurve_auth = ComboCurveAuth(service_account, api_key)

print("Authentication Worked")

auth_headers = combocurve_auth.get_auth_headers()

url = "https://api.combocurve.com/v1/wells?take=25"

resultsList = []


def process_page(response_json):
    results = response_json
    resultsList.extend(results)


has_more = True

while has_more:
    response = requests.request("GET", url, headers=auth_headers)
    url = get_next_page_url(response.headers)
    process_page(response.json())
    has_more = url is not None


print("yay")
