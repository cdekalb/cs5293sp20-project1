# Test to validate gendered word recognition

import project1
from project1 import main

def test_gender():
    text = "he she him her"
    genderedWords = project1.main.getGenderedEntities(text)
    assert genderedWords == 4, "Should not leave out any gendered words"