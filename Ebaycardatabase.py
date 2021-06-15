#!/usr/bin/env python
# coding: utf-8

# In this guided project, we'll work with a dataset of used cars from eBay Kleinanzeigen, a classifieds section of the German eBay website.
# The aim of this project is to clean the data and analyze the included used car listings. You'll also become familiar with some of the unique benefits jupyter notebook provides for pandas.

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


autos = pd.read_csv('autos.csv', encoding='Windows-1252')


# In[3]:


autos


# In[4]:


print (autos.info())
print (autos.head(5))


# There are several rows with null data in columns 6,8,10,13,15

# In[5]:


autos.columns


# In[6]:


new_columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
       'last_seen']
autos.columns = new_columns
print (autos.columns)


# In[7]:


print(autos.head())


# Reword some of the column names based on the data dictionary to be more descriptive:
# * yearOfRegistration to registration_year
# * monthOfRegistration to registration_month
# * notRepairedDamage to unrepaired_damage
# * dateCreated to ad_created
# 
# Changed the rest of the column names from camelcase to snakecase.

# In[8]:


autos.describe(include='all')


# In[9]:


print(autos['odometer'].head())
print(autos['price'].head())


# In[10]:


autos['odometer'] = autos['odometer'].str.replace('km','')
autos['odometer'] = autos['odometer'].str.replace(',','')
autos['odometer'] = autos['odometer'].astype(int)
print(autos['odometer'].head())
autos['price'] = autos['price'].str.replace('$','')
autos['price'] = autos['price'].str.replace(',','')
autos['price'] = autos['price'].astype(int)
print(autos['price'].head())


# In[11]:


autos.rename({'odometer':'odometer_km'},axis = 1, inplace=True)


# we learned that there are a number of text columns where almost all of the values are the same (seller and offer_type). We also converted the price and odometer columns to numeric types and renamed odometer to odometer_km.

# In[12]:


print(autos['price'].unique().shape)
print(autos['price'].describe())
print(autos['price'].value_counts().sort_index(ascending=True).head(100))


# In[13]:


print(autos['odometer_km'].unique().shape)
print(autos['odometer_km'].describe())
print(autos['odometer_km'].value_counts().sort_index(ascending=True).head(100))


# In[14]:


autos = autos[autos['price'].between(100,500000)]
autos = autos[autos['power_ps'].between(50,600)]


# removing price outliers below 100 and above 500,000

# In[15]:


print(autos['price'].unique().shape)
print(autos['price'].describe())
print(autos['price'].value_counts().sort_index(ascending=False).head(100))


# In[16]:


print(autos['date_crawled'].str[:10].value_counts(normalize=True,dropna=False).sort_index())


# In[17]:


print(autos['ad_created'].str[:10].value_counts(normalize=True,dropna=False).sort_index())


# In[18]:


print(autos['last_seen'].str[:10].value_counts(normalize=True,dropna=False).sort_index())


# In[19]:


print(autos['registration_year'].describe())


# registration year has some weird years like 1000 and 9999

# In[20]:


print(autos['registration_year'].between(0,1900).value_counts())
print(autos['registration_year'].between(2016,9999).value_counts())


# In[21]:


autos = autos[autos['registration_year'].between(1900,2016)]
print(autos['registration_year'].value_counts(normalize=True).sort_index())


# Removed all registration years below 1900 and above 2016

# going to aggregate by brands

# In[22]:


unique_brands = autos['brand'].value_counts(normalize=True).sort_values(ascending=False)
print (unique_brands.head(10))
brands_index = unique_brands.iloc[0:10].index
print (brands_index)


# I will aggregate only the 10 ten brands, as the 10th brand has less than 2% of share.

# In[23]:


table_disord ={}
for unique in brands_index:
    dataset = autos.loc[autos['brand']==unique]
    mean_price = int(round(dataset['price'].mean()))
    table_disord [unique] = mean_price
        
table_display = []
for key in table_disord:
    key_val_as_tuple = (table_disord[key], key)
    table_display.append(key_val_as_tuple)
    table_sorted = sorted (table_display, reverse = True)
for entry in table_sorted:
    print(entry[1], ':',"$" "{:,}".format(entry[0]))
    
    
##    table_disord ={}
##for unique in brands_index:
##    total = 0
##    len_unique = 0
##    dataset = autos.loc[autos['brand']==unique]
##    for row in dataset.values:
##        price = row[4]
##        total = total + price
##        len_unique +=1
##    avg_price = round (total / len_unique)
##    table_disord [unique] = avg_price


# of the top 10 brands: most expensive in average audi, least expensive in average renault

# In[24]:


bmp_series = pd.Series(table_disord)
print(bmp_series)
df = pd.DataFrame(bmp_series, columns=['mean_price'])
df


# In[25]:


table_disordtoo ={}
for unique in brands_index:
    dataset = autos.loc[autos['brand']==unique]
    mean_mileage = int(round(dataset['odometer_km'].mean()))
    table_disordtoo [unique] = mean_mileage
    
