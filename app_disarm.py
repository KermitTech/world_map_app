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

#########################################
############ Polygon DATA ###############
geOdf = gpd.read_file('data/world-administrative-boundaries.kml')
print(geOdf.head())

geo_json_data = geOdf.to_json()
data_json=json.loads(geo_json_data)
# for feature in data_json['features']:
#     name = feature['properties']['Name'] 
#     polygon = feature['geometry']['type']  # Access the 'Name' key within 'properties'



def create_map(selected_country):

    m = Map(zoom=1)
    m.layout.height="600px"

    m.layers = ()

    solid_background = Rectangle(
        bounds=[[-60, -300], [100, 185]],  # Covers the entire map
        color="white",
        fill_color="white",
        fill_opacity=1.0,
    )

    # m.add_layer(solid_background)

    layer = GeoJSON(
            data=json.loads(geo_json_data),
            colormap=linear.Blues_05,
            style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
            # style={'fillOpacity': 1.0, "color":"white", 'fillColor': 'green'},
            hover_style={'fillColor': 'red' , 'fillOpacity': 0.2},
            key_on="name") 
    
    m.add_layer(layer)

       # Utility function to check if a point is inside a polygon
    def point_in_polygon(point, polygon):
        point = Point(point[1], point[0])  # Longitude, Latitude
        poly = Polygon(polygon)
        return poly.contains(point)

    def handle_click(**kwargs):
        if kwargs.get('type') == 'click':
            coordinates = kwargs.get('coordinates')
            print(coordinates)
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
                    print(selected_country)

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
        


app_ui = ui.page_fluid(
    ui.head_content(ui.include_css("styles.css")), 
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
       )   
)



app = App(app_ui, server)