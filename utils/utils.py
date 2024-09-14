def return_features(conn,lat,lon):

    lat = float(lat)
    lon = float(lon)

    df = conn.execute(f'''SELECT 
                        accumulated_temperature
                        , soil_moisture_regime
                        , soil_nutrient_regime
                    FROM esc_features_interpolated
                    ORDER BY ABS(lat - {lat}) + ABS(lon - {lon}) ASC
                    LIMIT 1''').fetch_df()

    accumulated_temperature = df['accumulated_temperature'][0]
    soil_moisture_regime = df['soil_moisture_regime'][0]
    soil_nutrient_regime = df['soil_nutrient_regime'][0]

    return accumulated_temperature, soil_moisture_regime, soil_nutrient_regime