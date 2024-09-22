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


def tree_facts(species, api_key):
    
    import google.generativeai as genai
    import os
    import streamlit as st

    prompt = f'''Please generate a a brief summary of the following ancient tree species in the UK: {species}.
            The information is being used for a dashboard which estimates ecosuitability of tree species for rewilding poor quality farmland in the UK.
            Do not hallucinate. Be factual and interesting. Don't return any pre-amble'''

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt,stream=False)
    # for chunk in response:
    with st.chat_message("ai"):
        st.write(response.text)
