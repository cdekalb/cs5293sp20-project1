# Project 1

Class:
CS 5293

Author:
Creighton DeKalb

# Project Summary

The purpose of this project was to take in any number of .txt files and redact certain words in the text depending on whether those words are dates, names, gendered, or are associated with some concept. The project used the spaCy library to perform the heavylifting by using entity recognition and word association through vector similarity.

# Installing

In order to run this project, the user needs to install pipenv. This can be done in the command line using the command:

    pipenv install

The spaCy library also needs to be installed and can be done so with the command:

    pipenv install spacy

Two other libraries are required to be downloaded for spaCy to be able to work with the English language. Those libraries can be downloaded with the commands:

    python -m spacy download en_core_web_sm
    python -m spacy download en_core_web_lg

# Prerequisites

To access the project, the user must navigate to the command line and run the command:

    git clone https://github.com/cdekalb/cs5293sp20-project1.git

# Tests

There are seven test files in the project: 
- test_concept.py

The concept test uses a provided string of words. The test generates a list of tokens to redact and asserts that the list is not empty.

- test_dates.py

The dates test uses entity recognition to find the dates in a provided string and then generates a list of tokens to redact and asserts that the list has length 3.

- test_gender.py

The gender test uses the getGenderEntities method in main.py to find the gendered words in a provided string. The test then generate a list of tokens to redact and asserts the list has length 4.

- test_names.py

The names test uses the getPersonEntities method in main.py to find the names in a provided string. The test then generates a list of tokens to redact and asserts the list has length 4.

- test_redact.py

The redact test uses the redact method in main.py to redact certain tokens from a given list. The test asserts that the produced redacted text is not empty.

- test_redaction_combine.py

The redaction combine test uses the combineRedactions method in main.py to combine two lists and remove duplicates. The test asserts that the total number of redactions for the provided redaction lists is 6.

- test_word_tokenize.py

The word tokenize test uses the wordTokenize method to word tokenize a given string.The test asserts that the produced list of word tokens is not empty.

To run the tests, the user must navigate to the command line and run the command:

    pipenv run python -m pytest

# Deployment

The main file takes in an input file from the working directory, redacts the names, dates, gendered words, and words relating to a given concept. All redactions are contingent on the existence of their corresponding flags in the main command. Then the main file outputs the redacted text into its own file, and places the newly redacted file into the files folder in the working directory.

The main file is split up into eight methods, not including the main method. The execution and explanation for these methods are as follows:

- readTextFile(textFile)

The readTextFile method takes in a path to a readable .txt file and reads it into a string.

- wordTokenize(text)

The wordTokenize method takes in a string of text and performs word tokenization. The method returns a list, where each index of the list contains each word token.

- getPersonEntities(text)

The getPersonEntities method takes in a string of text, word tokenizes it, and performs entity recognition to find the entities with the label 'PERSON.' Then the method stores the index of the entity to a redactions list. The method returns the list of redactions and the number of redactions that occurred.

- getDateEntities(text)

The getDateEntities method takes in a string of text, word tokenizes it, and performs entity recognition to find the entities with the label 'DATE.' Then the method stores the index of the entity to a redactions list. The method returns the list of redactions and the number of redactions that occurred.

- getGenderedEntities(text)

The getGenderedEntities method takes in a string of text, word tokenizes it, then checks the similarity of each token in the inputted text with a list of gendered pronouns. If the similarity of a token from the inputted text and a token from the gendered pronouns is above 0.8, the method will add the token from the input text to the redactions list. The method returns the redactions list and the number of redactions. The value of 0.8 was chosen based on initial testing showing that most gendered words would become redacted while not redacting any non-gendered words.

- getConcept(text, concept)

The getConcept method takes in a string of text and a concept, then word tokenizes the string, and the checks the similarity of each token in the inputted text with the inputted concept. If the similarity of a token from the inputted text and the concept is above 0.65, the method will add the token from the input text to the redactions list. The method returns the redactions list and the number of redactions. The value of 0.65 was chosen based on initial testing showing that most words related to the concept would become redacted while not redacting any words not related to the conceot.

- combineRedactions(redactions1, redactions2)

The combineRedactions method takes in two redactions lists and combines the lists while removing any duplicates. The method returns the list of unique redactions and the total number of redactions.

- redact(wordTokenized, redactions)

The redact method takes in a word tokenized list and a redactions list. The method then redacts each token in the word tokenized list according to which indices are in the redactions list. The method returns the redacted text and the number of redactions that occurred.

To run the code, navigate from the command line to the cs5293sp20-project1 directory in which all the project files exist. In the command line, enter the following:

    pipenv run python project1\main.py --input '*.txt' --dates --names --gender --concept <concept> --output 'files\' --stats

The dates, names, gender, concept, and stats flags are all optional.

This command will run the main.py file in the project1 directory, with the arguments '--input', to give the list of files to be redacted, and '--output', to give the required directory into which the redacted files will be stored.

# Assumptions and Bugs

## For this project, a few assumptions were made:

   1: The provided text does not contain html tags, or anything similar. The input files should be human readable text.

   2: The dates that are being redacted do not appear in the MM/DD/YYYY format or similar numbered formats. This is because spaCy's entity recognition comprehends those dates as numbered values and not dates.

   3: All newline characters in the input text have a preceding space character.

## Bugs

If the provided text contains extra whitespace besides newlines, the code will run, but an error will appear in the command line saying that the code is trying to perform vector similarity on an empty value. This occurs from the gender and concept recognition methods. However, it should not affect the redacted text files.

## Notes

Due to time constraints, I elected to leave out the second input flag that reads files ending in .md from the otherfiles file.