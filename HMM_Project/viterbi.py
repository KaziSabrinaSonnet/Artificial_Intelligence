"""
demonstration of the Viterbi algorithm
"""

import numpy as np

class HmmStates:
    def __init__(self, name, adjstates, emissionprob):
        self.name = name # name of state
        self.adjs = adjstates # dictionary of adjacent states + transition probability
        self.ep = emissionprob # dictionary of emission probabilities

class VState:
    def __init__(self, hmmstate, prob):
        self.state = hmmstate
        self.p = prob

class Hmm(HmmStates):
    def __init__(self):
        """
        create HMM from data set
        genertated transition and emission lists
        """

        ## TODO: create the actual HMM

        self.hmm = [HmmStates('S', {'S': 0.8, 'R': 0.2}, {'H': 0.8, 'G': 0.2}),
            HmmStates('R', {'S': 0.4, 'R': 0.6}, {'H': 0.4, 'G': 0.6})] # dummy HMM for testing purpose

        # prior probabilities TODO: compute prior probabilities from HMM
        self.prior = {'S': 2/3, 'R': 1/3}
        

    def viterbi(self, observation):
        # compute prob of hidden states for first observed state
        ps_old = {} # most likely probabilities of current hidden state
        vseq = [None]*len(observation) # most likely sequence
        ps_max = 0
        for s in self.hmm:
            ps_old[s] = self.prior[s.name] * s.ep[observation[0]]
            if ps_old[s] > ps_max:
                vseq[0] = VState(s, ps_old[s])
                ps_max = ps_old[s]

        i = 1
        for o in observation[1:len(observation)]:
            ps_new = {}
            ps_max = 0
            for s in self.hmm:
                temp = 0
                for sp in ps_old:
                    if ps_old[sp] * sp.adjs[s.name] * s.ep[o] > temp: temp = ps_old[sp] * sp.adjs[s.name] * s.ep[o] #TODO fix this!!!!
                ps_new[s] = temp
                if temp > ps_max:
                    vseq[i] = VState(s, temp) # save state with highest probability
                    ps_max = temp
            ps_old = ps_new
            i += 1

        return vseq

hmm = Hmm()
viterby_seq = hmm.viterbi(['H', 'H', 'G', 'G', 'G', 'H'])
for i in range(len(viterby_seq)):
    print(viterby_seq[i].state.name + ' ' + str(viterby_seq[i].p))
#print(viterby_seq)

