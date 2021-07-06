#!/usr/bin/env python
# coding: utf-8

# The dataset we'll use describes Euro daily exchange rates between 1999 and 2021. The euro (symbolized with €) is the official currency in most of the countries of the European Union.
# 
# If the exchange rate of the euro to the US dollar is 1.5, you get 1.5 US dollars if you pay 1.0 euro (one euro has more value than one US dollar at this exchange rate).
# 
# Daria Chemkaeva put together the data set and made it available on Kaggle — the data source is the European Central Bank. Note that the dataset gets regular updates — we downloaded it on January 2021.

# In[1]:


import pandas as pd
exchange_rates = pd.read_csv('euro-daily-hist_1999_2020.csv')
pd.set_option('display.max_columns', None)

print (exchange_rates.head())

exchange_rates.info()

exchange_rates.tail()


# In[2]:


exchange_rates.rename(columns={'[US dollar ]': 'US_dollar','[UK pound sterling ]':'GBP','[Swiss franc ]':'CHF','[Mexican peso ]':'MXN', 
                               'Period\\Unit:': 'Time'},
                      inplace=True)
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True)


# In[3]:


euro_to_dollar = exchange_rates[["Time", "US_dollar"]]
euro_to_dollar.info()


# In[4]:


euro_to_dollar["US_dollar"].value_counts()


# In[5]:


euro_to_dollar = euro_to_dollar.loc[euro_to_dollar["US_dollar"] != '-']
euro_to_dollar["US_dollar"].value_counts()


# In[6]:


euro_to_dollar["US_dollar"] = euro_to_dollar["US_dollar"].astype(float)
euro_to_dollar.info()


# In[7]:


euro_to_dollar['rolling_mean'] = euro_to_dollar["US_dollar"].rolling(30).mean()
euro_to_dollar.head()


# In[8]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#Enables Jupyter to display graphs

plt.plot(euro_to_dollar['Time'],
         euro_to_dollar['rolling_mean'])
plt.show()


# We show comparatively how the euro-dollar rate changed before the 2008 crisis, and then how it behaved in 2008 when the crisis became worldwide, and then in 2009 when the crisis started to solve. We can use a line plot.

# In[9]:


### Defining time periods
toda_crisis = euro_to_dollar.copy(
                   )[(euro_to_dollar['Time'].dt.year >= 2006) & (euro_to_dollar['Time'].dt.year < 2010)]
pre_crisis = toda_crisis.copy(
       )[toda_crisis['Time'].dt.year < 2008]
crisis = toda_crisis.copy(
       )[(toda_crisis['Time'].dt.year == 2008)]
post_crisis = toda_crisis.copy(
       )[(toda_crisis['Time'].dt.year > 2008)]


print(pre_crisis.describe())
print(crisis.describe())
print(post_crisis.describe())


# In[ ]:





# In[10]:


euro_to_pound = exchange_rates[["Time", "GBP"]]
euro_to_pound.info()


# In[11]:


euro_to_pound["GBP"].value_counts()


# In[12]:


euro_to_pound = euro_to_pound.loc[euro_to_pound["GBP"] != '-']
euro_to_pound["GBP"].value_counts()


# In[13]:


euro_to_pound['rolling_mean'] = euro_to_pound["GBP"].rolling(30).mean()
euro_to_pound.head()


# In[14]:


plt.plot(euro_to_pound['Time'],
         euro_to_pound['rolling_mean'])
plt.show()


# In[15]:


### Defining time periods for pound vs euro
toda_crisisgbp = euro_to_pound.copy(
                   )[(euro_to_pound['Time'].dt.year >= 2006) & (euro_to_pound['Time'].dt.year < 2010)]
pre_crisisgbp = toda_crisisgbp.copy(
       )[toda_crisisgbp['Time'].dt.year < 2008]
crisisgbp = toda_crisisgbp.copy(
       )[(toda_crisisgbp['Time'].dt.year == 2008)]
post_crisisgbp = toda_crisisgbp.copy(
       )[(toda_crisisgbp['Time'].dt.year > 2008)& (toda_crisisgbp['Time'].dt.year < 2010) ]


print(pre_crisisgbp.describe())
print(crisisgbp.describe())
print(post_crisisgbp.describe())


# In[ ]:





# In[16]:


euro_to_chf = exchange_rates[["Time", "CHF"]]
euro_to_chf.info()


# In[17]:


euro_to_chf["CHF"].value_counts()


# In[18]:


euro_to_chf= euro_to_chf.loc[euro_to_chf["CHF"] != '-']
euro_to_chf["CHF"].value_counts()


# In[19]:


