from ipyleaflet import Choropleth, Map, Popup
from shapely.geometry import Point, Polygon
from branca.colormap import linear
from ipywidgets import HTML
# from IPython.display import display






def create_map(selected_country, polygon_data, mapping_data):

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
        # tooltip={"content"}  
        

        ) 
    

    def mouse_over(**kwargs):
        #Close all popups
        for l in list(m.layers):
            if isinstance(l, Popup):
                m.remove_layer(l)

        if kwargs.get('type') == 'mousemove':
            coordinates = kwargs.get('coordinates')
            if coordinates:
                    
                    mouse_over = None
                    
                    for feature in polygon_data['features']:
                        if feature['geometry']['type'] == 'Polygon':
                            if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
                                mouse_over = feature['properties']['Name']
                                break
                        elif feature['geometry']['type'] == 'MultiPolygon':
                            for polygon in feature['geometry']['coordinates']:
                                if point_in_polygon(coordinates, polygon[0]):
                                    mouse_over = feature['properties']['Name']
                                    break

                    if mouse_over:
                        # html_content = HTML(value=f"<b>{mouse_over}</b><br>Hei")
                        # popup.close_popup()
                        # close_popup()
                        # output_widget = widgets.Output(layout={'border': '1px solid black'})
                        # output_control = WidgetControl(widget=output_widget, position='bottomright')
                        # m.add_control(output_control)
                        # with output_widget:
                        #     output_widget.clear_output()
                        #     print(mouse_over)

                        # m.popup = HTML('Hello World!!')
                        # m.open_popup(m)
                        # message1 = HTML()
                        # message1.value = "Try clicking the marker!"
                        popup = Popup(
                                location=coordinates,
                                # child=print(mouse_over),
                                # child=mouse_over,
                                # child=message1,
                                # child =html_content,
                                # child=widgets.HTML("Test popup content"),
                                child=HTML("<b>static</b>"),
                                # auto_close=True,
                                # close_on_escape_key=True,
                                # max_width=250
                                # close_on_escape_key=True
                                )
                        #m.open_popup(popup)
                        #popup.open_popup()
                        m.add_layer(popup)
                        # m.remove(popup)
                        # # m.close_popup(m)
                        # print(mouse_over)
                        #mouse_over_country.set(mouse_over)
                        #print(mouse_over_country)
                        # tooltip.value = f"<b>{mouse_over}</b>"
                #         tooltip.layout.visibility = 'visible'

                # # Update the position of the tooltip box based on the mouse coordinates
                #         tooltip.layout.left = f'{coordinates[0]}px'
                #         tooltip.layout.top = f'{coordinates[1]}px'
                #     else:
                # # Hide the tooltip if no country is hovered over
                #         tooltip.layout.visibility = 'hidden'

            
    # m.on_interaction(mouse_over)

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
        # print(kwargs)
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


    # tooltip = HTML()
    # tooltip.layout.margin = '0px 20px 20px 0px'
    # tooltip.layout.visibility = 'hidden'  # Initially hidden

    # # Create a container to hold the map and the tooltip
    # container = VBox([m, tooltip])
    # display(container)

    # def mouse_over(**kwargs):
    #     #Close all popups
    #     # for l in list(m.layers):
    #     #     if isinstance(l, Popup):
    #     #         m.remove_layer(l)

    #     if kwargs.get('type') == 'mousemove':
    #         coordinates = kwargs.get('coordinates')
    #         if coordinates:
                    
    #                 mouse_over = None
                    
    #                 for feature in polygon_data['features']:
    #                     if feature['geometry']['type'] == 'Polygon':
    #                         if point_in_polygon(coordinates, feature['geometry']['coordinates'][0]):
    #                             mouse_over = feature['properties']['Name']
    #                             break
    #                     elif feature['geometry']['type'] == 'MultiPolygon':
    #                         for polygon in feature['geometry']['coordinates']:
    #                             if point_in_polygon(coordinates, polygon[0]):
    #                                 mouse_over = feature['properties']['Name']
    #                                 break

    #                 if mouse_over:
    #                     # html_content = HTML(value=f"<b>{mouse_over}</b><br>Hei")
    #                     # popup.close_popup()
    #                     # close_popup()
    #                     # output_widget = widgets.Output(layout={'border': '1px solid black'})
    #                     # output_control = WidgetControl(widget=output_widget, position='bottomright')
    #                     # m.add_control(output_control)
    #                     # with output_widget:
    #                     #     output_widget.clear_output()
    #                     #     print(mouse_over)

    #                     # m.popup = HTML('Hello World!!')
    #                     # m.open_popup(m)
    #                     # message1 = HTML()
    #                     # message1.value = "Try clicking the marker!"
    #                     popup = Popup(
    #                             location=coordinates,
    #                             # child=print(mouse_over),
    #                             # child=mouse_over,
    #                             # child=message1,
    #                             # child =html_content,
    #                             # child=widgets.HTML("Test popup content"),
    #                             # child=f"Country: {mouse_over}",
    #                             # auto_close=True,
    #                             # close_on_escape_key=True,
    #                             # max_width=250
    #                             # close_on_escape_key=True
    #                             )
    #                     #m.open_popup(popup)
    #                     #popup.open_popup()
    #                     m.add_layer(popup)
    #                     # m.remove(popup)
    #                     # # m.close_popup(m)
    #                     # print(mouse_over)
    #                     #mouse_over_country.set(mouse_over)
    #                     #print(mouse_over_country)
    #                     # tooltip.value = f"<b>{mouse_over}</b>"
    #             #         tooltip.layout.visibility = 'visible'

    #             # # Update the position of the tooltip box based on the mouse coordinates
    #             #         tooltip.layout.left = f'{coordinates[0]}px'
    #             #         tooltip.layout.top = f'{coordinates[1]}px'
    #             #     else:
    #             # # Hide the tooltip if no country is hovered over
    #             #         tooltip.layout.visibility = 'hidden'

             



    # m.on_interaction(mouse_over)
    m.on_interaction(handle_click)   
    


    # layer.on_click(handle_click)


    return m