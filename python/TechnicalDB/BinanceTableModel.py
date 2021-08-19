import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime,BIGINT
from setting import Base
from setting import ENGINE

#ローソク足モデル
class BINANCE_KLINES_1DAY_MODEL(Base):
    __tablename__ = 'BINANCE_KLINES_1DAY'
    symbol = Column('symbol', String(20),primary_key=True)
    openTIme = Column('openTime', DateTime,primary_key=True)
    openPrice = Column('open', Float)
    closePrice = Column('close', Float)
    highPrice = Column('high', Float)
    lowPrice = Column('low', Float)
    coinVolume = Column('coinVolume', Float)
    usdtVolume = Column('usdtVolume', Float)

#ローソク足モデル
class BINANCE_KLINES_1DAY_BTC_MODEL(Base):
    __tablename__ = 'BINANCE_KLINES_1DAY_BTC'
    symbol = Column('symbol', String(20),primary_key=True)
    openTIme = Column('openTime', DateTime,primary_key=True)
    openPrice = Column('open', Float)
    closePrice = Column('close', Float)
    highPrice = Column('high', Float)
    lowPrice = Column('low', Float)
    coinVolume = Column('coinVolume', Float)
    usdtVolume = Column('usdtVolume', Float)
    takerBuyUsdtVolume = Column('takerBuyUsdtVolume', Float)

#ローソク足モデル
class BINANCE_KLINES_4HOUR_MODEL(Base):
    __tablename__ = 'BINANCE_KLINES_4HOUR'
    symbol = Column('symbol', String(20),primary_key=True)
    openTIme = Column('openTime', DateTime,primary_key=True)
    openPrice = Column('open', Float)
    closePrice = Column('close', Float)
    highPrice = Column('high', Float)
    lowPrice = Column('low', Float)
    coinVolume = Column('coinVolume', Float)
    usdtVolume = Column('usdtVolume', Float)
    takerBuyUsdtVolume = Column('takerBuyUsdtVolume', Float)

#ローソク足モデル
class BINANCE_KLINES_1HOUR_MODEL(Base):
    __tablename__ = 'BINANCE_KLINES_1HOUR'
    symbol = Column('symbol', String(20),primary_key=True)
    openTIme = Column('openTime', DateTime,primary_key=True)
    openPrice = Column('open', Float)
    closePrice = Column('close', Float)
    highPrice = Column('high', Float)
    lowPrice = Column('low', Float)
    coinVolume = Column('coinVolume', Float)
    usdtVolume = Column('usdtVolume', Float)
    takerBuyUsdtVolume = Column('takerBuyUsdtVolume', Float)

#ローソク足モデル
class BINANCE_KLINES_1MIN_MODEL(Base):
    __tablename__ = 'BINANCE_KLINES_1MIN'
    symbol = Column('symbol', String(20),primary_key=True)
    openTIme = Column('openTime', DateTime,primary_key=True)
    openPrice = Column('open', Float)
    closePrice = Column('close', Float)
    highPrice = Column('high', Float)
    lowPrice = Column('low', Float)
    coinVolume = Column('coinVolume', Float)
    usdtVolume = Column('usdtVolume', Float)
    takerBuyUsdtVolume = Column('takerBuyUsdtVolume', Float)

#TICKER モデル
class BINANCE_TICKER_INFO_MODEL(Base):
    __tablename__ = 'BINANCE_TICKER_INFO'
    symbol = Column('symbol', String(20),primary_key=True)
    tickerTime = Column('tickerTime', DateTime,primary_key=True)
    price = Column('price', Float)

#TICKER モデル
class BINANCE_TICKER_INFO_SPOT_MODEL(Base):
    __tablename__ = 'BINANCE_TICKER_INFO_SPOT'
    symbol = Column('symbol', String(20),primary_key=True)
    tickerTime = Column('tickerTime', DateTime,primary_key=True)
    price = Column('price', Float)

#通貨ペアマスタ
class BINANCE_SYMBOL_MASTER(Base):
    __tablename__ = 'BINANCE_SYMBOL_MASTER'
    symbol = Column('symbol', String(20),primary_key = True)
    point = Column('point', Integer)
    updatetime = Column('updatetime',DateTime)    

#通貨ペアマスタ
class BINANCE_SYMBOL_MASTER_SPOT(Base):
    __tablename__ = 'BINANCE_SYMBOL_MASTER_SPOT'
    symbol = Column('symbol', String(20),primary_key = True)
    point = Column('point', Integer)
    updatetime = Column('updatetime',DateTime)    

#通貨ペアマスタ
class BINANCE_SYMBOL_MASTER_SPOT_BTC(Base):
    __tablename__ = 'BINANCE_SYMBOL_MASTER_SPOT_BTC'
    symbol = Column('symbol', String(20),primary_key = True)
    point = Column('point', Integer)
    updatetime = Column('updatetime',DateTime)    

def main(args):
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)