CREATE TABLE BINANCE_TICKER_INFO_SPOT_BTC (
  symbol varchar(20) NOT NULL,
  tickerTime datetime NOT NULL,
  price float DEFAULT NULL,
  PRIMARY KEY (symbol,tickerTime)
)