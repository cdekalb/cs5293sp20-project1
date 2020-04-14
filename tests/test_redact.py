# Test to validate redactions

import project1
from project1 import main

def test_redact():
    wordTok = ['Matthew', ',', 'Mark', ',', 'Luke', ',', 'John']
    redactions = [[0, 2, 4, 6], 4]
    redactedText = project1.main.redact(wordTok, redactions)
    assert redactedText != None, "Should not be empty"