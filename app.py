import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import matplotlib.pyplot as plt

st.header('UK Farmland Classification')
st.subheader('Grade 4+')

# eng_ag = gpd.read_file('shapefiles/AgriculturalLandClassificationProvisionalEngland-SHP/Agricultural_Land_Classification_Provisional_England.shp')
scot_ag = gpd.read_file('/Users/dougaltoms/Downloads/Hutton_LCA250K_OpenData/LCA_250K.shp')

#==============================
# Check unique Land Use Codes
# eng_ag['alc_grade'].unique()
scot_ag['LCCODE'].unique().astype(int)

#==============================
# Extract digits from codes to make a uniform grading between England and Scotland
# eng_ag['NUMERIC_GRADE'] = eng_ag['alc_grade'].str.extract('(\d+)', expand=False).astype(float)
scot_ag['NUMERIC_GRADE'] = scot_ag['LCCODE'].astype(str).str.extract('(\d+)', expand=False).astype(float)

#==============================
# Filter each DF to remove huge ranges/NaNs <-- need to read up on what these codes actually mean
# eng_ag = eng_ag[eng_ag['NUMERIC_GRADE'] > 0]
scot_ag = scot_ag[scot_ag['NUMERIC_GRADE'] < 9]

#==============================
# Convert to same coords system, concat and plot based on new Land Use codes
scot_ag = scot_ag.to_crs('EPSG:4326')
# eng_ag = eng_ag.to_crs('EPSG:4326')
# eng_scot_ag = gpd.pd.concat([eng_ag, scot_ag])
# plot = eng_scot_ag.plot(figsize=(8,10), column='NUMERIC_GRADE', missing_kwds = {"color": "red"})

# eng_ag.plot(column='alc_grade', figsize=(8, 10), legend=True)

plot_df = scot_ag[['geometry','NUMERIC_GRADE']]
plot_df = plot_df[plot_df['NUMERIC_GRADE']>1]
m = plot_df.explore(column='NUMERIC_GRADE', color='red', tiles='CartoDB positron')

st_folium(m, zoom=6)