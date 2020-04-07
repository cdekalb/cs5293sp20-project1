import argparse
import re
import spacy
import glob
from pathlib import Path
import os

def readTextFile(textFile):
    # Open the contents of the inputted file
    inputFile = open('project1/' + str(textFile), mode = "r")

    # Read the contents of the text file
    text = inputFile.read()

    return text

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
    if len(redactions1) != 0 and len(redactions2) != 0:
        # Concatenate the redaction indices
        redactions = redactions1[0] + redactions2[0]

        # Remove duplicates using a dictionary
        uniqueRedactions = list(dict.fromkeys(redactions))

        numCopies = len(redactions) - len(uniqueRedactions)

        # Calculate the total number of redactions for the text without duplicates
        numRedactions = redactions1[1] + redactions2[1] - numCopies

    elif len(redactions1) == 0 and len(redactions2) != 0:
        # Concatenate the redaction indices
        redactions = redactions2[0]

        # Remove duplicates using a dictionary
        uniqueRedactions = list(dict.fromkeys(redactions))

        numCopies = len(redactions) - len(uniqueRedactions)

        # Calculate the total number of redactions for the text without duplicates
        numRedactions = redactions2[1] - numCopies

    elif len(redactions2) == 0 and len(redactions1) != 0:
        # Concatenate the redaction indices
        redactions = redactions1[0]

        # Remove duplicates using a dictionary
        uniqueRedactions = list(dict.fromkeys(redactions))

        numCopies = len(redactions) - len(uniqueRedactions)

        # Calculate the total number of redactions for the text without duplicates
        numRedactions = redactions1[1] - numCopies

    else:
        uniqueRedactions = []
        numRedactions = 0

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
            wordTokChar = wordTokChar + '_'

        # Replace the text to be redacted with wordTokChar
        wordTokenized[redactions[0][i]] = wordTokChar

    # Parse through each word in the tokenized list
    for k in range(len(wordTokenized)):

        # Concatenate the words to get a string that combines the redacted text and untouched text
        redactedText = redactedText + wordTokenized[k] + " "

    return redactedText, redactions[1]

def main(inputFile, names, dates, gender, concept, conceptId, stats, output, outputPath):
    # Read in the text file
    text = readTextFile(inputFile)

    # Word tokenize the text
    wordTok = wordTokenize(text)

    # If names flag is given
    if names:
        # Get the person entities and corresponding indices of the redactions
        personRedactions = getPersonEntities(text)

        # Get the number of name redactions
        numPersonRedactions = personRedactions[1]
    else:
        # Leave name redactions object empty
        personRedactions = []

    # If dates flag is given
    if dates:
        # Get the date entities and corresponding indices of the redactions
        dateRedactions = getDateEntities(text)

        # Get the number of date redactions
        numDateRedactions = dateRedactions[1]
    else:
        # Leave date redactions object empty
        dateRedactions = []

    # If gender flag is given
    if gender:
        # Get the gendered words and corresponding indices of the redactions
        genderedRedactions = getGenderedEntities(text)

        # Get the number of gendered word redactions
        numGenderedRedactions = genderedRedactions[1]
    else:
        # Leave gendered words object empty
        genderedRedactions = []
    
    # If concept flag is given
    if concept:
        # Get the concept words and corresponding indices of the redactions
        conceptRedactions = getConcept(inputFile, conceptId)

        # Get the number of concept word redactions
        numConceptRedactions = conceptRedactions[1]
    else:
        # Leave the concept words object empty
        conceptRedactions = []
    
    # Combine the date and person redaction lists
    datePersonRedactions = combineRedactions(personRedactions, dateRedactions)

    # Combine the gender and concept redaction lists
    genderConceptRedactions = combineRedactions(genderedRedactions, conceptRedactions)

    # Combine all of the redaction lists
    totalRedactions = combineRedactions(genderConceptRedactions, datePersonRedactions)

    # Perform the redaction
    finalRedactions = redact(wordTok, totalRedactions)

    # If output flag is given
    if output:
        # Add the required file extension for the redactions to be saved in
        outputFileName = inputFile + ".redacted"

        # Get the path of the main file
        pathName = os.path.dirname(os.path.realpath("project1/main.py"))

        # Create the path into which the redacted files will be saved
        completeSavePath = os.path.join(pathName, outputPath, outputFileName)

        # Open a newly created file
        file1 = open(completeSavePath, "w")

        # Write the redacted text
        file1.write(str(finalRedactions[0]))

        # If stats flag is given
        if stats:
            # Create strings that provide the given stats
            personStr = "\nNumber of name redactions: " + str(numPersonRedactions) + "\n"
            dateStr = "Number of date redactions: " + str(numDateRedactions) + "\n"
            genderStr = "Number of genedered word redactions: " + str(numGenderedRedactions) + "\n"
            conceptStr = "Number of concept redactions: " + str(numConceptRedactions) + "\n"
            totalRedactStr = "Total number of redactions: " + str(finalRedactions[1]) + "\n"

            # Write each of the stats strings to the file
            file1.write(personStr)
            file1.write(dateStr)
            file1.write(genderStr)
            file1.write(conceptStr)
            file1.write(totalRedactStr)

        # Close the file
        file1.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # Add the required parser arguments
    parser.add_argument("--input", type=str, required=True, nargs='+',
        help="Text files on which redactions will be implemented.")
    parser.add_argument("--names", action='store_true', help="Chosen if names are to be redacted")
    parser.add_argument("--dates", action='store_true', help="Chosen if dates are to be redacted")
    parser.add_argument("--gender", action='store_true', help="Chosen if gendered words are to be redacted")
    parser.add_argument("--concept", type=str, help="Chosen if a concept is to be redacted")
    parser.add_argument("--output", type=str, required=True,
    help="The path of the program output")
    parser.add_argument("--stats", action='store_true', 
    help="Chosen if resulting statistics are desired")

    args = parser.parse_args()

    # For the flags provided, set their corresponding boolean variables to true
    if args.names:
        names = True
    else:
        names = False

    if args.dates:
        dates = True
    else:
        dates = False
    
    if args.gender:
        gender = True
    else:
        gender = False

    if args.concept:
        concept = True
        # Store the conceptId
        conceptId = args.concept[0]
    else:
        concept = False
        # Leave the conceptId empty
        conceptId = ''

    if args.output:
        output = True
        # Store the provided output path
        outputPath = str(args.output)
    else:
        output = False
        # Leave the output path empty
        outputPath = ''

    if args.stats:
        stats = True
    else:
        stats = False

    if args.input:
        # Create empty list to store the inputted files
        files = []

        # Add the inputted files to the list
        for path in Path('project1').rglob(str(args.input[0])):
            files.append(path.name)

        # Parse through the inputted files
        for f in files:
            main(f, names, dates, gender, concept, conceptId, stats, output, outputPath)