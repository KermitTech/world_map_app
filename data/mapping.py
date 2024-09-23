import country_converter as coco
from data.data_cleaning import new_df_disarm 
from data.polygon_data import data_json


########## Some aggregations on the data
### number of peace agreements per country
converter = coco.CountryConverter()



no_distinct_gwno = new_df_disarm['gwno'].nunique()
# print(no_distinct_gwno)

counts_pa_perCountry = new_df_disarm.groupby('gwno')['pa_name'].count()

### converting counts_pa_perCountry (it is a series) into a dataframe
counts_pa_perCountry_df = counts_pa_perCountry.reset_index()

### change the pa_column name
counts_pa_perCountry_df = counts_pa_perCountry_df.rename(columns={"pa_name":"pa_counts"}) 

#### convert the gwno code to iso3 and short country name
iso3 = converter.convert(names=counts_pa_perCountry_df['gwno'], src="GWcode", to="ISO3")
short_country_name = converter.convert(names=counts_pa_perCountry_df['gwno'], src="GWcode", to="name_short")

#### insert the new columns into the dataframe counts_pa_perCountry_df
counts_pa_perCountry_df.insert(loc=1, column='ISO3', value = iso3)
counts_pa_perCountry_df.insert(loc=2, column='country_name', value = short_country_name)

#### removed south Yemen
counts_pa_perCountry_df = counts_pa_perCountry_df.drop(counts_pa_perCountry_df[counts_pa_perCountry_df['gwno'] == '678'].index)
# print(counts_pa_perCountry_df)

mapping  = dict(zip(counts_pa_perCountry_df['ISO3'].str.strip(), counts_pa_perCountry_df['pa_counts']))
# print(mapping)



##########################################
### Making sure that the iso3 values in the geo data is the same as the iso3 in 
### the Excel file

for d in data_json["features"]:
    if d["Name"] not in mapping:
            mapping[d["Name"]] = 0

# print(mapping)  # it has iso3 country names and total number of agreements for each country
