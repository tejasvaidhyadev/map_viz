from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import numpy as np
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
import pandas as pd

def get_continent(col):
    try:
        cn_a2_code =  country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown' 
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except:
        cn_continent = 'Unknown' 
    return (cn_a2_code, cn_continent)

geolocator = Nominatim(user_agent="world-Map-NLP")

def geolocate(country):
    try:
        loc = geolocator.geocode(country)
        return (loc.latitude, loc.longitude)
    except:
        return np.nan

def display_name(country):
    try:
        return geolocator.geocode(country).raw['display_name']
    except:
        # Return missing value
        return np.nan

if __name__ == '__main__':
    df = pd.read_csv('country.csv')
    df['name_location'] = df['Name'].apply(geolocate)
    df['display_name'] = df['Name'].apply(display_name)
    df = df.dropna()

    # Create map
    # Create a world map to show distributions of users 
    world_map= folium.Map(tiles="cartodbdark_matter")
    marker_cluster = MarkerCluster().add_to(world_map)

    for i in range(len(df)):
            latnlong = df.iloc[i]['name_location']
            radius=5
            popup_text = """{}
                        """
            popup_text = popup_text.format(
                                    df.iloc[i]['display_name']
                                    )
            folium.map.Marker(location = latnlong, popup= popup_text, parse_html=True, show =True, icon=folium.features.CustomIcon('https://media.giphy.com/media/J15kf9dOEIeSk/giphy.gif',icon_size=(55,55))
    ).add_to(marker_cluster)
    #show the map
    world_map
    world_map.save("index.html")