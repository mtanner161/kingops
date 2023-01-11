# Import packages needed
from datetime import date, datetime, timedelta
import datetime as dt
import glob
import re
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages


def save_image(filename):

    # PdfPages is a wrapper around pdf
    # file so there is no clash and
    # create files with no error.
    p = PdfPages(filename)

    # get_fignums Return list of existing
    # figure numbers
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]

    # iterating over the numbers in list
    for fig in figs:

        # and saving the files
        fig.savefig(p, format='pdf')

    # close the object
    p.close()


productionNumbers = pd.read_csv(r".\kingops\data\productionHistoryMaster.csv")

productionNumbers.Date = pd.to_datetime(productionNumbers.Date)
productionNumbers["Quarter"] = pd.PeriodIndex(productionNumbers.Date, freq="Q")

datesAll = list(productionNumbers["Date"])
datesQ = list(productionNumbers["Quarter"])
netOil = list(productionNumbers["Net Oil Sales Volume (BBL/M)"])
netGas = list(productionNumbers["Gross MCFE Sales Volume (MCFE/M)"])

figNetOil = plt.figure()
figNetGas = plt.figure()
figNetBoe = plt.figure()

figNetOil, ax = plt.subplots()
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(12)))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.set_title('Manual DateFormatter', loc='left', y=0.85, x=0.02,
             fontsize='medium')

for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')

plt.plot(datesAll, netOil)
plt.plot(datesAll, netGas)


def save_image(filename):

    # PdfPages is a wrapper around pdf
    # file so there is no clash and
    # create files with no error.
    p = PdfPages(filename)

    # get_fignums Return list of existing
    # figure numbers
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]

    # iterating over the numbers in list
    for fig in figs:

        # and saving the files
        fig.savefig(p, format='pdf')

    # close the object
    p.close()


filename = r".\kingops\data\productionChart.pdf"
save_image(filename)

print("yay")
