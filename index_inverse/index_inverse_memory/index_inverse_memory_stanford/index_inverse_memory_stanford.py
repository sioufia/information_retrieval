from ...index_inverse_common.index_inverse_common import IndexInverseCommon

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

class IndexMemoryStanford(IndexInverseCommon):
    def __init__(self):
        # Dictionnaries to build
        IndexInverseCommon.__init__(self)
        self.dico_docID = {}  # {doc:docID}
        self.nb_doc = 0

        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.wl = WordNetLemmatizer()


    def removeStopWords(self,wordList): #Remove stop words from a list of words
        wordList_filtered = [w for w in wordList if not w in self.stop_words]
        return wordList_filtered

    @staticmethod
    def lineSplit(line): #Split a line of words into a list of words
        return line.split()

    def lemmatisation(self,wordList):
        return list(map(self.wl.lemmatize, wordList))

    def indexConstruction(self,path): #Construction of the index
        self.termID = 0
        temp_index = {}

        for i in range(0, 9):  # Browsing blocks
            print(i)
            path_temp = path + str(i) + "/"
            for root, dirs, files in os.walk(path_temp):
                for file in files:
                    filename = str(i) + file
                    self.dico_docID[self.nb_doc] = filename

                    with open(path_temp + file, 'r') as f:

                        self.wordList = []

                        for line in f.readlines():
                            self.wordList += self.lineSplit(line)

                        self.wordList = self.removeStopWords(self.wordList)
                        self.wordList = self.lemmatisation(self.wordList)

                        for w in self.wordList:
                            if not w in self.D_terme_termeid.keys(): #Checking if the term already exists in the dictionnary
                                self.D_terme_termeid[w] = self.termID
                                temp_index[self.termID] = {}
                                temp_index[self.termID][self.nb_doc] = 1
                                self.termID += 1
                            
                            #If the term_id already exists but this posting doc not
                            elif self.nb_doc not in temp_index[self.D_terme_termeid[w]].keys():
                                temp_index[self.D_terme_termeid[w]][self.nb_doc] = 1
                            
                            #If the posting for this term_id already exists
                            else:
                                temp_index[self.D_terme_termeid[w]][self.nb_doc] += 1

                    self.nb_doc += 1
        
        #index is under the format {termid:{docID:freq}} --> We format it to the format {termid:[[docid:freq]]} to fit the search method 
        self.D_terme_id_postings = {a:[[b,temp_index[a][b]]for b in temp_index[a].keys()] for a in temp_index.keys()} 

def constructmemory_index_Stanford(path):
    index = IndexMemoryStanford()
    index.indexConstruction(path)
    index.weight_calculation_index()
    return index



