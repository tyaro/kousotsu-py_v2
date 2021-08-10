CREATE TABLE TECHNICAL_MACD(
    pair VARCHAR(20) NOT NULL,
    calcTime DATETIME NOT NULL,
    price double,
    EMA26_1D double,
    EMA12_1D double,
    SIGNAL_1D double,
    EMA26_4H double,
    EMA12_4H double,
    SIGNAL_4H double,
    EMA26_1H double,
    EMA12_1H double,
    SIGNAL_1H double,
    EMA26_15M double,
    EMA12_15M double,
    SIGNAL_15M double,
    PRIMARY KEY(pair,calcTime)
)