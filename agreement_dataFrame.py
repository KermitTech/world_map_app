

def agreement_table(agreement, df, country):
    
    df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name', 'pa_comment']]
    # df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name']]
    
    # print(df_new)
    df_new = df_new.rename(columns={'pa_date': 'Date', 'conflict_name': 'Conflict Name', 'pa_comment':'Comment'})


    return df_new
