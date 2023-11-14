import pandas as pd
import re
import urllib.request
import pprint as pp
from urllib.request import urlopen
from bs4 import BeautifulSoup

# List of sku numbers to run
sku_list = [

]

# Setting up the user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)

# Setting up a dataframe
mc_dict = {'Sku':[], 'Marketing_Copy': [], 'Img_1': [], 'Img_2': [], 'Img_3': [], 'Img_4': []}

# Setting up a list for dictionaries
dict_list= []

for sku in sku_list:
    
    # Adding the sku to the mc_dict Sku column
    mc_dict['Sku'].append(sku)
    
    # Extracting the page source for the sku from Signature Hardwares website and creating a soup object
    page = urlopen('https://www.signaturehardware.com/drea-wall-mount-bathroom-faucet---brushed-gold/{}.html'.format(sku))
    soup = BeautifulSoup(page, 'lxml')
    
    # Extracting Marketing Copy and adding it to mc_dict
    try:
        main_div = soup.find("div", {"class": "col-sm-12 col-md-8 col-lg-9 px-0 short-desc"})
        marketing_copy = str(main_div.text).strip()
        # print(marketing_copy)
        # main_df.append({'Marketing_Copy': marketing_copy}, ignore_index=True)
        mc_dict['Marketing_Copy'].append(marketing_copy)
    except:
        # main_df.append({'Marketing_Copy': 'NULL'})
        mc_dict['Marketing_Copy'].append('NULL')
    
    # Extracting Images and adding them to mc_dict
    img_div = soup.find("div", {"class": "c-product-detail__images c-product-detail__images--pdp js-pdp-carousel-wraper primary-images col-12 col-lg-7 position-relative"})
    alt_srcs = img_div.find_all("img", attrs = {'srcset' : True})
    alt_srcs = list(alt_srcs)
    src_list = []
    for src in alt_srcs:
        src = src['src']
        if src.endswith('w=950&fmt=auto'):
            src_list.append(src)

    try:
        mc_dict['Img_1'].append(src_list[0])
    except:
        mc_dict['Img_1'].append('NULL')
    
    try:
        mc_dict['Img_2'].append(src_list[1])
    except:
        mc_dict['Img_2'].append('NULL')

    try:
        mc_dict['Img_3'].append(src_list[2])
    except:
        mc_dict['Img_3'].append('NULL')
    
    try:
        mc_dict['Img_4'].append(src_list[3])
    except:
        mc_dict['Img_4'].append('NULL')
    
    # Extracting all specs into dictionaries and adding them to dict_list
    divs = soup.find("div", {"class": "product-specifications-inner"})
    keys = divs.find_all("span", {"class": "attribute-label"})
    values = divs.find_all("span", {"class": "attribute-value"})

    d = {'Sku': []}
    d['Sku'].append(sku)
    for key, value in zip(keys, values):
        d[key.text] = value.text
    dict_list.append(d)
    pp.pprint(d)

# Creating dataframes from the dict_list and mc_dict dictionaries
mc_df = pd.DataFrame.from_dict(mc_dict).fillna('NULL')
main_df = pd.DataFrame.from_dict(dict_list).fillna('NULL')

# Changing the Sku column from main_df from list to a string format
sku_col = main_df['Sku']
new_col = []
for sku in sku_col:
    sku = str(sku)[2:8]
    new_col.append(sku)

main_df['Sku'] = new_col

# Creating and printing the final dataframe
final_df = pd.merge(mc_df, main_df, how='left', left_on='Sku', right_on='Sku')
pp.pprint(final_df)

print('Run Complete!')

#  Writing the dataframe to an excel worksheet
final_df.to_excel('SH_MC_Data.xlsx', sheet_name='SH_MC_Data')
