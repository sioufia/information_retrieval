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

    def __init__(self,path):
        self.path =  path #path to the stanford library location
        self.D_terme_termeid = {}
        self.D_terme_id_postings = {}

    def mapReducer(self):
        """Function to perform map reduce approach on stanford"""

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

        global continuer #This variable makes sure reducers do not stop if the buffer is empty but mappers are still working
        continuer = True

        global term_termid
        term_termid = {}

        global current_termid
        current_termid = 0

        # Create the threads
        class CreateListDocuments(Thread):
            """Thread to create a list of (doc path, docname, docID)"""
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
            """Thread to compute mapper part"""

            lock = Lock()
            semaphore = Semaphore(10)

            def __init__(self):
                Thread.__init__(self)

            @staticmethod
            def lineSplit(line):  # Split a line of words into a list of words
                return line.split()

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

                        global dico_docID
                        dico_docID[documents[0][2]] = documents[0][1]

                        self.wordList = []

                        for line in f.readlines():
                            self.wordList += self.lineSplit(line)

                        self.wordList = self.removeStopWords(self.wordList)
                        self.wordList = self.lemmatisation(self.wordList)

                        global term_termid
                        global current_termid
                        for w in self.wordList:
                            #if w not in term_termid.keys():
                                #term_termid[w] = current_termid
                            self.tuple_list += [(w, documents[0][2])]
                                #current_termid += 1
                            #else:
                                #self.tuple_list += [(term_termid[w], documents[0][2])]

                        del documents[0]


                        global buffer
                        buffer += self.tuple_list
                        # print(len(buffer))


                    Mapper.lock.release()
                    Mapper.semaphore.release()



        class Reducer(Thread):
            """Class to perform reducer part"""

            lock = Lock()
            semaphore = Semaphore(10)

            def __init__(self):
                Thread.__init__(self)

            def run(self):

                while buffer != [] or continuer:

                    Reducer.semaphore.acquire(self)
                    Reducer.lock.acquire()

                    t = buffer[0]

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
                    #print(len(buffer))

                    Reducer.lock.release()
                    Reducer.semaphore.release()


        # Run threads
        self.createDocs = CreateListDocuments("/Users/alexandresioufi/Documents/Projets infos/recherche/pa1-data/")
        self.map = Mapper()
        self.red = Reducer()

        # Start threads
        self.createDocs.start()
        time.sleep(3) #Let some time to fill the doc list
        self.map.start()
        time.sleep(3) #Let some time to fill the buffer
        self.red.start()

        #Wait for the mappers to finish
        self.map.join()
        print("OK")

        continuer = False

        #Wait for the reducers to finish
        self.red.join()

        self.dico_docID = dico_docID  # {doc:docID}
        self.dico_index = index  # {term:{docID:freq}}


def constructmapred_index_Stanford(collection_path):
    start_time = time.time()
    a = mapReduceStanford(collection_path)
    a.mapReducer()
    print("MapReduce construction for Stanford index : %s seconds ---" % (time.time() - start_time))
    return a

if __name__ == "__main__":
    collection_path = input("What is the path of the Stanford collection ? ") 
    index = constructmapred_index_Stanford(collection_path)
    print(index)













