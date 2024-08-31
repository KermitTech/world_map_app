from ipyleaflet import Choropleth, Map, GeoJSON, Popup, Marker
from shapely.geometry import Point, Polygon
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget  
from branca.colormap import linear
import json
import pandas as pd
import numpy as np
from IPython.display import display, IFrame



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



def create_map():

    layer = Choropleth(
            geo_data=geo_json_data,
            choro_data=mapping,
            colormap=linear.Blues_05,
            style={'fillOpacity': 1.0, "color":"black"},
            key_on="name")  

    m = Map(center=(50.6252978589571, 0.34580993652344), zoom=1)  
       
    m.add_layer(layer)

    selected_country = reactive.Value(None)
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
                    print(f"Clicked country: {clicked_country}")
                    selected_country.set(clicked_country)
                    print(f"Clicked country: {selected_country}")
                else:
                    #print("No country found at the clicked location.")
                    selected_country.set("No country found at the clicked location.")


    m.on_interaction(handle_click)    

    return m


def home_ui():
    return ui.page_fluid(
        ui.h2("Home Page"),
        ui.p("Welcome to the Home Page!"),
        ui.input_action_button("show_map", "Go to Map Page"),
    )


def server(input, output, session):

    page = reactive.Value("home")

    # Switch to map page
    @reactive.Effect
    @reactive.event(input.show_map)
    def show_map_page():
        page.set("map")

    # Switch to home page
    @reactive.Effect
    @reactive.event(input.show_home)
    def show_home_page():
        page.set("home")
    

    @output
    @render.ui
    def main_ui():
        if page.get() == "home":
            return home_ui()  # Call the home_ui function defined outside
        elif page.get() == "map":
            return ui.page_fluid(
                output_widget("map"),
                ui.input_action_button("show_home", "Go Back to Home Page"),
            )

    @output
    @render_widget
    def map():
        return create_map()
    
    


app_ui = ui.page_fluid(
    ui.output_ui("main_ui"),
    # output_widget("map"),
)

app = App(app_ui, server)

