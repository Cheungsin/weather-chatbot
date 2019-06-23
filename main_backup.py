#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 22:11:39 2019

@author: chengxin
"""


import requests
import json



def getWeather(cityName):
    cityData = open("./cityCode.json", encoding='utf-8')
    cityData = json.load(cityData)
    cityCode = None
    for city in cityData:
        if city['pinyin'].upper() == cityName.upper():
            cityCode = city['code']
            break
    if cityCode == None:
        print("Sorry! I don't know this city: " + cityName)
        return
    #r = requests.get("http://www.weather.com.cn/data/cityinfo/" + cityCode + ".html")
    r = requests.get("http://wthrcdn.etouch.cn/weather_mini?citykey=" + cityCode)
    r.encoding = 'utf8'
    print(r.text)
    return r
    
#getWeather("Beijing")
#getWeather("Guangzhou")
#getWeather("shenzhen")
    


import spacy
nlp = spacy.load('en_core_web_md')
#doc = nlp("What's the Shenzhen's weather like today?")
doc = nlp("Do I need to wear more clothes in Beijing tomorrow?")
#for ent in doc.ents:
    #print("test*")
    #print(ent.text, ent.label_)
    #if ent.label_ == 'GPE':
        #getWeather(ent.text)


include_entities = ['DATE', 'ORG', 'PERSON', 'GPE']

def extract_entities(message):
    ents=dict.fromkeys(include_entities)
    doc=nlp(message)
    for ent in doc.ents:
        if ent.label_ in include_entities:
            ents[ent.label_]=ent.text
    return ents
print(extract_entities('Do I need to wear more clothes in Haizhu tomorrow?'))



#print(doc.similarity(nlp("can")))
