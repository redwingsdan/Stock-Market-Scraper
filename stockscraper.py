import requests
import csv
import time
import schedule
from bs4 import BeautifulSoup
from decimal import Decimal, ROUND_DOWN
from datetime import date

class Stock:
    def __init__(self, name, holdings):
        self.name = name
        self.holdings = holdings
        self.price = 0
    def get_stock_name(self):
        return self.name + ' (' + str(format(self.holdings, '.4f')) + ' shares)'
    #Calculate the value of the stock based on the holdings
    def get_value(self):
        stock_price_dec = Decimal(self.price.replace("$","").replace(",","")) #convert stock price to a decimal
        return Decimal(Decimal(self.holdings) * stock_price_dec).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        
def populate_stocks(stocks):
    print('Populating stocks...')
    csvFileName = 'csv_owned_stocks.csv'
    with open(csvFileName, newline='') as csvfile:
        r = csv.reader(csvfile)
        existingData = [line for line in r]
    #Add stocks from the read csv file
    for colIndex in range(len(existingData[0])):
        #For each header, add a stock using the header and the corresponding value
        stockToAdd = Stock(existingData[0][colIndex], Decimal(existingData[1][colIndex]))
        stocks.append(stockToAdd)
        print('Added stock', stockToAdd.get_stock_name())

def writer (header, data, filename, option):
    if option == 'write':
        with open (filename, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerow(data)
    elif option == 'update':
        with open (filename, 'a', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    else:
        print('Unknown option')
       
def updater(filename, newData, newHeaders):
    #read existing csv data except the header
    with open(filename, newline='') as csvfile:
        r = csv.reader(csvfile)
        next(r)
        existingData = [line for line in r]
    #write the new headers first and then the existing data
    with open(filename, 'w', newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(newHeaders)
        w.writerows(existingData)
    #append the new data after the existing data
    totalIndex = newHeaders.index('Total') #Use the change column index
    priceChange = newData[totalIndex] - Decimal(existingData[-1][totalIndex])
    percentageChange = None if Decimal(existingData[-1][totalIndex]) == 0 else (priceChange / Decimal(existingData[-1][totalIndex])) * 100
    changeIndex = newHeaders.index('Change (%)') #Use the change column index
    newData.insert(changeIndex, str(priceChange) + ' (' + str(format(percentageChange, '.2f')) + '%)')
    writer(None, newData, filename, 'update')
    
def load_stock_data(t):
    base_url = "https://www.google.com/finance/quote/"
    exchange_types = ['NASDAQ', 'NYSE']
    stocks = []
    populate_stocks(stocks);
    #Get the price info for all the populated stocks
    for stock in stocks:
        ticker_wizard = None
        #Load the page with a valid ticker
        for exchange_type in exchange_types:
            url = base_url + stock.name + ":" + exchange_type
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            ticker_wizard = soup.select("c-wiz main")
            if len(ticker_wizard) > 0:
                break
        #Iterate through the child elements until we get to the stock price
        child_div = ticker_wizard[0]
        c_wiz = list(child_div.children)[1]
        child_div_level = list(c_wiz.children)[0]
        for levels in range(6):
            child_div_level = list(child_div_level.children)[0]
        stock_price = list(child_div_level.children)[1]
        for levels in range(5):
            stock_price = list(stock_price.children)[0]
        stock.price = stock_price.get_text()
    #Export the price info to an excel doc
    csvFileName = 'csv_stock_prices.csv'
    csvHeader = ['Date', 'Total', 'Change (%)'] + list(map(lambda s: s.name, stocks))
    today = date.today()
    formattedDate = today.strftime("%m/%d/%y")
    csvData = list()
    csvData.append(str(formattedDate))
    csvData.append(sum(list(map(lambda s: s.get_value(), stocks)))) #total row
    csvData.extend(list(map(lambda s: str(s.get_value()), stocks)))
    updater(csvFileName, csvData, csvHeader)
    print('Finished loading stock data for', formattedDate)

schedule.every().day.at("16:00").do(load_stock_data, 'Loading stock data')
while True:
    schedule.run_pending()
    print('Waiting to load data')
    time.sleep(60) # wait one minute
#Use this call instead of the scheduler to test
#Replace the input CSV to test using different data
#load_stock_data(None) 