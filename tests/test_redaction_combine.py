# Test to validate redaction combination

import project1
from project1 import main

def test_gender():
    redaction1 = [0, 1, 2]
    redaction2 = [3, 4, 5]
    totalRedactions = project1.main.combineRedactions(redaction1, redaction2)
    assert len(totalRedactions) == 6, "Should not leave out any redaction indeces"