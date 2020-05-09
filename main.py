"""
Author: Antariksh Narain
Email: antariksh.cloud@gmail.com

This program reads data from train.txt and uses the data to predict 
the possible POS tag sequence for the strings in test.txt
"""
from collections import namedtuple
import numpy as np

class ModelParameters:
    """
    Class to computer model parameters
        - pi -> initial probabilites
        - A -> Transition probabilities
        - B -> Emission probabilities
    """
    def __init__(self, input_file_name):
        self.tokens = set()
        self.poss = set()
        self.lines = self._process_file(input_file_name)
        self.pi = np.zeros((len(self.poss)))
        self.A = np.zeros((len(self.poss), len(self.poss)))
        self.B = np.zeros((len(self.tokens), len(self.poss)))
        self.tokens = list(self.tokens)
        self.poss = list(self.poss)
        self._process_data()

        print(self.poss)
        print(self.pi)
        print(self.A)
        print(self.B)    

    def _process_file(self, filename):
        file = open(filename, mode='r', encoding='utf-8')
        lines = []
        # TODO: Process tokens and pos tag pairs
        pair = namedtuple('TokenPOS', 'token pos')
        for line in file.readlines():
            line = line.replace('\n','')
            new_line = []
            for word in line.split(' '):
                token, pos = word.split('/')
                self.tokens.add(token)
                self.poss.add(pos)
                new_line.append(pair(token=token, pos=pos))
            lines.append(new_line)
        file.close()
        return lines

    def _process_data(self):
        """
        Groups the data 
        """
        for line in self.lines:
            # TODO: Update pi
            self.pi[self.poss.index(line[0].pos)] += 1
            
            # TODO: Update Transition Prob. wrt to POS tag
            for i in range(1, len(line)):
                self.A[self.poss.index(line[i-1].pos), self.poss.index(line[i].pos)] += 1
            
            # TODO: Update Emission Prob.
            for token, pos in line:
                self.B[self.tokens.index(token), self.poss.index(pos)] += 1
        
        # TODO: normalize dictionary values
        self.pi /= np.sum(self.pi, axis = 0)
        self.A /= np.sum(self.A, axis=1, keepdims=True)
        print(self.B)
        self.B /= np.sum(self.B, axis=0, keepdims=True)


    def ViterbiDecoding(self, idx):
        # TODO: create 2-D matrix for Dynamic Programming
        dp_mat = np.zeros((len(self.poss), len(idx)))
        dp_mat[:,0] = self.pi * self.B[idx[0],:]
        print(self.poss)
        #print(dp_mat)
        for i in range(1,len(idx)):
            lst = np.multiply(self.A, dp_mat[:,i-1].reshape((dp_mat[:,i-1].size, 1)))
            lst2 = self.B[idx[i],:] * lst
            dp_mat[:,i] = np.max(lst2, axis=0)
        #    print(dp_mat)

        print(dp_mat)
        # TODO: Print sequence
        l = np.argmax(dp_mat, axis=0)
        print([self.poss[p] for p in l])

    def test(self, input_file_name):
        file = open(input_file_name, mode='r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            line = line.replace('\n','')
            idx = [self.tokens.index(word) for word in line.split(' ')]
            print(self.B[idx,:])
            print(line)
            self.ViterbiDecoding(idx)
        file.close()


if __name__ == "__main__":
    mp = ModelParameters("train.txt")
    mp.test("test.txt")
    