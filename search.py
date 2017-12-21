#from index_inverse.index_inverse_class import Index

class Search():
    def __init__(self, request):
        if not isinstance(request, str):
            raise TypeError("La requête doit être une chaîne de caractère")

        self.request = request
    
    def display_docs(postings):
        """Method that displays the document number of postings list"""
        if len(postings) == 0:
            print ("No results found")
        i = 1
        for doc in postings:
            print("Result {0} : Document {1} ".format(i, doc))
            i += 1

class SearchBoolean(Search):
    
    def __init__(self, request):
        Search.__init__(self, request)
        request_list = self.request.split()
        self.request = request_list
    
    def operator_action(postings1, operator, postings2):
        if not isinstance(postings1, list):
            raise TypeError("Les postings doivent être sous le format liste")
        if not isinstance(postings2, list):
            raise TypeError("Les postings doivent être sous le format liste")
        
        set_postings1 = set(postings1)
        set_postings2 = set(postings2)

        if operator == "AND":
            return list(set_postings1.intersection(set_postings2))

        if operator == "OR":
            return list(set_postings1.union(set_postings2))

        if operator == "NOT":
            return list(set_postings1.difference(set_postings2))
    
    def do_search(self, index):
        """Method that that takes an index and a search object and return the fusion of the different postings"""
        allowed_operators = ['AND', 'OR', 'NOT']
        current_fusion = index.get_termeid_postings(self.request[0])
        """if len(self.request) == 1:
            return terme1_postings"""
        i = 1
        while i < len(self.request):
            if self.request[i] in allowed_operators:
                try:
                    current_fusion = SearchBoolean.operator_action(current_fusion, self.request[i], index.get_termeid_postings(self.request[i+1]))
                    i += 2
                except IndexError:
                    #Case where the request is finished by an operator
                    return current_fusion
            else:
                #case where 2 strings are not seperated by an operator. It is considered as AND
                current_fusion = SearchBoolean.operator_action(current_fusion, 'AND', index.get_termeid_postings(self.request[i]))
                i += 1
        
        return current_fusion

class SearchVector(Search):
    pass



        