CREATE OR REPLACE TABLE esc_features_interpolated
AS 
SELECT cast(lon as numeric) as lon
        , cast(lat as numeric) as lat
        , cast(accumulated_temperature as numeric) as accumulated_temperature
        , cast(soil_moisture_regime as numeric) as soil_moisture_regime
        , cast(soil_nutrient_regime as numeric) as soil_nutrient_regime
FROM gdf