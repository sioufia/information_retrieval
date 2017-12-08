import nltk
from parser_CACM import *

"""Ce fichier gère le traitement linguistique de la collection CACM"""

def stock_stopwords_list(filename):
    with open(filename, "r") as f:
        L = []
        for word in f:
            L.append(word[:-1])
        return L

def segmenter(collection_documents):
    for doc in collection_documents:
        collection_documents[doc] = nltk.word_tokenize(collection_documents[doc])

def traiter_tokens_collection(collection_documents, stopwords_file):
    stopwords = stock_stopwords_list(stopwords_file)
    collection_without_stopwords = {}
    for elt in collection_documents:
        collection_without_stopwords[elt] = []
        for token in collection_documents[elt]:
            if (token.lower() not in stopwords) and (token.lower() not in [",",".",";"]):
                collection_without_stopwords[elt].append(token.lower())
    return collection_without_stopwords

def traitement_linguistique_cacm():
    collection_documents = parser()
    segmenter(collection_documents)
    collection_documents_traité = traiter_tokens_collection(collection_documents, "CACM/common_words")
    return collection_documents_traité

