from vaisdemo.Truecaser import *
import pickle
import os
import time
import string

class MyTrueCaser():
    def __init__(self):
        self.uniDist = None
        self.backwardBiDist = None
        self.forwardBiDist = None
        self.trigramDist = None
        self.wordCasingLookup = None

    def evaluateTrueCaser(self, sentence):
        if not self.uniDist:
            # print("TrueCaser model is not loaded. Skip!")
            return sentence
        correctTokens = 0
        totalTokens = 0

        tokensCorrect = sentence.lower().split()
        tokens = [token for token in tokensCorrect]
        tokensTrueCase = getTrueCase(tokens, 'title', self.wordCasingLookup, self.uniDist, self.backwardBiDist, self.forwardBiDist, self.trigramDist)

        return " ".join(tokensTrueCase)

    def load_model(self):
        time.sleep(5)
        root_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_dir, 'distributions.obj')
        if os.path.exists(file_path):
            f = open(file_path, 'rb')
            self.wordCasingLookup = pickle.load(f)
            self.uniDist = pickle.load(f)
            self.backwardBiDist = pickle.load(f)
            self.forwardBiDist = pickle.load(f)
            # trigramDist = pickle.load(f)
            # trigramDist = None
            f.close()
