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
    stocks.append( Stock('KHC', 42) )
    stocks.append( Stock('MCD', 10.056) )
    stocks.append( Stock('T', 71.3165) )
    stocks.append( Stock('INTC', 98.6304) )
    stocks.append( Stock('JNJ', 33.2222) )
    stocks.append( Stock('KO', 98.816) )
    stocks.append( Stock('MSFT', 24.0577) )
    
    stocks.append( Stock('AMD', 35) )
    stocks.append( Stock('AMZN', 2) )
    stocks.append( Stock('AAPL', 28.097) )
    stocks.append( Stock('AMAT', 44.174) )
    stocks.append( Stock('CSGP', 1) )
    stocks.append( Stock('COST', 4.007) )
    stocks.append( Stock('GIS', 45.384) )
    stocks.append( Stock('GMHI', 30) )
    stocks.append( Stock('IBM', 23.306) )
    stocks.append( Stock('NKE', 28.054) )
    stocks.append( Stock('PENN', 63) )
    stocks.append( Stock('SPCE', 15) )
    stocks.append( Stock('V', 13.018) )
    stocks.append( Stock('WMT', 22.094) )
    stocks.append( Stock('WELL', 55.119) )
    stocks.append( Stock('WYND', 111.055) )
    for stock in stocks:
        print('Added stock', stock.get_stock_name())

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
        print('Valued at:', str(stock.get_value()));
    #Export the price info to an excel doc
    csvFileName = 'csv_stock_prices.csv'
    csvHeader = ['Date', 'Total'] + list(map(lambda s: s.name, stocks))
    today = date.today()
    formattedDate = today.strftime("%m/%d/%y")
    csvData = list()
    csvData.append(str(formattedDate))
    csvData.append(sum(list(map(lambda s: s.get_value(), stocks)))) #total row
    csvData.extend(list(map(lambda s: str(s.get_value()), stocks)))
    #writer(csvHeader, csvData, csvFileName, 'write')
    updater(csvFileName, csvData, csvHeader)

schedule.every().day.at("12:00").do(load_stock_data, 'Loading stock data')
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute