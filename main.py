import time

from index_inverse.index_inverse_BSBI.index_cacm_bsbi.index_cacm_bsbi import constructbsbi_index_CACM
from index_inverse.index_inverse_BSBI.index_stanford_bsbi.index_stanford_bsbi import constructbsbi_index_Stanford
from index_inverse.index_inverse_mapreduce.map_reduce_cacm.map_reduce_cacm import constructmapred_index_CACM
from index_inverse.index_inverse_memory.index_inverse_memory_cacm.index_inverse_memory_cacm import constructmemory_index_CACM
from index_inverse.index_inverse_memory.index_inverse_memory_stanford.index_inverse_memory_stanford import constructmemory_index_Stanford
from search.search import Search, SearchBoolean, SearchVector


def search_engine():
    collection = input("On which collection do you want to make a query ? (cacm/stanford) : ")

    if collection == "cacm":
        type_of_index_building = input("Which type of building do you want to use to make your index ? (bsbi/mapreduce/memory) : ")
        collection_path = input("What is the path of the CACM collection ? ")
        stopwords_path = input("What is the path of the Stopwords for CACM collection ? ")
        
        if type_of_index_building == "bsbi":
            index_folder = input("In which folder do you want to create CACM index ? : ")
            index = constructbsbi_index_CACM(collection_path, stopwords_path, index_folder)
        elif type_of_index_building == "mapreduce":
            index = constructmapred_index_CACM(collection_path, stopwords_path)
        elif type_of_index_building == "memory":
            index = constructmemory_index_CACM(collection_path, stopwords_path)
        else:
            raise ValueError("Not a type of index building allowed")
        
        # half_collection is only used to estimate the size of voc for half the collection
            # index.half_collection()

            #To compute range frequency plot
            #index.rang_freq()  #Need to debug

            #print("There are {} tokens in the collection".format(str(index.nb_tokens))) #Need to debug
            #print("There are {} distinct words in the vocabulary".format(str(index.size_voc()))) #Need to debug
    
    elif collection == "stanford":
        path = input("Path for stanford collection ?")
        index = constructmemory_index_Stanford(path)
    
    else:
        raise ValueError("Not a collection allowed")
        
    type_search = input("Type of search ? (boolean/vector) : ")
    user_request = input("Search : ")

    while user_request != "Stop":
        if type_search == "boolean":
            start_time = time.time()
            current_search = SearchBoolean(user_request)
            result_list = current_search.do_search(index)
            Search.display_docs(result_list, type_search)
            print("Results in %s seconds ---" % (time.time() - start_time))
        
        elif type_search == "vector":
            start_time = time.time()
            current_search = SearchVector(user_request)
            result_list = current_search.do_search(index, 20)
            Search.display_docs(result_list, type_search)
            print("Results in %s seconds ---" % (time.time() - start_time))
        
        type_search = input("boolean or vector ")
        user_request = input("Recherche ")


if __name__ == "__main__":
    search_engine()
