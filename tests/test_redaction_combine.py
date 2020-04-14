# Test to validate redaction combination

import project1
from project1 import main

def test_redaction_combine():
    redaction1 = [[0, 1, 2], 3]
    redaction2 = [[3, 4, 5], 3]
    totalRedactions = project1.main.combineRedactions(redaction1, redaction2)
    assert totalRedactions[1] == 6, "Should not leave out any redaction indeces"