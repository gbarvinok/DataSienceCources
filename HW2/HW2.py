
# coding: utf-8

# ### Генерируем список дат, для подстановки в УРЛ

# In[3]:

from datetime import date
from dateutil.rrule import rrule, DAILY
import datetime

a = date(2017,01, 01)
b = datetime.datetime.today()

date_list=[]
for dt in rrule(DAILY, dtstart=a, until=b):
    date_list += [dt.strftime("%Y-%m-%d")]

#date_list


# In[4]:

date_list[0]


# ### URL

# In[21]:

URL_firstPart='http://m.football.ua/default.aspx?menu_id=football_pda_news&dt='


# In[29]:

full_urls = []
for date in date_list:
    full_urls += [URL_firstPart+date]


# In[5]:

import requests
import bs4
import re
import datetime
import time 

import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# ### тестируем запрос на одной дате

# In[6]:

full_url='http://m.football.ua/default.aspx?menu_id=football_pda_news&dt='+ date_list[0]
page_data = requests.get(full_url)
source = bs4.BeautifulSoup(page_data.content, 'html.parser')
links = source.find_all(href=re.compile("http://m.football.ua/news/"))
articles={}
for link in links:        
    aticle_time = link.previous_sibling.previous_sibling.previous_sibling.string
    #print(datetime.datetime.combine(datetime.datetime.strptime(date_list[0], "%Y-%m-%d").date(), datetime.datetime.strptime(aticle_time, "%H:%M").time()))
    article_dt=datetime.datetime.combine(datetime.datetime.strptime(date_list[0], "%Y-%m-%d").date(), datetime.datetime.strptime(aticle_time, "%H:%M").time())
    article_title = link.string
    #print(article_title)
    articles[article_dt] = article_title.strip()
    #print(articles)
#print(date, "downloaded")
#time.sleep(1)


# In[57]:

datetime.datetime.combine(datetime.datetime.strptime(date_list[0], "%Y-%m-%d").date(), datetime.datetime.strptime(aticle_time, "%H:%M").time())


# In[56]:

datetime.datetime.strptime(date_list[0], "%Y-%m-%d").date()


# In[66]:

d = datetime.datetime(2016,12,12)
d


# In[67]:

date_1 = datetime.datetime.strptime('2016-12-12', "%Y-%m-%d")
date_1


# In[6]:

date_1 = datetime.datetime.combine(date_1,datetime.time(23,59))


# In[78]:

news=pd.DataFrame(articles.items())
news.columns=['DateTime', 'Title']
news.head()


# In[80]:

news.dtypes


# ### тянем данные

# In[83]:

articles={}
for date in date_list:
    full_url='http://m.football.ua/default.aspx?menu_id=football_pda_news&dt='+ date
    page_data = requests.get(full_url)
    source = bs4.BeautifulSoup(page_data.content, 'html.parser')
    links = source.find_all(href=re.compile("http://m.football.ua/news/"))
    for link in links:        
        aticle_time = link.previous_sibling.previous_sibling.previous_sibling.string
        #print(datetime.datetime.combine(datetime.datetime.strptime(date_list[0], "%Y-%m-%d").date(), datetime.datetime.strptime(aticle_time, "%H:%M").time()))
        article_dt=datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d").date(), datetime.datetime.strptime(aticle_time, "%H:%M").time())
        article_title = link.string
        #print(article_title)
        articles[article_dt] = article_title.strip()
        #print(articles)
    print(date, "downloaded")
    time.sleep(1)


# ### загружаем в DataFrame

# In[91]:

news=pd.DataFrame(articles.items())
news.columns=['crt', 'Title']
news=news.sort_values(by=['DateTime'], ascending=[True])
news=news.reset_index()
news.head()


# In[128]:

#news.shape
#news.dtypes
news.head()


# In[93]:

del news['index']


# In[95]:

news['index']=news.index


# ### ошибка, но индекс поменяло

# In[104]:

news.set_index(['DateTime'],inplace=True)


# In[111]:

news.plot()


# ### Группа за день

# In[125]:

news.ix[:,:'Title'].groupby(pd.TimeGrouper('24H')).count().plot()


# In[126]:

news.reset_index(inplace=True)


# ## Средний промежуток

# In[129]:

firstdate = news.head(1).iloc[0]['DateTime']
lastdate = news.tail(1).iloc[0]['DateTime']
timedelta_between_updates = (lastdate-firstdate)/(news.shape[0] - 1)
timedelta_between_updates.value


# In[130]:

timedelta_between_updates_in_seconds = timedelta_between_updates.value/float(10**9)
timedelta_between_updates_in_seconds


# ### Частота обновлений

# In[131]:

frequency=1/timedelta_between_updates_in_seconds
frequency


# In[132]:

news.to_csv('footballua_data.csv', encoding='utf-8')

