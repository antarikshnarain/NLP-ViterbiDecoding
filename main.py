"""
Author: Antariksh Narain
Email: antariksh.cloud@gmail.com

This program reads data from train.txt and uses the data to predict 
the possible POS tag sequence for the strings in test.txt
"""
from collections import namedtuple

class ModelParameters:
    """
    Class to computer model parameters
        - pi -> initial probabilites
        - A -> Transition probabilities
        - B -> Emission probabilities
    """
    def __init__(self, input_file_name):
        self.lines = self._process_file(input_file_name)
        self.pi = dict()
        self.A = dict()
        self.B = dict()
        self.tokens = set()
        self.poss = set()
        self._process_data()
        
        # TODO: Print Processed tables
        self.__print(self.pi, self.poss, [])
        print("\n\n")
        self.__print(self.A, self.poss, self.poss)
        print("\n\n")
        self.__print(self.B, self.poss, self.tokens)
        print("\n\n")
    
    def __update_dictionary(self, dictionary: dict, value1: str, value2: str = None):
        if value2 == None:
            if dictionary.get(value1) == None:
                dictionary[value1] = 1
            else:
                dictionary[value1] += 1
        else:
            if dictionary.get(value1) == None:
                dictionary[value1] = dict()
            self.__update_dictionary(dictionary[value1], value2)

    def __normalize(self, dictionary: dict):
        total = sum(dictionary.values())
        for k in dictionary:
            dictionary[k] /= total

    def __print(self, dictionary: dict, seq1: list, seq2: list):
        if len(seq2) == 0:
            for val in seq1:
                if dictionary.get(val) == None:
                    print("0", end='\t')
                else:
                    print("%.2f"%dictionary[val], end='\t')
            print()
        else:
            print('',end='\t')
            print("\t".join(seq2))
            for v in seq1:
                print(v, end='\t')
                self.__print(dictionary[v], seq1=seq2, seq2=[])

    def _process_file(self, filename):
        file = open(filename, mode='r', encoding='utf-8')
        lines = []
        # TODO: Process tokens and pos tag pairs
        pair = namedtuple('TokenPOS', 'token pos')
        for line in file.readlines():
            new_line = []
            for word in line.split(' '):
                token, pos = word.split('/')
                new_line.append(pair(token=token.replace('\n',''), pos=pos.replace('\n','')))
            lines.append(new_line)
        file.close()
        return lines

    def _process_data(self):
        """
        Groups the data
        """
        for line in self.lines:
            # TODO: Update pi
            self.__update_dictionary(self.pi, line[0].pos)
            # TODO: Update Transition Prob. wrt to POS tag
            for i in range(1, len(line)):
                self.__update_dictionary(self.A, line[i-1].pos, line[i].pos)
            # TODO: Update Emission Prob.
            for token, pos in line:
                self.tokens.add(token)
                self.poss.add(pos)
                self.__update_dictionary(self.B, pos, token)
        
        # TODO: normalize dictionary values
        self.__normalize(self.pi)
        for k in self.A:
            self.__normalize(self.A[k])
        for k in self.B:
            self.__normalize(self.B[k])

    def ViterbiDecoding(self):
        pass

    def test(self, input_file_name):
        file = open(input_file_name, mode='r', encoding='utf-8')
        lines = file.readlines()
        for line in lines():
            line = line.replace('\n','')


        file.close()


if __name__ == "__main__":
    mp = ModelParameters("train.txt")