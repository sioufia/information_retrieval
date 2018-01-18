import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator
from threading import Thread, Semaphore, Lock
import os
import time

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
wl = WordNetLemmatizer()

class mapReduceStanford:

    # lock = Lock()

    def __init__(self,path):

        self.path = path

    def mapReducer(self):

        global documents #List of documents to be treated
        documents = []
        # print(documents)

        global buffer #Buffer of documents that have been mapped but not reduced
        buffer = []

        global docID #Counting global docID
        docID = 1

        global index #Final index
        index = {}

        global dico_docID #Final dico for doc,docID
        dico_docID = {}

        global continuer
        continuer = True

        # Create the threads

        class CreateListDocuments(Thread):

            def __init__(self,path):
                Thread.__init__(self)
                self.path = path

            def run(self):
                for i in range(0, 9):  # Browsing blocks
                    print(i)
                    path_temp = self.path + str(i) + "/"
                    for root, dirs, files in os.walk(path_temp):  # Browsing files
                        for file in files:
                            doc = path_temp + file
                            docname = str(i) + file
                            global documents, docID
                            documents += [(doc,docname,docID)]
                            docID += 1

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

            # @staticmethod
            # def return_docID():
            #     return docID
            #
            # @staticmethod
            # def increment_docID():
            #     docID += 1

            # def return_buffer(a):
            #     buffer += [a]

            def run(self):
                while documents != []:

                    Mapper.semaphore.acquire(self)
                    Mapper.lock.acquire()

                    self.tuple_list = []

                    with open(documents[0][0], 'r') as f:

                        global dico_docID
                        dico_docID[documents[0][2]] = documents[0][1]

                        self.wordList = []

                        for line in f.readlines():
                            self.wordList += self.lineSplit(line)

                        self.wordList = self.removeStopWords(self.wordList)
                        self.wordList = self.lemmatisation(self.wordList)

                        for w in self.wordList:
                            self.tuple_list += [(w, documents[0][2])]

                        del documents[0]


                        global buffer
                        buffer += self.tuple_list
                        # print(len(buffer))


                    Mapper.lock.release()
                    Mapper.semaphore.release()



        class Reducer(Thread):

            lock = Lock()
            semaphore = Semaphore(5)

            def __init__(self):
                Thread.__init__(self)

            def run(self):

                while buffer != [] or continuer:

                    Reducer.semaphore.acquire(self)
                    Reducer.lock.acquire()
                    t = buffer[0]
                    print(t)

                    global index
                    if t[0] not in index.keys():
                        index[t[0]] = {}
                        index[t[0]][t[1]] = 1
                    else:
                        if t[1] not in index[t[0]].keys():
                            index[t[0]][t[1]] = 1
                        else:
                            index[t[0]][t[1]] += 1

                    del buffer[0]
                    print("yo" + str(len(buffer)))

                    Reducer.lock.release()
                    Reducer.semaphore.release()


        # Run threads

        self.createDocs = CreateListDocuments("C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/pa1-data (1)/pa1-data/")
        self.map = Mapper()
        self.red = Reducer()

        self.createDocs.start()
        time.sleep(3)
        self.map.start()
        time.sleep(3)
        self.red.start()

        #Wait for the mappers to finish
        self.map.join()

        continuer = False

        #Wait for the reducers to finish
        self.red.join()

        self.dico_docID = dico_docID  # {doc:docID}
        self.dico_index = index  # {term:{docID:freq}}



mapReduce = mapReduceStanford("C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/pa1-data (1)/pa1-data/")
mapReduce.mapReducer()
print(mapReduce.dico_index)













