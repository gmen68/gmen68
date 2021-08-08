#!/usr/bin/env python
# coding: utf-8

# # 6. Guided Project Clean And Analyze Employee Exit Surveys
# 
# In this project, we'll play the role of data analyst and pretend our stakeholders want to know the following:
# 
# - Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
# - Are younger employees resigning due to some kind of dissatisfaction? What about older employees?
# 
# **We'll work with exit surveys from employees of the Department of Education, Training and Employment (DETE) and the Technical and Further Education (TAFE) institute in Queensland, Australia.**
# 
# We will import the databases and study them to understand the info they have.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


dete_survey = pd.read_csv('dete_survey.csv')
tafe_survey = pd.read_csv('tafe_survey.csv')


# In[3]:


print (dete_survey.info())
print (dete_survey.head(5))
print (dete_survey.isnull().sum())


# In[4]:


print (tafe_survey.info())
print (tafe_survey.head(5))
print (tafe_survey.isnull().sum())


# ## Identify Missing Values and Drop Unnecessary Columns
# 
# Both the dete_survey and tafe_survey dataframes contain many columns that seem unnecesary for the analysis requested. 
# 
# It must be noted that column names are different in both dataframes. 
# 
# A question we must answer:
# 
#  - How to find which columns reflect that the employee left because he was dissatisfied?
# 
# Also in Dete Survey, there are values declared as Not Stated that must be cleaned to reflect a NaN value. We accomplish this by rereading the 'dete_survey.csv' and indicating to read the 'Not stated' values as 'NaN'
# 
# Next we will delete columns we do not need for the analysis:  
# - columns 28 to 48 for dete_survey
# - columns 17 to 65 for the tafe_survey
# 
# We will create new files named dete_survey_updated and tafe_survey_updated respectively.
# 

# In[5]:


dete_survey = pd.read_csv('dete_survey.csv', na_values = 'Not Stated')


# In[6]:


dete_survey_updated = dete_survey.drop(dete_survey.columns[28:49], axis = 1)
print (dete_survey_updated.info())


# In[7]:


tafe_survey_updated = tafe_survey.drop(tafe_survey.columns[17:66], axis = 1)
print (tafe_survey_updated.info())


# Now we need to standardize the column names 

# In[8]:


dete_survey_updated.columns = dete_survey_updated.columns.str.strip().str.replace('\s', '_').str.lower()
print(dete_survey_updated.columns)


# In[9]:


mapping = {'Record ID': 'id','CESSATION YEAR': 'cease_date','Reason for ceasing employment': 'separationtype','Gender. What is your Gender?': 'gender','CurrentAge. Current Age': 'age','Employment Type. Employment Type': 'employment_status','Classification. Classification': 'position','LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service','LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'}
tafe_survey_updated = tafe_survey_updated.rename(mapping, axis=1)
print(tafe_survey_updated.columns)


# In[10]:


print (dete_survey_updated.head())
print (tafe_survey_updated.head())
print (dete_survey_updated['separationtype'].head(15))


# ## New Column Names
# 
# Changes to dete_survey_updated:
# 
# - Make all the capitalization lowercase.
# - Remove any trailing whitespace from the end of the strings.
# - Replace spaces with underscores ('_').
# 
# Changes to tafe_survey_updated:
# 
# - Rename columns as dete_survey_updated:
# 
# 
#     * 'Record ID': 'id'
#     * 'CESSATION YEAR': 'cease_date'
#     'Reason for ceasing employment': 'separationtype'
#     * 'Gender. What is your Gender?': 'gender'
#     * 'CurrentAge. Current Age': 'age'
#     * 'Employment Type. Employment Type': 'employment_status'
#     * 'Classification. Classification': 'position'
#     * 'LengthofServiceOverall. Overall Length of Service at Institute (in years)': 'institute_service'
#     * 'LengthofServiceCurrent. Length of Service at current workplace (in years)': 'role_service'

# In[11]:


print (dete_survey_updated['separationtype'].value_counts())
print (tafe_survey_updated['separationtype'].value_counts())


# In[12]:


tafe_resignations= tafe_survey_updated[tafe_survey_updated['separationtype']=='Resignation'].copy()
print (tafe_resignations['separationtype'].value_counts())


# In[13]:


res_type = {'Resignation-Other reasons','Resignation-Other employer','Resignation-Move overseas/interstate'}

dete_resignations = dete_survey_updated.copy()[(dete_survey_updated['separationtype'].isin(res_type))]

print (dete_resignations['separationtype'].value_counts())


