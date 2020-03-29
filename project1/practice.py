import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')
stop = stopwords.words('english')

example = """
On Wednesday, March 18th I called John to let him know that he had a package from Maria that 
arrived on 3/17. Later, I received a message from him saying that he received the package from her.
"""

# Part of speech tags a cleaned text document
def posTag(text):
    # Sentence tokenize the inputted text
    sentTokenized = nltk.sent_tokenize(text = text)
    # Word tokenize the tokenized sentences
    wordTokenized = [nltk.word_tokenize(sent) for sent in sentTokenized]
    # Part of speech tag the word tokenized sentences
    posTagged = [nltk.pos_tag(word) for word in wordTokenized]
    return posTagged

# Redacts the names from the text document
def redactNames(posTaggedDocument):
    for sent in range(len(posTaggedDocument)):
        for word in range(len(posTaggedDocument[sent])):
            if posTaggedDocument[sent][word][1] == "NNP":
                print(posTaggedDocument[sent][word][0])

def entityRecognition(text):
    entityTotal = []
    for sent in range(len(text)):
        pattern = 'NP: {<DT>?<JJ>*<NN>}'
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(text[sent])
        entityTotal.append(cs)
    return entityTotal

def spacyTokenize(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for token in doc:
        print(token.text)


text = strip_html_tags(example)
spacyTokenize(text)
# posTagged = posTag(text)
# entity = entityRecognition(posTagged)
# print(entity)
