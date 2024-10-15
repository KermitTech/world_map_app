from ipyleaflet import Choropleth, Map
from shapely.geometry import Point, Polygon
from branca.colormap import linear
import country_converter as coco
# import threading
import time

converter = coco.CountryConverter()
last_check_time = 0
# hover_timer = None

def create_map(selected_country, polygon_data, mapping_data, country_text):

    m = Map(center=(51.505, -0.09), zoom = 2, min_zoom=2)
    m.layout.height="70vh"
    m.layout.width="100%"


    m.layers = ()

    layer = Choropleth(
        geo_data= polygon_data, # data_json,
        choro_data=mapping_data,  
        colormap=linear.Paired_03,   ## Blues_03, Paired_03, PRGn_03
        # style={'fillOpacity': 1.0, "color":"black"},
        key_on="Name", 
        hover_style={'fillColor': 'red' , 'fillOpacity': 0.2},
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
            if coordinates:
                # Identify the country by checking the GeoJSON data
                clicked_country = None
                found = False
                for feature in polygon_data['features']:
                    # clicked_country = 'NOR'; break
                    # print(feature)
                    if feature['geometry']['type'] == 'Polygon':
                        if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
                            clicked_country = feature['Name']
                            break
                    elif feature['geometry']['type'] == 'GeometryCollection':
                        for polygon in feature['geometry']['geometries']:
                            if point_in_polygon(coordinates, polygon['coordinates'][0]):
                                    clicked_country = feature['Name']
                                    found = True
                                    break
                        if found: break

                if clicked_country:
                    selected_country.set(clicked_country)
    
    m.on_interaction(handle_click) 

    

    # def handle_click(**kwargs):
    #     # print(kwargs)
    #     if kwargs.get('type') == 'click':
    #         coordinates = kwargs.get('coordinates')
    #         # print(coordinates)
    #         if coordinates:
    #             # Identify the country by checking the GeoJSON data
    #             clicked_country = None
    #             # for feature in geo_json_data['features']:
    #             for feature in polygon_data['features']:
    #                 if feature['geometry']['type'] == 'Polygon':
    #                     print(feature)
    #                     if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
    #                         clicked_country = feature['properties']['Name']
    #                         break
    #                 elif feature['geometry']['type'] == 'MultiPolygon':
    #                     for polygon in feature['geometry']['coordinates']:
    #                         if point_in_polygon(coordinates, polygon[0]):
    #                             clicked_country = feature['properties']['Name']
    #                             break

    #             if clicked_country:
    #                 selected_country.set(clicked_country)
    #                 # print(selected_country)






      
    

    #########  update the tooltip #######
    def update_tooltip(hover_country, country_text):
        if hover_country:
            country_name = hover_country 
            # country_name = threading.active_count()
        else:
            # country_name = "Hover over a country"
            country_name = ""  # Default text
    
    # Update the output for the tooltip
        # print(country_name)
        country_text.set(country_name)


    ##### Define the tooltip text ##### 
    def mouse_over(**kwargs):
        ##Throttle
        global last_check_time
        current_time = time.time()
        if current_time - last_check_time > 0.2:
            last_check_time = current_time
        
        # ##Debounce
        # global hover_timer
        # # Cancel the previous timer if it exists
        # if hover_timer is not None:
        #     print('Hei')
        #     hover_timer.cancel()

        # def perform_hover_check(): 
            coordinates = kwargs.get('coordinates')
            if coordinates:                    
                    # mouse_over = None
                    hover_country = None
                    found = False
                    for feature in polygon_data['features']:
                        # hover_country = 'Norway'; break
                        if feature['geometry']['type'] == 'Polygon':
                            if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
                                # clicked_country = feature['Name']
                                # hover_country = feature['Name']
                                hover_country = converter.convert(names=feature['Name'], src="iso3", to="name_short")
                                break
                        elif feature['geometry']['type'] == 'GeometryCollection':
                            for polygon in feature['geometry']['geometries']:
                                if point_in_polygon(coordinates, polygon['coordinates'][0]):
                                        # clicked_country = feature['Name']
                                        # hover_country = feature['Name']
                                        hover_country = converter.convert(names=feature['Name'], src="iso3", to="name_short")

                                        found = True
                                        break
                            if found: break
                    
                    if hover_country != country_text.get():
                        # print(hover_country)
                        update_tooltip(hover_country, country_text)

        # Start a new timer to delay execution by 0.2 seconds
        # hover_timer = threading.Timer(0.2, perform_hover_check)
        # hover_timer.start()
    

    # m.on_interaction(mouse_over)


    return m