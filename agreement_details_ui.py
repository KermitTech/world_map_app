import pandas as pd
from shiny import ui



def agreement_details(agreement):

    ui_details = ui.page_fluid(
        ui.input_action_button("show_country_details_page", "Agreement page", class_= 'country-details-btn'),
        ui.h2(f"agreement details page for {agreement}"))

    return ui_details 