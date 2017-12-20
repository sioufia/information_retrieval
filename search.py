#from index_inverse.index_inverse_class import Index

class Search():
    def __init__(self, request):
        if not isinstance(request, str):
            raise TypeError("La requête doit être une chaîne de caractère")

        self.request = request

class SearchBoolean(Search):
    
    def __init__(self, request):
        Search.__init__(self, request)
        
        allowed_operators = ['AND', 'OR', 'NOT']
        request_list = self.request.split()
        
        if len(request_list)%2 == 0:
            raise ValueError("La requête n'est pas au bon format")
        
        """i = 1
        while i < len(request_list):
            try:
                if request_list[i] not in allowed_operators or  :
                    raise ValueError("Opérateur non autorise. Les opérateurs acceptés sont AND, OR et NOT")
                else:
                    i = i + 1"""
        
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
        terme1_postings = index.get_termeid_postings(self.request[0])
        if len(self.request) == 1:
            return terme1_postings
        
        else:
            terme2_postings = index.get_termeid_postings(self.request[2])
            current_fusion = SearchBoolean.operator_action(terme1_postings, self.request[1], terme2_postings)

            i = 3
            while i < len(self.request):
                current_fusion = SearchBoolean.operator_action(current_fusion, self.request[i], index.get_termeid_postings(self.request[i+1]))
                i = i + 2

            return current_fusion

class SearchVector(Search):
    pass



        