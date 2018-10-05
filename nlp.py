# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 11:45:12 2018

@author: endy franklin
This machine learning code predicts if a mail
received from a user is either a spam mail or a ham mail

"""

import nltk
import pandas as pd
import string
from nltk.corpus import stopwords

#nltk.download_shell()
#open file to read it
messages=[line.rstrip() for line in open('C:/Users/endy franklin/Desktop/sms_dataset/SMSSpamCollection')]

#print(len(messages))

#messages[0]

#print the first 10 messages and number them using enumerate
for mess_num, message in enumerate(messages[:10]):
    print(mess_num, message)
    print('\n')
    
#read as csv
messages=pd.read_csv('C:/Users/endy franklin/Desktop/sms_dataset/SMSSpamCollection', sep='\t', names=['labels','message'])

#exploring the data
messages.groupby('labels').describe()

#add a new column called length to determine the length of the text
messages['length']=messages['message'].apply(len)

#text pre-processing
#removing punctuations
mess='Sample message! Notice : it has punctuations'
#string.punctuation
nopunc=[c for c in mess if c not in string.punctuation]
nopunc=''.join(nopunc)

stopwords.words('english')
nopunc.split()
clean_mess=[word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

#incorporating it into a function
def text_process(mess):
    nopunc=[char for char in mess if char not in string.punctuation]
    nopunc=''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

messages['message'].apply(text_process)

#converting the list of messages to tokens
#count how many times a word occurs in a message (term frequency)
#weight the count so that frequent tokens get lower weights (inverse document frequency)
#normalize the vector to unit length, to abstract the original text length

from sklearn.feature_extraction.text import CountVectorizer
bow_transformer=CountVectorizer(analyzer=text_process).fit(messages['message'])
print(len(bow_transformer.vocabulary_))
mess4=messages['message'][3]
print(mess4)
bow4=bow_transformer.transform([mess4])
print(bow4)
bow_transformer.get_feature_names()[9554]


#getting the bag of words for the entire message
message_bow=bow_transformer.transform(messages['message'])

#tfidf
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer=TfidfTransformer().fit(message_bow)

tfidf4=tfidf_transformer.transform(bow4)
print(tfidf4)

#converting the entire bag of word corpus into a tfidf corpus
messages_tfidf=tfidf_transformer.transform(message_bow)
print(messages_tfidf)
#training our model using naive bayes
from sklearn.naive_bayes import MultinomialNB
detect_model=MultinomialNB().fit(messages_tfidf,messages['labels'])



#splitting
from sklearn.cross_validation import train_test_split
msg_train, msg_test, label_train, label_test = train_test_split(messages['message'], messages['labels'], test_size=0.3)

#using piplines
from sklearn.pipeline import Pipeline
pipeline=Pipeline([
        ('bow', CountVectorizer(analyzer=text_process)),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB())
        ])
    

pipeline.fit(msg_train, label_train)

prediction=pipeline.predict(msg_test)

from sklearn.metrics import classification_report
print(classification_report(label_test, prediction))


    
