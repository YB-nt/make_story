from typing import Collection
from pymongo import MongoClient
import requests as req
from pprint import pprint
from bs4 import BeautifulSoup
import re

base_url ='https://webzine.munjang.or.kr/archives/category/novel/page/'
def add_url(base_url):
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
        return doc
    else:
        print(resp.status_code)

# def insert_data(data):
#     """
#     input: 
#     type: dict{dict}

#     불러온 데이터를 mongodb에 넣어준다.
#     """
#     # 소설 데이터 불러오기
#     HOST = 'cluster0.qmemv.mongodb.net'
#     USER = 'yb-nt'
#     PASSWORD = 'ybnt'
#     DATABASE_NAME = 'myFirstDatabase'
#     COLLECTION_NAME = 'novel'
#     MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

#     client = MongoClient(MONGO_URI)
#     database = client[DATABASE_NAME]
#     collection = database[COLLECTION_NAME]

#     collection.insert_one(data)

doc ={}
novel_list = add_url(base_url)
for check_url in novel_list:
    if(len(check_url)<37):
        # print(check_url)
        novel_list.remove(check_url)

for count,url in enumerate(novel_list):
    # print(url)
    doc[str(count)]=load_data(url)

pprint(doc)
# url = 'https://webzine.munjang.or.kr/archives/150439'
# print(load_data(url))