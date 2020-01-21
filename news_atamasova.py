#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-

f=open('./base.txt','w')
f.write('')
f.close()
f=open('./out.txt','w')
f.write('')
f.close()

from requests import request
from bs4 import BeautifulSoup
address='https://www.rbc.ru'
def getHtmlText(root):
    return request('GET', root).text
import re
def search(text):
#     strings = ['республик[^ ]+ парт[^ ]+ соед[^ ]+ штат[^ ]+','демократ[^ ]+ парт[^ ]+ соед[^ ]+ штат[^ ]+','демократ[^ ]+ парт[^ ]+ США','республик[^ ]+ парт[^ ]+ США'] 
#закомментированно, так как на момент выполнения очень мало новостей с такими упоминаниями
    strings = ['росси[^ ]'] 
    for string in strings:
        match = re.search(string, text)
        if match:
            return True
    return False
import time

for j in range(0,360*24):
    f=open('./base.txt','r')
    base=f.read().split('\n')
    f.close()
    contents =getHtmlText(address+'/short_news')
    soup = BeautifulSoup(contents, 'lxml')
    results = soup.findAll("div", {"class" : "js-news-feed-item"})
    f=open('./base.txt','a')

    res=open('./out.txt','a')
    for i in results:
        href=BeautifulSoup(str(i), 'lxml').findAll("a",{"class":"item__link"})[0]['href']
        if not (href in base):
            f.write(href)
            f.write('\n')
            if (href.find("https://www.rbc.ru/"))>=0:
                content=getHtmlText(href)
                soup=BeautifulSoup(content,'lxml')
                title=soup.findAll("div", {"class" : "article__header__title"})
                text=soup.findAll("div", {"class" : "article__text"})
                if(search(title[0].text.lower()))or(search(text[0].text.lower())):
                    print('Нашел связанную новость')
                    res.write("{\n")
                    res.write("title:{\n")
                    res.write(title[0].text)
                    res.write("\n}\n")
                    
                    res.write("text:{\n")
                    text=text[0].text
                    while(text.find("  ")>=0):
                        text=text.replace("  "," ")
                    while(text.find("\n\n")>=0):
                        text=text.replace("\n\n","\n")
                    res.write(text)
                    res.write("}\n")
                    author=soup.findAll("div", {"class" : "article__authors"})
                    res.write("author:{\n")
                    for i in author:
                        res.write(i.text)
                    res.write("\n}\n")
                    res.write("}\n")

    res.close()
    f.close()
    time.sleep(10)
    print(str(j+1)+"я итерация")


# In[ ]:




