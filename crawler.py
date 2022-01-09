import pandas as pd
import requests as req
from bs4 import BeautifulSoup 
import re


def add_url(category):
    base_url =f'https://webzine.munjang.or.kr/archives/category/{category}/page/'
    url_list =[]
    temp =[]
    for i in range(1,68):
        url = base_url+str(i)
        resp = req.get(url)
        if(resp.status_code==200):
            soup = BeautifulSoup(resp.content,"html.parser")
            div_tag = soup.findAll('div', class_='post_title')
            for i in div_tag:
                link = i.find('a',href=True)
                if link.text:
                    temp.append(link['href'])
        else:
            print(resp.status_code)
            continue
    return temp 

def load_data(url):
    doc =[]
    resp = req.get(url)
    if(resp.status_code==200):
        soup = BeautifulSoup(resp.content,"html.parser") 
        contents = soup.find(class_='entry-content')
        temp_contents = contents.find_all('p')
        for value in temp_contents:
            if value.text:
                # print(value.text)
                if (len(value.text)>10):
                    doc.append(value.text)
        doc = ''.join(doc)
        # print(tyep(doc))
        return doc
    else:
        print(resp.status_code)

def append_csv(df,data):
    df.append(data)
    return df

category ="novel"
temp_data = []
text_list = add_url(category)
for check_url in text_list:
    if(len(check_url)<37):
       text_list.remove(check_url)


for count,url in enumerate(text_list):
    data_list = load_data(url)
    # print(data_list)
    temp_data.append(data_list)

sub_text ='\n\xa0\xa0\xa0'
for idx,value in enumerate(temp_data):
    temp_data[idx] = re.sub(sub_text,"",value)


df = pd.DataFrame(temp_data)
df.to_csv('text_data.csv')
    


    
