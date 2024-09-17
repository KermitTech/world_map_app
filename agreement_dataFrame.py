import pandas as pd
from shiny import render


def agreement_table(agreement, df, country):

    # print(agreement)
 
    df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name', 'pa_comment']]
    # print(df_new)
    df_new = df_new.rename(columns={'pa_date': 'Agreement Date', 'conflict_name': 'Conflict Name', 'pa_comment':'Comment'})

    return df_new