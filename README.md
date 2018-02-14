                                        Information Retrieval Project @CentraleSupélec@3rdYear

DESCRIPTION:
This project enables a user to make a query to 2 different collections: cacm and stanford.

It is divided into 3 main parts:
    1/ Construction of the index with 3 different methods (folder: index_inverse) :
        - In Memory method (folder: index_inverse/index_inverse_memory)
        - BSBI method (folder: index_inverse/index_inverse_BSBI)
        - MapReduce method (folder: index_inverse/index_inverse_mapreduce)
    
    2/ Modelisation of 2 different type of searches (folder: search) :
        - Boolean search 
        - Vectorial search
    
    3/ Evaluation of the query for the collection CACM (folder: evaluation ; file: main_evaluation) :
        - Curve recall/precision
        - Mean average precision
        - For each request, it computes E,F measures and R precision. However several queries did not have any
        relevant documents so these statistics could not be computed.

STEPS TO FOLLOW TO:

/!\ When path for stanford collection is required, enter the path to the folder which contains the blocks,
    with a "/" at the end of the path. Ex : "...../pa1-data/"

    Use the search engine: 
    1/ Go to the folder riproject via your terminal : cd riproject
    2/ Launch the file main.py via your terminal : python main.py
    3/ Follow the steps indicated via your terminal

        Note for the search engine:
        Only the in memory index construction is used for the STANFORD collection (it took to much time for BSBI and
        MapReduce).
    
    Construct the index via different methods:
    1st Method - BSBI:
        For CAM
        1/ Go to the folder riproject via your terminal : cd riproject
        2/ Run the foolowing command via your terminal : python -m index_inverse.index_inverse_BSBI.index_cacm_bsbi.index_cacm_bsbi
        For Stanford (run the same command but change the name) --> It currently takes too much time (around 20 hours)

    2nd Method - MapReduce:
        For CAM
        1/ Go to the folder riproject via your terminal : cd riproject
        2/ Run the foolowing command via your terminal : python -m index_inverse.index_inverse_mapreduce.map_reduce_cacm.map_reduce_cacm
        For Stanford (run the same command but change the name) --> It currently takes too much time.

    3rd Method - In memory:
        For CAM
        1/ Go to the folder riproject via your terminal : cd riproject
        2/ Run the following command via your terminal : python -m index_inverse.index_inverse_memory.index_inverse_memory_cacm.index_inverse_memory_cacm
        For Stanford (run the same command but change the name)
    
    Use the CACM evaluation:
        1/ Go to the folder riproject via your terminal : cd riproject
        2/ Run main_evaluation.py. Results are printed in the terminal.
