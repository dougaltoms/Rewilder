import streamlit as st
import pickle
import pandas as pd

st.header('Importing a pickled regression model')
st.markdown('---')

col1, col2, col3, col4, col5 =  st.columns(5)

with col1:
    latitude = st.number_input('Latitude', value=56)
with col2:
    longitude = st.number_input('Longitude', value=-2)
with col3:
    accumulated_temperature = st.number_input('Accumulated Temperature', value=1400)
with col4:
    soil_moisture_regime = st.number_input('SMR', value=3)
with col5:
    soil_nutrient_regime = st.number_input('SNR', value=3)


with open('model.pickle', 'rb') as file:
    model = pickle.load(file)


    input_data = pd.DataFrame({
        'latitude': [latitude],
        'longitude': [longitude],
        'accumulated_temperature': [accumulated_temperature],
        'soil_moisture_regime': [soil_moisture_regime],
        'soil_nutrient_regime': [soil_nutrient_regime]})

    with st.spinner('Running model...'):
        prediction = model.predict(input_data)
        prediction_df = pd.DataFrame(prediction, columns=['AH', 'ASP', 'BPO', 'CAR', 'HBM', 'PBI', 'POK', 'ROK', 'ROW', 'SBI', 'SC', 'SLI', 'SOK', 'SP', 'WCH', 'WEM'])

        top_species = prediction_df.T.nlargest(3, 0).reset_index()
        top_species.columns = ['Species', 'Ecosuit Score']

        st.dataframe(top_species)

