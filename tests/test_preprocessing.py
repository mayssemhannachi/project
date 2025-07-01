import pytest
import warnings
from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

from scripts.preprocessing import preprocess_text

@pytest.mark.parametrize("input_text,expected", [
    ("This is a TEST.", "test"),  # Lowercase, stopword removal
    ("<b>Hello</b> world!", "hello world"),  # HTML removal, punctuation
    ("Visit http://example.com now!", "visit"),  # URL removal
    ("Numbers 123 and symbols #!$", "number symbol"),  # Numbers/symbols removal
    ("Cats are running", "cat running"),  # Lemmatization (cat)
    ("", ""),  # Empty string
    (None, ""),  # None input
])
def test_preprocess_text(input_text, expected):
    assert preprocess_text(input_text) == expected