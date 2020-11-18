import pickle
import nltk
import numpy
import json
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize, sent_tokenize
from flask import Flask, request, render_template, jsonify

short_pos = open("short_reviews_new/positive.txt","r" ,encoding="utf8", errors='ignore').read()
short_neg = open("short_reviews_new/negative.txt","r",  encoding="utf8", errors='ignore').read()

documents = []

for r in short_pos.split('\n'):
    documents.append( (r, "positive") )

for r in short_neg.split('\n'):
    documents.append( (r, "negative") )

print('1'*80)

all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)


print('2'*80)
for w in short_pos_words:
    all_words.append(w.lower())

for w in short_neg_words:
    all_words.append(w.lower())

print('3'*80)
all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())

print('4'*80)

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]
training_set = featuresets
print('5'*80)
model = NaiveBayesClassifier.train(training_set)
print('6'*80)


Pkl_Filename = "Pickle_RL_Model.pkl"  
with open(Pkl_Filename, 'wb') as file:  
    pickle.dump(model, file)