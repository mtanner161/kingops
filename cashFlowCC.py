# ComboCurve API Res Monthly Cash Flow and Economic One Liners
# Developed by Michael Tanner
##
# Runs and exports clean csv's for (1) Reserves Category Monthly Cash Flow (2) Individual Well Economics and (3) Forecasted Production (both oil and gas)

# testgit adding anthor line
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

projectId = "612fc3d36880c20013a885df"
scenarioId = "62223bfe08cb6400134b32da"


# This code chunk gets the Monthly Cash Flow for given Scenerio
# Call Stack - Get Econ Id

auth_headers = combocurve_auth.get_auth_headers()
# URl econid
url = (
    "https://api.combocurve.com/v1/projects/"
    + projectId
    + "/scenarios/"
    + scenarioId
    + "/econ-runs"
)

response = requests.request(
    "GET", url, headers=auth_headers
)  # GET request to pull economic ID for next query

jsonStr = response.text  # convert to JSON string
dataObjBetter = json.loads(jsonStr)  # pass to data object - allows for parsing
row = dataObjBetter[0]  # sets row equal to first string set (aka ID)
econId = row["id"]  # set ID equal to variable

print(econId)  # check that varaible is passed correctly

# Reautenticated client
auth_headers = combocurve_auth.get_auth_headers()
# Set new url parsed with updated econID
urlone = (
    "https://api.combocurve.com/v1/projects/"
    + projectId
    + "/scenarios/"
    + scenarioId
    + "/econ-runs/"
    + econId
    + "/monthly-exports"
)

response = requests.request("POST", urlone, headers=auth_headers)  # runs POST request

# same as above chunk, parses JSON string and pull outs econRunID to be passed in next GET request
jsonStr = response.text
dataObjEconRunId = json.loads(jsonStr)
row = dataObjEconRunId
econRunId = row["id"]
print(econRunId)

# Reautenticated client
auth_headers = combocurve_auth.get_auth_headers()
# set new url with econRunID, skipping zero

urltwo = (
    "https://api.combocurve.com/v1/projects/"
    + projectId
    + "/scenarios/"
    + scenarioId
    + "/econ-runs/"
    + econId
    + "/monthly-exports/"
    + econRunId
    + "?take=200"
)

resultsList = []


def process_page(response_json):
    results = response_json["results"]
    resultsList.extend(results)


has_more = True

while has_more:
    response = requests.request("GET", urltwo, headers=auth_headers)
    urltwo = get_next_page_url(response.headers)
    process_page(response.json())
    has_more = urltwo is not None


numEntries = len(resultsList)

### Working on rolling up monthly cash flow in a Res Cat Monthly Output

# lists for each of the columns I need rolled up
grossOilWellHeadVolumeTable = []
grossGasWellHeadVolumeTable = []
oilRevenueTable = []
gasRevenueTable = []
totalNetRevenueTable = []
totalExpenseTable = []
netIncomeTable = []
totalCapexTable = []
beforeIncomeTaxCashFlowTable = []
totalTaxTable = []
dateTable = []

# Setting row, wellId and date to correct values
for i in range(0, numEntries):
    row = resultsList[i]
    wellId = row["well"]
    output = row["output"]
    date = row["date"]
    # getting the total variables casted as floats for addition
    totalGrossOilVolume = float(output["grossOilWellHeadVolume"])
    totalNetRevenue = float(output["totalRevenue"])
    totalGrossGasVolume = float(output["grossGasWellHeadVolume"])
    oilRev = float(output["oilRevenue"])
    gasRev = float(output["gasRevenue"])
    totalExpense = float(output["totalExpense"])
    netIncome = float(output["netIncome"])
    totalCapex = float(output["totalCapex"])
    biCashFlow = float(output["beforeIncomeTaxCashFlow"])
    totalTaxSum = (
        float(output["totalSeveranceTax"])
        + float(output["adValoremTax"])
        + float(output["totalProductionTax"])
    )

    # loop to confirm new well and same date
    for j in range(i + 1, numEntries):
        row2 = resultsList[j]
        wellId2 = row2["well"]
        date2 = row2["date"]
        # check to make sure wellID ISNT the same and the date is, then calculate all date
        if (wellId2 != wellId) and (date2 == date):
            output = row2["output"]
            totalGrossOilVolume = totalGrossOilVolume + float(
                output["grossOilWellHeadVolume"]
            )
            totalNetRevenue = totalNetRevenue + float(output["totalRevenue"])
            totalGrossGasVolume = totalGrossGasVolume + float(
                output["grossGasWellHeadVolume"]
            )
            oilRev = oilRev + float(output["oilRevenue"])
            gasRev = gasRev + float(output["gasRevenue"])
            totalExpense = totalExpense + float(output["totalExpense"])
            netIncome = netIncome + float(output["netIncome"])
            totalCapex = totalCapex + float(output["totalCapex"])
            biCashFlow = biCashFlow + float(output["beforeIncomeTaxCashFlow"])
            totalTaxSum = (
                totalTaxSum
                + float(output["totalSeveranceTax"])
                + float(output["adValoremTax"])
                + float(output["totalProductionTax"])
            )
    # counter to confirm same date
    dateCount = dateTable.count(date)
    # if dateCount is 0, then add each new summed variable to new list
    if dateCount == 0:
        dateTable.append(date)
        grossOilWellHeadVolumeTable.append(totalGrossOilVolume)
        totalNetRevenueTable.append(totalNetRevenue)
        grossGasWellHeadVolumeTable.append(totalGrossGasVolume)
        oilRevenueTable.append(oilRev)
        gasRevenueTable.append(gasRev)
        totalExpenseTable.append(totalExpense)
        netIncomeTable.append(netIncome)
        totalCapexTable.append(totalCapex)
        beforeIncomeTaxCashFlowTable.append(biCashFlow)
        totalTaxTable.append(totalTaxSum)


# Begins printing the clean CSV
fp = open(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\monthlyCashFlowRollupFinal2022Forecast.csv",
    "w",
)

# writes the header
headerString = (
    "Date,"
    + "Total Gross Oil Volume (bbl),"
    + "Total Net Reveune ($),"
    + "Total Gross Gas Volume (MCF),"
    + "Oil Revenue ($),"
    + "Gas Revenue ($),"
    + "Total Expenses ($),"
    + "Net Income ($),"
    + "Total CAPEX ($),"
    + "Before Income Tax Cash Flow ($),"
    + "Total Taxes ($)"
    + "\n"
)
fp.write(headerString)

# writes specific variables to correct CSV cell
for i in range(0, len(dateTable)):
    var = (
        str(dateTable[i])
        + ","
        + str(grossOilWellHeadVolumeTable[i])
        + ","
        + str(totalNetRevenueTable[i])
        + ","
        + str(grossGasWellHeadVolumeTable[i])
        + ","
        + str(oilRevenueTable[i])
        + ","
        + str(gasRevenueTable[i])
        + ","
        + str(-1 * totalExpenseTable[i])
        + ","
        + str(netIncomeTable[i])
        + ","
        + str(-1 * totalCapexTable[i])
        + ","
        + str(beforeIncomeTaxCashFlowTable[i])
        + ","
        + str(-1 * totalTaxTable[i])
        + "\n"
    )
    fp.write(var)

fp.close()

print("yay")

# test
