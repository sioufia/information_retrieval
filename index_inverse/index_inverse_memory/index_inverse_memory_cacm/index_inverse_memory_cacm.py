import nltk
from math import *
from operator import itemgetter
import matplotlib.pyplot as plt
import time

from ...index_inverse_common.index_inverse_common import IndexInverseCommonCacm

class IndexCACMMemory(IndexInverseCommonCacm):
    def __init__(self, collection_dic={}):
        IndexInverseCommonCacm.__init__(self, collection_dic)
        self.nb_tokens = 0

    #def size_voc(self):
        #"""Method to return the size of the vocabulary"""
        #return len(self.D_terme_id_postings.keys())
    

    def index_inverse(self):
        """Method that generates the index of CACM. 
        It takes the doc collection as entry.
        It returns 2 dictionnaries : 
        - D_terme_termeid : keys are the terms of the collection and values are the id of the terms
        - D_terme_id_postings : keys are the ids of the terms and values are the postings list. 
        A posting list is composed of element :  an element is a doc_id, and the weight of the term in the doc
        """

        terme_id=0

        nd_list = {}

        temp_index = {}

        for doc in self.collection_dic:
            for terme in self.collection_dic[doc]:
                #Counting number tokens
                self.nb_tokens += 1
                #Updating index
                if terme not in self.D_terme_termeid.keys():
                    self.D_terme_termeid[terme] = terme_id
                    temp_index[terme_id] ={} #No solution found to avoid dictionary for postings if we want to stock the weight of the terms
                    temp_index[terme_id][doc] = 1 #Stock the frequency for the value first
                    terme_id += 1
                
                #If the term_id already exists but this posting doc not
                elif doc not in temp_index[self.D_terme_termeid[terme]].keys():
                    temp_index[self.D_terme_termeid[terme]][doc] = 1
                
                #If the posting for this term_id already exists
                else:
                    temp_index[self.D_terme_termeid[terme]][doc] += 1
            
            self.nb_doc += 1
        
        self.D_terme_id_postings = {a:[[b,temp_index[a][b]]for b in temp_index[a].keys()] for a in temp_index.keys()} 


    
def constructmemory_index_CACM(collection_path, stopwords_path):
    start_time = time.time()
    index = IndexCACMMemory()
    index.parserCacm(collection_path)
    index.tokenizerCacm()
    index.manage_tokens_collectionCacm(stopwords_path)
    index.index_inverse()
    index.weight_calculation_index()
    print("InMemory construction for CACM index : %s seconds ---" % (time.time() - start_time))
    return index

if __name__ == "__main__":
    print('main memory')
    collection_path = input("What is the path of the CACM collection ? ")
    stopwords_path = input("What is the path of the Stopwords for CACM collection ? ")
    index = constructmemory_index_CACM(collection_path, stopwords_path)
    





    
            
    
    




        
