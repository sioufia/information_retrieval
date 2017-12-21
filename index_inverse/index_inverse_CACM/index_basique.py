def index_inverse(collection):
    """Method that generates the index of CACM. It returns 2 dictionnaries : 
    - D_terme_termeid : keys are the terms of the collection and values are the id of the terms
    - D_terme_id_postings : keys are the ids of the terms and values are the postings list. 
    A posting list is composed of element :  an element is a doc_id, and the weight of the term in the doc
    """
    D_terme_termeid = {}
    D_terme_id_postings = {}

    terme_id=0

    for doc in collection:
        for terme in collection[doc]:
            if terme not in D_terme_termeid.keys():
                D_terme_termeid[terme] = terme_id
                D_terme_id_postings[terme_id] =[]
                D_terme_id_postings[terme_id].append((doc)) 
                terme_id += 1

            elif doc not in D_terme_id_postings[D_terme_termeid[terme]]:
                D_terme_id_postings[D_terme_termeid[terme]].append(doc)

    return D_terme_termeid, D_terme_id_postings