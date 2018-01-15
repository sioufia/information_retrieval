from index_inverse.index_inverse_CACM.construction_index_cacm_class import ConstructionIndex, ConstructionIndexCACM
from index_inverse.index_inverse_Stanford.index_stanford import IndexStanford
from search.search import Search, SearchBoolean, SearchVector
import time


def search_engine():
    collection = input("Collection: ")

    #Generated the index from the collection
    if collection == "cacm":
        start_time = time.time()
        index = ConstructionIndexCACM()
        index.parser("CACM/cacm.all")
        index.segmenter()
        index.traiter_tokens_collection("CACM/common_words")
        nb_doc = index.index_inverse()
        index.weight_calculation_index(nb_doc)
        print("Index construction : %s seconds " % (time.time() - start_time))
    elif collection == "stanford":
        start_time = time.time()
        index = IndexStanford()
        path = input("Path for stanford collection")
        index.indexConstruction(path)
        print("Index construction : %s seconds " % (time.time() - start_time))

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
            result_list = current_search.do_search(index, 20)
            Search.display_docs(result_list, type_search)
            print("Results in %s seconds ---" % (time.time() - start_time))
            user_request = input("Recherche ")

        else:
            type_search = input("boolean or vector ")
            user_request = input("Recherche ")


search_engine()






