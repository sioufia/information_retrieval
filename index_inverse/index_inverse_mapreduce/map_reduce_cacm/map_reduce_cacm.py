from threading import Thread, Semaphore, Lock
import time
import nltk

from ...index_inverse_common.index_inverse_common import IndexInverseCommonCacm

class MapReduceCACM(IndexInverseCommonCacm):
    def __init__(self):
        IndexInverseCommonCacm.__init__(self)
        #self.dico_index = {}

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

        global term_termid
        term_termid = {}

        global current_termid
        current_termid = 0

        for docID in self.collection_dic.keys():
            documents += [(docID, self.collection_dic[docID])]
            #print(self.collection_dic[docID])



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
                    global term_termid
                    global current_termid
                    docID_temp = documents[0][0]

                    for word in documents[0][1]:
                        if word not in term_termid.keys():
                            term_termid[word] = current_termid
                            buffer += [(current_termid,docID_temp)]
                            current_termid += 1
                        else:
                            buffer += [(term_termid[word],docID_temp)]

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
                    #print(len(buffer))
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
        #self.dico_index = index  # {term:{docID:freq}}

        #index is under the format {termid:{docID:freq}} --> We format it to the format {termid:[[docid:freq]]} to fit the search method 
        self.D_terme_id_postings = {a:[[b,index[a][b]]for b in index[a].keys()] for a in index.keys()} 

        self.D_terme_termeid = term_termid

def constructmapred_index_CACM(collection_path, stopwords_path):
    start_time = time.time()
    a = MapReduceCACM()
    a.parserCacm(collection_path)
    a.tokenizerCacm()
    a.manage_tokens_collectionCacm(stopwords_path)
    a.mapreducer()
    a.weight_calculation_index()
    print("MapReduce construction for CACM index : %s seconds ---" % (time.time() - start_time))
    return a

if __name__ == "__main__":
    collection_path = input("What is the path of the CACM collection ? ")
    stopwords_path = input("What is the path of the Stopwords for CACM collection ? ")
    index = constructmapred_index_CACM(collection_path, stopwords_path)
    print(index)

