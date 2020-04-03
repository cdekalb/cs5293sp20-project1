import argparse
import spacy

def getPersonEntities(text):
    redactions = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            redactions.append(ent.end)
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

def redact(wordTokenized, redactions):
    redactedText = ""
    for i in range(len(redactions)):
        wordTokenized[redactions[i] - 1] = u'\u2588'
    for j in range(len(wordTokenized)):
        redactedText = redactedText + wordTokenized[j] + " "
    return redactedText

def main(text):


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, 
        help="Text file on which redactions will be implemented.")
    parser.add_argument("--input", type=str, required=False,
        help="Other files to on which redactions will be implemented")
# TODO: Figure out alternate parsers. Writing method for a flag?
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)