import nltk 
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import json
import random
import pickle

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
        
except:
    words = []
    labels =[]
    docs_x =[]
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            # stemming: take each word in pattern to root word
            # tokenize: get all words in pattern
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds) #both already a list so extening will just add it
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"]) 
                
    #remove duplicate words
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words))) #set takes words and remove duplicate elements
                                    # list converts result of set into list
                                    # sorted sort the words 
    labels = sorted(labels)

    # convert words in pattern to "bag of words" since nn only takes numbers
    # frequency of words in a list

    training =[]
    output =[]

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        
        wrds = [stemmer.stem(w) for w in doc]
        
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
                
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)
        
    #change to np array for tflearn

    training = np.array(training)
    output = np.array(output)
    
    
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tf.compat.v1.reset_default_graph()

#first (input) layer with length of "bag of words"
net = tflearn.input_data(shape=[None, len(training[0])])
#2 hidden layers with 8 neurons
net = tflearn.fully_connected(net, 8) 
net = tflearn.fully_connected(net, 8) 
#output layer: softmax activation gives probability to each neuron
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") 
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)

def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input ("You: ")
        if inp.lower() == "quit":
            break
        
        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]
        
        if results[results_index] > 0.05:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    
            print(random.choice(responses))
        
        else:
            print("I don't quite understand your question. Could you ask another question?")
        
chat()

