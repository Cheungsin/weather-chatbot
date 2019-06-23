#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 22:11:39 2019

@author: chengxin
"""


import requests
import json
import re
import spacy
import random
import hashlib
import urllib.parse

globleDict = {}
def initInterPreter():
    # Import necessary modules
    from rasa_nlu.training_data import load_data
    #from rasa_nlu.config import RasaNLUModelConfig
    from rasa_nlu.model import Trainer
    from rasa_nlu import config
    
    # Create a trainer that uses this config
    trainer = Trainer(config.load("config_spacy.yml"))
    
    # Load the training data
    training_data = load_data('training_dataset9.json')
    
    # Create an interpreter by training the model
    globleDict['interpreter'] = trainer.train(training_data)
    print('train interpreter success!!!')
    
initInterPreter()

def receiveMsg(msg): #收到msg
    print('hahaha')
    #if msg == 'weather':
    print('yeah!!!')
    #nlp = spacy.load('en_core_web_md')
    #doc = nlp(msg)
    #doc = nlp("What's the Shenzhen's weather like today?")
    #doc = nlp("Do I need to wear more clothes in Beijing tomorrow?")
    #for ent in doc.ents:
        #print(ent.text, ent.label_)
        #if ent.label_ == 'GPE':
            #return parseOneDayStr(getOneDayData(getWeather(ent.text), 1), 'all')
    return parseMsg(globleDict['interpreter'].parse(msg))

def transToEn(mystr):
    aid = '20190623000309737'
    p = 'aSISSl_xSRtDtrXfD83V'
    print('p')
    print(p)
    salt = random.randint(32768, 65536)
    print('salt')
    print(salt)
    s = aid + str(mystr) + str(salt) + p
    print('s')
    print(s)
    m = hashlib.md5()
    b = s.encode(encoding='utf-8')
    m.update(b)
    sign = m.hexdigest()
    print('sign')
    print(sign)
    q = 'appid=' + aid + '&from=zh&to=en&q=' + urllib.parse.quote(mystr) + '&salt=' + str(salt) + '&sign=' + sign
    print('q')
    print(q)
    r = requests.get("http://api.fanyi.baidu.com/api/trans/vip/translate?" + q)
    r.encoding = 'utf8'
    print('r.text')
    print(r.text)
    enStr = json.loads(r.text)
    returnStr = ''
    for es in enStr['trans_result']:
        returnStr = returnStr + es['dst'] + '\n' 
    return returnStr

def getWeather(cityName): #使用接口获得天气数据
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
    #print(r.text)
    weatherData = json.loads(r.text)
    return weatherData
    
#getWeather("Beijing")
#getWeather("Guangzhou")
#getWeather("shenzhen")

def getOneDayData(weatherData, day): # 参数：API获得的数据，希望获取的日期（-1：昨天，0：今天，1：1天后，2:2天后...）
    #print(weatherData)
    if (day == -1):
        data = weatherData['data']['yesterday']
        data['date'] = weatherData['data']['city'] + '昨日(' + data['date']
    else:
        data = weatherData['data']['forecast'][day]
        if (day == 0):
            data['date'] = weatherData['data']['city'] + '今日(' + data['date']
        elif (day == 1):
            data['date'] = weatherData['data']['city'] + '明日(' + data['date']
        elif (day == 2):
            data['date'] = weatherData['data']['city'] + '后天(' + data['date']
        else:
            data['date'] = weatherData['data']['city'] + str(day) + '天后(' + data['date']
    #print(data)
    return data
#getOneDayData(getWeather("shenzhen"), -1)

def parseOneDayStr(oneDayData, style):
    if style == 'all':
        stri = oneDayData['date'] + ')天气:' + '\n' + oneDayData['low'] + ', ' + oneDayData['high'] + '\n' + oneDayData['type'] + '\n' + (oneDayData['fx'] if 'fx' in oneDayData else oneDayData['fengxiang']) + ', ' + re.search(r'(?<=CDATA\[).*(?=\]\])', (oneDayData['fl'] if 'fl' in oneDayData else oneDayData['fengli'])).group()
    elif style == 'onlyTemperature':
        stri = oneDayData['date'] + ')温度:' + '\n' + oneDayData['low'] + ', ' + oneDayData['high']
    elif style == 'onlyClimate':
        stri = oneDayData['date'] + ')气候:' + '\n' + oneDayData['type']
    elif style == 'onlyWind':
        stri = oneDayData['date'] + ')风向风力:' + '\n' + (oneDayData['fx'] if 'fx' in oneDayData else oneDayData['fengxiang']) + ', ' + re.search(r'(?<=CDATA\[).*(?=\]\])', (oneDayData['fl'] if 'fl' in oneDayData else oneDayData['fengli'])).group()
    print(stri)
    print('translate stri:')
    print(transToEn(stri))
    return transToEn(stri)
#parseOneDayStr(getOneDayData(getWeather("shenzhen"), 1), 'all')
#parseOneDayStr(getOneDayData(getWeather("guangzhou"), 2), 'onlyTemperature')
#parseOneDayStr(getOneDayData(getWeather("beijing"), 0), 'onlyClimate')
#parseOneDayStr(getOneDayData(getWeather("shanghai"), 3), 'onlyWind')



#print('------start:')
#print(interpreter.parse("What's the weather like in Shenzhen today?"))
#print('------end')
#print(interpreter.parse("What's the highest building of Shenzhen?"))

params = {}
def parseMsg(interpreter):  
    print('interpreter')
    print(interpreter)

    #interpreter = {'intent': {'name': 'askWeather', 'confidence': 0.9988591247903451}, 'entities': [{'start': 27, 'end': 35, 'value': 'shenzhen', 'entity': 'city', 'confidence': 0.9973445414808976, 'extractor': 'CRFEntityExtractor'}, {'start': 41, 'end': 42, 'value': '?', 'entity': 'city', 'confidence': 0.6232087923091154, 'extractor': 'CRFEntityExtractor'}], 'intent_ranking': [{'name': 'askWeather', 'confidence': 0.9988591247903451}, {'name': 'greet', 'confidence': 0.0009235777715449384}, {'name': 'bye', 'confidence': 0.00011801225976564498}, {'name': 'negative', 'confidence': 9.855893707871175e-05}, {'name': 'affirmative', 'confidence': 7.262412655369333e-07}], 'text': "What's the weather like in Shenzhen today?"}

    if ((interpreter['intent']['name'] == 'askWeather' and interpreter['intent']['confidence'] > 0.9) or globleDict['shouldContinue'] == True):
    
        print(interpreter['entities'])
        
        for ent in interpreter['entities']:
            if ent['entity'] == 'city' and ent['confidence'] > 0.1:
                print('city!!!')
                print(ent['value'])
                params['city'] = ent['value']
            elif ent['entity'] == 'time' and ent['confidence'] > 0.1:
                params['time'] = ent['value']
                print('time!!!')
                print(ent['value'])
                print(params)
            elif ent['entity'] == 'weathers' and ent['confidence'] > 0.1:
                print('weathers!!!')
                print(ent['value'])
                params['weathers'] = ent['value']
        
        #flag = 0 #0:可返回数据 1:需继续询问城市 2:需继续询问时间
        returnStr = 'None'
        #for param in params:
        if 'city' in params and 'time' in params: #存在城市 且 存在时间
            globleDict['shouldContinue'] = False
            if 'weathers' in params: #问的是具体的天气
                print('has weathers!!!')
            else: #问的是天气情况
                day = 0
                if params['time'].lower() == 'yesterday':
                    day = -1
                elif params['time'].lower() == 'today':
                    day = 0
                elif params['time'].lower() == 'tomorrow':
                    day = 1
                elif params['time'].lower() == 'the day after tomorrow':
                    day = 2
                elif params['time'].lower() == 'three days later':
                    day = 3
                elif params['time'].lower() == 'four days later':
                    day = 4
                else:
                    day = 404 #超过可查询的时间
                    
                if day == 404:
                    returnStr: '当前时间无法查询，请重试。'
                else:
                    returnStr = parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'all')
                    params.clear()
        elif 'city' in params: #只存在城市，不存在时间
            #flag = 2
            returnStr = 'What time?'
            globleDict['shouldContinue'] = True
        elif 'time' in params:
            #flag = 1
            returnStr = 'What city?'
            globleDict['shouldContinue'] = True
        return returnStr
            
                        





#include_entities = ['DATE', 'ORG', 'PERSON', 'GPE']

#def extract_entities(message):
#    ents=dict.fromkeys(include_entities)
#    doc=nlp(message)
#    for ent in doc.ents:
#        if ent.label_ in include_entities:
#            ents[ent.label_]=ent.text
#    return ents
#print(extract_entities('Do I need to wear more clothes in Haizhu tomorrow?'))



#print(doc.similarity(nlp("can")))
