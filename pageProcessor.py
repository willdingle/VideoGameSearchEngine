from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import regex as re
from nltk.corpus import stopwords

# Process contents of html file and return the tokens
def processPage(page):
    stops = set(stopwords.words("english"))

    # Parse html using beautifulsoup
    soup = BeautifulSoup(page, "html.parser")
    # Find all div elements
    divs = soup.find_all("div")
    cleanedTokens = {}
    # Go through each paragraph and remove punctuation, convert to lowercase
    for div in divs:
        cleanedDivs = div.get_text()
        reText = re.sub(r"[^A-Za-z0-9- ]+", "", str(cleanedDivs))
        words = word_tokenize(reText)
        for word in words:
            word = word.lower()
            if word not in stops:
                if word not in cleanedTokens:
                    cleanedTokens.update( {word : 1} )
                else:
                    cleanedTokens[word] += 1
    return cleanedTokens