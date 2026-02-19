# Intentional bugs for AI agent to detect and fix

import os  # Unused import (LINTING bug)

def add_numbers(a, b): # Missing colon (SYNTAX bug)
    return a + b

def test_addition():
    assert add_numbers(2, 3) == 5
