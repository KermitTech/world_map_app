from shiny import ui, render, reactive
from legend import create_legend
from map import create_map
from country_details_ui import country_details
from agreement_details_ui import agreement_details
from agreement_dataFrame import agreement_table
from data.data_cleaning import new_df_disarm 
from data.http_to_hhtps import replace_http
from data.mapping import mapping
from data.polygon_data import data_json
from shinywidgets import output_widget, render_widget 



########################################
##### Server function 

def server(input, output, session):

    page = reactive.Value("map")
    selected_country = reactive.Value(None)
    selected_agreement = reactive.Value(None)

    # Switch to map page
    @reactive.Effect
    @reactive.event(input.show_map_page)
    def show_map_page():
        page.set("map")

    # Switch to country_details page from map page
    @reactive.Effect
    def update_to_country_details_page():
        if selected_country.get():
            page.set("country_details")


    # switch to agreement details page
    @reactive.Effect
    def update_to_agreemnet_details_page():
        country = selected_country.get()

        if country: 
            pa_name = new_df_disarm[new_df_disarm['ISO3']==country]['pa_name']
            for d in range(len(pa_name)):
                button_id = f"{d}"
                if input[button_id]():  # Detects if this button was clicked
                    selected_agreement.set(pa_name.iloc[d])
                    page.set("agreement_details")

    # switch to country details page from the agreement page
    @reactive.Effect
    @reactive.event(input.show_country_details_page)
    def show_country_details_from_agreement_page():
        page.set("country_details")

    
    # Go to page to download the entire text for the peace agreement
    @reactive.Effect
    @reactive.event(input.Download_entire_agreement)
    async def test_message():
        # print("Download button clicked!")
        agreement = selected_agreement.get()
        country = selected_country.get()
        # print(agreement)
        download = new_df_disarm[(new_df_disarm['ISO3']==country) & (new_df_disarm['pa_name']==agreement)]['linktofulltextagreement']
        download = download.apply(replace_http)
        # print(download)
        download_link = download.iloc[0]
        await session.send_custom_message('test_message', f"{download_link}")


    ##########################################
    ### Agreement details ui

    @output
    # @render.data_frame
    @render.ui
    def agreement_details_ui():
        df = new_df_disarm
        if page.get() == "agreement_details":
            agreement = selected_agreement.get()
            return agreement_details(agreement, df)

    #########################################
    ### Agreement table

    @output
    @render.data_frame
    def table():
        agreement = selected_agreement.get()
        df = new_df_disarm
        country = selected_country.get()
        return agreement_table(agreement, df, country)
    
    ##########################################
    ### Country details ui

    @output
    @render.ui
    def country_details_ui():
        if page.get() == "country_details":
            country = selected_country.get()
            df = new_df_disarm
            pa_count = mapping[country]
            return country_details(country, df, pa_count)

       
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