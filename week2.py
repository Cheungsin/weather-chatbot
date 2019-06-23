####################
#######意图识别######
####################

#part1. 原始的意图识别方式
bot_template = "BOT : {0}"
user_template = "USER : {0}"

#1.1
# Define a function that responds to a user's message: respond
def respond(message):
    # Concatenate the user's message to the end of a standard bot respone
    bot_message = "I can hear you! You said: " + message
    # Return the result
    return bot_message


# Define a function that sends a message to the bot: send_message
def send_message(message):
    # Print user_template including the user_message
    print(user_template.format(message))
    # Get the bot's response to the message
    response = respond(message)
    # Print the bot template including the bot's response.
    print(bot_template.format(response))

# Send a message to the bot
send_message("hello")

#1.2
#用简单的模式，识别意图。有相应队列中的词项，就当作是有此意图。
import re
keywords = {
            'greet': ['hello', 'hi', 'hey'], #关键词变成pattern
            'thankyou': ['thank', 'thx'], 
            'goodbye': ['bye', 'farewell']
           }
# Define a dictionary of patterns。定义一个模式字典
patterns = {}

# Iterate over the keywords dictionary
for intent, keys in keywords.items():
    # Create regular expressions and compile them into pattern objects
    patterns[intent] =re.compile('|'.join(keys))
    
# Print the patterns
print(patterns)

responses = {'greet': 'Hello you! :)', 
             'thankyou': 'you are very welcome', 
             'default': 'default message', 
             'goodbye': 'goodbye for now'
            }

# Define a function to find the intent of a message
def match_intent(message): #find intent匹配句子中的意图
    matched_intent = None
    for intent, pattern in patterns.items():
        # Check if the pattern occurs in the message 
        if pattern.search(message):
            matched_intent = intent
    return matched_intent

# Define a respond function
def respond(message):
    # Call the match_intent function
    intent = match_intent(message)
    # Fall back to the default response
    key = "default"
    if intent in responses:
        key = intent
    return responses[key]

# Send messages
send_message("hello!")
send_message("bye byeee")
send_message("thanks very much!")


# Define find_name()
def find_name(message):
    name = None
    # Create a pattern for checking if the keywords occur
    name_keyword = re.compile(r"(name|call)")
    # Create a pattern for finding capitalized words
    name_pattern = re.compile("[A-Z]{1}[a-z]*")
    if name_keyword.search(message):
        # Get the matching words in the string
        name_words = name_pattern.findall(message) #findall()
        if len(name_words) > 0:
            # Return the name if the keywords are present
            name = ' '.join(name_words) #str.join(...)
    return name

# Define respond()
def respond(message):
    # Find the name
    name = find_name(message)
    if name is None:
        return "Hi there!"
    else:
        return "Hello, {0}!".format(name)

# Send messages
send_message("my name is David Copperfield")
send_message("call me Ishmael")
send_message("people call me Cassandra")


import spacy
import numpy as np
sentences = [' i want to fly from boston at 838 am and arrive in denver at 1110 in the morning', 
 ' what flights are available from pittsburgh to baltimore on thursday morning', 
 ' what is the arrival time in san francisco for the 755 am flight leaving washington', 
 ' cheapest airfare from tacoma to orlando', 
 ' round trip fares from pittsburgh to philadelphia under 1000 dollars', 
 ' i need a flight tomorrow from columbus to minneapolis', 
 ' what kind of aircraft is used on a flight from cleveland to dallas', 
 ' show me the flights from pittsburgh to los angeles on thursday', 
 ' all flights from boston to washington', 
 ' what kind of ground transportation is available in denver', 
 ' show me the flights from dallas to san francisco', 
 ' show me the flights from san diego to newark by way of houston', 
 ' what is the cheapest flight from boston to bwi', 
 ' all flights to baltimore after 6 pm', 
 ' show me the first class fares from boston to denver', 
 ' show me the ground transportation in denver', 
 ' all flights from denver to pittsburgh leaving after 6 pm and before 7 pm', 
 ' i need information on flights for tuesday leaving baltimore for dallas dallas to boston and boston to baltimore', 
 ' please give me the flights from boston to pittsburgh on thursday of next week', 
 ' i would like to fly from denver to pittsburgh on united airlines', 
 ' show me the flights from san diego to newark', 
 ' please list all first class flights on united from denver to baltimore', 
 ' what kinds of planes are used by american airlines', 
 " i'd like to have some information on a ticket from denver to pittsburgh and atlanta", 
 " i'd like to book a flight from atlanta to denver", 
 ' which airline serves denver pittsburgh and atlanta', 
 " show me all flights from boston to pittsburgh on wednesday of next week which leave boston after 2 o'clock pm", 
 ' atlanta ground transportation', ' i also need service from dallas to boston arriving by noon', 
 ' show me the cheapest round trip fare from baltimore to dallas']


 # Load the spacy model: nlp, en_core_web_md
