import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime,BIGINT
from setting import Base
from setting import ENGINE

# 高卒たんテーブル
class KOUSOTSU_METHOD_MODEL(Base):
    __tablename__ = 'KOUSOTSU_METHOD'
    symbol = Column('pair', String(20),primary_key=True)
    calcTime = Column('calcTime', DateTime,primary_key=True)
    kousotsuPrice1 = Column('kousotsuPrice1', Float)
    kousotsuPrice2 = Column('kousotsuPrice2', Float)
    kousotsuPrice3 = Column('kousotsuPrice3', Float)
    EntryPointLong = Column('EntryPointLong', Float)
    EntryPointShort = Column('EntryPointShort', Float)
    TREND = Column('TREND', String(10))
    


def main(args):
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)