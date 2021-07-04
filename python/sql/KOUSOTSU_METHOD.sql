CREATE TABLE KOUSOTSU_METHOD(
    pair VARCHAR(20) NOT NULL,
    calcTime DATETIME NOT NULL,
    kousotsuPrice1 double,
    kousotsuPrice2 double,
    kousotsuPrice3 double,
    EntryPointLong double,
    EntryPointShort double,
    PRIMARY KEY(pair,calcTime)
)