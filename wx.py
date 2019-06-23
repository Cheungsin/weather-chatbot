#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 01:35:22 2019

@author: chengxin
"""

import wxpy
bot = wxpy.Bot(cache_path=True)

print('123*')
print(bot.friends().search('杨承欣'))
ycx = bot.friends().search('杨承欣')[0]

ycx.send('Hello')

@bot.register(ycx)
def reply_ycx(msg):
    print(msg.text)
    return msg.text

@bot.register(ycx) 
def reply_ycx(msg):  
    print(msg.text)  
    weather = main.reveiveMsg(msg.text)  
    print(weather) 
    return weather 

wxpy.embed()

