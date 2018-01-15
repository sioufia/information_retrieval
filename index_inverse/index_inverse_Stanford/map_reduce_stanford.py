import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator
from threading import Thread, Semaphore, Lock
import os

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
wl = WordNetLemmatizer()

class mapReduceStanford:

    lock = Lock()

    def __init__(self,path):

        self.path = path

    def mapReducer(self):

        global documents
        documents = []

        global buffer
        buffer = []

        global docID
        docID = 1

        global index
        index = {}

        global dico_docID
        dico_docID = {}

        # Create the threads

        class CreateListDocuments(Thread):

            for i in range(0, 9):  # Browsing blocks
                print(i)
                path_temp = self.path + str(i) + "/"
                for root, dirs, files in os.walk(path_temp):  # Browsing files
                    for file in files:
                        doc = path_temp + file
                        docname = str(i) + file
                        documents += [(doc,docname)]

        class Mapper(Thread):

            lock = Lock()
            semaphore = Semaphore(5)

            def __init__(self):
                Thread.__init__(self)

            @staticmethod
            def lineSplit(line):  # Split a line of words into a list of words
                return line.split()

            # @staticmethod
            # def shuffle_order(tuple_list):
            #     a = sorted(tuple_list, key=operator.itemgetter(0))
            #     return a

            @staticmethod
            def removeStopWords(wordList):  # Remove stop words from a list of words
                wordList_filtered = [w for w in wordList if not w in stop_words]
                return wordList_filtered

            @staticmethod
            def lemmatisation(wordList):
                return list(map(wl.lemmatize, wordList))

            def run(self):
                while documents != []:

                    Mapper.semaphore.acquire(self)
                    Mapper.lock.acquire()

                    self.tuple_list = []

                    with open(documents[0][0], 'r') as f:

                        dico_docID[docID] = documents[0][1]

                        self.wordList = []

                        for line in f.readlines():
                            self.wordList += self.lineSplit(line)

                        self.wordList = self.removeStopWords(self.wordList)
                        self.wordList = self.lemmatisation(self.wordList)

                        for w in self.wordList:
                            self.tuple_list += (w, docID)

                        docID += 1
                        del documents[0]
                        buffer += self.tuple_list

                    Mapper.lock.release()
                    Mapper.semaphore.release()

        class Reducer(Thread):

            lock = Lock()
            semaphore = Semaphore(5)

            def __init__(self):
                Thread.__init__(self)

            def run(self):

                while buffer != []:

                    Reducer.semaphore.acquire(self)
                    Reducer.lock.acquire()
                    t = buffer[0]
                    if t(0) not in index.keys():
                        index[t(0)] = {}
                        index[t(0)][t(1)] = 1
                    else:
                        if t(1) not in index[t(0)].keys():
                            index[t(0)][t(1)] = 1
                        else:
                            index[t(0)][t(1)] += 1

                    Reducer.lock.release()
                    Reducer.semaphore.release()


        # Run threads

        self.createDocs = CreateListDocuments()
        self.map = Mapper()
        self.red = Reducer()

        self.createDocs.start()
        self.map.start()
        self.red.start()


        self.dico_docID = dico_docID  # {doc:docID}
        self.dico_index = index  # {term:{docID:freq}}



mapReduce = mapReduceStanford("C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/pa1-data (1)/pa1-data/")
mapReduce.mapReducer()
print(mapReduce.dico_index)













