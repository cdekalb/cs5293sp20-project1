# Test to validate word tokenization

import project1
from project1 import main

def test_word_tokenize():
    text = "Matthew Mark Luke John"
    wordTok = project1.main.wordTokenize(text)
    assert wordTok != None, "Should not be empty"