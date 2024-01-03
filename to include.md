THE USE OF REMOVING STOP WORDS IS CURRENTLY IN USE - NEED TO TEST WITH AND WITHOUT

Pre-processing:
- Stop words - from nltk.corpus import stopwords
- Stemming
- Lemmatisation - from nltk.stem import WordNetLemmatizer

Others to definitely include:
- Extra weight to terms including titles, headings, etc
- Query expansion: spelling correction, thesaurus
- Named entities - Chunking

Maybe:
- Document similarity - cosine
- Query expansion: Relevance feedback
- Wildcard queries: k-gram indexes