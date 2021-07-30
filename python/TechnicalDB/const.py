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

# 高卒たんメソッド
PRICE_CHANGE_ = 'PriceChange'
GAIN_VALUE_ = 'GainValue'
PRE_GAIN_VALUE_ = 'PreGainValue'
PRE_HIGH_ = 'PreHigh'
PRE_LOW_ = 'PreLow'
PRE_OPEN_ = 'PreOpen'
PRE_CLOSE_ = 'PreClose'
KOUSOTSU_PRICE_0_ = 'kousotsuPrice0'
KOUSOTSU_PRICE_1_ = 'kousotsuPrice1'
KOUSOTSU_PRICE_2_ = 'kousotsuPrice2'
KOUSOTSU_PRICE_3_ = 'kousotsuPrice3'
OPERATOR_ = 'Operator'
KOUSOTSU_HH_ = 'kousotsuHH'
KOUSOTSU_LL_ = 'kousotsuLL'
KOUSOTSU_HH_PRE_ = 'kousotsuHHP'
KOUSOTSU_LL_PRE_ = 'kousotsuLLP'
LONG_ENTRY_POINT_ = 'EntryPointLong'
SHORT_ENTRY_POINT_ = 'EntryPointShort'
CALC_TIME_ = 'calcTime'

# テクニカルで追加されるカラム名
CHANGE_RATE_ = 'ChangeRate'
CHANGE_RATE_MAX_10DAYS_ = 'ChangeRateMax10days'
CHANGE_RATE_MIN_10DAYS_ = 'ChangeRateMin10days'
UP_RATE_ = 'UpRate'
DOWN_RATE_ = 'DownRate'
EMA_200_ = 'EMA200'
EMA_100_ = 'EMA100'
EMA_50_ = 'EMA50'
RSI_14_ = 'RSI14'
FRIEND_RATE_UP_ ='FriendRateUp'
FRIEND_RATE_DOWN_ ='FriendRateDown'
EMA_S_ = 'EMA_S'
EMA_M_ = 'EMA_M'
TREND_ = 'TREND'
