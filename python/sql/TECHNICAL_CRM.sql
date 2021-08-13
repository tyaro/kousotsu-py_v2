-- 変動率の中央値
CREATE TABLE TECHNICAL_CRM(
    calcTime DATETIME NOT NULL,
    MED01 double,
    MED05 double,
    MED10 double,
    MED15 double,
    MED30 double,
    MED60 double,
    MED240 double,
    MED360 double,
    MED480 double,
    MED720 double,
    PRIMARY KEY(calcTime)
)