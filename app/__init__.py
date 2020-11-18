import nltk
import numpy
import json
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize, sent_tokenize
from flask import Flask, request, render_template, jsonify
import pickle

app = Flask(__name__)

Pkl_Filename = "Pickle_RL_Model.pkl"  

with open(Pkl_Filename, 'rb') as file:  
    Pickled_LR_Model = pickle.load(file)

def form_sent(sent):
    return {word: True for word in nltk.word_tokenize(sent)}

# short_pos = open("short_reviews_old/positive.txt","r" ,encoding="utf8", errors='ignore').read()
# short_neg = open("short_reviews_old/negative.txt","r",  encoding="utf8", errors='ignore').read()

# documents = []

# for r in short_pos.split('\n'):
#     documents.append( (r, "positive") )

# for r in short_neg.split('\n'):
#     documents.append( (r, "negative") )

# print('1'*80)

# all_words = []

# short_pos_words = word_tokenize(short_pos)
# short_neg_words = word_tokenize(short_neg)


# print('2'*80)
# for w in short_pos_words:
#     all_words.append(w.lower())

# for w in short_neg_words:
#     all_words.append(w.lower())

# print('3'*80)
# all_words = nltk.FreqDist(all_words)
# word_features = list(all_words.keys())

# print('4'*80)

# def find_features(document):
#     words = word_tokenize(document)
#     features = {}
#     for w in word_features:
#         features[w] = (w in words)

#     return features

# featuresets = [(find_features(rev), category) for (rev, category) in documents]
# training_set = featuresets
# print('5'*80)
# model = NaiveBayesClassifier.train(training_set)
# print('6'*80)

@app.route('/',methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        print('in predict')
        data = request.get_json()
        message = data['text']
        print(message)
        print(sent_tokenize(message))
        token = nltk.word_tokenize(message)
        print('Part of speech : ',nltk.pos_tag(token))
        tagged = nltk.pos_tag(token)
        named_entity = nltk.ne_chunk(tagged)
        print('-'*80)
        print(named_entity)
        print('-'*80)
        lines = message
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.word_tokenize(lines)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        print(nouns)
        unique_nouns = []
        for each in nouns:
            if each.lower() not in unique_nouns:
                if each.lower().isalnum() == True:
                    unique_nouns.append(each.lower())
        classifier = Pickled_LR_Model.classify(form_sent(message))
        nltk_data = [{'classifier' : classifier},{'topics' : unique_nouns}]
    return jsonify(nltk_data)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5024)
