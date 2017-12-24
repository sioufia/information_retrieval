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
        for terme in collection[doc]:
            if terme not in D_terme_termeid.keys():
                D_terme_termeid[terme] = terme_id
                D_terme_id_postings[terme_id] ={} #No solution found to avoid dictionary for postings if we want to stock the weight of the terms
                D_terme_id_postings[terme_id][doc] = 1 #Stock the frequency for the value first
                terme_id += 1
            
            #If the term_id already exists but this posting doc not
            elif doc not in D_terme_id_postings[D_terme_termeid[terme]].keys():
                D_terme_id_postings[D_terme_termeid[terme]][doc] = 1
            
            #If the posting for this term_id already exists
            else:
                D_terme_id_postings[D_terme_termeid[terme]][doc] += 1
    
    nd = weight_calculation(D_terme_id_postings, nb_doc)
                
    return D_terme_termeid, D_terme_id_postings

def weight_calculation(D_terme_id_postings, nb_doc):
    "Method that calculates the weight of each term in each doc"
    nd = {} # initialize doc weigh
    for t in D_terme_id_postings:
        idf_t = log((nb_doc/len(D_terme_id_postings[t])))

        for d in D_terme_id_postings[t]:
            #Calculate tf_t_d
            if D_terme_id_postings[t][d] != 0:
                tf_t_d = 1 + log(D_terme_id_postings[t][d])
            elif D_terme_id_postings[t][d] == 0:
                tf_t_d = 0
            
            #Calculate idf_t
            #Case when trying to make the index of request
            if idf_t !=0:
                D_terme_id_postings[t][d] = tf_t_d * idf_t # stock the weight not normalized
            elif idf_t == 0:
                D_terme_id_postings[t][d] = tf_t_d

            if d in nd:
                nd[d] += D_terme_id_postings[t][d]*D_terme_id_postings[t][d]
            else:
                nd[d] = D_terme_id_postings[t][d]*D_terme_id_postings[t][d]

    #Calculate the norm of the weight of each doc
    for doc in nd:
        if nd[doc] !=0:
            nd[doc] = 1/(sqrt(nd[doc]))
    
    #Normalize each weight
    for t in D_terme_id_postings:
        for d in D_terme_id_postings[t]:
            D_terme_id_postings[t][d] *= nd[d] # stock the weight normalized
    
    
            


    
            
    
                