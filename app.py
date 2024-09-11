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

st.header('Rewilder')
st.subheader('Mapping rewilding suitability for native ancient tree species')

df = pd.read_csv('/Users/dougaltoms/Documents/Rewilder/ecological_site_classification.csv')

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="Data Input", description=""),
    stx.TabBarItemData(id=2, title="Results", description=""),
    stx.TabBarItemData(id=3, title="Map", description=""),
    ], default=1)

if str(chosen_id) == '1':

    col1, col2, col3, col4, col5 =  st.columns(5)
    with col1:
        latitude = st.number_input('Latitude', value=56, min_value = 50, max_value=60)
        st.session_state['latitude'] = latitude
    with col2:
        longitude = st.number_input('Longitude', value=-2, min_value=-7, max_value=2)
        st.session_state['longitude'] = longitude
    with col3:
        accumulated_temperature = st.number_input('Accumulated Temp', value=1400, step=10, min_value = 140, max_value=2200)
        st.session_state['accumulated_temperature'] = accumulated_temperature
    with col4:
        soil_moisture_regime = st.selectbox('SMR', options=[0,1,2,3,4,5,6,7,8], index=4)
        st.session_state['soil_moisture_regime'] = soil_moisture_regime
    with col5:
        soil_nutrient_regime = st.selectbox('SNR', options=[0,1,2,3,4,5,6],index=3)
        st.session_state['soil_nutrient_regime'] = soil_nutrient_regime

    with st.expander('Show map'):
        st.image('uk_agri_capability.png')

if str(chosen_id) == '2':
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

if str(chosen_id) == '3':

    st.write('Streamlit Plot')
    df = df[df['latitude'].between((st.session_state.latitude)-.5, (st.session_state.latitude)+.5)]
    df = df[df['longitude'].between((st.session_state.longitude)-.5, (st.session_state.longitude)+.5)]
    st.map(df)

    filtered_plot = st.toggle('Plot Land Use')
    if filtered_plot:
        with st.spinner('Creating Map'):
            with open('pickle/uk_ag.pickle', 'rb') as file:
                    
                    uk_ag = pickle.load(file)
                    st.session_state['uk_ag'] = uk_ag[['geometry', 'NUMERIC_GRADE']]
                
            point = gpd.GeoSeries([Point(st.session_state.longitude, st.session_state.latitude)], crs="EPSG:4326")

            if st.session_state.uk_ag.crs != point.crs:
                st.session_state.uk_ag = st.session_state.uk_ag.to_crs(point.crs)

            st.session_state.uk_ag['distance_to_point'] = st.session_state.uk_ag['geometry'].distance(point[0])
            threshold = .2
            uk_ag_filtered = st.session_state.uk_ag[st.session_state.uk_ag['distance_to_point'] <= threshold]
            uk_ag_filtered = uk_ag_filtered.dissolve(by='NUMERIC_GRADE')
            uk_ag_filtered = uk_ag_filtered.reset_index()

            # st.dataframe(uk_ag_filtered)

            m = uk_ag_filtered.explore('NUMERIC_GRADE',cmap='Blues',tiles="Esri.WorldImagery", attr = "© Dougal Toms")
            Marker(
                    location=[st.session_state.longitude, st.session_state.latitude],
                    tooltip="Chosen location",
                ).add_to(m)
            st_folium(m)

st.markdown('---')
feedback = st.feedback("faces")
if feedback:
    st.write('Thank you for submitting feedback')
