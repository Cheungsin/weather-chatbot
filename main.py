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
    training_data = load_data('data/training_dataset14.json')
    
    # Create an interpreter by training the model
    globleDict['interpreter'] = trainer.train(training_data)
    
initInterPreter()

def receiveMsg(msg): #收到msg
    return parseMsg(globleDict['interpreter'].parse(msg))

def transToEn(mystr):
    aid = '20190623000309737'
    p = 'aSISSl_xSRtDtrXfD83V'
    salt = random.randint(32768, 65536)
    s = aid + str(mystr) + str(salt) + p
    m = hashlib.md5()
    b = s.encode(encoding='utf-8')
    m.update(b)
    sign = m.hexdigest()
    q = 'appid=' + aid + '&from=zh&to=en&q=' + urllib.parse.quote(mystr) + '&salt=' + str(salt) + '&sign=' + sign
    r = requests.get("http://api.fanyi.baidu.com/api/trans/vip/translate?" + q)
    r.encoding = 'utf8'
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
    weatherData = json.loads(r.text)
    return weatherData
    
#getWeather("Beijing")
#getWeather("Guangzhou")
#getWeather("shenzhen")

def getOneDayData(weatherData, day): # 参数：API获得的数据，希望获取的日期（-1：昨天，0：今天，1：1天后，2:2天后...）
    if (day == -1):
        data = weatherData['data']['yesterday']
        data['date'] = '{} yesterday({})'.format(weatherData['data']['city'], data['date'])
        data['isgoing'] = False
    else:
        data = weatherData['data']['forecast'][day]
        if (day == 0):
            data['date'] = '{} today({})'.format(weatherData['data']['city'], data['date'])
            data['isgoing'] = False
        elif (day == 1):
            data['date'] = '{} tomorrow({})'.format(weatherData['data']['city'], data['date'])
            data['isgoing'] = True
        elif (day == 2):
            data['date'] = '{} the day after tomorrow({})'.format(weatherData['data']['city'], data['date'])
            data['isgoing'] = True
        else:
            data['date'] = '{} {} days later({})'.format(weatherData['data']['city'], str(day), data['date'])
            data['isgoing'] = True
    #print(data)
    return data
#getOneDayData(getWeather("shenzhen"), -1)

def parseOneDayStr(oneDayData, style):
    if style == 'all':
        stri = 'The weather condition of {} will be as follows: the highest temperature will be {}℃  and the lowest temperature will be {}℃ . And it will be "{}" at that time.'.format(oneDayData['date'], re.search(r'\d+', oneDayData['high']).group(), re.search(r'-?\d+', oneDayData['low']).group(), oneDayData['type'])
    elif style == 'onlyTemperature':
        stri = 'For ' + '{}, the highest temperature will be {}℃ and the lowest temperature will be {}℃.'.format(oneDayData['date'], oneDayData['high'], oneDayData['low'])
    elif style == 'onlyClimate':
        stri = 'For ' + '{}, The weather will be "{}" at that time.'.format(oneDayData['date'], oneDayData['type'])
    elif style == 'onlyWind':
        stri = 'For ' + '{}, The strength of wind will be "{}", and the direction will be "{}" at that time.'.format(oneDayData['date'], (oneDayData['fx'] if 'fx' in oneDayData else oneDayData['fengxiang']), re.search(r'(?<=CDATA\[).*(?=\]\])', (oneDayData['fl'] if 'fl' in oneDayData else oneDayData['fengli'])).group())
    return transToEn(stri)
#parseOneDayStr(getOneDayData(getWeather("shenzhen"), 1), 'all')
#parseOneDayStr(getOneDayData(getWeather("guangzhou"), 2), 'onlyTemperature')
#parseOneDayStr(getOneDayData(getWeather("beijing"), 0), 'onlyClimate')
#parseOneDayStr(getOneDayData(getWeather("shanghai"), 3), 'onlyWind')