euro_to_chf['rolling_mean'] = euro_to_chf["CHF"].rolling(30).mean()
euro_to_chf.head()


# In[20]:


plt.plot(euro_to_chf['Time'],
         euro_to_chf['rolling_mean'])
plt.show()


# In[21]:


### Defining time periods for pound vs euro
toda_crisischf = euro_to_chf.copy(
                   )[(euro_to_chf['Time'].dt.year >= 2006) & (euro_to_chf['Time'].dt.year < 2010)]
pre_crisischf = toda_crisischf.copy(
       )[toda_crisischf['Time'].dt.year < 2008]
crisischf = toda_crisischf.copy(
       )[(toda_crisischf['Time'].dt.year == 2008)]
post_crisischf = toda_crisischf.copy(
       )[(toda_crisischf['Time'].dt.year > 2008)& (toda_crisischf['Time'].dt.year < 2010) ]


print(pre_crisischf.describe())
print(crisischf.describe())
print(post_crisischf.describe())


# In[22]:



### Adding the FiveThirtyEight style
import matplotlib.style as style
style.use('fivethirtyeight')

### Adding the subplots
plt.figure(figsize=(12, 6))
ax1 = plt.subplot(2,3,1)
ax2 = plt.subplot(2,3,2)
ax3 = plt.subplot(2,3,3)
axes = [ax1, ax2, ax3]

### Changes to all the subplots
for ax in axes:
    ax.set_ylim(1.15, 1.65)
    ax.set_yticks([False])
    ax.grid(False)
      
    
    
### Ax1: Pre-crisis
ax1.plot(pre_crisis['Time'], pre_crisis['rolling_mean'],
        color='#BF5FFF')
ax1.set_xticklabels([])
#print(ax1.get_xticks())
#print(ax1.get_yticks())
ax1.text(732463, 1.72, 'PRE- CRISIS', fontsize=18, weight='bold',
        color='#BF5FFF')
ax1.text(732453, 1.67, 'Mean 1.305298', weight='bold',
        alpha=0.3)
ax1.axhline(y=01.48, xmin=0.82, xmax=0.95, alpha=0.5, color ='grey',linestyle='dotted') 
ax1.text(732793, 1.48, '1.47', weight= 'bold',
        alpha=0.8, color = '#BF5FFF')
ax1.axhline(y=01.17, xmin=0.1, xmax=0.25, alpha=0.5, color ='grey',linestyle='dotted') 
ax1.text(732423, 1.17, '1.18', weight= 'bold',
        alpha=0.8, color = '#BF5FFF')
ax1.text(732493, 1.1, '2006-2007', weight= 'bold',
        alpha=0.8, color = 'grey')

### Ax2: Crisis
ax2.plot(crisis['Time'], crisis['rolling_mean'],
        color='#ffa500')
ax2.set_xticklabels([])
#print(ax2.get_xticks())
#print(ax2.get_yticks())
ax2.text(733143, 1.72, 'CRISIS', fontsize=18, weight='bold',
        color='#ffa500')
ax2.text(733103, 1.67, 'Mean 1.476526', weight='bold',
         alpha=0.3)
ax2.axvspan(xmin=733153, xmax=733273, ymin=0, ymax=0.9,
           alpha=0.3, color='grey')
ax2.axhline(y=1.59, xmin=0.32, xmax=0.61, alpha=0.5, color ='grey',linestyle='dotted') 
ax2.text(733183, 1.62, '1.58', weight= 'bold',
        alpha=0.8, color = '#ffa500')
ax2.axhline(y=1.26, xmin=0.85, xmax=0.95, alpha=0.5, color ='grey',linestyle='dotted') 
ax2.text(733283, 1.25, '1.27', weight= 'bold',
        alpha=0.8, color = '#ffa500')
ax2.text(733173, 1.1, '2008', weight= 'bold',
        alpha=0.8, color = 'grey')

### Ax3: Post-Crisis
ax3.plot(post_crisis['Time'], post_crisis['rolling_mean'],
        color='#00B2EE')
ax3.set_xticklabels([])
#print(ax3.get_xticks())
#print(ax3.get_yticks())
ax3.text(733497, 1.72, 'POST-CRISIS', fontsize=18, weight='bold',
        color='#00B2EE')
ax3.text(733497, 1.67, 'Mean 1.389154', weight='bold',
         alpha=0.3)
ax3.axhline(y=1.50, xmin=0.80, xmax=0.97, alpha=0.5, color ='grey',linestyle='dotted') 
ax3.text(733657, 1.51, '1.49', weight= 'bold',
        alpha=0.8, color = '#00B2EE')
