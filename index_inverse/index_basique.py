def index_inverse(collection):
    """La collection est un dictionnaire avec pour clefs le numéro du document, et
    pour valeur le contenu du document. Cette fonction va générer un dictionnaire 
    avec pour clef chaque terme de la collection et pour valeur le numéro du document
    auquel le terme appartient.
    """
    D_terme_termeid = {}
    D_terme_id_postings = {}

    terme_id=0

    for doc in collection:
        for terme in collection[doc]:
            if terme not in D_terme_termeid.keys():
                D_terme_termeid[terme] = terme_id
                D_terme_id_postings[terme_id] =[]
                D_terme_id_postings[terme_id].append(doc)
                terme_id += 1
            else:
                terme_id_cours = D_terme_termeid[terme]
                D_terme_id_postings[terme_id_cours].append(doc)
    return D_terme_termeid, D_terme_id_postings