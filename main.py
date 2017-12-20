from index_inverse.index_inverse_CACM.main import *
#from index_inverse.index_inverse_Stanford.main import *
from search import Search, SearchBoolean, SearchVector
from index_inverse.index_inverse_class import Index


def search_engine(collection):
    #Generated the index from the collection
    if collection == "cacm":
        terme_termeid, termeid_postings = main_CACM()  
    elif collection == "stanford":
        terme_termeid, termeid_postings = main_STANFORD()
    
    index = Index(terme_termeid, termeid_postings)

    type_search = input("boolean or vector ")
    user_request = input("Recherche ")

    while user_request != "Stop":
        if type_search == "boolean":
            try:
                current_search = SearchBoolean(user_request)
                print (current_search.do_search(index))
                user_request = input("Recherche ")
            except ValueError:
                user_request = input("Les opérateurs autorisés sont AND, OR et NOT ")

        """if type_search != "vector":
            current_search = SearchVector(user_request)"""
        
    

search_engine("cacm")
