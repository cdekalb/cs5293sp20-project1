# Test to validate name recognition

import project1
from project1 import main

def test_names():
    text = "Matthew, Mark, Luke, John"
    names = project1.main.getPersonEntities(text)
    assert names != None, "Should not be empty"