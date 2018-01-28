import nltk
from math import *
from operator import itemgetter
import matplotlib.pyplot as plt

class ConstructionIndex():
    def __init__(self, collection_dic = {}):
        #collection_dic is a dictionnary with the doc number as key and the content of the doc as value
        self.collection_dic = collection_dic 
        self.D_terme_termeid = {}
        self.D_terme_id_postings = {}
        self.nb_tokens = 0

    #def size_voc(self):
        #"""Method to return the size of the vocabulary"""
        #return len(self.D_terme_id_postings.keys())
    
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
        stopwords = ConstructionIndex.stock_stopwords_list(stopwords_file)
        collection_without_stopwords = {}
        for elt in self.collection_dic:
            collection_without_stopwords[elt] = []
            for token in self.collection_dic[elt]:
                if (token.lower() not in stopwords) and (token.lower() not in [",",".",";",")","(","?","\t","\\"]):
                    collection_without_stopwords[elt].append(token.lower())
        self.collection_dic = collection_without_stopwords

    def index_inverse(self):
        """Method that generates the index of CACM. 
        It takes the doc collection as entry.
        It returns 2 dictionnaries : 
        - D_terme_termeid : keys are the terms of the collection and values are the id of the terms
        - D_terme_id_postings : keys are the ids of the terms and values are the postings list. 
        A posting list is composed of element :  an element is a doc_id, and the weight of the term in the doc
        """

        terme_id=0

        nb_doc = 0

        nd_list = {}

        for doc in self.collection_dic:
            nb_doc += 1
            for terme in self.collection_dic[doc]:
                #Counting number tokens
                self.nb_tokens += 1
                #Updating index
                if terme not in self.D_terme_termeid.keys():
                    self.D_terme_termeid[terme] = terme_id
                    self.D_terme_id_postings[terme_id] ={} #No solution found to avoid dictionary for postings if we want to stock the weight of the terms
                    self.D_terme_id_postings[terme_id][doc] = 1 #Stock the frequency for the value first
                    terme_id += 1
                
                #If the term_id already exists but this posting doc not
                elif doc not in self.D_terme_id_postings[self.D_terme_termeid[terme]].keys():
                    self.D_terme_id_postings[self.D_terme_termeid[terme]][doc] = 1
                
                #If the posting for this term_id already exists
                else:
                    self.D_terme_id_postings[self.D_terme_termeid[terme]][doc] += 1
        
        return nb_doc

    def weight_calculation_index(self, nb_doc):
        "Method that calculates the weight of each term in each doc of the inverse doc"
        nd = {} # initialize doc weigh
        for t in self.D_terme_id_postings:
            idf_t = log((nb_doc/len(self.D_terme_id_postings[t])))

            for d in self.D_terme_id_postings[t]:
                #Calculate tf_t_d
                if self.D_terme_id_postings[t][d] != 0:
                    tf_t_d = 1 + log(self.D_terme_id_postings[t][d])
                elif self.D_terme_id_postings[t][d] == 0:
                    tf_t_d = 0
                
                #Calculate idf_t
                #Case when trying to make the index of request
                if idf_t !=0:
                    self.D_terme_id_postings[t][d] = tf_t_d * idf_t # stock the weight not normalized
                elif idf_t == 0:
                    self.D_terme_id_postings[t][d] = tf_t_d

                if d in nd:
                    nd[d] += self.D_terme_id_postings[t][d]*self.D_terme_id_postings[t][d]
                else:
                    nd[d] = self.D_terme_id_postings[t][d]*self.D_terme_id_postings[t][d]

        #Calculate the norm of the weight of each doc
        for doc in nd:
            if nd[doc] !=0:
                nd[doc] = 1/(sqrt(nd[doc]))
        
        #Normalize each weight
        for t in self.D_terme_id_postings:
            for d in self.D_terme_id_postings[t]:
                self.D_terme_id_postings[t][d] *= nd[d] # stock the weight normalized

    def rang_freq(self):
        """"Method that computes the range frequency plot for all tokens in collection"""
        #Retrieving tokens and frequencies
        l = []
        for k,v in self.collection_dic.items():
            l += [(k,len(v))]

        #Sorting by frequency
        l = sorted(l, key = itemgetter(1), reverse=True)

        #Constructino freq and range lists
        rang = []
        freq = []
        for i in range(len(l)):
            rang += [i+1]
            freq += [l[i][1]]

        print(len(rang))
        print(len(freq))
        plt.scatter(rang, freq)
        plt.title('Range vs Frequency')
        plt.xlabel('Range')
        plt.ylabel('Frequency')
        plt.show()


class ConstructionIndexCACM(ConstructionIndex):
    """Class for the construction of CACM index"""

    def __init__(self):
        ConstructionIndex.__init__(self)
    
    def parser(self, filename):
        """Method that takes a file with several documents as entry.
           It updates the collection_dic attribute with the doc number as key, and the content
           of the doc as value"""
        
        with open(filename, "r") as f:
            doc_number = '0'
            doc_section = '0'
            section_list = [".B",".A",".N",".X",".C",".I",".T",".W",".K"]
            for line in f:
                if line[:2] in section_list:
                    doc_section = str(line[:2])
                    if line[:2] == ".I":
                        doc_number = (str(line[3:]))[:-1]
                        self.collection_dic[doc_number] = "" 
                elif doc_section in [".I",".T",".W",".K"]:
                    self.collection_dic[doc_number] += " " + line[:-1]


    def half_collection(self):
        """Method to use half the collection"""
        self.half_collection_dic = {}
        n = len(self.collection_dic.keys())
        i=0
        for k,v in self.collection_dic.items():
            if i>n/2:
                break
            self.half_collection_dic[k]=v
            i += 1
        self.collection_dic = self.half_collection_dic


    
            
    
    




        
