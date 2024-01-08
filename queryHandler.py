import regex as re

import tf_idf

def getDocIDs(term, vocab, postings):
    if term in vocab:
        vocabID = vocab[term]
        docsContaining = postings[vocabID]
        return docsContaining
    return False

def processQuery(query, vocab, postings, docIDs, totalTerms):
    queryRaw = query
    query = query.lower()
    query = re.sub(r"[^A-Za-z0-9- ]+", "", query)
    # Splits search query into terms and gets doc IDs of docs containing each term
    queryTerms = query.split(" ")
    docsFound = [] # [{docID : rawTermFreq}, {docID : rawTermFreq}, ...]
    for term in queryTerms:
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

    #Display results and save them to a file
    file = open("results.txt", "a")
    print("----- " + queryRaw + " -----")
    file.write("----- " + queryRaw + " -----\n")
    resultsDisp = 0
    for docID in docsContainingAll:
        if docsContainingAll[docID] == 0: break
        resultsDisp += 1
        currentResult = str(resultsDisp) + ". " + docIDs[docID] + "\t" + str(docsContainingAll[docID])
        print(currentResult)
        file.write(currentResult + "\n")
        if resultsDisp == 10: break
    print("")
    file.write("\n")
    file.close()