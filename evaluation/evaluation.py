from search.search import Search, SearchVector

class Evaluation():
    """Class that compare the result of one request with the relevant
    documents in the sample test. Its attributes are:
    - A dictionnary with rappel of relevant doc as key, and precision of relevant doc as value
    - A dictionnary with rappel as key and precision as value.
      Keys are (0.O, 0.1, 0.2, ..., 0.9, 1) --> The interpolation
    - The request : a string
    - The sample test : a list the relevant docs
    """

    def __init__(self, query, sample_test):
        if not isinstance(query, str):
            raise TypeError("La requête doit être une chaine de caractère")
        
        if not isinstance(sample_test, list):
            raise TypeError("Le banc de test doit être sous format de liste")
        
        self.rappel_precision_relevant_doc ={}
        self.rappel_precision_interpolation = {}
        self.query = query
        self.sample_test = sample_test
    
    def precision_for_relevant_doc(self, index):
        """Calculate the precision for each relevant doc found 
           in the query results"""
        
        current_search = SearchVector(self.query)
        result_list = current_search.do_search(index)
        total_nb_relevant_doc = len(self.sample_test)
        current_nb_relevant_doc_found = 0
        current_nb_doc_retrieved = 0

        for doc in result_list:
            current_nb_doc_retrieved += 1
            #If the document is relevant
            if int(doc[0]) in self.sample_test:
                current_nb_relevant_doc_found += 1
                rappel = current_nb_relevant_doc_found / total_nb_relevant_doc
                precision = current_nb_relevant_doc_found / current_nb_doc_retrieved
                self.rappel_precision_relevant_doc[rappel] = precision
    
    def interpolate_rappel_precision(self):
        """Interpolate the curve Rappel-Precision"""
        i = 0
        rappel = 0
        temp_dic = self.rappel_precision_relevant_doc
        for i in range(11):
            temp_dic = {k:v for (k,v) in temp_dic.items() if rappel<k}
            #The case where not all relevant documents have been found
            if len(temp_dic) == 0:
                precision = 0
            else:
                precision = max(temp_dic.values())
            self.rappel_precision_interpolation[round(rappel,1)] = precision
            rappel += 0.1
        
            
            


        


        
        

    