def getClimateDetail(oneDayData, msgStr):
    flag = ''
    if msgStr.find('rainy') != -1 or msgStr.find('sunny') != -1 or msgStr.find('cloudy') != -1 or msgStr.find('stormy') != -1:
        if oneDayData['type'].find('雨') != -1:
            flag = 'rainy' #有雨
        elif oneDayData['type'].find('晴') != -1:
            flag = 'sunny'
        elif oneDayData['type'].find('云') != -1:
            flag = 'cloudy'
        elif oneDayData['type'].find('雷') != -1 or oneDayData['type'].find('大雨') != -1 or oneDayData['type'].find('暴雨') != -1:
            flag = 'stormy'
    elif msgStr.find('hot') != -1 or msgStr.find('cold') != -1 or msgStr.find('warm') != -1 or msgStr.find('cool') != -1:
        if int(re.search(r'-?\d+', oneDayData['high']).group()) > 30:
            flag = 'hot' #有雨
        elif int(re.search(r'-?\d+', oneDayData['low']).group()) > 20 and int(re.search(r'-?\d+', oneDayData['high']).group()) <= 30:
            flag = 'warm'
        elif int(re.search(r'-?\d+', oneDayData['low']).group()) > 10 and int(re.search(r'-?\d+', oneDayData['high']).group()) <= 20:
            flag = 'cool'
        elif int(re.search(r'-?\d+', oneDayData['high']).group()) <= 10:
            flag = 'cold'
    elif msgStr.find('windy') != -1 or msgStr.find('storm') != -1:
        if int(re.search(r'\d+', re.search(r'(?<=CDATA\[).*(?=\]\])', (oneDayData['fl'] if 'fl' in oneDayData else oneDayData['fengli'])).group()).group()) > 7:
            flag = 'storm'
        else:
            flag = 'windy'
    return flag
    

