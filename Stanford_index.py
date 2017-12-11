
# coding: utf-8

# In[6]:


import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os


# In[7]:


print("yolo let's go")


# In[8]:


path = "C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/pa1-data (1)/pa1-data/"
path_2 = "C:/Users/titou/Desktop/Centrale/Option OSY/RI-W/Stanford_treated/"


# In[9]:


nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
wl = WordNetLemmatizer()


# In[10]:


#Dictionnaries to build
dico_termID = {} #{term:termID}
dico_docID = {} #{doc:docID}
dico_index = {} #{termID:docID}
docID = 0 #initialisation of docIDs
termID = 0 #initialisation of termIDs


# In[11]:


for i in range(0,9): #Browsing blocks
    path_temp = path + str(i) + "/"
    for root,dirs,files in os.walk(path_temp):
        for file in files:
            filename = str(i)+file
            dico_docID[docID] = filename
            
            
            with open(path_temp + file, 'r') as f:
                for line in f.readlines():
                    
                    #Stop words
                    wordList = line.split()
                    wordList_filtered = [w for w in wordList if not w in stop_words]
                    
                    #Lemmatisation
                    wordList_filtered = list(map(wl.lemmatize,wordList_filtered))
                    
                    #Construction de l'index
                    #termID
                    for w in wordList_filtered:
                        dico_termID[termID] = w
                        dico_index[termID] = docID
                        termID += 1
                  
            docID += 1 #Next document


# In[16]:


i=0
path_temp = path + str(i) + "/"
for root,dirs,files in os.walk(path_temp):
    for file in files:
        filename = str(i)+file
        dico_docID[docID] = filename


        with open(path_temp + file, 'r') as f:
            for line in f.readlines():

                #Stop words
                wordList = line.split()
                wordList_filtered = [w for w in wordList if not w in stop_words]

                #Lemmatisation
                wordList_filtered = list(map(wl.lemmatize,wordList_filtered))

                #Construction de l'index
                #termID
                for w in wordList_filtered:
                    dico_termID[termID] = w
                    dico_index[termID] = docID
                    termID += 1

        docID += 1 #Next document


# In[17]:


print(docID)
print(termID)


# In[18]:


print(dico_docID)

