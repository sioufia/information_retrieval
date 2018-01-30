import time
from operator import itemgetter
import ast
import json
from math import *

from ...index_inverse_common.index_inverse_common import IndexInverseCommon

class IndexInverse(IndexInverseCommon):

    def __init__(self):
        #self.D_terme_termeid = {}
        #self.D_terme_id_postings = {}
        #self.nb_doc = 1
        IndexInverseCommon.__init__(self)
        self.doc_docid = {}
        self.current_termid = 0
    
    @staticmethod
    def sortingBlock(termid_doc_f, block_number):
        """Takes a list of (termid, docid) from a block and made a dic with:
        #Keys: termid
        #Values : postings list of tuples (docid, frequency)"""
        start_time = time.time()

        termid_doc_f.sort(key=itemgetter(0,1))

        termid_postings = {}
        freq_term_doc = 0
        current_couple = termid_doc_f[0]
        for elt in termid_doc_f:
            #The last tuple is the same as the current: same termid in the same doc
            if current_couple == elt:
                freq_term_doc +=1
            
            else:
                #Same termid but it's not in the same doc
                if current_couple[0] in termid_postings.keys():
                    termid_postings[current_couple[0]].append([current_couple[1], freq_term_doc])
                #New termid
                else:
                    termid_postings[current_couple[0]] = [[current_couple[1], freq_term_doc]]
                
                current_couple = elt
                freq_term_doc = 1
        
        #Need to handle the last current element
        if current_couple[0] not in termid_postings.keys():
            termid_postings[current_couple[0]] = [[current_couple[1], freq_term_doc]]
        else:
            termid_postings[current_couple[0]].append([current_couple[1], freq_term_doc])
        
        print("Sorting block " + str(block_number) + " : {} seconds ".format(time.time() - start_time))
        return termid_postings  

    @staticmethod
    def writeBlockToDiskJson(dic_termid_postings, main_path, filename):
        start_time = time.time()
        with open(main_path + filename, "a") as f:
            for termid in dic_termid_postings:
                line = '{"' + str(termid) + '":"' + str(dic_termid_postings[termid]) + '"}' + '\n'
                f.write(str(line))

        print("Writing block to disk JSON " + filename + " : {} seconds ".format(time.time() - start_time))

    def mergeBlock(self, path_file, pref_files_block):
        """Merge the blocks of an index."""
        start_time = time.time()
        read_buffer = list(self.D_terme_termeid.values())
        read_buffer = [i for i in range (100)]
        files = []
        
        #Open all the files and append it to a file
        for elt in range(9):
            f = open(path_file + pref_files_block + str(elt), "r")
            files.append(f)
        
        buffer_termid = {} #key:block, value:(termid, postinglist)

        index_final_file = open(path_file + "index_final_stanford", "a") 

        while len(read_buffer) > 1:
            L= [] #A list of tuples (termid, postinglist)
            for block in range(0,9):
                if block not in buffer_termid or buffer_termid[block][0] < read_buffer[0]:
                    line = files[block].readline()
                    buffer_termid[block] = IndexInverse.convertPostingsFromStringToList(line) #Stock the tuple (termid, postinglist)
                
                if buffer_termid[block][0] == read_buffer[0]:
                    L += buffer_termid[block][1]

            
            if L:
                line = '{"' + str(read_buffer[0]) + '":"' + str(L) + '"}' + '\n'
                index_final_file.write(line)

            del read_buffer[0] # Removing the termid for which the posting list was merged

        print("Merging block : {} seconds ".format(time.time() - start_time))

    @staticmethod
    def convertPostingsFromStringToList(line):
        """Method that takes a line from a block and convert it to a tuple (termid, posting_list)"""
        termid_key = int(list(json.loads(line.replace("\n","")).keys())[0])
        postings_list = ast.literal_eval(json.loads(line.replace("\n",""))[str(termid_key)])
        return (termid_key, postings_list)
    
    def convertIndexDiskIntoIndexMemory(self, filename):
        """Method that gets the index from disk and associate it to the index_inverse in memory"""
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                termid, postings = IndexInverse.convertPostingsFromStringToList(line)
                self.D_terme_id_postings[termid] = postings
    




    
        

                






        
