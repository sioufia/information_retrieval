class Index():

    def __init__(self, D_terme_termeid, D_termeid_postings):
        if not isinstance(D_terme_termeid, dict):
            raise TypeError("D_terme_termeid doit être un dictionnaire")
        if not isinstance(D_termeid_postings, dict):
            raise TypeError("D_termeid_postings doit être un dictionnaire")
        
        self.D_terme_termeid = D_terme_termeid
        self.D_termeid_postings = D_termeid_postings
    
    def get_termeid_postings(self, terme):
        if not isinstance(terme, str):
            raise TypeError("Le terme cherché doit être sous format chaîne de caractère")
        
        if terme in self.D_terme_termeid:
            return (self.D_termeid_postings[self.D_terme_termeid[terme]])

        else:
            return []
    
