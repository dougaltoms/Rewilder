def return_features(df, lat, lon):

    lat = float(lat)
    lon = float(lon)

    row = (
        df.loc[:, ['lat', 'lon', 'accumulated_temperature', 'soil_moisture_regime', 'soil_nutrient_regime']]
        .assign(distance=lambda x: abs(x['lat'] - lat) + abs(x['lon'] - lon))
        .sort_values(by='distance')
        .head(1)
        .drop(columns='distance')
    )

    accumulated_temperature = round(row['accumulated_temperature'].iloc[0])
    soil_moisture_regime = round(row['soil_moisture_regime'].iloc[0],2)
    soil_nutrient_regime = round(row['soil_nutrient_regime'].iloc[0],2)

    return accumulated_temperature, soil_moisture_regime, soil_nutrient_regime
