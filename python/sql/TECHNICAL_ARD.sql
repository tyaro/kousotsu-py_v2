CREATE TABLE TECHNICAL_ARR(
    pair VARCHAR(20) NOT NULL,
    calcTime DATETIME NOT NULL,
    price double,
    ART double,
    ARR5 double,
    ARR10 double,
    ARR20 double,
    ARRE5 double,
    ARRE10 double,
    ARRE20 double,
    PRIMARY KEY(pair,calcTime)
)