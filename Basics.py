#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# 
# * For this project, we're working as data analysts for a company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# * **We only build apps that are free to download and install, and our main source of revenue consists of in-app ads.**
# 
# * This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the ads, the better. Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.
# 

# In[1]:


from csv import reader

#Esta es para Apple
opened_file = open ('AppleStore.csv')
read_file = reader (opened_file)
apple_play = list(read_file)
apple_header = apple_play[0]
apple_play = apple_play[1:]

#Esta es para Google
opened_file = open ('googleplaystore.csv')
read_file = reader (opened_file)
go_play = list(read_file)
go_header = go_play[0]
go_play = go_play[1:]

#Esta es la funcion de explorar
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row
    #if rows_and_columns:
    #    print('Number of rows:', len(dataset))
    #    print('Number of columns:', len(dataset[0])


# Estas son las columnas de Google:
# 
# | App |  Category |  Rating |  Reviews |  Size |  Installs |  Type |  Price |  Content Rating |  Genres |  Last Updated |  Current Ver |  Android Ver |
# |:---:|:---------:|:-------:|:--------:|:-----:|:---------:|:-----:|:------:|:---------------:|:-------:|:-------------:|:------------:|:------------:|
# |  0  |     1     |    2    |     3    |   4   |     5     |   6   |    7   |        8        |    9    |       10      |      11      |      12      |
# 
# 
# Estas son las columnas de Apple:
# 
# | id |  track_name |  size_bytes |  currency |  price |  rating_count_tot |  rating_count_ver |  user_rating |  user_rating_ver |  ver |  cont_rating |  prime_genre |  sup_devices.num |  ipadSc_urls.num |  lang.num |
# |----|-------------|-------------|-----------|--------|-------------------|-------------------|--------------|------------------|------|--------------|--------------|------------------|------------------|-----------|
# | 0  | 1           | 2           | 3         | 4      | 5                 | 6                 | 7            | 8                | 9    | 10           | 11           | 12               | 13               | 14        |

# In[2]:


#Aqui exploramos
explore_data (go_play, 0, 3)
explore_data (apple_play, 0, 3)
print (go_header)
print (apple_header)


# In[4]:


#aqui encontramos el error. Ya borrado. 
#print (go_play [10472])
# ya fue ejecutado, no volver a borrar 
#del go_play [10472]
#print (go_play [10472])


# In[7]:


#solo para checar la app de 10472
#for row in go_play[10472:10473]:
#    print (row [0], row[9])
    


# In[7]:


#para detectar duplicados en google
unique_apps = [] 
duplicate_apps = [] 

for app in go_play: 
    name = app[0] 
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

print ('number duplicates:', len(duplicate_apps))
print ('\n')
print ('examples:', duplicate_apps[0:5])


# In[8]:


#para detectar duplicados en apple
unique_apps = [] 
duplicate_apps = [] 

for app in apple_play: 
    name = app[0] 
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

print ('number duplicates:', len(duplicate_apps))
print ('\n')
print ('examples:', duplicate_apps[0:5])


# Ya sabemos que hay duplicados en la data obtenida. 1181 en la lista de Google, y 0 en la lista de Apple.
# Por ello haremos una limpieza del listado de Google, usando el criterio que la cantidad de reviews determina la antiguedad de la linea, y mientras mas reviews, mas nuevo el registro. Por tanto, nos quedaremos con el registro donde todo lo demás sea igual, pero la cantidad de reviews sea mayor

# In[9]:


print ('Expected length: ', len(go_play) - 1181)


# In[10]:


#para remover los duplicados de Google creamos un diccionario

reviews_max= {}
for app in go_play:
    name = app[0]
    n_reviews = float (app[3])
    if name in reviews_max and reviews_max[name]<n_reviews:
        reviews_max[name]=n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print (len (reviews_max))


# In[12]:


#ahora usamos el diccionario para remover de la lista
android_clean = []
already_added = []
for app in go_play:
    name = app[0]
    n_reviews = float (app[3])
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)

print (len(android_clean))             

explore_data(android_clean, 0, 3, True)


# In[13]:


#aqui detectamos que hay lineas en amabas listas que son apps que no vienen en inglés
print (apple_play[813][1])
print (apple_play[6731][1])
print ('\n')
print (android_clean[4412][0])
print (android_clean[7940][0])


# In[14]:


#creamos una función para detectar palabras que tienen mas de 3 caracteres que no esten en ingles.  
def noneng(string):
    count = 0
    for character in string:
        if ord(character)>=127:
            count = count +1
        if count >3:
            return False
    return True


words = ['Instagram','爱奇艺PPS -《欢乐颂2》电视剧热播','Docs To Go™ Free Office Suite','Instachat 😜']
for string in words:
    print (noneng(string))


# In[17]:


#ahora usamos la función para tratar de quitar de las listas app que no vienen en inglés, primero google

android_eng= []
nonenglish = []

for app in android_clean:
    name = app[0]
    if noneng(name)== True:
        android_eng.append(app)     
    else:
        nonenglish.append(app)

print (len(android_clean)-len(android_eng))        
print (len (android_eng))
print (len (nonenglish))

explore_data(android_eng, 0, 3, True)
explore_data(nonenglish, 0, 3, True)


