import country_converter as coco
from shiny import ui

converter = coco.CountryConverter()

 


def country_details(country, df):
    # df = new_df_disarm

    pa_name = df[df['ISO3']==country]['pa_name']
    short_country_name = converter.convert(names=country, src="ISO3", to="name_short")
    
    
    ui_details = ui.div(ui.page_fluid(
        ui.input_action_button("show_map_page", "Map Page", class_= 'country-details-btn'),
        # ui.h2(f"Welcome to the country details Page for {short_country_name}!", class_="country-details-title"), 
        ui.h2(f"{short_country_name}", class_="country-details-title"), 
        *[ui.div(ui.input_action_button(f"{d}", pa_name.iloc[d], class_="agreement_btn")) for d in range(len(pa_name))],
       
        # ui.layout_columns(
        #     *[ui.column(4,ui.div(ui.input_action_button(f"{d}", pa_name.iloc[d]), class_="agreement_btn")) for d in range(len(pa_name))],
        #     # ui.column(8, ui.output_data_frame("table_agreement")), 
        #     )


    ) , class_="country-details-container")

    return ui_details 


