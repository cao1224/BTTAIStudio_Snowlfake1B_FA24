import streamlit as st
import folium
import pandas as pd
import os
from streamlit_folium import st_folium
import json

county = os.path.join('USA_Counties_(Generalized).geojson')
with open(county) as f:
    county_geojson = json.load(f)

# Filter GeoJSON to include only features for Florida
florida_geojson = {
    "type": "FeatureCollection",
    "features": [
        feature for feature in county_geojson["features"]
        if feature.get("properties") and feature["properties"].get("STATE_NAME") == "Florida"
    ]
}

data = os.path.join('Florida_county.csv')
svi_data = pd.read_csv(data)
svi_data['COUNTY'] = svi_data['COUNTY'].str.replace(r'\s*County', '', regex=True)



# Customize the sidebar
st.set_page_config(layout="wide")
# Customize page title
st.title("Social Vulnerability Index: Map of Florida")
st.markdown("Data Source: CDC/ATSDR & FGIO")
st.markdown("Social vulnerablity refers to the demographic and socioeconomic factors that contribute to communities being more adversely affected by public heath emergencies and other external hazards and stressors that cuase disease and injury.")

st.write("")  # Adds a blank line

markdown = ("""
GitHub Repository: <https://github.com/EvelynXu12321/SNOWFLAKE>
""")

st.sidebar.title("Filters")
st.sidebar.info(markdown)
st.sidebar.title("SVI Type")

# Define display names and map them to actual column names in your dataset
column_map = {
    'Socioeconomic Status': 'SPL_THEME1',
    'Household Characteristics': 'SPL_THEME2',
    'Racial & Ethnic Minority Status': 'SPL_THEME3',
    'Housing Type & Transportation': 'SPL_THEME4',
    'Overall': 'SPL_THEMES'
}

# Define color mappings for each choropleth type
color_map = {
    'Socioeconomic Status': 'YlOrRd',    # Color palette for red shades
    'Household Characteristics': 'BuGn',    # Color palette for green shades
    'Racial & Ethnic Minority Status': 'PuBu',   # Color palette for blue shades
    'Housing Type & Transportation': 'OrRd',    # Color palette for orange shades
    'Overall': 'Purples',    # Color palette for purple shades
}

# Create a dropdown in the sidebar to select a single layer to display
selected_option = st.sidebar.selectbox(
    "Select a Category:",
    list(column_map.keys())
).strip()

st.sidebar.write("")  # Adds a blank line
st.sidebar.write("")  # Add more blank lines if needed

# picture
logo = "https://imgur.com/Nc2lPGT.png"
st.sidebar.image(logo)


# Map the selected display name to the actual column name and color
column_name = column_map[selected_option]
color = color_map[selected_option]

# Create the map with Folium
m = folium.Map(location=[27.5, -82], zoom_start=6)

# Create the choropleth layer
choropleth = folium.Choropleth(
    geo_data=florida_geojson,
    name=selected_option,
    data=svi_data,
    columns=['COUNTY', column_name],
    key_on='feature.properties.NAME',
    fill_color=color,
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f'{selected_option} Rate'
).add_to(m)


for feature in florida_geojson['features']:
    # Access properties and geometry directly
    county_name = feature['properties']['NAME']
    population = feature['properties']['POPULATION']

    spl_value = svi_data.loc[svi_data['COUNTY'] == county_name, column_name].values
    spl_value_text = f"{selected_option}: {spl_value[0]}" if len(spl_value) > 0 else f"{selected_option}: N/A"

    folium.GeoJson(
        feature['geometry'],
        line_opacity=0,
        tooltip=folium.Tooltip(f"County: {county_name}<br>Population: {population}<br>{spl_value_text}"),
        style_function=lambda x: {'color': 'transparent'}  # Set border color to transparent this is my code now, update ur code 
    ).add_to(m)


# # Add Layer Control
# folium.LayerControl().add_to(m)

# Display the map in Streamlit
st.write(f"Choropleth Map for {selected_option}")
st_folium(m, width=700, height=500)

#st.caption("SVI provides specific socially and spatially relevant information to help public health officials and local planners better prepare communities to respond to emergency events such as severe weather, floods, disease outbreaks, or chemical exposure.")


##TODO
#state comparoison and country comparison