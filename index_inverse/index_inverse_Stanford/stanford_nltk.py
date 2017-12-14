from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os


path = "C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/pa1-data (1)/pa1-data/0/"


for root,dirs,files in os.walk(path):
    for file in files:
        with open(path + file, 'r') as f:
            for line in f.readlines():
                print(line)

