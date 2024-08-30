CREATE OR REPLACE TABLE ecological_site_classification
    (x FLOAT
    , y FLOAT
    , accumulated_temperature INT
    , continentality INT
    , dams INT
    , moisture_deficit INT
    , soil_moisture_regime INT
    , soil_nutrient_regime INT
    , elevation INT
    , specied VARCHAR(3)
    , yc INT
    , cyc INT
    , limitingfact VARCHAR(4)
    , ecosuit FLOAT
    , nvc1 VARCHAR(3)
    , nvc2 VARCHAR(3)
    , nvc3 VARCHAR(3)
    , latitude FLOAT
    , longitude FLOAT);