# ## Clean the data
# 
# In each dataframe only the regisgnation rows in the separationtype column were selected and assigned to a new dataframe (dete_resignations (311 rows) and tafe_resignations (340 rows)) to answer the question:
# 
# - Are employees who have only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been at the job longer?

# In[14]:


print (dete_resignations['cease_date'].value_counts(dropna=False))


# In[15]:


dete_resignations['cease_date'] = dete_resignations.cease_date.str.extract(r'([2][0-9][0-9][0-9])', expand=True)
dete_resignations['cease_date']=dete_resignations['cease_date'].astype('float64')
print (dete_resignations['cease_date'].value_counts(dropna=False))                                                                              


# In[16]:


print (dete_resignations['cease_date'].value_counts(dropna=False).sort_index(ascending=True))
print (dete_resignations['dete_start_date'].value_counts(dropna=False).sort_index(ascending=True))  
print (tafe_resignations['cease_date'].value_counts(dropna=False).sort_index(ascending=True))  


# There are a lot of NaN values in the 3 columns
# 
# We will align time of service in both databases, using the tafe institute_service column as a guide. 

# In[17]:


print (tafe_resignations['institute_service'].value_counts(dropna=False).sort_index(ascending=True))

dete_resignations['institute_service'] = dete_resignations['cease_date']-dete_resignations['dete_start_date']

print (dete_resignations['institute_service'].value_counts(dropna=False).sort_index(ascending=True))


# In[18]:


di = {0.0: "Less than 1 year", 1.0: "1-2", 2.0:"1-2",3.0:"3-4",4.0:"3-4", 5.0:"5-6", 6.0:"5-6",7.0:"7-10", 8.0:"7-10", 9.0:"7-10",10.0:"7-10", 11.0:"11-20",12.0:"11-20",13.0:"11-20",14.0:"11-20",15.0:"11-20",16.0:"11-20",17.0:"11-20",18.0:"11-20",19.0:"11-20",20.0:"11-20",21:"More than 20 years",22:"More than 20 years",23:"More than 20 years",24:"More than 20 years",25:"More than 20 years",26:"More than 20 years",27:"More than 20 years",28:"More than 20 years",29:"More than 20 years",30:"More than 20 years",31:"More than 20 years",32:"More than 20 years",33:"More than 20 years",34:"More than 20 years",35:"More than 20 years",36:"More than 20 years",38:"More than 20 years",39:"More than 20 years",41:"More than 20 years",42:"More than 20 years",49:"More than 20 years"}

dete_resignations['institute_service'] = dete_resignations['institute_service'].map(di)

print (dete_resignations['institute_service'].value_counts(dropna=False).sort_index(ascending=True))


# tafe_survey_updated:
#  - Contributing Factors. Dissatisfaction
#  - Contributing Factors. Job Dissatisfaction
# 
# dete_survey_updated:
#  - job_dissatisfaction
#  - dissatisfaction_with_the_department
#  - physical_work_environment
#  - lack_of_recognition
#  - lack_of_job_security
#  - work_location
#  - employment_conditions
#  - work_life_balance
#  - workload
#  
# Will create a new column called dissatisfied in each dataframe that will map if in any column there is a True, a False or NaN, and then copy to a new dataframe with ending _up. 

# In[19]:


print (tafe_resignations['Contributing Factors. Dissatisfaction'].value_counts(dropna=False).sort_index(ascending=True))
print (tafe_resignations['Contributing Factors. Job Dissatisfaction'].value_counts(dropna=False).sort_index(ascending=True))


# In[20]:


def update_vals(x):
    if pd.isnull(x):
        return np.nan
    if x == '-':
        return False
    else:
        return True

factors = ['Contributing Factors. Dissatisfaction','Contributing Factors. Job Dissatisfaction']   
    
tafe_resignations[factors] = tafe_resignations[factors].applymap(update_vals)

print (tafe_resignations['Contributing Factors. Dissatisfaction'].value_counts(dropna=False).sort_index(ascending=True))  
print (tafe_resignations['Contributing Factors. Job Dissatisfaction'].value_counts(dropna=False).sort_index(ascending=True))  


# In[21]:


print (tafe_resignations.info())


# In[22]:


tafe_resignations['dissatisfied']= tafe_resignations[factors].any(axis=1, skipna=False)
print (tafe_resignations['dissatisfied'].value_counts(dropna=False).sort_index(ascending=True))  


# In[23]:


factors_dete = ['job_dissatisfaction', 'dissatisfaction_with_the_department', 'physical_work_environment', 'lack_of_recognition', 'lack_of_job_security', 'work_location','employment_conditions','work_life_balance','workload']

