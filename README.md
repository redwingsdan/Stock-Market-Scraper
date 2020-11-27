This is a stock market scraper which pulls price info daily from Google Finance at 4:00pm.

Inputs are provided via a csv (csv_owned_stocks.csv) of the stock names and the current holdings.

The resulting prices are applied to the stock holdings and then the date, total value, change from previous run and the calculated prices are exported to a new CSV (csv_stock_prices.csv).