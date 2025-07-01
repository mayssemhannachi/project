import pytest
from scripts.nlp_pipeline import nlp_process

@pytest.mark.parametrize("text,expected_lang,expected_sentiment", [
    ("I love this!", "en", "positive"),
    ("I hate this!", "en", "negative"),
    ("This is okay.", "en", "positive"),  
    ("C'est une belle journée.", "fr", "neutral"),  
    ("", "unknown", "neutral"),
])
def test_nlp_process(text, expected_lang, expected_sentiment):
    result = nlp_process(text)
    # Language detection is not always perfect, so we check if it starts with the expected code
    if expected_lang != "unknown":
        assert result["language"].startswith(expected_lang)
    else:
        assert result["language"] == "unknown"
    assert result["sentiment"] == expected_sentiment
    assert isinstance(result["sentiment_score"], float)