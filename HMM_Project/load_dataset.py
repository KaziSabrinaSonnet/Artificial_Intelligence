"""
function to load date form datatset.json in to python

How to use: Include this piece of code in your file:
    import load_dataset
    tagged_data = load_datatset.read_file('datatset.json')
"""

import json

def read_file(filename):
    with open(filename, 'rt') as infile:
            dataset = json.load(infile)

    words = []
    tags = []
    for num in dataset:
        # only load already tagged data
        cnt = 0
        for i in range(len(dataset[num])):
            if dataset[num][i][1] == 0: cnt += 1
        if cnt == len(dataset[num]): continue

        # add words and tags to word and tag list
        for i in range(len(dataset[num])):
            words.append(dataset[num][i][0])
            if dataset[num][i][1] == -1: tags.append('Negative')
            elif dataset[num][i][1] == 0: tags.append('Neutral')
            elif dataset[num][i][1] == 1: tags.append('Positive')   
        words.append('')
        tags.append('')
    return words, tags