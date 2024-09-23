import json
import geopandas as gpd


#########################################
############ Polygon DATA ###############
geOdf = gpd.read_file('data/world-administrative-boundaries.kml')
# print(geOdf.head())

geo_json_data = geOdf.to_json()
data_json=json.loads(geo_json_data) ## this is converting a json string into a dictionary

#### We need to make a new column named "Name" to use as key_on
for d in data_json["features"]:
    d["Name"] = d["properties"]["Name"]

# print(data_json)