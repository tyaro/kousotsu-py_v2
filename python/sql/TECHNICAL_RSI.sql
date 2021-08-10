CREATE TABLE TECHNICAL_RSI(
    pair VARCHAR(20) NOT NULL,
    calcTime DATETIME NOT NULL,
    price double,
    1min double,
    15min double,
    1hour double,
    4hour double,
    1day double,
    PRIMARY KEY(pair,calcTime)
)