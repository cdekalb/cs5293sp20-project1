# Test to validate concept recognition

import project1
from project1 import main

def test_concept():
    text = "babies children kids"
    conceptWords = project1.main.getConcept(text, "kids")
    assert conceptWords != None, "Should not leave out any words related to the concept"