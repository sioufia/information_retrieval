from index_inverse.index_inverse_CACM.main import *
#from index_inverse.index_inverse_Stanford.main import *
from search import Search, SearchBoolean, SearchVector
from index_inverse.index_inverse_class import Index
import time


def search_engine():
    collection = input("Collection: ")

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
            start_time = time.time()
            current_search = SearchBoolean(user_request)
            result_list = current_search.do_search(index)
            Search.display_docs(result_list, type_search)
            print("Results in %s seconds ---" % (time.time() - start_time))
            user_request = input("Recherche ")
        
        elif type_search == "vector":
            start_time = time.time()
            current_search = SearchVector(user_request)
            result_list = current_search.do_search(index, 10)
            Search.display_docs(result_list, type_search)
            print("Results in %s seconds ---" % (time.time() - start_time))
            user_request = input("Recherche ")

        else:
            type_search = input("boolean or vector ")
            user_request = input("Recherche ")


search_engine()




