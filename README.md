# Weather chatbot

Here is an automatic chat bot of weather forecast based on rasa_nlu and some open resource interfaces of climate. It can tell you the weather in the coming four days of almost all the cities in China, even some smaller districts of a city. To use it, you just need to ask it some questions about weather and follow its instructions, and it will give back the answers to you in English.

## API uses
Here I use the API based on the data of China Meteorological Administration. It provides free weather forecast of the coming 4 days of almost all the GPEs of China.
Since the feedback from API is in Chinese, I also use the BIDU translator to translate it into English.

## Basic Tools and techniques 
Here I use some nlp techniques based on rasa_nlu with the config using sklearn as the pipeline. I generated and used a big training dataset to build the rasa interpreter. With the techniques of intent classification, semantic slot filling, entities extractions and so on, the chat bot can answer your questions about weather accurately. 

## Deployment and uses
This chatbot can be deployed on wechat based on the wxpy project. You just need to load the chatbot in the cmd. After successfully loaded, you can ask your chatbot on wechat to get the answers of weather forecasting.

### Here are demos:

![Demo1](https://github.com/Cheungsin/weather-chatbot/blob/master/Demo/Demo1.gif?raw=true)
https://github.com/Cheungsin/weather-chatbot/blob/master/Demo/Demo1.mp4

![Demo2](https://github.com/Cheungsin/weather-chatbot/blob/master/Demo/Demo2.gif?raw=true)
https://github.com/Cheungsin/weather-chatbot/blob/master/Demo/Demo2.mp4
