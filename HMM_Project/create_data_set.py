"""
create_data_set.py creates a untaged dataset from the raw data in Restaurant_reviews.csv.
The output is a json file where the tags can easily be added.
"""

import numpy as np
import json
import pandas as pd 
import re
import os
import io
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#importing raw data 
raw_data = pd.read_csv('Restaurant_Reviews.csv', delimiter = '\t', quoting= 3)

# remove certain words from stopwords list
to_remove = ['but', 'very', 'out', 'most', 'off', 'below', 'nor', 'more', 'down', 'above',
    'up', 'any', 'under', 'too', 'few', 'against',  'no', 'not', 'just', 'only']
new_stopwords = set(stopwords.words('english')).difference(to_remove)

#cleaning tests 
data_dct = {}
for i in range(0, 1000):    
    dataset = []
    review= re.sub('[^a-zA-Z]',' ', raw_data['Review'][i])
    review= review.lower()
    review = review.split()
    ps = PorterStemmer()
    review= [ps.stem(word) for word in review if not word in new_stopwords]
    if len(review) <= 20:
        for k in range(len(review)):
            dataset.append([review[k], 0])
    data_dct[i] = dataset

if os.path.isfile('dataset.json'):
        # checks if file exSists
        print ("File exists already exists")
else:
    print ("creating file...")
    with open('dataset.json', 'wt') as outfile:
        json.dump(data_dct, outfile, indent=4)


