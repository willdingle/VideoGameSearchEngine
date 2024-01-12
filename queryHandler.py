import regex as re
from nltk.corpus import stopwords
from nltk import PorterStemmer

import tf_idf

def getDocIDs(term, vocab, postings):
    if term in vocab:
        vocabID = vocab[term]
        docsContaining = postings[vocabID]
        return docsContaining
    return False

def processQuery(query, vocab, postings, docIDs, totalTerms, docInfo):
    stops = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    queryRaw = query
    query = query.lower()
    query = re.sub(r"[^A-Za-z0-9- ]+", "", query)
    # Splits search query into terms and gets doc IDs of docs containing each term
    queryTerms = query.split(" ")
    docsFound = [] # [{docID : rawTermFreq}, {docID : rawTermFreq}, ...]
    for term in queryTerms:
        if term not in stops:
            term = stemmer.stem(term) #Stem term
            getIDsResult = getDocIDs(term, vocab, postings)
            if (getIDsResult):
                docsFound.append(getIDsResult)
    if len(docsFound) == 0:
        print("----- " + queryRaw + " -----")
        print("NO RESULTS")
        print("")
        file = open("results.txt", "a")
        file.write("----- " + queryRaw + " -----\n")
        file.write("NO RESULTS\n\n")
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

    # Sort results by descending tf-idf score
    docsContainingAllTemp = sorted(docsContainingAll.items(), key=lambda x:x[1], reverse=True)
    docsContainingAll = dict(docsContainingAllTemp)

    # Display results and save them (and the average of the tf-idf scores) to a file
    file = open("results.txt", "a")
    print("----- " + queryRaw + " -----")
    print("RANKING | DOCNAME | RATING | PUBLISHER | GENRE | DEVELOPER")
    file.write("----- " + queryRaw + " -----\n")
    file.write("RANKING | DOCNAME | RATING | PUBLISHER | GENRE | DEVELOPER\n")
    resultsDisp = 0
    sumTfIdf = 0
    for docID in docsContainingAll:
        if docsContainingAll[docID] == 0: break
        resultsDisp += 1
        sumTfIdf += docsContainingAll[docID]
        currentResult = str(resultsDisp) + ". " + str(docIDs[docID]) + " | " + str(docInfo[docID][0]) + " | " + str(docInfo[docID][1]) + " | " + str(docInfo[docID][2]) + " | " + str(docInfo[docID][3]) + " | " + str(docsContainingAll[docID])
        print(currentResult)
        file.write(currentResult + "\n")
        if resultsDisp == 10: break
    avgTfIdf = sumTfIdf / resultsDisp
    print("")
    file.write("Average tf-idf: " + str(avgTfIdf) + "\n\n")
    file.close()