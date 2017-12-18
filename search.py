class Search():
    def __init__(self, request):
        if not isinstance(request, str):
            raise TypeError("La requête doit être une chaîne de caractère")

        self.request = request.split()

class SearchBoolean(Search):
    def transform_request_list(self):
        allowed_operators = ['AND', 'OR', 'NOT']
        self.request


        
