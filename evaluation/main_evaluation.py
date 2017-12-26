from .evaluation import Evaluation
from index_inverse.index_inverse_CACM.construction_index_cacm_class import ConstructionIndex, ConstructionIndexCACM


def main():
    index = ConstructionIndexCACM()
    index.parser("CACM/cacm.all")
    index.segmenter()
    index.traiter_tokens_collection("CACM/common_words")
    nb_doc = index.index_inverse()
    index.weight_calculation_index(nb_doc)
    return index

