from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import regex as re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Process contents of html file and return the tokens
def processPage(page):
    stops = set(stopwords.words("english"))
    lemmer = WordNetLemmatizer()

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
                word = lemmer.lemmatize(word)
                if word not in cleanedTokens:
                    cleanedTokens.update( {word : 1} )
                else:
                    cleanedTokens[word] += 1
    return cleanedTokens

# Get information about the page from the videogame-labels.csv file
def getPageInfo(fileName):
    file = open("videogame-labels.csv", "r")
    contents = file.read()
    file.close()

    lines = contents.split("\n")
    for line in lines:
        info = line.split(",")
        if info[0] == "url": continue

        url = info[0].split("/")[2] #url = name of the page (e.g. game.html)
        if url == fileName:
            return [info[1], info[2], info[3], info[4]] #[rating, publisher, genre, developer]
        
    raise Exception("File not found in details csv")