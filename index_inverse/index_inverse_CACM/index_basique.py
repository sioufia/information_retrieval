from math import *

def index_inverse(collection):
    """Method that generates the index of CACM. It returns 2 dictionnaries : 
    - D_terme_termeid : keys are the terms of the collection and values are the id of the terms
    - D_terme_id_postings : keys are the ids of the terms and values are the postings list. 
    A posting list is composed of element :  an element is a doc_id, and the weight of the term in the doc
    """
    D_terme_termeid = {}
    D_terme_id_postings = {}

    terme_id=0

    nb_doc = 0

    nd_list = {}

    for doc in collection:
        nb_doc += 1
        nd = 0 # initialize doc weigh
        for terme in collection[doc]:
            if terme not in D_terme_termeid.keys():
                D_terme_termeid[terme] = terme_id
                D_terme_id_postings[terme_id] ={} #No solution found to avoid dictionary for postings if we want to stock the weight of the terms
                D_terme_id_postings[terme_id][doc] = 1 #Stock the frequency for the value first
                terme_id += 1

            elif doc not in D_terme_id_postings[D_terme_termeid[terme]].keys():
                D_terme_id_postings[D_terme_termeid[terme]][doc] = 1
            
            else:
                D_terme_id_postings[D_terme_termeid[terme]][doc] += 1
    
    weight_calculation(D_terme_id_postings, nb_doc)
                
    return D_terme_termeid, D_terme_id_postings

def weight_calculation(D_terme_id_postings, nb_doc):
    "Method that calculates the weight of each term in each doc"
    nd = {} # initialize doc weigh
    for t in D_terme_id_postings:
        idf_t = log((nb_doc/len(D_terme_id_postings[t])))
        for d in D_terme_id_postings[t]:
            tf_t_d = 1 + log(D_terme_id_postings[t][d])
            D_terme_id_postings[t][d] = tf_t_d * idf_t # stock the weight not normalized
            if d in nd:
                nd[d] += tf_t_d * idf_t
            else:
                nd[d] = tf_t_d * idf_t
    
    for doc in nd:
        nd[doc] = 1/(sqrt(nd[doc]))
    
    for t in D_terme_id_postings:
        for d in D_terme_id_postings[t]:
            D_terme_id_postings[t][d] *= nd[d] # stock the weight normalized
    
            


    
            
    
                