print (dete_resignations[factors_dete[5]].value_counts(dropna=False).sort_index(ascending=True))  

dete_resignations['dissatisfied']= dete_resignations[factors_dete].any(axis=1, skipna=False)

print (dete_resignations['dissatisfied'].value_counts(dropna=False).sort_index(ascending=True))  


# In[24]:


dete_resignations_up = dete_resignations.copy()
tafe_resignations_up = tafe_resignations.copy()


# In[25]:


dete_resignations_up['institute'] = 'DETE'
tafe_resignations_up['institute'] = 'TAFE'
print (dete_resignations_up.head())  
print (tafe_resignations_up.head())


# In[26]:


print (dete_resignations_up['institute_service'].value_counts(dropna=False).sort_index(ascending=True))
print (dete_resignations_up['institute_service'].count())

print (tafe_resignations_up['institute_service'].value_counts(dropna=False).sort_index(ascending=True))
print (tafe_resignations_up['institute_service'].count())


# In[27]:


combined = pd.concat([dete_resignations_up, tafe_resignations_up], ignore_index=True)
print (combined.shape)
print (combined.count())


# In[28]:


combined_updated = combined.dropna(axis=1,thresh=500)
print (combined_updated.info())


# ## Combine the dataframes
# 
# Combined the dataframes, drop any columns with less than 500 non null values and assigned to combined_update

# In[29]:


print (combined_updated['institute_service'].value_counts())
print (combined_updated['institute_service'].count())


# In[30]:


di = {'Less than 1 year':'New','1-2':'New','3-4':'Experienced','5-6':'Experienced','7-10':'Established', '11-20':'Veteran', 'More than 20 years':'Veteran'}

new_col = combined_updated['institute_service'].copy()

new_col = new_col.map(di)

combined_updated = combined_updated.assign(service_cat=new_col.values)

print (combined_updated['service_cat'].value_counts())
print (combined_updated['service_cat'].count())


# In[31]:


print (combined_updated['dissatisfied'].value_counts(dropna=False))

combined_updated.loc[:,'dissatisfied']=combined_updated['dissatisfied'].fillna(value=False)

print (combined_updated['dissatisfied'].value_counts(dropna=False))


# In[32]:


pv_melt = pd.pivot_table(combined_updated,index = 'service_cat', values = 'dissatisfied')

print(pv_melt)

pv_melt.plot(kind ='bar', y= 'dissatisfied', legend = False)


# From the pivot table and the bar chart above we can answer the first question of our project and it is that the more experienced you are the more dissatisfied you will be. The level of dissatisfaction is lower for New and Experienced while for Veterain and Established they have the highest level of dissatisfied employees.
# 
# ## Cleaning the age data for analysis
# 
# We will try to answer also the question of dissatisfaction related to employee age. 
# For that we will conduct a similar exercise cleaning and then creating a pivot table and plot. 

# In[33]:


print (combined_updated['age'].value_counts(dropna=False).sort_index(ascending=True))


# In[34]:


di = {'20 or younger':'20 or younger','21  25':'21-30','21-25':'21-30','26  30':'21-30','26-30':'21-30','31  35':'31-40','31-35':'31-40','36  40':'31-40','36-40':'31-40','41  45':'41-50','41-45':'41-50','46  50':'41-50','46-50':'41-50','51-55':'51 or older','56 or older':'51 or older','56-60':'51 or older','61 or older':'51 or older'}
combined_updated.loc[:,'age'] = combined_updated['age'].map(di)
print (combined_updated['age'].value_counts(dropna=False).sort_index(ascending=True))


# In[35]:


pv_melt = pd.pivot_table(combined_updated,index = 'age', values = 'dissatisfied')

get_ipython().run_line_magic('matplotlib', 'inline')

print(pv_melt)

pv_melt.plot(kind ='bar', y= 'dissatisfied', legend = False)


# From the pivot table and the bar chart above we can answer the new question of our project and it is that the older you are the more dissatisfied you will be.
# 
# ## Understanding difference among DETE and TAFE institutes 
# 
# We will try to answer also the question of dissatisfaction related to institute of employment. 
# For that we will conduct a similar exercise creating a pivot table and plot using as variable the institute of employment. 

# In[36]:


pv_melt = pd.pivot_table(combined_updated,index = 'institute', values = 'dissatisfied')

print(pv_melt)

pv_melt.plot(kind ='bar', y= 'dissatisfied', legend = False)


# Fewer employees who worked for TAFE have some kind of dissatisfaction while DETE employees have more dissatisfaction.
# 
# 
