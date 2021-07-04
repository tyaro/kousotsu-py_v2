CREATE VIEW VIEW_TICKER_INFO as (
    SELECT * from BINANCE_TICKER_INFO as a
    WHERE a.tickerTime = (
        SELECT max(tickerTime) from BINANCE_TICKER_INFO as b
        WHERE a.symbol = b.symbol
        )
)