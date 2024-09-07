import streamlit as st
import pickle
import pandas as pd
import extra_streamlit_components as stx

st.header('Rewilder')
st.subheader('Mapping rewilding suitability for native ancient tree species')

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="Data Input", description=""),
    stx.TabBarItemData(id=2, title="Results", description=""),
], default=1)

if str(chosen_id) == '1':

    col1, col2, col3, col4, col5 =  st.columns(5)

    with col1:
        latitude = st.number_input('Latitude', value=56)
        st.session_state['latitude'] = latitude
    with col2:
        longitude = st.number_input('Longitude', value=-2)
        st.session_state['longitude'] = longitude
    with col3:
        accumulated_temperature = st.number_input('Accumulated Temp', value=1400, step=10)
        st.session_state['accumulated_temperature'] = accumulated_temperature
    with col4:
        soil_moisture_regime = st.number_input('SMR', value=3)
        st.session_state['soil_moisture_regime'] = soil_moisture_regime
    with col5:
        soil_nutrient_regime = st.number_input('SNR', value=3)
        st.session_state['soil_nutrient_regime'] = soil_nutrient_regime

if str(chosen_id) == '2':
    with st.spinner('Running model...'):
        with open('model.pickle', 'rb') as file:

            model = pickle.load(file)
            st.session_state['model'] = model


            input_data = pd.DataFrame({
                'latitude': [st.session_state.latitude],
                'longitude': [st.session_state.longitude],
                'accumulated_temperature': [st.session_state.accumulated_temperature],
                'soil_moisture_regime': [st.session_state.soil_moisture_regime],
                'soil_nutrient_regime': [st.session_state.soil_nutrient_regime]})

            st.session_state['input_data'] = input_data

            file.close()

            prediction = st.session_state.model.predict(st.session_state.input_data)
            prediction_df = pd.DataFrame(prediction, columns=['AH', 'ASP', 'BPO', 'CAR', 'HBM', 'PBI', 'POK', 'ROK', 'ROW', 'SBI', 'SC', 'SLI', 'SOK', 'SP', 'WCH', 'WEM'])

            top_species = prediction_df.T.nlargest(5, 0).reset_index()
            top_species.columns = ['Species', 'Ecosuit Score']

            st.dataframe(top_species, use_container_width=True)

with st.expander('Show map'):
    st.image('uk_agri_capability.png')

st.markdown('---')
feedback = st.feedback("faces")
if feedback:
    st.write('Thank you for submitting feedback')
