import pandas as pd
from shiny import ui




def agreement_details(agreement, df):

    #df = new_df_disarm
    pa_3rd = df[df['pa_name'] == agreement]['pa_3rd'].iloc[0]
    # table = agreement_table(agreement, df)

    ui_details = ui.div(ui.page_fluid(
        ui.div(
            ui.input_action_button("show_country_details_page", "Agreement page", class_= 'country-details-btn'),
            ui.div(ui.input_action_button("Download_entire_agreement", "", class_= "Download_btn"))
        , class_="header-container"),
        ui.h2(f'Details for the agreement "{agreement}"', class_="agreement-details-title"),
        # ui.p(f"{pa_3rd }"),
        ui.output_data_frame("table")
        # ui.output_ui("table")
        ), class_="country-details-container")

    return ui_details 