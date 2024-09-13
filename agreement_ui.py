import pandas as pd
from shiny import ui



##### Data to be shown in the details country page after selecting an agreement

# def table_details_country(selected_option, df):
#     # df = new_df_disarm
#     try:
#         if selected_option is not None and 0 <= int(selected_option) < len(df):   #selected_option in new_df_disarm['pa_name'].values: #== new_df_disarm[new_df_disarm['pa_name']].index:
#             # print(1)
#             df_options = df.iloc[[selected_option]][['pa_date', 'conflict_name', 'pa_comment']]
#             df_options = df_options.rename(columns={'pa_date': 'Agreement Date', 'conflict_name': 'Conflict Name', 'pa_comment':'Comment'})
#         else:
#             df_options = pd.DataFrame(columns=['Agreement Date', 'Conflict Name', 'Comment'])
        
#         # print(df)
#     except ValueError:
#         # Handle case where selected_option is not an integer
#         df_options = pd.DataFrame(columns=['Agreement Date', 'Conflict Name', 'Comment'])
#     return df






def agreement_details_ui(country, df):

    
    
    ui_details = ui.div(ui.page_fluid(



    ) , class_="country-details-container")

    return ui_details 