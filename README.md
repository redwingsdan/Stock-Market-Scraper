This is a stock market scraper which pulls price info daily from Google Finance at 4:00pm.

Inputs are provided via a csv (csv_owned_stocks.csv) of the stock names and the current holdings.

The resulting prices are applied to the stock holdings and then the date, total value, change from previous run and the calculated prices are exported to a new CSV (csv_stock_prices.csv).

## USAGE:

1. Ensure that the stockscraper.py file is in the same directory as csv_owned_stocks.csv and csv_stock_prices.csv

2. Enter your owned stocks in csv_owned_stocks.csv
 * The first row should be the ticker id for the stock
 * The second row should be your total holdings for that stock

3. Append your owned stocks in the csv_stock_prices.csv header

4. Run the script in command line with
```python
python stockscraper.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
