CREATE VIEW VIEW_TICKER_INFO_SPOT as (
    SELECT * from BINANCE_TICKER_INFO_SPOT as a
    WHERE a.tickerTime = (
        SELECT max(tickerTime) from BINANCE_TICKER_INFO_SPOT as b
        WHERE a.symbol = b.symbol
        )
)