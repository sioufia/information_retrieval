from .evaluation import Evaluation
from index_inverse.index_inverse_CACM.construction_index_cacm_class import ConstructionIndex, ConstructionIndexCACM
import matplotlib.pyplot as plt

def get_doc_relevants_query(query_nb):
    """Method that get the relevant doc for a query from the query set"""
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
    """Method that parse the query.text file. It returns a dictionnary with query_number as key
       and query as value."""
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
    """Method that takes all the interpolation of precision/recall for different queries. 
       It calculates the average for precision for each recall.
       It return a dictionnary with recall as key, and precision as value.
       """
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
    """Main Method that produces the interpolate curve Precision/Recall from the query set"""

    #Creation of the CACM index
    index = ConstructionIndexCACM()
    index.parser("CACM/cacm.all")
    index.segmenter()
    index.traiter_tokens_collection("CACM/common_words")
    nb_doc = index.index_inverse()
    index.weight_calculation_index(nb_doc)

    #Get the queries under the dictionnary format from the file query.text file
    queries = loop_query_test()

    L=[]

    for query in queries:
        relevant_doc = get_doc_relevants_query(query)
        A = Evaluation(query = queries[query], sample_test=relevant_doc)
        A.precision_for_relevant_doc(index)
        A.interpolate_rappel_precision()
        L.append(A.rappel_precision_interpolation)

    #Calculate the average of each value of recall
    interpolate_general = calculate_average(L)

    #Make the interpolate curve Rappel-Precision
    Rappel = list(interpolate_general.keys())
    Precision = list(interpolate_general.values())
    plt.scatter(Rappel, Precision)
    plt.title('Precision/Recall interpolation')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.show()
    
    return interpolate_general



                





