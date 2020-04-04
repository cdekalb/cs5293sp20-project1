# Test to validate date recognition

import project1
from project1 import main

def test_dates():
    text = "Monday, Tuesday, Wednesday"
    dates = project1.main.getDateEntities(text)
    assert len(dates) == 3, "Should not leave out any dates"