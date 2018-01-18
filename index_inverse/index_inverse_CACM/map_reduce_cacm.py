from threading import Thread, Semaphore, Lock
import time
import nltk

class MapReduceCACM:
    def __init__(self):

        self.collection_dic = {}
        self.D_terme_termeid = {}
        self.D_terme_id_postings = {}
        self.dico_index = {}


    def parser(self, filename):
        """Method that takes a file with several documents as entry.
           It updates the collection_dic attribute with the doc number as key, and the content
           of the doc as value"""

        with open(filename, "r") as f:
            doc_number = '0'
            doc_section = '0'
            section_list = [".B", ".A", ".N", ".X", ".C", ".I", ".T", ".W", ".K"]
            for line in f:
                if line[:2] in section_list:
                    doc_section = str(line[:2])
                    if line[:2] == ".I":
                        doc_number = int((str(line[3:]))[:-1])
                        self.collection_dic[doc_number] = ""
                elif doc_section in [".I", ".T", ".W", ".K"]:
                    self.collection_dic[doc_number] += " " + line[:-1]

    def segmenter(self):
        """Method that tokenizes the content of the attribute
           collection_dic """
        for doc in self.collection_dic:
            self.collection_dic[doc] = nltk.word_tokenize(self.collection_dic[doc])

    @classmethod
    def stock_stopwords_list(cls, filename):
        """Method that takes a file with stopwords and return it as a list"""
        L = []
        with open(filename, "r") as f:
            for word in f:
                L.append(word[:-1])
            f.close()
        return L

    def traiter_tokens_collection(self, stopwords_file):
        """Method that removes the stopwords of each doc in the
           collection. It removes the punctuation too."""
        stopwords = MapReduceCACM.stock_stopwords_list(stopwords_file)
        collection_without_stopwords = {}
        for elt in self.collection_dic:
            collection_without_stopwords[elt] = []
            for token in self.collection_dic[elt]:
                if (token.lower() not in stopwords) and (token.lower() not in [",", ".", ";", ")", "(", "?", "\t", "\\"]):
                    collection_without_stopwords[elt].append(token.lower())
        self.collection_dic = collection_without_stopwords



    def mapreducer(self):
        """Function to compute map reduce approach"""

        global documents
        documents = []

        global buffer  # Buffer of documents that have been mapped but not reduced
        buffer = []

        global index  # Final index
        index = {}

        global dico_docID  # Final dico for doc,docID
        dico_docID = {}

        global continuer
        continuer = True

        for docID in self.collection_dic.keys():
            documents += [(docID, self.collection_dic[docID])]
            print(self.collection_dic[docID])



        class Mapper(Thread):

            lock = Lock()
            semaphore = Semaphore(5)

            def __init__(self):
                Thread.__init__(self)


            def run(self):
                while documents != []:

                    Mapper.semaphore.acquire(self)
                    Mapper.lock.acquire()

                    global buffer
                    docID_temp = documents[0][0]

                    for word in documents[0][1]:
                        buffer += [(word,docID_temp)]

                    del documents[0]
                    Mapper.lock.release()
                    Mapper.semaphore.release()

        class Reducer(Thread):
            lock = Lock()
            semaphore = Semaphore(5)

            def __init__(self):
                Thread.__init__(self)

            def run(self):
                while buffer != [] or continuer == True:

                    Reducer.semaphore.acquire(self)
                    Reducer.lock.acquire()
                    t = buffer[0]
                    print(len(buffer))
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

                    Reducer.lock.release()
                    Reducer.semaphore.release()

        self.map = Mapper()
        self.red = Reducer()


        self.map.start()
        time.sleep(3)
        self.red.start()

        # Wait for the mappers to finish
        self.map.join()

        continuer = False

        # Wait for the reducers to finish
        self.red.join()


        # self.dico_docID = dico_docID  # {doc:docID}
        self.dico_index = index  # {term:{docID:freq}}


a = MapReduceCACM()
a.parser("C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/riproject/CACM/cacm.all")
a.segmenter()
a.traiter_tokens_collection("C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/riproject/CACM/common_words")
a.mapreducer()
print(a.dico_index)

