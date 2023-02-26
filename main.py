import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import matplotlib.cm as cm
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-app")

location = geolocator.geocode("Addis Ababa, Ethiopia", country_codes='ET')

print(location.address)
print((location.latitude, location.longitude))
viridis = cm.get_cmap('viridis')


def get_color(score):
    return viridis(score/100)


df1 = pd.read_csv("arabica_data_cleaned.csv")
df2 = pd.read_csv("robusta_data_cleaned.csv")
df_list = [df1, df2]
coffee_df = pd.concat(df_list)
print(coffee_df.columns)
ethiopia_coffee_df = coffee_df.loc[(coffee_df['Country.of.Origin'] == "Ethiopia") & (coffee_df['Species'] == 'Arabica')]


ethiopia_map = gpd.read_file('Ethiopia.geojson')
ethiopia_map = ethiopia_map.to_crs(epsg='4326')

ethiopia_center = [9.0240, 38.7465]
ethiopia_zoom = 6
m = folium.Map(location=ethiopia_center, zoom_start=ethiopia_zoom)

marker_cluster = MarkerCluster().add_to(m)


region_colors = {'guji-hambela': 'green', 'sidamo': 'blue', 'yirgacheffe': 'red', 'oromia': 'yellow'}

default_color = 'gray'

for index, row in ethiopia_coffee_df.iterrows():
    region = row['Region']
    folium.Popup(region, parse_html=True).add_to(marker_cluster)
    if region in region_colors:
        color = get_color(row['Total.Cup.Points'])
    else:
        color = default_color
    location = geolocator.geocode(region, country_codes='ET')
    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
        folium.Marker(location=[latitude, longitude], icon=folium.Icon(color=color),
                      tooltip=region).add_to(marker_cluster)


m.save("ethiopia_coffee_map.html")
