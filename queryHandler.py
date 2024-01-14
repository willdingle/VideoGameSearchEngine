import regex as re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from nltk import ne_chunk, pos_tag
import os

import tf_idf

def getDocIDs(term, vocab, postings):
    if term in vocab:
        vocabID = vocab[term]
        docsContaining = postings[vocabID]
        return docsContaining
    return False

def spellCheck(term):
    checker = SpellChecker()
    correctedTerm = checker.correction(term)
    
    if "-" in term and term != correctedTerm: 
        dashIndex = term.index("-")
        correctedTerm = correctedTerm[0 : dashIndex] + "-" + correctedTerm[dashIndex : len(term)]

    if correctedTerm != term:
        choice = "a"
        while choice != "Y" and choice != "N":
            choice = input("Instead of " + term + ", did you mean " + correctedTerm + "(Y/N)? ").upper()
        if choice == "N":
            return term

    if term != correctedTerm: print("Corrected term", term, "to", correctedTerm)
    return correctedTerm

def entityRecog(terms):
    speechTags = pos_tag(terms, tagset="universal")
    namedEntities = ne_chunk(speechTags)
    print(namedEntities)

def processQuery(query, vocab, postings, docIDs, totalTerms, docInfo):
    stops = set(stopwords.words("english"))
    lemmer = WordNetLemmatizer()

    queryRaw = query
    #entityRecog(queryRaw.split(" ")) #Named Entity Recognition on the query terms
    query = query.lower()
    query = re.sub(r"[^A-Za-z0-9- ]+", "", query)
    # Splits search query into terms and gets doc IDs of docs containing each term
    queryTerms = query.split(" ")
    docsFound = [] # [{docID : rawTermFreq}, {docID : rawTermFreq}, ...]
    for term in queryTerms:
        term = spellCheck(term) #Spell check term
        if term not in stops:
            term = lemmer.lemmatize(term) #Lemmatise term
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
    docsContainingAll = {} #{docID : tf_idf}
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

    # Factor in relevance feedback
    if os.path.isfile("relFeedback.txt"):
        file = open("relFeedback.txt", "r")
        contents = file.read()
        file.close()
        lines = contents.split("\n")
        for line in lines:
            if line != "":
                parts = line.split(",") #[query, doc]
                parts[1] = int(parts[1])
                if parts[0] == query:
                    if parts[1] in docsContainingAll:
                        docsContainingAll[parts[1]] += 100
                    else:
                        docsContainingAll.update( {parts[1] : 100} )

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