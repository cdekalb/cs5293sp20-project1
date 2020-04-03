import re
import nltk
import spacy
# from nltk.corpus import stopwords
# from nltk.tokenize import sent_tokenize
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')
# stop = stopwords.words('english')
# python -m spacy download en_core_web_sm
# python -m spacy download en_core_web_lg

example = """
On Wednesday, March 18th I called John to let him know that he had a package from Maria that 
arrived on 3/17. Later, I received a message from him saying that he received the package from 
her on Thursday.
"""

def wordTokenize(text):

    wordTok = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for token in doc:
        wordTok.append(token.text)

    return wordTok

def getPersonEntities(text):
    # Create empty vector to store the index of the tokenized words that need redacting
    redactions = []

    # Use spacy to perform entity recognition on the tokenized words
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Parse through the found entities
    for ent in doc.ents:
        # Check if the entity is a person
        if ent.label_ == "PERSON":
            # If the entity consists of one or more tokenized words, add each corresponding index 
            # to the redactions list
            for i in range(ent.end - ent.start):
                redactions.append(i + ent.start)

    return redactions

def getDateEntities(text):
    # Create empty vector to store the index of the tokenized words that need redacting
    redactions = []

    # Use spacy to perform entity recognition on the tokenized words
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Parse through the found entities
    for ent in doc.ents:
        # Check if the entity is a date
        if ent.label_ == "DATE":
            # If the entity consists of one or more tokenized words, add each corresponding index 
            # to the redactions list
            for i in range(ent.end - ent.start):
                redactions.append(i + ent.start)

    return redactions

def getGenderedEntities(text):
    # Create empty vector to store the tokenized words that need redacting
    textRedactions = []

    # Create empty vector to store the indeces of the words that need redacting
    redactions = []

    # Remove newline and tab characters so the nlp similarity method will not throw unwanted 
    # errors
    cleanText = text.replace('\n', '')
    cleanText = cleanText.replace('\t', '')

    # Create string of gendered pronouns
    genderPronouns = "he she"

    # Use spacy to perform word tokenization on the cleaned text
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(cleanText)

    # Word tokenize the original text
    originalDoc = nlp(text)

    # Word tokenize the gendered pronouns
    genderDoc = nlp(genderPronouns)

    # Parse through the word tokens of cleaned text
    for token1 in doc:
        # Parse through the word tokens of the gendered pronouns
        for token2 in genderDoc:
            # Check if the similarity of token from text and token from gendered pronouns
            # is above some threshold and the token from text is not already in textRedactions 
            if(token1.similarity(token2) > 0.8 and str(token1) not in textRedactions):
                # Add token from text to textRedactions
                textRedactions.append(str(token1))
    
    # Parse through the word tokens in the original text
    for token in originalDoc:
        # Check if the word is in textRedactions
        if str(token.text) in textRedactions:
            # Append the index of the word to redactions
            redactions.append(token.i)

    return redactions

def combineRedactions(redactions1, redactions2):
    redactions = redactions1 + redactions2
    redactions = list(dict.fromkeys(redactions))
    return redactions

def redact(wordTokenized, redactions):

    # Create empty vector to store text and redacted text
    redactedText = ""

    # Parse through each redaction index
    for i in range(len(redactions)):

        # Create empty vector to store character-for-character full block characters for redacted
        # tokens 
        wordTokChar = ""

        # For each character in the word to be redacted, add a full block character to wordTokChar
        for j in range(len(wordTokenized[redactions[i]])):
            wordTokChar = wordTokChar + u'\u2588'

        # Replace the text to be redacted with wordTokChar
        wordTokenized[redactions[i]] = wordTokChar

    # Parse through each word in the tokenized list
    for k in range(len(wordTokenized)):

        # Concatenate the words to get a string that combines the redacted text and untouched text
        redactedText = redactedText + wordTokenized[k] + " "

    return redactedText

wordTok = wordTokenize(example)
personRedactions = getPersonEntities(example)
dateRedactions = getDateEntities(example)
genderedRedactions = getGenderedEntities(example)
datePersonRedactions = combineRedactions(personRedactions, dateRedactions)
totalRedactions = combineRedactions(genderedRedactions, datePersonRedactions)
text = redact(wordTok, totalRedactions)
print(text)
