import re

pattern = r'http://'

def replace_http(url):
    if isinstance(url, str):
        return re.sub(pattern, 'https://', url)
    return url







########## Fixing the urls: 
# 1: missing urls : I could not find them in any refrences

# new_df_disarm[new_df_disarm['pa_name'] == 'Mahipar agreement']['linktofulltextagreement'] = 
# new_df_disarm[new_df_disarm['pa_name'] == 'Basic Charter (Fundamental Charter)']['linktofulltextagreement'] =
# new_df_disarm[new_df_disarm['pa_name'] == 'National reconciliation agreement']['linktofulltextagreement'] =
# new_df_disarm[new_df_disarm['pa_name'] == 'Paris Accord']['linktofulltextagreement'] =
# new_df_disarm[new_df_disarm['pa_name'] == 'Juba Agreement']['linktofulltextagreement'] =



# 2: http --> https
# import re

# # df_download = new_df_disarm[['linktofulltextagreement']].astype(str)
# # print(df_download)
# pattern = r'http://'
# # df_download = re.sub(pattern, 'https://', new_df_disarm['linktofulltextagreement'])
# # print(df_download)
# def replace_http(url):
#     if isinstance(url, str):
#         return re.sub(pattern, 'https://', url)
#     return url
# df_download['linktofulltextagreement'] = df_download['linktofulltextagreement'].apply(replace_http)
# print(df_download)