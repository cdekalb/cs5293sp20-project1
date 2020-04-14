# Test to validate date recognition

import project1
from project1 import main

def test_dates():
    text = "Monday, Tuesday, Wednesday"
    dates = project1.main.getDateEntities(text)
    assert dates != None, "Should not leave out any dates"