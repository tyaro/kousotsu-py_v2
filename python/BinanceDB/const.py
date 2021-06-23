#create view VIEW_BINANCE_CRYPTO_INFO2 as (SELECT * from BINANCE_CRYPTO_INFO2 as a where calcTime = (select max(calcTime) from BINANCE_CRYPTO_INFO2 where a.calctime = b.calctime))

# データフレームで使用するカラム名の定義

# KLINES DATA 
OPEN_TIME_ = 'OpenTime'    #開始時間
CLOSE_TIME_ = 'CloseTime'  #終了時間
OPEN_ = 'Open' # 始値
CLOSE_ = 'Close'   # 終値
HIGH_  = 'High'    # 高値
LOW_   = 'Low'     # 底値
VOLUME_ = 'Volume' # 取引量
QUOTE_ASSET_VOLUME_ = 'QuoteAssetVolume'   #
NUMBER_OF_TRADES_ = 'NumberOfTrades'   #
TAKER_BUY_BASE_ASSET_VOLUME_ = 'TakerBuyBaseAssetVolume'   #
TAKER_BUY_QUOTE_ASSET_VOLUME_ = 'TakerBuyQuoteAssetVolume' #
IGNORE_ = 'Ignore' #

# TICKERS PRICE DATA
SYMBOL_ = 'symbol'
PRICE_ = 'price'
POINT_ = 'point'
TIME_ = 'time'

# TICKERS PRICE DATA
TICKER_TIME_ = 'tickerTime'

# TICKERS PRICE DATAの項目名
TICKERS_INFO_COLUMNS = [
    SYMBOL_,
    PRICE_,
    TICKER_TIME_,
]

# TICKERS PRICE DATAの項目名
TICKERS_COLUMNS = [
    SYMBOL_,
    PRICE_,
    TIME_,
    POINT_,
]

# ローソク足をAPIからとってきたときの項目名定義
KLINES_COLUMNS = [
    OPEN_TIME_,
    OPEN_,
    HIGH_,
    LOW_,
    CLOSE_,
    VOLUME_,
    CLOSE_TIME_,
    QUOTE_ASSET_VOLUME_,
    NUMBER_OF_TRADES_,
    TAKER_BUY_BASE_ASSET_VOLUME_,
    TAKER_BUY_QUOTE_ASSET_VOLUME_,
    IGNORE_
    ]
