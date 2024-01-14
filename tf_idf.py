import math

# Returns dict with format {docID : tf_idf_score}
def getScores(docsFound, totalTerms):
    tf_idf_scores = []

    # numDocsTotal = no of docs in total
        # df = document frequency (no of docs term has occured in)
        # term freq in curr doc * log(numDocsTotal / df) = score
    for docsContaining in docsFound: # {docID : rawTermFreq, docID: rawTermFreq, ...}
        tf_idf_scores.append({})
        for docContaining in docsContaining: # docID
            tf = docsContaining[docContaining]
            tf = 1 + math.log(tf)
            numDocsTotal = 399
            df = len(docsContaining)
            idf = math.log(numDocsTotal / df)
            tf_idf = tf * idf
            tf_idf_scores[len(tf_idf_scores) - 1].update({docContaining : tf_idf})
    
    return tf_idf_scores