CREATE VIEW VIEW_TECHNICAL_INFOS as (
    SELECT * from TECHNICAL_INFOS as a
    WHERE a.calcTime = (
        SELECT max(calcTime) from TECHNICAL_INFOS as b
        WHERE a.pair = b.pair
        )
)