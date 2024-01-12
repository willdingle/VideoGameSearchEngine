import os
import pickle

import pageProcessor
import queryHandler

# Initialises the inverted index and stores it in files
    # Or initialises the inverted index by reading it from files
def init():
    global vocab
    global docIDs
    global docInfo
    global postings
    global totalTerms
    # If the files exist, open and load the inverted index
    if os.path.isfile("invertedIndex/vocab.pkl"):
        file = open("invertedIndex/vocab.pkl", "rb")
        vocab = pickle.load(file)
        file.close()
        file = open("invertedIndex/docIDs.pkl", "rb")
        docIDs = pickle.load(file)
        file.close()
        file = open("invertedIndex/postings.pkl", "rb")
        postings = pickle.load(file)
        file.close()
        file = open("invertedIndex/totalTerms.pkl", "rb")
        totalTerms = pickle.load(file)
        file.close()
        file = open("invertedIndex/docInfo.pkl", "rb")
        docInfo = pickle.load(file)
        file.close()

    # If the files don't exist, process each page to initialise the inverted index
    else:
        docIDsIndex = 0
        vocabIndex = 0
        for fileName in os.listdir(os.getcwd() + "/videogames"):
            file = open(os.getcwd() + "/videogames/" + fileName, "r", encoding="utf8")
            print(f"{docIDsIndex + 1}: {fileName} started processing")
            fileContents = file.read()
            file.close()
            docIDs.update({docIDsIndex : fileName})
            docInfo.update({docIDsIndex : pageProcessor.getPageInfo(fileName)})

            fileTokens = pageProcessor.processPage(fileContents)
            fileTokens.update({fileName.split(".", 1)[0] : 1})
            totalTerms.update({docIDsIndex : len(fileTokens)})
            for token in fileTokens:
                if token not in vocab:
                    vocab.update({token : vocabIndex})
                    postings.update({vocabIndex : {docIDsIndex : fileTokens[token]}})
                    vocabIndex += 1
                else:
                    vocabID = vocab[token]
                    postings[vocabID].update({docIDsIndex : fileTokens[token]})
            print(f"{docIDsIndex + 1}: {fileName} finished processing")
            docIDsIndex += 1
            
        file = open("invertedIndex/vocab.pkl", "wb")
        pickle.dump(vocab, file)
        file.close()
        file = open("invertedIndex/docIDs.pkl", "wb")
        pickle.dump(docIDs, file)
        file.close()
        file = open("invertedIndex/postings.pkl", "wb")
        pickle.dump(postings, file)
        file.close()
        file = open("invertedIndex/totalTerms.pkl", "wb")
        pickle.dump(totalTerms, file)
        file.close()
        file = open("invertedIndex/docInfo.pkl", "wb")
        pickle.dump(docInfo, file)
        file.close()
        

vocab = {} # {term : vocabID}
docIDs = {} # {docID : docName}
postings = {} # {vocabID : {docID : freq, docID: freq}}
docInfo = {} # {docID : [rating, publisher, genre, developer]}
totalTerms = {} # {docID : numOfTerms}

init()
while True:
    query = input("Search (0 to quit): ")
    print()
    if query == "0": break
    queryHandler.processQuery(query, vocab, postings, docIDs, totalTerms, docInfo)
