import os
import regex as re
import pickle

import pageProcessor
import queryHandler

# Initialises the inverted index and stores it in files
    # Or initialises the inverted index by reading it from files
def init():
    global vocabIndex
    global vocab
    global docIDs
    global docIDsIndex
    global postings
    global totalTerms
    # If the files exist, open and load the inverted index
    if os.path.isfile("vocab.pkl"):
        file = open("vocab.pkl", "rb")
        vocab = pickle.load(file)
        file.close()
        file = open("docIDs.pkl", "rb")
        docIDs = pickle.load(file)
        file.close()
        file = open("postings.pkl", "rb")
        postings = pickle.load(file)
        file.close()
        file = open("totalTerms.pkl", "rb")
        totalTerms = pickle.load(file)
        file.close()
    # If the files don't exist, process each page to initialise the inverted index
    else:
        fileNumber = 1
        for fileName in os.listdir(os.getcwd() + "/videogames"):
            file = open(os.getcwd() + "/videogames/" + fileName, "r", encoding="utf8")
            print(f"{fileNumber}: {fileName} started processing")
            fileContents = file.read()
            file.close()
            docIDs.update({docIDsIndex : fileName})

            fileTokens = pageProcessor.processPage(fileContents)
            totalTerms.update({docIDsIndex : len(fileTokens)})
            for token in fileTokens:
                if token not in vocab:
                    vocab.update({token : vocabIndex})
                    postings.update({vocabIndex : {docIDsIndex : fileTokens[token]}})
                    vocabIndex += 1
                else:
                    vocabID = vocab[token]
                    postings[vocabID].update({docIDsIndex : fileTokens[token]})
            docIDsIndex += 1
            
            file = open("vocab.pkl", "wb")
            pickle.dump(vocab, file)
            file.close()
            file = open("docIDs.pkl", "wb")
            pickle.dump(docIDs, file)
            file.close()
            file = open("postings.pkl", "wb")
            pickle.dump(postings, file)
            file.close()
            file = open("totalTerms.pkl", "wb")
            pickle.dump(totalTerms, file)
            file.close()
            print(f"{fileNumber}: {fileName} finished processing")
            fileNumber += 1

vocab = {} # {term : vocabID}
vocabIndex = 0
docIDs = {} # {docID : docName}
docIDsIndex = 0
postings = {} # {vocabID : {docID : freq, docID: freq}}
totalTerms = {} # {docID : numOfTerms}

init()
while True:
    query = input("Search (0 to quit): ")
    if query == "0": break
    queryHandler.processQuery(query, vocab, postings, docIDs, totalTerms)