ax3.axhline(y=1.26, xmin=0.10, xmax=0.37, alpha=0.5, color ='grey',linestyle='dotted') 
ax3.text(733547, 1.26, '1.27', weight= 'bold',
        alpha=0.8, color = '#00B2EE')
ax3.text(733577, 1.1, '2009', weight= 'bold',
        alpha=0.8, color = 'grey')


### Adding a title and a subtitle
ax.text(732372, 1.95, 'EURO-USD rate behaved differently during crisis vs pre & post',
         fontsize=20, weight='bold')
ax.text(732372, 1.85, '''EURO-USD exchange rates Pre, During and Post 2008 crisis''',
        fontsize=16)

### Adding a signature
ax.text(732372, 1, 'GM' + ' '*122 + 'Source: European Central Bank',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',
        size=14)


plt.show()

### Adding the subplots
plt.figure(figsize=(12, 6))
ax1 = plt.subplot(2,3,1)
ax2 = plt.subplot(2,3,2)
ax3 = plt.subplot(2,3,3)
axes = [ax1, ax2, ax3]

### Changes to all the subplots
for ax in axes:
    ax.set_ylim(0.6, 1)
    ax.set_yticks([False])
    ax.grid(False)
      
    
    
### Ax1: Pre-crisis
ax1.plot(pre_crisisgbp['Time'], pre_crisisgbp['rolling_mean'],
        color='#BF5FFF')
ax1.set_xticklabels([])
#print(ax1.get_xticks())
#print(ax1.get_yticks())
ax1.text(732463, 1.05, 'PRE- CRISIS', fontsize=18, weight='bold',
        color='#BF5FFF')
ax1.text(732453, 1, 'Mean 0.681875', weight='bold',
        alpha=0.3)
ax1.axhline(y=0.72, xmin=0.82, xmax=0.95, alpha=0.5, color ='grey',linestyle='dotted') 
ax1.text(732793, 0.715, '0.72', weight= 'bold',
        alpha=0.8, color = '#BF5FFF')
ax1.axhline(y=0.65, xmin=0.40, xmax=0.55, alpha=0.5, color ='grey',linestyle='dotted') 
ax1.text(732453, 0.63, '0.66', weight= 'bold',
        alpha=0.8, color = '#BF5FFF')
ax1.text(732493, 0.55, '2006-2007', weight= 'bold',
        alpha=0.8, color = 'grey')

### Ax2: Crisis
ax2.plot(crisisgbp['Time'], crisisgbp['rolling_mean'],
        color='#ffa500')
ax2.set_xticklabels([])
#print(ax2.get_xticks())
#print(ax2.get_yticks())
ax2.text(733143, 1.05, 'CRISIS', fontsize=18, weight='bold',
        color='#ffa500')
ax2.text(733103, 1, 'Mean 0.785519', weight='bold',
         alpha=0.3)
ax2.axhline(y=0.89, xmin=0.85, xmax=0.95, alpha=0.5, color ='grey',linestyle='dotted') 
ax2.text(733293, 0.885, '0.89', weight= 'bold',
        alpha=0.8, color = '#ffa500')
ax2.axhline(y=0.72, xmin=0.1, xmax=0.25, alpha=0.5, color ='grey',linestyle='dotted') 
ax2.text(733133, 0.71, '0.72', weight= 'bold',
        alpha=0.8, color = '#ffa500')
ax2.text(733173, 0.55, '2008', weight= 'bold',
        alpha=0.8, color = 'grey')

### Ax3: Post-Crisis
ax3.plot(post_crisisgbp['Time'], post_crisisgbp['rolling_mean'],
        color='#00B2EE')
ax3.set_xticklabels([])
#print(ax3.get_xticks())
#print(ax3.get_yticks())
ax3.text(733497, 1.05, 'POST-CRISIS', fontsize=18, weight='bold',
        color='#00B2EE')
ax3.text(733497, 1, 'Mean 0.891640', weight='bold',
         alpha=0.3)
ax3.axhline(y=0.93, xmin=0.1, xmax=0.25, alpha=0.5, color ='grey',linestyle='dotted') 
ax3.text(733507, 0.925, '0.93', weight= 'bold',
        alpha=0.8, color = '#00B2EE')
ax3.axhline(y=0.86, xmin=0.3, xmax=0.55, alpha=0.5, color ='grey',linestyle='dotted') 
ax3.text(733437, 0.86, '0.86', weight= 'bold',
        alpha=0.8, color = '#00B2EE')
ax3.text(733577, 0.58, '2009', weight= 'bold',
        alpha=0.8, color = 'grey')


### Adding a title and a subtitle
ax.text(732372, 1.22, 'EURO-GBP rate behaved differently during crisis vs pre & post',
         fontsize=20, weight='bold')
