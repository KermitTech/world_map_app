from ipyleaflet import Choropleth, Map, GeoJSON, Popup, Marker
from shapely.geometry import Point, Polygon
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget, render_plotly  
from branca.colormap import linear
import json
import pandas as pd
import numpy as np
from IPython.display import display, IFrame
import plotly.express as px
# import matplotlib.pyplot as plt



happiness_report = pd.read_csv("world_happiness_2019.csv")


with open('custom_geo.json', 'r') as f:
    geo_json_data = json.load(f)
    for d in geo_json_data["features"]:
        d["name"] = d["properties"]["name_sort"]



mapping  = dict(zip(happiness_report["Country or region"].str.strip(), happiness_report["Score"]))

proper_name_mapping = {
    "Russian Federation":"Russia",
    "Czech Republic":"Czechia",
    "North Macedonia":"Macedonia",
    "Central African Republic":"Central African Rep.",
    "Bosnia and Herzegovina":"Bosnia and Herz.",
    "Slovak Republic":"Slovakia",
    "Iran, Islamic Rep.":"Iran",
    "Somaliland":"Somalia",
    "Dominican Republic":"Dominican Rep.",
    "Venezuela, RB":"Venezuela",
    "Lao PDR":"Laos",
    "Yemen, Rep.":"Yemen",
    "South Sudan":"S. Sudan",
    "Papua New Guinea":"Guinea",
    "Congo (Brazzaville)":"Congo",
    "Congo (Kinshasa)":"Dem. Rep. Congo",
    "Cyprus Northern":"N. Cyprus",
    "Kyrgyz Republic":"Kyrgyzstan",
    "Korea, Dem. Rep.":"South Korea",
    "Palestinian Territories":"Palestinian",
    "Syrian Arab Republic":"Syria",
    "Egypt, Arab Rep.":"Egypt",
    "Gambia, The":"Gambia"

}

for d in geo_json_data["features"]:
    if d["name"] not in mapping:
        if d["name"] in proper_name_mapping.keys():
            mapping[d["name"]] = mapping[proper_name_mapping[d["name"]]]
        else:
            mapping[d["name"]] = 0

# print(mapping["Norway"])

def create_map(selected_country):

    layer = Choropleth(
            geo_data=geo_json_data,
            choro_data=mapping,
            colormap=linear.Blues_05,
            style={'fillOpacity': 1.0, "color":"black"},
            key_on="name")  

    m = Map(center=(50.6252978589571, 0.34580993652344), zoom=1)  
       
    m.add_layer(layer)

    # Utility function to check if a point is inside a polygon
    def point_in_polygon(point, polygon):
        point = Point(point[1], point[0])  # Longitude, Latitude
        poly = Polygon(polygon)
        return poly.contains(point)

    def handle_click(**kwargs):
        if kwargs.get('type') == 'click':
            coordinates = kwargs.get('coordinates')
            if coordinates:
                # Identify the country by checking the GeoJSON data
                clicked_country = None
                for feature in geo_json_data['features']:
                    if feature['geometry']['type'] == 'Polygon':
                        if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
                            clicked_country = feature['properties']['name']
                            break
                    elif feature['geometry']['type'] == 'MultiPolygon':
                        for polygon in feature['geometry']['coordinates']:
                            if point_in_polygon(coordinates, polygon[0]):
                                clicked_country = feature['properties']['name']
                                break

                if clicked_country:
                    selected_country.set(clicked_country)

    m.on_interaction(handle_click)    
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
    return fig


def country_details(country):
    return ui.page_fluid(
        ui.input_action_button("show_map_page", "Go Back to Map Page"),
        ui.h2(f"Welcome to the country details Page for {country}!"),
        ui.p(f"Happiness score for {country} = {mapping[country]}"),
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
    
    @output
    @render.ui
    def map_ui():
        if page.get() == "map":
            return ui.page_fluid(
                output_widget("map")
            )



app_ui = ui.page_fluid(
    ui.navset_pill(  
        ui.nav_panel("Data", 
                      ui.output_ui("map_ui"),
                      ui.output_ui("country_details_ui"),),
        ui.nav_panel("Download"),
        ui.nav_panel("About",
                      ui.h2("About This Application"),
                      ui.p("This application is designed to..."),
                      ),
        id="tab",
    ),  

    # output_widget("map"),
)

app = App(app_ui, server)

