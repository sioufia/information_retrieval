import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
from struct import pack, unpack



class IndexStanford:
    def __init__(self):
        # Dictionnaries to build
        self.dico_termID = {}  # {term:termID}
        self.dico_docID = {}  # {doc:docID}
        self.dico_index = {}  # {termID:docID}

        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.wl = WordNetLemmatizer()



    def removeStopWords(self,wordList): #Remove stop words from a list of words
        wordList_filtered = [w for w in wordList if not w in self.stop_words]
        return wordList_filtered

    def lineSplit(self,line): #Split a line of words into a list of words
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
                            if not w in self.dico_termID.keys(): #Checking if the term already exists in the dictionnary
                                self.dico_termID[w] = self.termID
                                self.dico_index[self.termID] = [self.docID]
                                self.termID += 1
                            else:
                                self.dico_index[self.dico_termID[w]] += [self.docID]

                    self.docID += 1

class IndexStanfordCompressed(IndexStanford):
    def __init__(self):
        IndexStanford.__init__(self)
    
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
                            if not w in self.dico_termID.keys(): #Checking if the term already exists in the dictionnary
                                self.dico_termID[w] = self.termID
                                self.dico_index[self.termID] = []
                                self.dico_index[self.termID].append(self.docID)
                                self.termID += 1
                            
                            else:
                                previous_doc_id = self.docID - sum(self.dico_index[self.dico_termID[w]])#Use of the sum function - to be optimized
                                #Check if there is a doublon of the term in the current doc
                                if previous_doc_id !=0:
                                    self.dico_index[self.dico_termID[w]].append(previous_doc_id)

                    self.docID += 1
        
        #Loop to encode with variable bytes the doc differences
        for termID in self.dico_index:
            for doc in self.dico_index[termID]:
                doc = vb_encode(doc)
    
    def get_termeid_postings(self, term):
        if not isinstance(term, str):
            raise TypeError("Le terme cherché doit être sous format chaîne de caractère")
        
        if term in self.dico_termID:
            postings = []
            postings_bytes = self.dico_index[self.dico_termID[term]]
            for vb_doc in postings_bytes:
                doc = vb_decode(vb_doc)
                if len(postings) == 0:
                    postings.append(doc)
                else:
                    postings.append(doc + postings[-1])
            return postings

        else:
            return []

def vb_encode(number):
    bytes = []
    c = "1"
    while True:
        if number < 128:
            binary_number = "{0:b}".format(number)
            if len(binary_number) < 7:
                binary_number = "0"*(7 - len(binary_number)) + binary_number    
            bytes = [(c + binary_number).encode('utf-8')] + bytes
            break
        else:
            binary_number = "{0:b}".format(number % 128)
            if len(binary_number) < 7:
                binary_number = "0"*(7 - len(binary_number)) + binary_number 
            bytes = [(c + binary_number).encode('utf-8')] + bytes
            number = number // 128
            c = "0"
    return bytes
    
    

def vb_decode(bytestream):
    n = 0
    numbers = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
            numbers.append(n)
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers

    



#index = IndexStanford()
#index.indexConstruction("/Users/alexandresioufi/Documents/Projets infos/recherche/pa1-data/")

#index_compressed = IndexStanfordCompressed()
#index_compressed.indexConstruction("/Users/alexandresioufi/Documents/Projets infos/recherche/pa1-data/")


