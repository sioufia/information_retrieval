import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator
import os

class mapReduceStanford:
    def __init__(self):

        self.dico_docID = {}  # {doc:docID}
        self.dico_index = {}  # {term:{docID:freq}}


        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.wl = WordNetLemmatizer()


    @staticmethod
    def lineSplit(line):  # Split a line of words into a list of words
        return line.split()

    @staticmethod
    def shuffle_order(tuple_list):
        a = sorted(tuple_list, key=operator.itemgetter(0))
        return a



    def removeStopWords(self,wordList): #Remove stop words from a list of words
        wordList_filtered = [w for w in wordList if not w in self.stop_words]
        return wordList_filtered

    def lemmatisation(self,wordList):
        return list(map(self.wl.lemmatize, wordList))


    def mapper(self,doc,docID):
        tuple_list = []
        with open(doc, 'r') as f:

            self.wordList = []

            for line in f.readlines():
                self.wordList += self.lineSplit(line)

            self.wordList = self.removeStopWords(self.wordList)
            self.wordList = self.lemmatisation(self.wordList)

            for w in self.wordList:
                tuple_list += (w,docID)

        return tuple_list




    def reducer(self,tuple_list):

        for t in tuple_list:
            if t(0) not in self.dico_index.keys():
                self.dico_index[t(0)] = {}
                self.dico_index[t(0)][t(1)] = 1
            else:
                if t(1) not in self.dico_index[t(0)].keys():
                    self.dico_index[t(0)][t(1)] = 1
                else:
                    self.dico_index[t(0)][t(1)] += 1




