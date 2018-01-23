import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import time
from operator import itemgetter
import ast
import json

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
        termid_doc_f =[]
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
                        termid_doc_f.append((self.term_termid[term], self.current_docid))
                        self.current_termid += 1
                        
                    else:
                        termid_doc_f.append((self.term_termid[term], self.current_docid))

                self.current_docid += 1

        print("Parsing block " + str(block_number) + " : {} seconds ".format(time.time() - start_time))
        return termid_doc_f
    
    @staticmethod
    def sortingBlock(termid_doc_f, block_number):
        #Takes a list of (termid, docid) from a block and made a dic with:
        #Keys: termid
        #Values : postings list of tuples (docid, frequency)
        start_time = time.time()

        termid_doc_f.sort(key=itemgetter(0,1))

        termid_postings = {}
        freq_term_doc = 0
        current_couple = termid_doc_f[0]
        for elt in termid_doc_f:
            #The last tuple is the same as the current: same termid in the same doc
            if current_couple == elt:
                freq_term_doc +=1
            
            #Same termid but it's not in the same doc
            elif current_couple[0] == elt[0]:
                if current_couple[0] not in termid_postings.keys():
                    termid_postings[current_couple[0]] = []

                termid_postings[current_couple[0]].append((current_couple[1], freq_term_doc))
                current_couple = elt
                freq_term_doc = 1
            
            #New termid
            else:
                current_couple = elt
                freq_term_doc = 1
        
        #Need to handle the last current element
        if current_couple[0] not in termid_postings.keys():
            termid_postings[current_couple[0]] = [(current_couple[1]), freq_term_doc]
        else:
            termid_postings[current_couple[0]].append((current_couple[1], freq_term_doc))
        
        print("Sorting block " + str(block_number) + " : {} seconds ".format(time.time() - start_time))
        return termid_postings

    def writeBlockToDiskJson(dic_termid_postings, filename):
        start_time = time.time()
        path_file = "/Users/alexandresioufi/Documents/Projets infos/recherche/disk_bsbi/" + filename
        with open(path_file, "a") as f:
            for termid in dic_termid_postings:
                line = '{"' + str(termid) + '":"' + str(dic_termid_postings[termid]) + '"}' + '\n'
                f.write(str(line))

        print("Writing block to disk JSON " + filename + " : {} seconds ".format(time.time() - start_time))


    def mergeBlock(self):
        start_time = time.time()
        index = {}
        path_file = "/Users/alexandresioufi/Documents/Projets infos/recherche/disk_bsbi/"
        #read_buffer = list(self.term_termid.values())
        read_buffer = [i for i in range(0,1000)]
        while len(read_buffer) > 1:
            L= [] #A list of tuples (block, termid, postinglist)
            for block in range(0,9):
                with open(path_file + str(block), "r") as f:
                    for i, line in enumerate(f):
                        if int(list(json.loads(line.replace("\n","")).keys())[0]) == read_buffer[0]:
                            dico = ast.literal_eval(json.loads(line.replace("\n",""))[str(read_buffer[0])])
                            L.append(dico)
                            del dico
                            break
            
            if len(L) != 0:
                index[read_buffer[0]] = IndexStanfordBSBI.mergePostingLists(L)
            else:
                print('L vide: {}'.format(read_buffer[0]))

            del read_buffer[0] # Removing the termid for which the posting list was merged

        print("Merging block : {} seconds ".format(time.time() - start_time))
        return index
    
    @staticmethod
    def mergePostingLists(postings_lists):
        start_time = time.time()
        #list of postings_list that are sorted by doc_id
        if len(postings_lists) == 1:
            return postings_lists
        else:
            set_postings_list = []
            for postings in postings_lists:
                set_postings_list.append(set(postings))
            del postings_lists #Save memory
    
            mergeLists = set_postings_list[0]
            i = 1
            while i < len(set_postings_list):
                mergeLists = mergeLists.union(set_postings_list[i])
                i += 1
            mergeLists = list(mergeLists)
            mergeLists.sort(key=itemgetter(0,1))
            return mergeLists



def main(collection_path):
    index = IndexStanfordBSBI()
    for i in range(0, 9):  # Browsing blocks    
        print(i)
        termid_docid_block = index.parseBlock(collection_path, i)
        termid_postings_block = IndexStanfordBSBI.sortingBlock(termid_docid_block, str(i))
        IndexStanfordBSBI.writeBlockToDiskJson(termid_postings_block, str(i))
        del termid_postings_block, termid_docid_block

#main("/Users/alexandresioufi/Documents/Projets infos/recherche/pa1-data/")




        


                






        
