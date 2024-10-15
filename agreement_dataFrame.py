

def agreement_table(agreement, df, country):
    
    # df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name', 'pa_comment']]
    # df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['ddr_un', 'disarm', 'demob', 'reint']]
    df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['disarm', 'demob', 'reint']]

    # df_new = df[(df['pa_name'] == agreement) & (df['ISO3'] == country)][['pa_date', 'conflict_name']]
    
    # print(df_new)
    # df_new = df_new.rename(columns={'pa_date': 'Date', 'conflict_name': 'Conflict Name', 'pa_comment':'Comment'})
    # df_new = df_new.rename(columns={'ddr_un': 'DDR', 'disarm': 'Disarmament', 'demob': 'Demobilization', 'reint':'reintegration'})
    df_new = df_new.rename(columns={'disarm': 'Disarmament', 'demob': 'Demobilization', 'reint':'reintegration'})


    return df_new
