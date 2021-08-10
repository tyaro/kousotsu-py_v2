CREATE TABLE TECHNICAL_EMA(
    pair VARCHAR(20) NOT NULL,
    calcTime DATETIME NOT NULL,
    price double,
    BTCPrice double,
    EMA200_1D double,
    EMA100_1D double,
    EMA75_1D double,
    EMA50_1D double,
    EMA25_1D double,
    BTC_EMA200_1D double,
    BTC_EMA100_1D double,
    BTC_EMA75_1D double,
    BTC_EMA50_1D double,
    BTC_EMA25_1D double,
    PRIMARY KEY(pair,calcTime)
)