from math import *

class IndexInverseCommon:
    def __init__(self):
        self.D_terme_termeid = {}
        self.D_terme_id_postings = {}
        self.nb_doc = 1
        

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

def size_voc(self):
        """Method to return the size of the vocabulary"""
        return len(self.D_terme_id_postings.keys())

