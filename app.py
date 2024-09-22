import streamlit as st
import pickle
import pandas as pd
import extra_streamlit_components as stx
from tree_mapping import tree_mapping
from streamlit_folium import st_folium
import folium
from folium import Marker
import geopandas as gpd
from shapely.geometry import Point
from utils.utils import return_features, tree_facts


st.header('Rewilder')
st.subheader('Mapping rewilding suitability for native ancient tree species')

api_key = st.secrets["API_KEY"]

df = pd.read_csv('ecological_site_classification.csv')
features_df = pd.read_csv('esc_features.csv')

tab1, tab2, tab3 = st.tabs(['Data Input', 'Results', 'Mapping'])

with tab1:
    col1, col2 =  st.columns(2)
    with col1:
        latitude = st.number_input('Latitude', value=51.0, min_value = 50.0, max_value=60.0, step=.1)
        st.session_state['latitude'] = latitude
    with col2:
        longitude = st.number_input('Longitude', value=-1.0, min_value=-7.0, max_value=2.0, step=.1)
        st.session_state['longitude'] = longitude

    accumulated_temperature, soil_moisture_regime, soil_nutrient_regime = return_features(features_df, st.session_state.latitude, st.session_state.longitude)
    st.session_state['accumulated_temperature'] = accumulated_temperature
    st.session_state['soil_moisture_regime'] = soil_moisture_regime
    st.session_state['soil_nutrient_regime'] = soil_nutrient_regime

    res1, res2, res3 =st.columns(3)
    with res1:
        st.metric('Accumulated Temperature', accumulated_temperature)
    with res2:  
        st.metric('Soil Moisture Regime', soil_moisture_regime)
    with res3:
        st.metric('Soil Nutrient Regime', soil_nutrient_regime)

with tab2:
    with st.spinner('Running model...'):
        with open('pickle/model.pickle', 'rb') as file:

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

            species_df = prediction_df.T.nlargest(5, 0).reset_index()
            species_df.columns = ['Species Code', 'Ecosuit Score']
            species_df['Species'] = species_df['Species Code'].map(tree_mapping)
    
            st.dataframe(species_df[['Species','Species Code', 'Ecosuit Score']], use_container_width=True, hide_index=True)

with tab3:

    popup_text = f''' <strong>Top 3 Predicted Tree Species</strong><br>
                            1. {species_df['Species'].iloc[0]} ({round(species_df['Ecosuit Score'].iloc[0],2)})<br>
                            2. {species_df['Species'].iloc[1]} ({round(species_df['Ecosuit Score'].iloc[1],2)})<br>
                            3. {species_df['Species'].iloc[2]} ({round(species_df['Ecosuit Score'].iloc[2],2)})'''
    
    with st.spinner('Creating Map'):
        with open('pickle/uk_ag.pickle', 'rb') as file:
                
                uk_ag = pickle.load(file)
                st.session_state['uk_ag'] = uk_ag[['geometry', 'NUMERIC_GRADE']]
            
        point = gpd.GeoSeries([Point(st.session_state.longitude, st.session_state.latitude)], crs="EPSG:4326")

        if st.session_state.uk_ag.crs != point.crs:
            st.session_state.uk_ag = st.session_state.uk_ag.to_crs(point.crs)

        st.session_state.uk_ag['distance_to_point'] = st.session_state.uk_ag['geometry'].distance(point[0])
        threshold = .10
        uk_ag_filtered = st.session_state.uk_ag[st.session_state.uk_ag['distance_to_point'] <= threshold]
        uk_ag_filtered = uk_ag_filtered.dissolve(by='NUMERIC_GRADE', sort=False)
        uk_ag_filtered = uk_ag_filtered.reset_index()
        uk_ag_filtered = uk_ag_filtered[['geometry', 'NUMERIC_GRADE']]
        
        m = folium.Map(location=(-38.625, -12.875))
        m = uk_ag_filtered.explore('NUMERIC_GRADE',m=m,cmap='autumn',tiles="Esri.WorldImagery", attr = "© Dougal Toms")
        folium.Marker(location=[st.session_state.latitude, st.session_state.longitude],popup=folium.Popup(popup_text, max_width=300), icon=folium.Icon(color="green", icon="tree")).add_to(m)
        st_folium(m,width=1000, height=500)

        # info = st.toggle('More info')

        with st.expander('More info'):

            tree_facts(species_df['Species'].iloc[0], api_key)

st.markdown('---')
with st.expander('Show map'):
    st.image('uk_agri_capability.png')
feedback = st.feedback("faces")
if feedback:
    st.write('Thank you for submitting feedback')
