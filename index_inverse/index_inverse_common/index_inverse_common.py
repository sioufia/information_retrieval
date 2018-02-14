from math import *
import matplotlib.pyplot as plt
import nltk
from operator import itemgetter

class IndexInverseCommon:
    def __init__(self):
        self.D_terme_termeid = {}
        self.D_terme_id_postings = {}
        self.nb_doc = 1
        self.collection_dic = {}
        
    def weight_calculation_index(self):
        "Method that calculates the weight of each term in each doc of the inverse doc."
        nd = {} # initialize doc weigh
        for t in self.D_terme_id_postings:
            idf_t = log((self.nb_doc/len(self.D_terme_id_postings[t])))

            for d in self.D_terme_id_postings[t]:
                #d[0] is the docid
                #d[1] is the frequency of the term in this docid
                #Calculate tf_t_d
                if d[1] != 0:
                    tf_t_d = 1 + log(d[1])
                elif d[1] == 0:
                    tf_t_d = 0
                
                #Calculate idf_t
                #Case when trying to make the index of request
                if idf_t !=0:
                    d[1] = tf_t_d * idf_t # stock the weight not normalized
                elif idf_t == 0:
                    d[1] = tf_t_d

                if d[0] in nd:
                    nd[d[0]] += d[1]*d[1]
                else:
                    nd[d[0]] = d[1]*d[1]

        #Calculate the norm of the weight of each doc
        for doc in nd:
            if nd[doc] !=0:
                nd[doc] = 1/(sqrt(nd[doc]))
        
        #Normalize each weight
        for t in self.D_terme_id_postings:
            for d in self.D_terme_id_postings[t]:
                d[1] *= nd[d[0]] # stock the weight normalized

    def rang_freq(self):
        """"Method that computes the range frequency plot for all tokens in collection"""
        # Retrieving tokens and frequencies
        l = []
        print(self.D_terme_id_postings)
        for k, v in self.D_terme_id_postings.items():
            f = 0
            for t in v:
                f += t[1]
            l += [(k, f)]

        # Sorting by frequency
        l = sorted(l, key=itemgetter(1), reverse=True)

        # Constructino freq and range lists
        rang = []
        freq = []
        rang_log = []
        freq_log = []
        for i in range(len(l)):
            rang += [i + 1]
            freq += [l[i][1]]
            rang_log += [log(i+1,10)]
            freq_log += [log(l[i][1],10)]

        plt.scatter(rang, freq)
        plt.title('Range vs Frequency')
        plt.xlabel('Range')
        plt.ylabel('Frequency')
        plt.show()

        plt.scatter(rang_log, freq_log)
        plt.title('Log Range vs Log Frequency')
        plt.xlabel('Log Range')
        plt.ylabel('Log Frequency')
        plt.show()

    def size_voc(self):
        """Method to return the size of the vocabulary"""
        return len(self.D_terme_id_postings.keys())

class IndexInverseCommonCacm(IndexInverseCommon):
    def __init__(self, collection_dic = {}):
        IndexInverseCommon.__init__(self)
        #collection_dic is a dictionnary with the doc number as key and the content of the doc as value
        self.collection_dic = collection_dic
    
    def parserCacm(self,filename):
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
    
    def tokenizerCacm(self):
        """Method that tokenizes the content of the attribute 
           collection_dic """
        for doc in self.collection_dic:
            self.collection_dic[doc] = nltk.word_tokenize(self.collection_dic[doc])
    
    @staticmethod
    def stock_stopwords_listCacm(filename):
        """Method that takes a file with stopwords and return it as a list"""
        L = []
        with open(filename, "r") as f:
            for word in f:
                L.append(word[:-1])
            f.close()
        return L
    
    def manage_tokens_collectionCacm(self, stopwords_file):
        """Method that removes the stopwords of each doc in the 
           collection. It removes the punctuation too."""
        stopwords = IndexInverseCommonCacm.stock_stopwords_listCacm(stopwords_file)
        collection_without_stopwords = {}
        for elt in self.collection_dic:
            collection_without_stopwords[elt] = []
            for token in self.collection_dic[elt]:
                if (token.lower() not in stopwords) and (token.lower() not in [",",".",";",")","(","?","\t","\\"]):
                    collection_without_stopwords[elt].append(token.lower())
        self.collection_dic = collection_without_stopwords
        self.nb_doc = len(self.collection_dic)
    
    def half_collection(self):
        """Method to use half the collection for cacm"""
        self.half_collection_dic = {}
        n = len(self.collection_dic.keys())
        i=0
        for k,v in self.collection_dic.items():
            if i>n/2:
                break
            self.half_collection_dic[k]=v
            i += 1
        self.collection_dic = self.half_collection_dic
    
    # def rang_freq(self):
    #     """"Method that computes the range frequency plot for all tokens in collection"""
    #     #Retrieving tokens and frequencies
    #     l = []
    #     for k,v in self.collection_dic.items():
    #         l += [(k,len(v))]
    #
    #     #Sorting by frequency
    #     l = sorted(l, key = itemgetter(1), reverse=True)
    #
    #     #Constructino freq and range lists
    #     rang = []
    #     freq = []
    #     for i in range(len(l)):
    #         rang += [i+1]
    #         freq += [l[i][1]]
    #
    #     plt.scatter(rang, freq)
    #     plt.title('Range vs Frequency')
    #     plt.xlabel('Range')
    #     plt.ylabel('Frequency')
    #     plt.show()