nlp = spacy.load('en_core_web_md')#en_core_web_md是一个数据库，其中词项量是300维的
#这个代码的作用是引入这个数据集，nlp是引入数据集后对应的方法，它可以把句子变成300维向量

# Calculate the length of sentences
n_sentences = len(sentences)

# Calculate the dimensionality of nlp，维度是300维
embedding_dim = nlp.vocab.vectors_length

# Initialize the array with zeros: X
X = np.zeros((n_sentences, embedding_dim))

# Iterate over the sentences
for idx, sentence in enumerate(sentences):#idx是句子的序号
    # Pass each each sentence to the nlp object to create a document
    doc = nlp(sentence)
    # Save the document's .vector attribute to the corresponding row in X
    X[idx, :] = doc.vector
    #把句子们变成矩阵


import pandas as pd
X_train = pd.read_csv('/Users/chengxin/ChatBot/Re_ AI-18/X_train.csv')
X_test = pd.read_csv('/Users/chengxin/ChatBot/Re_ AI-18/X_test.csv')
y_train = pd.read_csv('/Users/chengxin/ChatBot/Re_ AI-18/y_train.csv')['label']
y_test = pd.read_csv('/Users/chengxin/ChatBot/Re_ AI-18/y_test.csv')['label']


# Import SVC
from sklearn.svm import SVC

# Create a support vector classifier
clf = SVC()

# Fit the classifier using the training data
clf.fit(X_train,y_train)

# Predict the labels of the test set
y_pred = clf.predict(X_test)

# Count the number of correct predictions
n_correct = 0
for i in range(len(y_test)):
    if y_pred[i] == y_test[i]:
        n_correct += 1
        
print("Predicted {0} correctly out of {1} test examples.".format(n_correct, len(y_test)))


## Using spaCy's entity recogniser

# Define included entities
include_entities = ['DATE', 'ORG', 'PERSON']

# Define extract_entities()
def extract_entities(message):
    # Create a dict to hold the entities
    ents = dict.fromkeys(include_entities)
    # Create a spacy document
    doc = nlp(message)
    for ent in doc.ents :
        if ent.label_ in include_entities: #比如Marry的标签在里面
            # Save interesting entities
            ents[ent.label_] = ent.text
    return ents

print(extract_entities('friends called Mary who have worked at Google since 2010'))
print(extract_entities('people who graduated from MIT in 1999'))


## Assigning roles using spaCy's parser 依赖分析
def entity_type(word):
    _type = None
    if word.text in colors:
        _type = "color"
    elif word.text in items:
        _type = "item"
    return _type

colors = ['black', 'red', 'blue']
items = ['shoes', 'handback', 'jacket', 'jeans']


## Assigning roles using spaCy's parser

# Create the document
doc = nlp("let's see that jacket in red and some blue jeans")

# Iterate over parents in parse tree until an item entity is found
def find_parent_item(word):
    # Iterate over the word's ancestors
    for parent in doc:
        # Check for an "item" entity
        if entity_type(parent) == "item":
            return parent.text
    return None

# For all color entities, find their parent item
def assign_colors(doc):
    # Iterate over the document
    for word in doc:
        # Check for "color" entities
        if entity_type(word) == "color":
            # Find the parent
            item =  find_parent_item(word)
            print("item: {0} has color : {1}".format(item, word))

# Assign the colors
assign_colors(doc)


# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config


# Create a trainer
trainer = Trainer(config.load("___"))

# Load the training data
training_data = load_data('___')

# Create an interpreter by training the model
interpreter = trainer.train(___)

# Try it out
print(interpreter.parse("I'm looking for a Mexican restaurant in the North of town"))


print(interpreter.parse("show me Chinese food in the centre of town"))
print(interpreter.parse("I want an Indian restaurant in the west"))
print(interpreter.parse("are there any good pizza places in the center?"))
