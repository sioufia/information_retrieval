from index_inverse.index_inverse_CACM.main import *
#from index_inverse.index_inverse_Stanford.main import *

def request():
    A = input("Recherche ")
    return A

def search_from_request(request, D_terme_termeid, D_terme_id_postings):
    if request in D_terme_termeid:
        print(D_terme_id_postings[D_terme_termeid[request]])
    else:
        print("No results found")

def search_engine(collection):
    #Generated the index from the collection
    if collection == "cacm":
        terme_termeid, termeid_postings = main_CACM()
    elif collection == "stanford":
        terme_termeid, termeid_postings = main_STANFORD()

    user_request = request()

    while user_request != "Stop":
        search_from_request(user_request, terme_termeid, termeid_postings)
        user_request = request()

search_engine("cacm")
