import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from bs4 import BeautifulSoup
import requests


tesla = yf.Ticker("TSLA")
gme = yf.Ticker("GME")

tesla_data = tesla.history(period="max")
gme_data = gme.history(period="max")

tesla_data.reset_index(inplace=True)
gme_data.reset_index(inplace=True)

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data, "html.parser")
tables = soup.find_all("table")

# Tesla Revenue
tesla_revenue = pd.read_html(str(tables[1]))[0]
tesla_revenue.columns = ['Date', 'Revenue']
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# GME Revenue
gme_revenue = pd.read_html(str(tables[2]))[0]
gme_revenue.columns = ['Date', 'Revenue']
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r"\$", "", regex=True).str.replace(",", "").astype(float)
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(r"\$", "", regex=True).str.replace(",", "").astype(float)



def make_tesla_graph(tesla_data, tesla_revenue, stock, title):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    tesla_data['Date'] = pd.to_datetime(tesla_data['Date']).dt.tz_localize(None)
    tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])

    tesla_data = tesla_data[tesla_data['Date'] <= datetime.datetime(2021, 6, 1)]
    tesla_revenue = tesla_revenue[tesla_revenue['Date'] <= datetime.datetime(2021, 6, 1)]

    ax1.plot(tesla_data['Date'], tesla_data['Close'], 'purple', label='Stock Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price ($)', color='purple')
    ax1.tick_params('y', colors='purple')

    ax2 = ax1.twinx()
    ax2.plot(tesla_revenue['Date'], tesla_revenue['Revenue'], 'orange', label='Revenue')
    ax2.set_ylabel('Revenue ($ in millions)', color='orange')
    ax2.tick_params('y', colors='orange')

    plt.title(title)
    fig.tight_layout()
    plt.show()

def make_gme_graph(gme_data, gme_revenue, stock, title):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    gme_data['Date'] = pd.to_datetime(gme_data['Date']).dt.tz_localize(None)
    gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])

    gme_data = gme_data[gme_data['Date'] <= datetime.datetime(2021, 6, 1)]
    gme_revenue = gme_revenue[gme_revenue['Date'] <= datetime.datetime(2021, 6, 10)]

    ax1.plot(gme_data['Date'], gme_data['Close'], 'r-', label='Stock Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price ($)', color='r')
    ax1.tick_params('y', colors='r')

    ax2 = ax1.twinx()
    ax2.plot(gme_revenue['Date'], gme_revenue['Revenue'], 'b-', label='Revenue')
    ax2.set_ylabel('Revenue ($ in millions)', color='b')
    ax2.tick_params('y', colors='b')

    plt.title(title)
    fig.tight_layout()
    plt.show()

make_tesla_graph(tesla_data, tesla_revenue, 'TSLA', 'Tesla Stock Price and Revenue')
make_gme_graph(gme_data, gme_revenue, 'GME', 'GameStop Stock Price and Revenue')
