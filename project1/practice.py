import re
import spacy
import glob
from pathlib import Path
# python -m spacy download en_core_web_sm
# python -m spacy download en_core_web_lg

example = """
On Wednesday, March 18th I called John to let him know that he had a package from Maria that 
arrived on 3/17. Later, I received a message from him saying that he received the package from 
her on Thursday. Maria's husband is caring for their children right now. John's wife works with 
babies.
"""

def wordTokenize(text):
    # Create an empty list to store the word tokens
    wordTok = []

    # Use spacy to word tokenize the text
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Iteratively store the word tokens to wordTok
    for token in doc:
        wordTok.append(token.text)

    return wordTok

def getPersonEntities(text):
    # Create empty vector to store the index of the tokenized words that need redacting
    redactions = []

    # Keep track of how many redactions occur
    numRedactions = 0

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
            
            # Increase the number of redactions by 1
            numRedactions = numRedactions + 1

    return redactions, numRedactions

def getDateEntities(text):
    # Create empty vector to store the index of the tokenized words that need redacting
    redactions = []

    # Keep track of how many redactions occur
    numRedactions = 0

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
            
            # Increase the number of redactions by 1
            numRedactions = numRedactions + 1

    return redactions, numRedactions

def getGenderedEntities(text):
    # Create empty vector to store the tokenized words that need redacting
    textRedactions = []

    # Create empty vector to store the indeces of the words that need redacting
    redactions = []

    # Keep track of how many redactions occur
    numRedactions = 0

    # Remove newline and tab characters so the nlp similarity method will not throw unwanted 
    # errors
    cleanText = text.replace('\n', '')
    cleanText = cleanText.replace('\t', '')

    # Create string of gendered pronouns
    genderPronouns = "he she man woman"

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

            # Increase the number of redactions by 1
            numRedactions = numRedactions + 1

    return redactions, numRedactions

def getConcept(text, concept):
    # Create empty vector to store the tokenized words that need redacting
    textRedactions = []

    # Create empty vector to store the indeces of the words that need redacting
    redactions = []

    # Keep track of how many redactions occur
    numRedactions = 0

    # Remove newline and tab characters so the nlp similarity method will not throw unwanted 
    # errors
    cleanText = text.replace('\n', '')
    cleanText = cleanText.replace('\t', '')

    # Create string object to store the concept
    concept = str(concept)

    # Use spacy to perform word tokenization on the cleaned text
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(cleanText)

    # Word tokenize the original text
    originalDoc = nlp(text)

    # Word tokenize the gendered pronouns
    conceptDoc = nlp(concept)

    # Parse through the word tokens of cleaned text
    for token1 in doc:
        # Parse through the word tokens of the gendered pronouns
        for token2 in conceptDoc:
            # Check if the similarity of token from text and token from gendered pronouns
            # is above some threshold and the token from text is not already in textRedactions 
            if(token1.similarity(token2) > 0.65 and str(token1) not in textRedactions):
                # Add token from text to textRedactions
                textRedactions.append(str(token1))
    
    # Parse through the word tokens in the original text
    for token in originalDoc:
        # Check if the word is in textRedactions
        if str(token.text) in textRedactions:
            # Append the index of the word to redactions
            redactions.append(token.i)

            # Increase the number of redactions by 1
            numRedactions = numRedactions + 1

    return redactions, numRedactions

def combineRedactions(redactions1, redactions2):
    # Concatenate the redaction indices
    redactions = redactions1[0] + redactions2[0]

    # Remove duplicates using a dictionary
    uniqueRedactions = list(dict.fromkeys(redactions))

    numCopies = len(redactions) - len(uniqueRedactions)

    # Calculate the total number of redactions for the text without duplicates
    numRedactions = redactions1[1] + redactions2[1] - numCopies

    return uniqueRedactions, numRedactions

def redact(wordTokenized, redactions):

    # Create empty vector to store text and redacted text
    redactedText = ""

    # Parse through each redaction index
    for i in range(len(redactions[0])):

        # Create empty vector to store character-for-character full block characters for redacted
        # tokens 
        wordTokChar = ""

        # For each character in the word to be redacted, add a full block character to wordTokChar
        for j in range(len(wordTokenized[redactions[0][i]])):
            wordTokChar = wordTokChar + u'\u2588'

        # Replace the text to be redacted with wordTokChar
        wordTokenized[redactions[0][i]] = wordTokChar

    # Parse through each word in the tokenized list
    for k in range(len(wordTokenized)):

        # Concatenate the words to get a string that combines the redacted text and untouched text
        redactedText = redactedText + wordTokenized[k] + " "

    return redactedText, redactions[1]

def readTextFile(textFile):
    # Open the contents of the inputted file
    inputFile = open('project1/' + str(textFile), mode = "r")

    # Read the contents of the text file
    text = inputFile.read()

    return text

example = readTextFile('example.txt')
wordTok = wordTokenize(example)
personRedactions = getPersonEntities(example)
dateRedactions = getDateEntities(example)
genderedRedactions = getGenderedEntities(example)
conceptRedactions = getConcept(example, "kids")
datePersonRedactions = combineRedactions(personRedactions, dateRedactions)
genderConceptRedactions = combineRedactions(genderedRedactions, conceptRedactions)
totalRedactions = combineRedactions(genderConceptRedactions, datePersonRedactions)
finalRedactions = redact(wordTok, totalRedactions)
print(finalRedactions[0])
print(finalRedactions[1])
