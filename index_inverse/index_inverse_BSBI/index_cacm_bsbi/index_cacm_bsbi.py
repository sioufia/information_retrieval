import nltk
import time

from ..index_inverse.index_inverse import IndexInverse
from ...index_inverse_common.index_inverse_common import IndexInverseCommonCacm

class IndexCACMBSBI(IndexInverse, IndexInverseCommonCacm):
    def __init__(self, collection_dic = {}):
        IndexInverse.__init__(self)
        self.collection_dic = collection_dic
    
    def parseBlockCacm(self):
        """Function that takes a dictionnary with doc as key and tokens as value.
           It returns a list of tuples (termid, frequency)"""
        #block_number is the number of the block
        start_time = time.time()
        termid_doc_f =[]
        for doc in self.collection_dic:
            for term in self.collection_dic[doc]:
                if term not in self.D_terme_termeid.keys():
                    self.D_terme_termeid[term] = self.current_termid
                    termid_doc_f.append([self.D_terme_termeid[term], self.nb_doc])
                    self.current_termid += 1
                    
                else:
                    termid_doc_f.append([self.D_terme_termeid[term], self.nb_doc])

            self.nb_doc += 1

        print("Parsing block 0 : {} seconds ".format(time.time() - start_time))
        return termid_doc_f

def constructbsbi_index_CACM(collection_path, stopwords_path, index_folder):
    index = IndexCACMBSBI()
    index.parserCacm(collection_path)
    index.tokenizerCacm()
    index.manage_tokens_collectionCacm(stopwords_path)
    termid_docid_block = index.parseBlockCacm() #CACM is considered as just one block
    termid_postings_block = IndexInverse.sortingBlock(termid_docid_block, "0")
    IndexInverse.writeBlockToDiskJson(termid_postings_block, index_folder, "index_cacm")
    index.convertIndexDiskIntoIndexMemory(index_folder + "index_cacm")
    index.weight_calculation_index()
    return index

if __name__ == "__main__":
    index_folder = input("In which folder do you want to create your CACM index ? ")
    collection_path = input("What is the path of the CACM collection ? ")
    stopwords_path = input("What is the path of the Stopwords for CACM collection ? ") 
    index = constructbsbi_index_CACM(collection_path, stopwords_path, index_folder)
    print(index)