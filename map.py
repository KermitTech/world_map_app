from ipyleaflet import Choropleth, Map
from shapely.geometry import Point, Polygon
from branca.colormap import linear





def create_map(selected_country, polygon_data, mapping_data):

    m = Map(zoom=2)
    m.layout.height="600px"

    m.layers = ()

    layer = Choropleth(
        geo_data= polygon_data, # data_json,
        choro_data=mapping_data,  
        colormap=linear.Paired_03,   ## Blues_03, Paired_03, PRGn_03
        style={'fillOpacity': 1.0, "color":"black"},
        key_on="Name", 
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
                for feature in polygon_data['features']:
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