from ipyleaflet import Choropleth, Map, LegendControl, GeoJSON, GeoData, Popup, Marker, basemaps, TileLayer, LayersControl, Rectangle
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
from legend import create_legend
from map import create_map
from country_details_ui import country_details
# from agreement_ui import table_details_country

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

##### duplicate the columns with gwno of the type ... , ....
new_df_disarm['gwno'] = new_df_disarm['gwno'].str.split(', ')
# print(new_df_disarm[new_df_disarm['ID'] == 141])

new_df_disarm = new_df_disarm.explode('gwno').reset_index(drop=True)
# print(new_df_disarm[new_df_disarm['ID'] == 141])

new_df_disarm['ID'] = new_df_disarm.groupby('ID').cumcount() + 1 + (new_df_disarm['ID'] * 10)
# print(new_df_disarm[new_df_disarm['ID'] == 1412])

####### adding ISO3 and short country name columns ######### 
converter = coco.CountryConverter()

gwcodes = new_df_disarm['gwno']
# # print(gwcodes)

ISO3column = converter.convert(names=gwcodes, src="GWcode", to="ISO3")
shortCountryName = converter.convert(names=gwcodes, src="GWcode", to="name_short")
# #  print(ISO3column)
idx = 5 

new_df_disarm.insert(loc=idx, column='ISO3', value = ISO3column)
new_df_disarm.insert(loc=idx+1, column='country_name', value = shortCountryName)
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

##########################################
### Making sure that the iso3 values in the geo data is the same as the iso3 in 
### the Excel file

for d in data_json["features"]:
    if d["Name"] not in mapping:
            mapping[d["Name"]] = 0



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
    

    ##########################################
    ### Agreement details ui

    # @output
    # @render.data_frame 
    # def table_agreement():
    #     selected_option = input.var()
    #     df = new_df_disarm
    #     df_details = table_details_country(selected_option, df)
    #     # print(f"Selected Option: {selected_option}")
    #     return render.DataTable(df_details)
    
    # @output
    # @render.ui
    # def agreement_details_ui():



    ##########################################
    ### Country details ui

    @output
    @render.ui
    def country_details_ui():
        if page.get() == "country_details":
            country = selected_country.get()
            df = new_df_disarm
            return country_details(country, df)
            # print(country)
            # if country:
            #     return country_details(country)
            #     # ui.input_action_button("show_map_page", "Go Back to Map Page"),
            # else:
            #     return ui.page_fluid(
            #         ui.h2("No country selected"),
            #         ui.input_action_button("show_map_page", "Go Back to Map Page"),
            #     )
       
    ##########################################
    ### Map function 

    @output
    @render_widget
    def map():
        polygon_data = data_json
        mapping_data = mapping
        return create_map(selected_country, polygon_data, mapping_data)
        # return create_map()

    ##########################################
    ### Map ui

    @output
    @render.ui
    def map_ui():
        if page.get() == "map":
            return ui.page_fluid(
                ui.div(output_widget("map"), 
                ui.div(ui.HTML(create_legend(mapping)), class_="legend"),
                class_="leaflet-container"), 
            )
        



app_ui = ui.page_fluid(
    ui.head_content(ui.include_css("styles.css")), 
    ui.div(
        ui.navset_pill(  
            ui.nav_panel("Data", 
                ui.output_ui("map_ui"),     
                ui.output_ui("country_details_ui")     
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