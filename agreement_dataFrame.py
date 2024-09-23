import pandas as pd
from shiny import render, ui


def agreement_table(agreement, df, country):

    # print(agreement)
    
    df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name', 'pa_comment']]
    # df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name']]
    
    # print(df_new)
    df_new = df_new.rename(columns={'pa_date': 'Date', 'conflict_name': 'Conflict Name', 'pa_comment':'Comment'})
    # df_new = df_new.rename(columns={'pa_date': 'Date', 'conflict_name': 'Conflict Name'})

    # df_download = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['linktofulltextagreement']]
    
    # df_new['Download'] = df_download['linktofulltextagreement'].apply(
    #     lambda x: str(ui.div(
    #         ui.a("Download", href=x, target="_blank", class_="Download_btn")
    #     ))
    # )

    return df_new
    # return df_new.to_html(escape=False, index=False)