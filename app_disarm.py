from ipyleaflet import Choropleth, Map, GeoJSON, GeoData, Popup, Marker, basemaps, TileLayer, LayersControl, Rectangle
from shapely.geometry import Point, Polygon
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget, render_plotly 
import geopandas as gpd
from branca.colormap import linear
import json
import plotly.express as px
import pandas as pd
from htmltools import head_content
import country_converter as coco


#########################################
########### Excel DATA ##################

df_disarm = pd.read_excel("data/disarm_2022-03-11.xlsx")
# print(df_disarm.head())

## Using the first row values of df dataframe as the column names of the new_df.
headers = df_disarm.iloc[0]
new_df_disarm  = pd.DataFrame(df_disarm.values[1:], columns=headers)
new_df_disarm = new_df_disarm.dropna(subset=['ID'])
# print(new_df_disarm)
# print(new_df_disarm.columns)
# print(new_df_disarm[new_df_disarm['gwno'] =='700'])

##### doblicate the columns with gwno of the type ... , ....
new_df_disarm['gwno'] = new_df_disarm['gwno'].str.split(', ')
# print(new_df_disarm[new_df_disarm['ID'] == 141])

new_df_disarm = new_df_disarm.explode('gwno').reset_index(drop=True)
# print(new_df_disarm[new_df_disarm['ID'] == 141])

new_df_disarm['ID'] = new_df_disarm.groupby('ID').cumcount() + 1 + (new_df_disarm['ID'] * 10)
# print(new_df_disarm[new_df_disarm['ID'] == 1412])

####### adding ISO3 and short country name columns ######### 
converter = coco.CountryConverter()

# gwcodes = new_df_disarm['gwno']
# # print(gwcodes)

# ISO3column = converter.convert(names=gwcodes, src="GWcode", to="ISO3")
# shortCountryName = converter.convert(names=gwcodes, src="GWcode", to="name_short")
# #  print(ISO3column)
# idx = 5 

# new_df_disarm.insert(loc=idx, column='ISO3', value = ISO3column)
# new_df_disarm.insert(loc=idx+1, column='country_name', value = shortCountryName)
# print(new_df_disarm['country_name'])

########## Some aggregations on the data
### number of peace agreements per country

no_distinct_gwno = new_df_disarm['gwno'].nunique()
# print(no_distinct_gwno)

counts_pa_perCountry = new_df_disarm.groupby('gwno')['pa_name'].count()

### converting counts_pa_perCountry (it is a series) into a dataframe
counts_pa_perCountry_df = counts_pa_perCountry.reset_index()

### change the pa_column name
counts_pa_perCountry_df = counts_pa_perCountry_df.rename(columns={"pa_name":"pa_counts"}) 

#### convert the gwno code to iso3 and short country name
iso3 = converter.convert(names=counts_pa_perCountry_df['gwno'], src="GWcode", to="ISO3")
short_country_name = converter.convert(names=counts_pa_perCountry_df['gwno'], src="GWcode", to="name_short")

#### insert the new columns into the dataframe counts_pa_perCountry_df
counts_pa_perCountry_df.insert(loc=1, column='ISO3', value = iso3)
counts_pa_perCountry_df.insert(loc=2, column='country_name', value = short_country_name)

#### removed south Yemen
counts_pa_perCountry_df = counts_pa_perCountry_df.drop(counts_pa_perCountry_df[counts_pa_perCountry_df['gwno'] == '678'].index)
# print(counts_pa_perCountry_df)

mapping  = dict(zip(counts_pa_perCountry_df['ISO3'].str.strip(), counts_pa_perCountry_df['pa_counts']))
# print(mapping)


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

# res = list(data_json.keys())[1]
# print(res) # res = type or features 

# for feature in data_json['features']:
#     name = feature['properties']['Name'] 
#     polygon = feature['geometry']['type']  # Access the 'Name' key within 'properties'

##########################################
### Making sure that the iso3 values in the geo data is the same as the iso3 in 
### the Excel file

# for d in data_json["features"]:
#     if d["properties"]["Name"] not in mapping:
#             mapping[d["properties"]["Name"]] = 0

for d in data_json["features"]:
    if d["Name"] not in mapping:
            mapping[d["Name"]] = 0


# for d in data_json["features"]:
#     print(d["properties"])
    # if d["properties"]["Name"] not in mapping:

# print(data_json["features"][0]["properties"]["Name"])  # Should print 'UGA'
# print(mapping) 
        
#         if d["name"] in proper_name_mapping.keys():
#             mapping[d["name"]] = mapping[proper_name_mapping[d["name"]]]
#         else:
#             mapping[d["name"]] = 0

##########################################

