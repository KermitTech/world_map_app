import json
import geopandas as gpd
from pathlib import Path


#########################################
############ Polygon DATA ###############
data_path = Path(__file__).parent / "world-administrative-boundaries.json"
# data_path = Path(__file__).parent / "world-administrative-boundaries.kml"


geOdf = gpd.read_file(data_path)
# print(geOdf.iloc[21])

geo_json_data = geOdf.to_json()
data_json=json.loads(geo_json_data) ## this is converting a json string into a dictionary

#### We need to make a new column named "Name" to use as key_on
for d in data_json["features"]:
    d["Name"] = d["properties"]["iso3"]
    # d["Name"] = d["properties"]["Name"]
    # print(d["properties"]["iso3"])

# print(data_json)