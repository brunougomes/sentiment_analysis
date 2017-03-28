import json
import requests
import nltk
from nltk.tokenize import word_tokenize

import re, sys
import operator
from collections import Counter
from collections import defaultdict

from nltk import bigrams
from nltk.corpus import stopwords
import string

import pymongo
from pymongo import MongoClient

# TWITTER INFORMATION#
# user.screen_name,user.name,text,coordinates,place,geo,location,created_at,timestamp_ms,lang
# mongoexport --db rio_db --collection rio_collection --fieldFile D:\export\columns.txt --csv --out D:\export\rioresults.csv
# mongoexport --db rio2016_db --collection rio2016_collection --out D:\export\rioresults.json
# preprocessing

#emotes
emoticons_str = """
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

# emoji pattern
emoji_pattern = '[\U0001F300-\U0001F64F]'

# tokens especiais
regex_str = [
    emoticons_str,
    emoji_pattern,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r'(?:[\w_]+)', # other words
    r'\.\.\.', # tres pontos
    u'[U00010000-U0010ffff]',
    u'[uD800-uDBFF][uDC00-uDFFF]',
    '&gt;', # greater than
    '&lt;' # lower than
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE | re.UNICODE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE | re.UNICODE)

#stemming
stemmer = nltk.stem.RSLPStemmer()

def tokenize(s):
    tweet = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', 'URL', s)
    tweet = re.sub('[\s]+', ' ', tweet)
    tokens = tokens_re.findall(tweet)
    #stemming words
    #for i in range(len(tokens)):
    #    stemmed = stemmer.stem(tokens[i])
    #    if(stemmed != '?'):
    #        tokens[i] = stemmed

    return tokens

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if(lowercase):
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# pontuação e stopwords
punctuation = list(string.punctuation)
stop = stopwords.words('english') + stopwords.words('portuguese') + punctuation + ['RT', 'rt']

# mongodb
client = MongoClient('localhost', 27017)

#evento
db = client['rio2016_db']
collection = db['rio2016_collection']

# getTweepts in mongo db
tweets_iterator = collection.find()

for tweet in tweets_iterator:
    #preprocessamento
    tweet_tokens = preprocess(tweet['text'], True)
    print(tweet['text'])
    #print(tweet_tokens)

#Counter tokens
print(tweets_iterator.count())