# In[18]:


#ahora usamos la función para tratar de quitar de las listas app que no vienen en inglés, luego apple

apple_eng= []
applenonenglish = []

for app in apple_play:
    name = app[1]
    if noneng(name)== True:
        apple_eng.append(app)     
    else:
        applenonenglish.append(app)

print (len(apple_play)-len(apple_eng))        
print (len (apple_eng))
print (len (applenonenglish))

explore_data(apple_eng, 0, 3, True)
explore_data(applenonenglish, 0, 3, True)


# In[19]:


#ahora quitamos las apps que no son gratis

android_free = []

for app in android_eng:
    if app[7] == '0':
        android_free.append(app)
        
print (len (android_free))

apple_free = []
for app in apple_eng:
    if app[4] == '0.0':
        apple_free.append(app)
        
print (len (apple_free))


# Vamos a crear una app que tiene que poder ser exitosa tanto en Android como en iOS. Entonces, hay que buscar apps que cumplan con criterios en ambos listados y que sea atractiva para los usuarios, porque el sentido de todo esto es que sean relevantes. 

# In[24]:


#aqui vamos a crear unas tablas para mostrar la frecuencia de generos de las apps. Para ello definiremos dos funciones.

def freq_table (dataset, index):
    table = {}
    n = 0
    for row in dataset:
        n +=1
        value = row[index]
        if value in table:
            table[value] +=1
        else:
            table[value] = 1
    table_perc ={}
    for key in table:
        perc = round((table [key]/n)*100,2)
        table_perc[key] = perc
        
    return table_perc
    
def display_table(dataset, index):
    table = freq_table(dataset,index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
    table_sorted = sorted (table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])

#esta es para Genre de Android        
print ('Genre de Android')
display_table (android_free,9) 
print ('\n')
#esta es para Category de Android
print ('Category de Android')
display_table (android_free,1)  
print ('\n')
#esta es para Prime_genre de Apple
print ('prime genre de Apple')
display_table (apple_free,11)  


# ### What is the most common genre? What is the runner-up?
# **Andriod**
# +FAMILY : 18.91
# +GAME : 9.72
# **Apple**
# +Games : 58.16
# +Entertainment : 7.88
# 
# ### What other patterns do you see?
# Main apps are about entertainment
# 
# ### What is the general impression — are most of the apps designed for practical purposes (education, shopping, utilities, productivity, lifestyle) or more for entertainment (games, photo and video, social networking, sports, music)?
# Main apps are about entertainment in Apple, Google more balanced
# 
# 
# ### Can you recommend an app profile for the App Store market based on this frequency table alone? 
# 
# ### If there's a large number of apps for a particular genre, does that also imply that apps of that genre generally have a large number of users?
# no, we need to see installs

# ## Most Popular Apps by Genre on the App Store

# In[31]:


prime_genre = freq_table (apple_free,11)

print ('Genero : average number of ratings')
table_disord ={}
table_display = []
for genre in prime_genre:
    total = 0
    len_genre= 0
    
    for app in apple_free:
        genre_app = app[11]
        if genre_app == genre:
          usr_rating = float (app[5])
          total = total + usr_rating
          len_genre +=1    
    avg_rating = round (total/len_genre)
    table_disord [genre] = avg_rating

for key in table_disord:
    key_val_as_tuple = (table_disord[key], key)
    table_display.append(key_val_as_tuple)
    table_sorted = sorted (table_display, reverse = True)
for entry in table_sorted:
    print(entry[1], ':', entry[0])


# In[33]:


for app in apple_free:
    if app[11] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# In[34]:


for app in apple_free:
    if app[11] == 'Reference':
        print(app[1], ':', app[5]) # print name and number of ratings


# In[35]:


for app in apple_free:
    if app[11] == 'Book':
        print(app[1], ':', app[5]) # print name and number of ratings


# In[36]:


for app in apple_free:
    if app[11] == 'Weather':
        print(app[1], ':', app[5]) # print name and number of ratings


# Una aplicación de weather podría ser interesante porque puede ofrecer varios features no muy difíciles de producir

# ## Most Popular Apps by Genre on Google Play

# In[37]:


display_table (android_free, 5) 


# In[40]:


category_table = freq_table (android_free,1)

print ('Category : Average number of installs')
table_disord ={}
table_display = []
for category in category_table:
    total = 0
    len_category= 0
    
    for app in android_free:
        category_app = app[1]
        if category_app == category:
          usr_installs = app[5]
          usr_installs = usr_installs.replace('+','')
          usr_installs = usr_installs.replace(',','')
          usr_installs = float(usr_installs) 
          total = total + usr_installs
          len_category +=1    
    avg_installs = round (total/len_category)
    table_disord [category] = avg_installs

for key in table_disord:
    key_val_as_tuple = (table_disord[key], key)
    table_display.append(key_val_as_tuple)
    table_sorted = sorted (table_display, reverse = True)
for entry in table_sorted:
    print(entry[1], ':', entry[0])


# In[44]:


for app in android_free:
    if app[1] == 'WEATHER':
        print(app[0], ':', app[5]) # print name and number of ratings


# De nuevo apps de Weather podrían ser posibles

# In[ ]:




