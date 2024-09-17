import country_converter as coco
from shiny import ui

converter = coco.CountryConverter()

 


def country_details(country, df):
    # df = new_df_disarm

    pa_df = df[df['ISO3']==country][['pa_name', 'year']]
    pa_df = pa_df.sort_values(by=['year'], ascending=False)
    # print(pa_df)
    # pa_year = df[df['ISO3']==country][['pa_name', 'year']]
    # print(pa_year)
    short_country_name = converter.convert(names=country, src="ISO3", to="name_short")
    
    ui_details = ui.div(ui.page_fluid(
        ui.input_action_button("show_map_page", "Map Page", class_= 'country-details-btn'),
        ui.h2(f"{short_country_name}", class_="country-details-title"), 
        ui.div(
            # *[ui.div(ui.input_action_button(f"{d}", pa_name.iloc[d], class_="agreement_btn")) for d in range(len(pa_name))],
            *[ui.div(ui.input_action_button(f"{d}", f"{pa_df['year'].iloc[d]} : {pa_df['pa_name'].iloc[d]}", class_="agreement_btn")) for d in range(len(pa_df['pa_name']))],
            class_="agreement-container"
        )
    ) , class_="country-details-container")

    return ui_details 


