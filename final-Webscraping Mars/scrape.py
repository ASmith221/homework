
# coding: utf-8

# In[32]:


# Dependencies

from bs4 import BeautifulSoup as bs

import requests
import pymongo
from splinter import Browser

import tweepy

import time
import pandas as pd


# In[33]:


# Twitter API Keys
consumer_key = "3REpngub1g5pFnxOrmFy7RA7u"
consumer_secret = "B8Z6Qp4NsxDsEblyUwTqrQAd4CoCMAPkM9R8a81tGrOcy5fwwm"
access_token = "338862045-4oYBBr7iESvJCw7u9KEhUxBFIdSmMGwi9sohBk5z"
access_token_secret = "yQHd23XHo5iIrhFuVdJLq2aXgT4kHbV2BK7sNvz5X2fKc"
api_key="24c85411d38cdd9b4b1601ca2a92276d"


# In[34]:


# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[35]:


#Browser Chromedriver

executable_path = {"executable_path": "/Users/Adrienne/Downloads/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# # NASA Mars News

# In[54]:


#set up URL
news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)
#html = browser.html
#soup = BeautifulSoup(html, "html.parser")


# Get infor from Mars News URL
url = "https://mars.nasa.gov/news/"
response = requests.get(url)

soup = bs(response.text, 'html.parser')
#print(soup.prettify())

news_title = soup.find('div', 'content_title', 'a').text

news_p = soup.find('div', 'rollover_description_inner').text


# In[37]:


news_title


# In[53]:


news_p


# In[38]:


image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
html = browser.html
soup = bs(html, "html.parser")


# In[39]:


# Images from jpl.nasa.gov
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)
browser.find_by_id('full_image').click()
featured_image_url = browser.find_by_css('.fancybox-image').first['src']
print(featured_image_url)


# In[40]:


image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)
html = browser.html
soup = bs(html, "html.parser")

image = soup.find("img", class_="thumb")["src"]
featured_image_url = "https://www.jpl.nasa.gov" + image
print(featured_image_url)


# In[41]:


# Twitter API Keys
def get_file_contents(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

#consumer_key = get_file_contents('consumer_key')
#consumer_secret = get_file_contents('consumer_secret')
#access_token = get_file_contents('access_token')
#access_token_secret = get_file_contents('access_token_secret')

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# In[42]:


target_user = "MarsWxReport"
tweet = api.user_timeline(target_user, count =1)
mars_weather = ((tweet)[0]['text'])
print(mars_weather)


# In[52]:


# dataframe
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)
mars_data = pd.read_html(facts_url)
mars_data_db = pd.DataFrame(mars_data[0])
#mars_facts = mars_data.to_html(header = False, index = False)
mars_data_db


# In[50]:


hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)
html = browser.html
soup = bs(html, "html.parser")
mars_hemisphere = []

products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup=bs(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemisphere.append({"title": title, "img_url": image_url})


# In[48]:


mars_hemisphere

