CREATE VIEW VIEW_TICKER_INFO_SPOT_BTC as (
    SELECT * from BINANCE_TICKER_INFO_SPOT_BTC as a
    WHERE a.tickerTime = (
        SELECT max(tickerTime) from BINANCE_TICKER_INFO_SPOT_BTC as b
        WHERE a.symbol = b.symbol
        )
)