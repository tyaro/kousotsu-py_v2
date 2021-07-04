CREATE VIEW VIEW_KOUSOTSU_METHOD as (
    SELECT * from KOUSOTSU_METHOD as a
    WHERE a.calcTime = (
        SELECT max(calcTime) from KOUSOTSU_METHOD as b
        WHERE a.pair = b.pair
        )
)