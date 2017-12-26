from .evaluation import Evaluation
from index_inverse.index_inverse_CACM.construction_index_cacm_class import ConstructionIndex, ConstructionIndexCACM

def get_doc_relevants_query(query_nb):
    L = []
    with open("CACM/qrels.text", "r") as f:
        for line in f:
            line = line.split(" ")
            if int(line[0]) > query_nb:
                break
            elif int(line[0]) == query_nb:
                L.append(int(line[1]))
        return L

def loop_query_test():
    D = {}
    current_test_nb = 0
    current_section_list = ""
    section_list = [".I", ".N", ".W", ".A"]
    with open("CACM/query.text", "r") as f:
        for line in f:
            if line[:2] in section_list:
                current_section_list = line[:2]
                if line[:2] == ".I":
                    line = line.split(" ")
                    current_test_nb = int(line[1])
                    D[current_test_nb] = ""
            
            if current_section_list == ".W" and line[:2] !=".W":
                D[current_test_nb] += " " + line[:-1]
        return D

def calculate_average(D):
    new_dic = {}
    nb_test_query = 0
    for dic in D:
        nb_test_query += 1
        for rappel in dic:
            if rappel in new_dic:
                new_dic[rappel] += dic[rappel]
            else:
                new_dic[rappel] = dic[rappel]
    
    for rappel in new_dic:
        new_dic[rappel] /= nb_test_query

    return new_dic 



def main():
    index = ConstructionIndexCACM()
    index.parser("CACM/cacm.all")
    index.segmenter()
    index.traiter_tokens_collection("CACM/common_words")
    nb_doc = index.index_inverse()
    index.weight_calculation_index(nb_doc)
    print("Index OK")
    queries = loop_query_test()

    L=[]

    for query in queries:
        relevant_doc = get_doc_relevants_query(query)
        A = Evaluation(query = queries[query], sample_test=relevant_doc)
        A.precision_for_relevant_doc(index)
        A.interpolate_rappel_precision()
        L.append(A.rappel_precision_interpolation)
    
    interpolate_general = calculate_average(L)
    return interpolate_general



                





