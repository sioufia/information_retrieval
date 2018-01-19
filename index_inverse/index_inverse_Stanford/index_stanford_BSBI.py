import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import pickle
import time

class IndexStanfordBSBI:

    def __init__(self):
        self.doc_docid = {}
        self.term_termid = {}

        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.wl = WordNetLemmatizer()
        self.current_termid = 0
        self.current_docid = 0

    def removeStopWords(self,wordList): #Remove stop words from a list of words
        wordList_filtered = [w for w in wordList if not w in self.stop_words]
        return wordList_filtered

    def lemmatisation(self,wordList):
        return list(map(self.wl.lemmatize, wordList))
    
    #Functions that return a list of the terms in the doc after a linguistic process
    def parseDoc(self, path_doc):
        with open(path_doc, 'r') as f:
            wordList = []
            for line in f.readlines():
                wordList += line.split()
            wordList = self.removeStopWords(wordList)
            wordList = self.lemmatisation(wordList)
        return wordList
    
    #Function that takes a list of docs with tokens and returns a sorted index 
    def parseBlock(self, collection_path, block_number):
        #block_number is the number of the block
        start_time = time.time()
        termid_postings ={} 
        path_temp = collection_path + str(block_number) + "/"
        for root, dirs, files in os.walk(path_temp):
            for file in files:
                filename = str(block_number) + file
                self.doc_docid[self.current_docid] = filename
                path_file = path_temp + file
                wordDoc = self.parseDoc(path_file)
                for term in wordDoc:
                    if term not in self.term_termid.keys():
                        self.term_termid[term] = self.current_termid
                        termid_postings[self.term_termid[term]] = {} #No solution found to avoid dictionary for postings if we want to stock the weight of the terms
                        termid_postings[self.term_termid[term]][self.current_docid] = 1 #Stock the frequency for the value first
                        self.current_termid += 1
                    
                    #If the term has already been found in another block but not in the current block
                    elif self.term_termid[term] not in termid_postings:
                        termid_postings[self.term_termid[term]] = {} #No solution found to avoid dictionary for postings if we want to stock the weight of the terms
                        termid_postings[self.term_termid[term]][self.current_docid] = 1 #Stock the frequency for the value first                   

                    #If the term_id already exists but this posting doc not
                    elif self.current_docid not in termid_postings[self.term_termid[term]].keys():
                        termid_postings[self.term_termid[term]][self.current_docid] = 1
                    
                    #If the posting for this term_id already exists
                    else:
                        termid_postings[self.term_termid[term]][self.current_docid] += 1
                
            
                self.current_docid += 1

        print("Parsing block " + str(block_number) + " : {} seconds ".format(time.time() - start_time))
        return termid_postings

    def sortingBlock(dic_termid_postings):
        #Take an index of a block and sort it by termid
     
    def writeBlockToDisk(dic_termid_postings, filename):
        start_time = time.time()
        path_file = "/Users/alexandresioufi/Documents/Projets infos/recherche/disk_bsbi/" + filename
        with open(path_file, "wb") as f:
            pickler = pickle.Pickler(f)
            pickler.dump(dic_termid_postings)
            f.close()
        print("Writing block to disk " + filename + " : {} seconds ".format(time.time() - start_time))
    
def main(collection_path):
    index = IndexStanfordBSBI()
    for i in range(0, 9):  # Browsing blocks    
        print(i)
        termid_postings_block = index.parseBlock(collection_path, i)
        IndexStanfordBSBI.writeBlockToDisk(termid_postings_block, str(i))
        del termid_postings_block

#main("/Users/alexandresioufi/Documents/Projets infos/recherche/pa1-data/")



            



        


                






        
