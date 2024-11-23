# Video Game Search Engine
A search engine for searching through web pages containing information about PS2 games. This was programmed in Python using the libraries listed in the Dependencies section. The dataset of web pages are in the videogames folder.

## About
The search engine uses these techniques:
- Removing stop words
- Stemming
- Lemmatisation
- Tf-idf
- Spell checking and correction

## Setup
1. DEPENDENCIES:
    1. pip - `pip install [package]`
        - bs4
        - nltk
        - pyspellchecker
        - numpy
    2. nltk - `nltk.download([module])`:
        - stopwords
        - punkt
        - wordnet
        - averaged_perceptron_tagger
        - universal_tagset
        - maxent_ne_chunker
        - words

2. HOW TO RUN:
    - Run the main.py file.
