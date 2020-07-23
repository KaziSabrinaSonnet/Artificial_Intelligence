#%%
"""Importing the packages""" 
import collections
import sys
from collections import Counter
import json 

#%%
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
#%%
def transition_probabilities(words):
	""" Generates a morkov dictionary from a list of states. The dictionary maps a state to a dictionary of its neighbors and their probabilities.
	"""
	tp_dictionary = collections.defaultdict(list)
	for i in range(len(words) - 1):
		word, neighbor = words[i], words[i+1]
		tp_dictionary[word].append(neighbor)
	return {word: probabilities_dict(neighbors) for word, neighbors in tp_dictionary.items()}

def emission_probabilities(pairs):
	""" Generates a dictionary of emission probabilities from a list of pairs of HMM states (tags) and their obsevations (words).
	"""
	em_dictionary = collections.defaultdict(list)
	for state, emission in pairs:
		em_dictionary[state].append(emission)
	return {state: probabilities_dict(emissions) for state, emissions in em_dictionary.items()}

def joint_probabilities(pairs):
    """From a sequence of state and observations finds out the probability of most likely sequence.
    """
    track_list= []
    i= 0
    for state, observation in pairs:
        if observation != '':
            if any(state in sublist for sublist in track_list):
                s= max(sublist for sublist in track_list if state in sublist)
                a= s[:]
                a.append(observation)
                track_list.append(a)
            else:
                track_list.append([state, observation])
    c = collections.defaultdict(int)
    for value in track_list:
        c[tuple(value)]+= 1
    return {key: count * 1.0 / len(track_list) for key, count in c.items()}


def probabilities_dict(list):
	""" Helper function that generates a dictionary of probabilities from a list.
	"""
	counts = collections.defaultdict(int)
	for value in list:
		counts[value] += 1
	return {key: count * 1.0 / len(list) for key, count in counts.items()}

#%%
def train_hmm(filename):
    """ Trains a hidden markov model(resturant review) with data from a text file. Returns transition and emission probabilities as a dictionary
	"""
    words, tags = read_file(filename)
    jp= joint_probabilities(zip(tags, words))
    tp = transition_probabilities(tags)
    ep = emission_probabilities(zip(tags, words))
    return jp, tp, ep
#%%
def forward_algorithm(sentence, jp, tp, ep): 
    """
    
    
    to be continued.......
   
   
    """

#%%