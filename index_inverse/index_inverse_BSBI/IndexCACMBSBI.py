from IndexInverse import *

class IndexCACMBSBI(IndexInverse):
    def __init__(self):
        IndexInverse.__init__(self)
        self.collection_dic = {}
    
    def parser(self,filename):
        """Method that takes a file with several documents as entry.
           It updates the collection_dic attribute with the doc number as key, and the content
           of the doc as value"""
        
        with open(filename, "r") as f:
            doc_number = '0'
            doc_section = '0'
            section_list = [".B",".A",".N",".X",".C",".I",".T",".W",".K"]
            for line in f:
                if line[:2] in section_list:
                    doc_section = str(line[:2])
                    if line[:2] == ".I":
                        doc_number = (str(line[3:]))[:-1]
                        self.collection_dic[doc_number] = "" 
                elif doc_section in [".I",".T",".W",".K"]:
                    self.collection_dic[doc_number] += " " + line[:-1]
    
    def tokenizer(self):
        """Method that tokenizes the content of the attribute 
           collection_dic """
        for doc in self.collection_dic:
            self.collection_dic[doc] = nltk.word_tokenize(self.collection_dic[doc])
    
    @staticmethod
    def stock_stopwords_list(filename):
        """Method that takes a file with stopwords and return it as a list"""
        L = []
        with open(filename, "r") as f:
            for word in f:
                L.append(word[:-1])
            f.close()
        return L
    
    def manage_tokens_collection(self, stopwords_file):
        """Method that removes the stopwords of each doc in the 
           collection. It removes the punctuation too."""
        stopwords = IndexCACMBSBI.stock_stopwords_list(stopwords_file)
        collection_without_stopwords = {}
        for elt in self.collection_dic:
            collection_without_stopwords[elt] = []
            for token in self.collection_dic[elt]:
                if (token.lower() not in stopwords) and (token.lower() not in [",",".",";",")","(","?","\t","\\"]):
                    collection_without_stopwords[elt].append(token.lower())
        self.collection_dic = collection_without_stopwords
    
    def parseBlock(self):
        """Function that takes a dictionnary with doc as key and tokens as value.
           It returns a list of tuples (termid, frequency)"""
        #block_number is the number of the block
        start_time = time.time()
        termid_doc_f =[]
        for doc in self.collection_dic:
            for term in doc:
                if term not in self.term_termid.keys():
                    self.term_termid[term] = self.current_termid
                    termid_doc_f.append((self.term_termid[term], self.nb_doc))
                    self.current_termid += 1
                    
                else:
                    termid_doc_f.append((self.term_termid[term], self.nb_doc))

            self.nb_doc += 1

        print("Parsing block 0 : {} seconds ".format(time.time() - start_time))
        return termid_doc_f