params = {}
def parseMsg(interpreter):  

    #interpreter = {'intent': {'name': 'askWeather', 'confidence': 0.9988591247903451}, 'entities': [{'start': 27, 'end': 35, 'value': 'shenzhen', 'entity': 'city', 'confidence': 0.9973445414808976, 'extractor': 'CRFEntityExtractor'}, {'start': 41, 'end': 42, 'value': '?', 'entity': 'city', 'confidence': 0.6232087923091154, 'extractor': 'CRFEntityExtractor'}], 'intent_ranking': [{'name': 'askWeather', 'confidence': 0.9988591247903451}, {'name': 'greet', 'confidence': 0.0009235777715449384}, {'name': 'bye', 'confidence': 0.00011801225976564498}, {'name': 'negative', 'confidence': 9.855893707871175e-05}, {'name': 'affirmative', 'confidence': 7.262412655369333e-07}], 'text': "What's the weather like in Shenzhen today?"}

    #if ((interpreter['intent']['name'] == 'askWeather' and interpreter['intent']['confidence'] > 0.9) or globleDict['shouldContinue'] == True):
    if (interpreter['intent']['name'] == 'bye' or interpreter['intent']['name'] == 'affirmative'):
        returnStr = ['Thanks to you~',
                     'Bye~ Feel free to ask me anytime!',
                     'Thanks for your asking.',
                     'Bye~ I\'m glad to help you!'][random.randint(0, 3)] #1111 改过了
        params.clear()
    elif (interpreter['intent']['name'] == 'greet'):
        returnStr = ['Hi~ I\'m your weather assistant!',
                     'Hello, you can ask everything about the weather to me',
                     'Nice to meet you, I\'m your weather assistant!'][random.randint(0, 2)] #1111 改过了
    #elif ((interpreter['intent']['name'] == 'askWeather' or interpreter['intent']['name'] == 'giveTime') and interpreter['intent']['confidence'] > 0.6):
    elif (interpreter['intent']['confidence'] > 0.6):
        print(interpreter['entities'])
        
        for ent in interpreter['entities']:
            if ent['entity'] == 'city' and ent['confidence'] > 0.1:
                params['city'] = ent['value']
            elif ent['entity'] == 'time' and ent['confidence'] > 0.1:
                params['time'] = ent['value']
            elif ent['entity'] == 'contents' and ent['confidence'] > 0.1:
                params['contents'] = ent['value']
            elif ent['entity'] == 'elements' and ent['confidence'] > 0.1:
                params['elements'] = ent['value']
        
        #flag = 0 #0:可返回数据 1:需继续询问城市 2:需继续询问时间
        returnStr = 'None' ####
        #for param in params:
        if 'city' in params and 'time' in params: #存在城市 且 存在时间
            #globleDict['shouldContinue'] = False
                
            if False:
                #print('111')
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
                    returnStr = '当前时间无法查询，请重试。'
                else:
                    if 'elements' in params:
                        if 'contents' in params:
                            del params['contents'] 
                        print('has elements!!!')
                        if params['elements'].find('temperature') != -1:
                            returnStr = parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'onlyTemperature')
                        elif params['elements'].find('wind') != -1:
                            returnStr = parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'onlyWind')
                        elif params['elements'].find('ultraviolet') != -1:
                            returnStr = 'Sorry, I can\’t find the data of ultraviolet rays. Try to ask me something else.'
                        elif params['elements'].find('humidity') != -1:
                            returnStr = 'Sorry, I can\’t find the data of humidity. Try to ask me something else.'
                    elif 'contents' in params: #问的是具体的天气
                        if 'elements' in params:
                            del params['elements'] 
                        print('has contents!!!')
                        ###################todo
                        #returnStr = params['time'].lower() + ' is ' + getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents']) + ':\n' + parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'onlyClimate')
                        if params['contents'] == 'cold' or params['contents'] == 'cool' or params['contents'] == 'warm' or params['contents'] == 'hot':
                            returnStr = ('Yes. ' if params['contents'] == getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents']) else 'No. ') + parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'onlyTemperature') + 'That is a {} day. '.format(getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents']))
                        elif params['contents'] == 'sunny' or params['contents'] == 'cloudy' or params['contents'] == 'rainy' or params['contents'] == 'stormy':
                            returnStr = ('Yes. ' if params['contents'] == getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents']) else 'No. ') + parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'onlyClimate') + 'That is a {} day. '.format(getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents'])) + ('Remember to take your umbrella~' if (getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents']) == 'rainy' or getClimateDetail(getOneDayData(getWeather(params['city']), day), params['contents']) == 'stormy') else '')
                        #else:
                            #returnStr = params['time'].lower() + ' not have rain\n' + parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'onlyClimate')
                    else:
                        if 'contents' in params:
                            del params['contents'] 
                        if 'elements' in params:
                            del params['elements'] 
                        returnStr = parseOneDayStr(getOneDayData(getWeather(params['city']), day), 'all')
                    #params.clear()
        elif 'city' in params: #只存在城市，不存在时间
            #flag = 2
            returnStr = ['What time?','At what time?','Uh...So what\'s the time?'][random.randint(0, 2)] ##改过了
            globleDict['shouldContinue'] = True
        elif 'time' in params:
            #flag = 1
            returnStr = ['Which city?',
                         'Of which city?',
                         'Uh...So what\'s the city?',
                         'Could you tell me which city are you talking about?'][random.randint(0, 3)]  ##改过了
            globleDict['shouldContinue'] = True
        else:
            if interpreter['intent']['name'] == 'askWeather':
                returnStr = ['What time?','At what time?','Uh...So what\'s the time?'][random.randint(0, 2)] ##改过了
            else:
                returnStr = ['Sorry, I can not understand what you say.',
                             'Sorry, please ask me something about weather.',
                             'Try to ask me something about weather',
                             'Sorry I can\'t understand you, i\'m a weather assistant.'][random.randint(0, 3)] # 我是一个天气助手。 改过了
    else:
        returnStr = ['Sorry, I can not understand what you say.',
                     'Sorry, please ask me something about weather.',
                     'Try to ask me something about weather',
                     'Sorry I can\'t understand you, i\'m a weather assistant.'][random.randint(0, 3)]
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
