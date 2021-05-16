#!/usr/bin/env python
# coding: utf-8

# #Hacker News data analysis project
# This is a guided project to compare two types of posts to determine the following:
# 
# *Do Ask HN or Show HN receive more comments on average?
# *Do posts created at a certain time receive more comments on average?
# 

# In[5]:


#we import the file and print the first rows to check
from csv import reader

opened_file = open ('hacker_news.csv')
read_file = reader (opened_file)
hn = list(read_file)

for row in hn[0:5]:
    print (row)
    print('\n')
    


# | id | title | url | num_points | num_comments | author | created_at |
# |:--:|:-----:|:---:|:----------:|:------------:|:------:|:----------:|
# |  0 |   1   |  2  |      3     |       4      |    5   |      6     |

# In[6]:


#we'll remove the header from the file
headers = hn[0]
hn = hn[1:]
print ('this is the header:', headers)
for row in hn[0:5]:
    print (row)
    print('\n')


# In[11]:


#we'll separate posts AskHN, ShowHN and other
ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row [1]
    title_lower = title.lower()
    if title_lower.startswith('ask hn'):
        ask_posts.append(row)
    elif title_lower.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
        
print (len(ask_posts))
print (len(show_posts))
print (len(other_posts))


# In[13]:


print('Below are the first five rows in the ask_posts list of lists:')
print('\n')
for row in ask_posts[0:5]:
    print (row)
    print('\n')
print('Below are the first five rows in the show_posts list of lists:')
print('\n')
for row in show_posts[0:5]:
    print (row)
    print('\n')


# In[16]:


#Next, let's determine if ask posts or show posts receive more comments on average.
total_ask_comments = 0

for row in ask_posts:
    num_comments = int (row[4])
    total_ask_comments += num_comments
    
avg_ask_comments = round(total_ask_comments / len(ask_posts))
print ('This is the average comments for ask posts  ', avg_ask_comments)

total_show_comments = 0

for row in show_posts:
    num_comments = int (row[4])
    total_show_comments += num_comments
    
avg_show_comments = round(total_show_comments / len(show_posts))
print ('This is the average comments for show posts  ', avg_show_comments)


# Do show posts or ask posts receive more comments on average? The data shows ask posts receive +40% more comments than show posts.

# In[22]:


import datetime as dt

result_list = []

for row in ask_posts:
    created_at = row [6]
    num_comments = int(row[4])
    result_list.append([created_at, num_comments])
    
counts_by_hour = {}
comments_by_hour = {}

for row in result_list:
    date = row[0]
    parsed_date = dt.datetime.strptime(date, "%m/%d/%Y %H:%M")
    hour = parsed_date.strftime("%H")
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = row [1]
    else:
        counts_by_hour[hour]+= 1
        comments_by_hour[hour] += row[1]
        
        
print (counts_by_hour)
print (comments_by_hour)
        


# In[23]:


#calculate the average number of comments per post for posts created during each hour of the day

avg_by_hour = []

for hour in comments_by_hour:
    avg_by_hour.append([hour, (comments_by_hour[hour]/counts_by_hour[hour])])
    
print (avg_by_hour)    


# In[25]:


#Let's finish by sorting the list of lists and printing the five highest values in a format that's easier to read

swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1],row[0]])
    
print (swap_avg_by_hour)   


# In[42]:


sorted_swap = sorted(swap_avg_by_hour, reverse = True)

print ('Top 5 hours for Ask Posts Comments @ Eastern Time US')

for avg, hour in sorted_swap[0:5]:
    hour_format = dt.datetime.strptime(hour, "%H")
    hour_format = hour_format.strftime("%H:%M")
    print ("{h}: {a:.2f} average comments per post".format(h=hour_format,a=avg))
    print ('\n')
    
print ('Top 5 hours for Ask Posts Comments @ Central Mex Time')    
for avg, hour in sorted_swap[0:5]:
    hour_format = dt.datetime.strptime(hour, "%H")
    mex = dt.timedelta(hours=1)
    hour_format = hour_format - mex
    hour_format = hour_format.strftime("%H:%M")
    print ("{h}: {a:.2f} average comments per post".format(h=hour_format,a=avg))
    print ('\n')


# Which hours should you create a post during to have a higher chance of receiving comments?
# 15 hours

# Determine if show or ask posts receive more points on average.
# Determine if posts created at a certain time are more likely to receive more points.
# Compare your results to the average number of comments and points other posts receive.
# Use Dataquest's data science project style guide to format your project.
