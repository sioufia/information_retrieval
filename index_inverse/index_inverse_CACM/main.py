from .traitement_linguistique_cacm import *
from .index_basique import *
import time

def main_CACM():
    start_time = time.time()
    collection = traitement_linguistique_cacm()
    terme_termeid, termeid_postings = index_inverse(collection)
    print("--- %s seconds ---" % (time.time() - start_time))
    return (terme_termeid, termeid_postings)


