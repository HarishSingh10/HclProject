import pytest
import json
from unittest.mock import patch, MagicMock

import nlp_engine

def test_preprocess_text():
    """Test that text preprocessing normalizes strings properly."""
    raw_text = "Hello World!!! This is a TEST. \n  Let's see: 123"
    processed = nlp_engine.preprocess_text(raw_text)
    
    # "hello world this is a test let s see 123"
    assert "hello world" in processed
    assert "this is a test" in processed
    assert "let s see 123" in processed
    assert "!" not in processed

def test_preprocess_text_empty():
    """Test that empty or NaN values safely return empty string."""
    assert nlp_engine.preprocess_text("") == ""
    assert nlp_engine.preprocess_text(None) == ""

@patch("nlp_engine.client.chat.completions.create")
def test_generate_ai_resolution_valid(mock_create):
    """Test that AI resolutions parse JSON array back cleanly when API succeeds."""
    
    # Mock the returned API payload from Groq
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '["Fix one", "Fix two", "Fix three", "Fix four", "Fix five"]'
    mock_create.return_value = mock_response
    
    historical_data = [
        {"description": "My screen is black", "resolution_text": "Check monitor power"}
    ]
    
    result_json = nlp_engine.generate_ai_resolution("Screen is totally off.", historical_data)
    
    # We expect our JSON string list back
    result_list = json.loads(result_json)
    
    assert isinstance(result_list, list)
    assert len(result_list) == 5
    assert result_list[0] == "Fix one"

@patch("nlp_engine.client.chat.completions.create")
def test_generate_ai_resolution_fallback(mock_create):
    """Test that the engine catches exceptions safely and returns a friendly fallback message list."""
    # Force an exception (like API timeout or bad credentials)
    mock_create.side_effect = Exception("Groq backend is down")
    
    result_json = nlp_engine.generate_ai_resolution("The network is down.", [])
    result_list = json.loads(result_json)
    
    assert isinstance(result_list, list)
    assert "Our automated assistant is temporarily unavailable." in result_list[0]
