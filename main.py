import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import regex as re
from bs4 import BeautifulSoup
import pickle

import tf_idf

def init():
    global vocabIndex
    global vocab
    global docIDs
    global docIDsIndex
    global postings
    global totalTerms
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
    else:
        fileNumber = 1
        for fileName in os.listdir(os.getcwd() + "/videogames"):
            file = open(os.getcwd() + "/videogames/" + fileName, "r", encoding="utf8")
            print(f"{fileNumber}: {fileName} started processing")
            fileContents = file.read()
            file.close()
            docIDs.update({docIDsIndex : fileName})

            fileTokens = processPage(fileContents)
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

# Process contents of html file and return the tokens
def processPage(page):
    stops = set(stopwords.words("english"))
    # Parse html using beautifulsoup
    soup = BeautifulSoup(page, "html.parser")
    # Find all div elements
    paras = soup.find_all("div")
    cleanedTokens = {}
    # Go through each paragraph and remove punctuation, convert to lowercase and remove stopwords
    for p in paras:
        cleanedParas = p.get_text()
        reText = re.sub(r"[^A-Za-z ]-+", "", str(cleanedParas))
        words = word_tokenize(reText)
        for word in words:
            word = word.lower()
            if word not in stops:
                if word not in cleanedTokens:
                    cleanedTokens.update( {word : 1} )
                else:
                    cleanedTokens[word] += 1
    return cleanedTokens

def getDocIDs(term):
    if term in vocab:
        vocabID = vocab[term]
        docsContaining = postings[vocabID]
        return docsContaining
    return False

def processQuery(query):
    query = re.sub(r"[^A-Za-z ]-+", "", query)
    # Splits search query into terms and gets doc IDs of docs containing each term
    queryTerms = query.split(" ")
    docsFound = [] # [{docID : rawTermFreq}, {docID : rawTermFreq}, ...]
    for term in queryTerms:
        getIDsResult = getDocIDs(term)
        if (getIDsResult):
            docsFound.append(getIDsResult)
    if len(docsFound) == 0:
        print("----- " + query + " -----")
        print("NO RESULTS")
        return
    
    tf_idf_scores = tf_idf.getScores(docsFound, totalTerms) # [{docID : tf_idf, ...}, ...]

    # Finds and prints docs where all terms are found
    docsContainingAll = {}
    if len(tf_idf_scores) == 2:
        for docID in tf_idf_scores[0]:
            if docID in tf_idf_scores[1]:
                docsContainingAll.update({docID : tf_idf_scores[0][docID] + tf_idf_scores[1][docID]})
    elif len(tf_idf_scores) > 2:
        for docID in tf_idf_scores[0]:
            if docID in tf_idf_scores[1]:
                docsContainingAll.update({docID : tf_idf_scores[0][docID] + tf_idf_scores[1][docID]})
        for i in range(2, len(tf_idf_scores)):
            for docID in tf_idf_scores[i]:
                if docID in docsContainingAll:
                    docsContainingAll.update({docID : tf_idf_scores[i][docID] + docsContainingAll[docID]})
    else:
        docsContainingAll = tf_idf_scores[0]

    docsContainingAllTemp = sorted(docsContainingAll.items(), key=lambda x:x[1], reverse=True)
    docsContainingAll = dict(docsContainingAllTemp)
    print("----- " + query + " -----")
    resultsDisp = 0
    for docID in docsContainingAll:
        print(docIDs[docID], ":", docsContainingAll[docID])
        resultsDisp += 1
        if resultsDisp == 10: break

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
    processQuery(query)