bmp_seriestoo = pd.Series(table_disordtoo)
print(bmp_seriestoo)
df2 = pd.DataFrame(bmp_seriestoo, columns=['mean_mileage'])
df2


# In[26]:


df3 = df
df3['mean_mileage']=bmp_seriestoo
df3 = df3.sort_values(by=['mean_price'],ascending=False)

with pd.option_context('display.max_colwidth', 50, 'display.max_rows', None, 'display.max_columns', None, 'display.precision', 0, 'display.colheader_justify', 'center'):  # more options can be specified also
    print(df3)


# There is no correlation price vs mileage

# 'date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
#        'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
#        'odometer', 'registration_month', 'fuel_type', 'brand',
#        'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
#        'last_seen'

# In[27]:


selection= ['seller', 'offer_type', 'abtest', 'vehicle_type', 'gearbox', 'fuel_type', 'unrepaired_damage']
for column in selection:
    print(autos[column].value_counts())

autos['seller'] = autos['seller'].str.replace('privat','private')
autos['offer_type'] = autos['offer_type'].str.replace('Angebot','offer')
autos['gearbox'] = autos['gearbox'].str.replace('manuell','manual')
autos['gearbox'] = autos['gearbox'].str.replace('automatik','automatic')
autos['unrepaired_damage'] = autos['unrepaired_damage'].str.replace('nein','no')
autos['unrepaired_damage'] = autos['unrepaired_damage'].str.replace('ja','yes')

mapping_dict = {
    'limousine': 'limousine',
    'kleinwagen': 'compact',
    'kombi': 'combi',
    'bus': 'bus',
    'cabrio': 'convertible',
    'coupe': 'coupe',
    'suv': 'suv',
    'andere': 'other',
}

mapping_dicttoo = {
    'benzin': 'petrol',
    'diesel': 'diesel',
    'lpg': 'lpg',
    'cng': 'cng',
    'hybrid': 'hybrid',
    'elektro': 'electric',
    'andere': 'other',
}




autos["vehicle_type"]= autos["vehicle_type"].map(mapping_dict)
autos["fuel_type"]= autos["fuel_type"].map(mapping_dicttoo)




# In[28]:


selection= ['seller', 'offer_type', 'abtest', 'vehicle_type', 'gearbox', 'fuel_type', 'unrepaired_damage']
for column in selection:
    print(autos[column].value_counts())


# In[29]:


print(autos['last_seen'].value_counts(normalize=True,dropna=False).sort_index())


# In[30]:


#import datetime as dt

#for row in autos.values:
#    date = row[19]
#    parsed_date = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
#    row[19]=int(parsed_date.strftime("%Y%m%d"))
#    print(row[19])

#print(autos['last_seen'])
short_dates=[]
for row in autos.values:
    date = row[19]
    date_short= date[:10].replace('-','')
    short_dates.append(int(date_short))

autos.loc[:,'last_seen']=short_dates    
print (autos['last_seen'].head())


# In[31]:


print(autos['ad_created'].value_counts(normalize=True,dropna=False).sort_index())


# In[32]:


short_dates=[]
for row in autos.values:
    date = row[16]
    date_short= date[:10].replace('-','')
    short_dates.append(int(date_short))

autos.loc[:,'ad_created']=short_dates    
print (autos['ad_created'].head())


# In[33]:


print(autos['date_crawled'].value_counts(normalize=True,dropna=False).sort_index())


# In[34]:


short_dates=[]
for row in autos.values:
    date = row[0]
    date_short= date[:10].replace('-','')
    short_dates.append(int(date_short))

autos.loc[:,'date_crawled']=short_dates    
print (autos['date_crawled'].head())


# In[54]:


brand_index= autos['brand'].value_counts().head(5).index
print (brand_index)


# In[60]:


#vw_pop = autos.loc[autos['brand'] == 'volkswagen', 'model'].value_counts(normalize=True)
#vw_top_pop = vw_pop[vw_pop >0.01]*100
#vw_top_models = vw_top_pop.index
#vw_dict = {}
#for i in vw_top_models:
#    sel_rows = autos[autos['model']== i]
#    vw_counts = sel_rows['model'].count()
#    vw_dict[i] = vw_counts
    
#print (vw_dict)

for one in brand_index:   
    #top_brand = autos['brand'].value_counts().index[0]
    top_model = autos['model'].loc[(autos['brand']==one)].value_counts().index[0]
    second_model= autos['model'].loc[(autos['brand']==one)].value_counts().index[1]
    third_model= autos['model'].loc[(autos['brand']==one)].value_counts().index[2]
    print ('brand: ',one,' ', 'top model: ', top_model)
    print ('brand: ',one,' ', 'second model: ', second_model)
    print ('brand: ',one,' ', 'third model: ', third_model)
    
    
    


# In[ ]:




