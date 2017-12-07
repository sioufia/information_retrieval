from traitement_linguistique_cacm import *
import time

def main():
    start_time = time.time()
    A = traitement_linguistique_cacm()
    print("--- %s seconds ---" % (time.time() - start_time))
    return(A)


