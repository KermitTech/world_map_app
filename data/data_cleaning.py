import pandas as pd
import country_converter as coco


#########################################
########### Excel DATA ##################

df_disarm = pd.read_excel("data/disarm_2022-03-11.xlsx")
# print(df_disarm.head())

## Using the first row values of df dataframe as the column names of the new_df.
headers = df_disarm.iloc[0]
new_df_disarm  = pd.DataFrame(df_disarm.values[1:], columns=headers)
new_df_disarm = new_df_disarm.dropna(subset=['ID'])
# print(new_df_disarm)
# print(new_df_disarm.columns)
# print(new_df_disarm[new_df_disarm['gwno'] =='700'])

##### duplicate the columns with gwno of the type ... , ....
new_df_disarm['gwno'] = new_df_disarm['gwno'].str.split(', ')
# print(new_df_disarm[new_df_disarm['ID'] == 141])

new_df_disarm = new_df_disarm.explode('gwno').reset_index(drop=True)
# print(new_df_disarm[new_df_disarm['ID'] == 141])

new_df_disarm['ID'] = new_df_disarm.groupby('ID').cumcount() + 1 + (new_df_disarm['ID'] * 10)
# print(new_df_disarm[new_df_disarm['ID'] == 1412])

####### adding ISO3 and short country name columns ######### 
converter = coco.CountryConverter()

gwcodes = new_df_disarm['gwno']
# # print(gwcodes)

ISO3column = converter.convert(names=gwcodes, src="GWcode", to="ISO3")
shortCountryName = converter.convert(names=gwcodes, src="GWcode", to="name_short")
# #  print(ISO3column)
idx = 5 

new_df_disarm.insert(loc=idx, column='ISO3', value = ISO3column)
new_df_disarm.insert(loc=idx+1, column='country_name', value = shortCountryName)
# print(new_df_disarm['country_name'])