def create_map(selected_country):

    m = Map(zoom=2)
    m.layout.height="600px"

    m.layers = ()

    # solid_background = Rectangle(
    #     bounds=[[-60, -300], [100, 185]],  # Covers the entire map
    #     color="white",
    #     fill_color="white",
    #     fill_opacity=1.0,
    # )

    # m.add_layer(solid_background)

    layer = Choropleth(
        # geo_data=json.loads(geo_json_data),
        geo_data=data_json,
        choro_data=mapping,
        #columns=["Name", "value"],  
        colormap=linear.Blues_05,
        # style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
        style={'fillOpacity': 1.0, "color":"black"},
        key_on="Name", 
        # key_on="features.properties.Name"
        hover_style={'fillColor': 'red' , 'fillOpacity': 0.2}
        ) 
    
    m.add_layer(layer)

    # layer = GeoJSON(
    #         data=json.loads(geo_json_data),
    #         colormap=linear.Blues_05,
    #         style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
    #         # style={'fillOpacity': 1.0, "color":"white", 'fillColor': 'green'},
    #         hover_style={'fillColor': 'red' , 'fillOpacity': 0.2},
    #         # key_on="name"
    #         ) 
    
    # m.add_layer(layer)

    # Utility function to check if a point is inside a polygon
    def point_in_polygon(point, polygon):
        point = Point(point[1], point[0])  # Longitude, Latitude
        poly = Polygon(polygon)
        return poly.contains(point)

    def handle_click(**kwargs):
        if kwargs.get('type') == 'click':
            coordinates = kwargs.get('coordinates')
            # print(coordinates)
            if coordinates:
                # Identify the country by checking the GeoJSON data
                clicked_country = None
                # for feature in geo_json_data['features']:
                for feature in data_json['features']:
                    if feature['geometry']['type'] == 'Polygon':
                        if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
                            clicked_country = feature['properties']['Name']
                            break
                    elif feature['geometry']['type'] == 'MultiPolygon':
                        for polygon in feature['geometry']['coordinates']:
                            if point_in_polygon(coordinates, polygon[0]):
                                clicked_country = feature['properties']['Name']
                                break

                if clicked_country:
                    selected_country.set(clicked_country)
                    # print(selected_country)

    m.on_interaction(handle_click)   


    layer.on_click(handle_click)


    return m


######################################
### some dumy random data to test ###
dummy_data = pd.DataFrame({
    "variable_1": [1, 2, 2, 3, 4],
    "variable_2": [5, 6, 7, 8, 9]
})


def histogram_plot(selected_var):
    fig = px.histogram(dummy_data, x=selected_var)
    #fig.show()
    fig.update_layout(
            title={
                # 'text': "Count of The Incident",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            font=dict(
                size=18,
                color="RebeccaPurple"
            )
    )
    return fig


def country_details(country):
    return ui.page_fluid(
        ui.input_action_button("show_map_page", "Go Back to Map Page"),
        ui.h2(f"Welcome to the country details Page for {country}!"),
        ui.p(f"Happiness score for {country} "), # = {mapping[country]}
        ui.input_select("var", "Select variable", choices=["variable_1", "variable_2"]),
        # output_widget("histogram"),  
        ui.layout_columns(
           ui.column(6, output_widget("histogram")),
            ui.column(6, ui.h2(f"Extra detail for {country}!")) 
        ),
    )




def server(input, output, session):

    page = reactive.Value("map")
    selected_country = reactive.Value(None)

    # Switch to map page
    @reactive.Effect
    @reactive.event(input.show_map_page)
    def show_map_page():
        page.set("map")

    # Switch to country_details page
    @reactive.Effect
    def update_to_country_details_page():
        if selected_country.get():
            page.set("country_details")
    
 
    @output
    @render_plotly
    def histogram(): 
        selected_var = input.var() #dummy_data["variable_1"]    
        return histogram_plot(selected_var)
        # return histogram_plot()

    @output
    @render.ui
    def country_details_ui():
        if page.get() == "country_details":
            country = selected_country.get()
            # print(country)
            if country:
                return country_details(country)
                # ui.input_action_button("show_map_page", "Go Back to Map Page"),
            else:
                return ui.page_fluid(
                    ui.h2("No country selected"),
                    ui.input_action_button("show_map_page", "Go Back to Map Page"),
                )
       
    
    @output
    @render_widget
    def map():
        return create_map(selected_country)
        # return create_map()
    
    @output
    @render.ui
    def map_ui():
        if page.get() == "map":
            return ui.page_fluid(
                output_widget("map")
            )
        


# app_ui = ui.page_fluid(
#     ui.head_content(ui.include_css("styles.css")), 
#     ui.navset_pill(  
#         ui.nav_panel("Data", 
            
#             ui.div(ui.output_ui("map_ui"), class_="leaflet-container"),     
#             ui.output_ui("country_details_ui"), 
#         ),          
#             ui.nav_panel("Download"),
#             ui.nav_panel("About",
#                         ui.h2("About This Application"),
#                         ui.p("This application is designed to..."),
#                         ),
#         id="tab",
#         class_="custom-nav-tabs"
#        )   
# )

app_ui = ui.page_fluid(
    ui.head_content(ui.include_css("styles.css")), 
    ui.div(
        ui.navset_pill(  
            ui.nav_panel("Data", 
                
                ui.div(ui.output_ui("map_ui"), class_="leaflet-container"),     
                ui.output_ui("country_details_ui"), 
            ),          
                ui.nav_panel("Download"),
                ui.nav_panel("About",
                            ui.h2("About This Application"),
                            ui.p("This application is designed to..."),
                            ),
            id="tab",
        ),
        class_="custom-nav-tabs" 
    )  
)

app = App(app_ui, server)