ax.text(732372, 1.17, '''EURO-GBP exchange rates Pre, During and Post 2008 crisis''',
        fontsize=16)

### Adding a signature
ax.text(732372, 0.45, 'GM' + ' '*122 + 'Source: European Central Bank',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',
        size=14)


plt.show()


### Adding the subplots
plt.figure(figsize=(12, 6))
ax1 = plt.subplot(2,3,1)
ax2 = plt.subplot(2,3,2)
ax3 = plt.subplot(2,3,3)
axes = [ax1, ax2, ax3]

### Changes to all the subplots
for ax in axes:
    ax.set_ylim(1.3, 1.7)
    ax.set_yticks([False])
    ax.grid(False)

### Ax1: Pre-crisis
ax1.plot(pre_crisischf['Time'], pre_crisischf['rolling_mean'],
        color='#BF5FFF')
ax1.set_xticklabels([])
#print(ax1.get_xticks())
#print(ax1.get_yticks())
ax1.text(732463, 1.8, 'PRE- CRISIS', fontsize=18, weight='bold',
        color='#BF5FFF')
ax1.text(732453, 1.75, 'Mean 1.604720', weight='bold',
        alpha=0.3)
ax1.axhline(y=1.545, xmin=0.1, xmax=0.25, alpha=0.5, color ='grey',linestyle='dotted') 
ax1.text(732533, 1.535, '1.55', weight= 'bold',
        alpha=0.8, color = '#BF5FFF')
ax1.axhline(y=1.675, xmin=0.75, xmax=0.9, alpha=0.5, color ='grey',linestyle='dotted') 
ax1.text(732753, 1.665, '1.67', weight= 'bold',
        alpha=0.8, color = '#BF5FFF')
ax1.text(732493, 1.4, '2006-2007', weight= 'bold',
        alpha=0.8, color = 'grey')

### Ax2: Crisis
ax2.plot(crisischf['Time'], crisischf['rolling_mean'],
        color='#ffa500')
ax2.set_xticklabels([])
#print(ax2.get_xticks())
#print(ax2.get_yticks())
ax2.text(733143, 1.8, 'CRISIS', fontsize=18, weight='bold',
        color='#ffa500')
ax2.text(733103, 1.75, 'Mean 1.594302', weight='bold',
         alpha=0.3)
ax2.axhline(y=1.50, xmin=0.70, xmax=0.85, alpha=0.5, color ='grey',linestyle='dotted') 
ax2.text(733223, 1.50, '1.50', weight= 'bold',
        alpha=0.8, color = '#ffa500')
ax2.axhline(y=1.661, xmin=0.05, xmax=0.2, alpha=0.5, color ='grey',linestyle='dotted') 
ax2.text(733113, 1.655, '1.65', weight= 'bold',
        alpha=0.8, color = '#ffa500')
ax2.text(733173, 1.4, '2008', weight= 'bold',
        alpha=0.8, color = 'grey')

### Ax3: Post-Crisis
ax3.plot(post_crisischf['Time'], post_crisischf['rolling_mean'],
        color='#00B2EE')
ax3.set_xticklabels([])
#print(ax3.get_xticks())
#print(ax3.get_yticks())
ax3.text(733497, 1.8, 'POST-CRISIS', fontsize=18, weight='bold',
        color='#00B2EE')
ax3.text(733497, 1.75, 'Mean 1.512066', weight='bold',
         alpha=0.3)
ax3.axhline(y=1.481, xmin=0.2, xmax=0.35, alpha=0.5, color ='grey',linestyle='dotted') 
ax3.text(733557, 1.475, '1.48', weight= 'bold',
        alpha=0.8, color = '#00B2EE')
ax3.axhline(y=1.54, xmin=0.05, xmax=0.2, alpha=0.5, color ='grey',linestyle='dotted') 
ax3.text(733477, 1.54, '1.54', weight= 'bold',
        alpha=0.8, color = '#00B2EE')
ax3.text(733577, 1.4, '2009', weight= 'bold',
        alpha=0.8, color = 'grey')


### Adding a title and a subtitle
ax.text(732372, 1.95, 'EURO-CHF rate behaved differently during crisis vs pre & post',
         fontsize=20, weight='bold')
ax.text(732372, 1.9, '''EURO-CHF exchange rates Pre, During and Post 2008 crisis''',
        fontsize=16)

### Adding a signature
ax.text(732372, 1.3, 'GM' + ' '*122 + 'Source: European Central Bank',
        color = '#f0f0f0', backgroundcolor = '#4d4d4d',
        size=14)


plt.show()


# In[ ]:




