import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

class IndexStanford:
    def __init__(self):
        # Dictionnaries to build
        self.D_terme_termeid = {}  # {term:termID}
        self.dico_docID = {}  # {doc:docID}
        self.D_terme_id_postings = {}  # {termID:docID postings}

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
        self.docID = 0
        self.termID = 0

        for i in range(0, 9):  # Browsing blocks
            print(i)
            path_temp = path + str(i) + "/"
            for root, dirs, files in os.walk(path_temp):
                for file in files:
                    filename = str(i) + file
                    self.dico_docID[self.docID] = filename

                    with open(path_temp + file, 'r') as f:

                        self.wordList = []

                        for line in f.readlines():
                            self.wordList += self.lineSplit(line)

                        self.wordList = self.removeStopWords(self.wordList)
                        self.wordList = self.lemmatisation(self.wordList)

                        for w in self.wordList:
                            if not w in self.D_terme_termeid.keys(): #Checking if the term already exists in the dictionnary
                                self.D_terme_termeid[w] = self.termID
                                self.D_terme_id_postings[self.termID] = [self.docID]
                                self.termID += 1
                            else:
                                self.D_terme_id_postings[self.D_terme_termeid[w]] += [self.docID]

                    self.docID += 1

    def get_termeid_postings(self, terme):
        if not isinstance(terme, str):
            raise TypeError("Le terme cherché doit être sous format chaîne de caractère")

        if terme in self.D_terme_termeid:
            return (self.D_terme_id_postings[self.D_terme_termeid[terme]])

        else:
            return []


# index = IndexStanford()
# index.indexConstruction("C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/pa1-data/")


