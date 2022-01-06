# Import Needed Modules 
import json
import requests
import time
import sys
from csv import writer

#1 Access Yahoo API and Error Check
try: 
    apikey='MmIX0qS0ZN9hDVDRXkv8r8ETs36Wmdyg26gj5R8e'  # my API key

    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols":sys.argv[1]}
    headers = {
      'x-api-key': apikey
       }

    response = requests.request("GET", url, headers=headers, params=querystring)  # access API

    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        stock_json = response.json()
except IndexError:   # report error if not found and exit
    print("Stock Ticker Is Not Found")
    exit()


# Time Conversion and Error Check
try:
    timestamp = int(str(stock_json['quoteResponse']['result'][0]["regularMarketTime"]))  # retrieve the market time
    converted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp))  # convert the market time to an understandable form
except IndexError:  # report error if no time is found and exit
    print("Stock Ticker Is Not Found")
    exit()

# Print Results and Error Check
try:
    print("Company Name: " + stock_json['quoteResponse']['result'][0]["displayName"] + ", Current Price: $" +  # retrieve and print the company name, current price, and current time
      str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"]) + ", Current Market Time: " + converted_time)
except KeyError:  # report error if name or price is not found and exit
    print("Stock Ticker Is Not Found")
    exit()

# Write to CSV
with open('Quiz2.csv', 'a', newline='') as file_object:  # open a csv called Quiz2.csv
    writer_object = writer(file_object)
    writer_object.writerow([sys.argv[1], converted_time, str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"])])  # write the stock ticker, time, and price to the csv
    file_object.close()  # close the connection until opened again
