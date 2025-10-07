from unittest.mock import patch
from backend.services.custom_llm import LlamaServerLLM

@patch('requests.post')
def test_llama_server_llm_call(mock_post):
    """Test the _call method of the LlamaServerLLM."""
    mock_post.return_value.raise_for_status.return_value = None
    mock_post.return_value.json.return_value = {
        'choices': [{'message': {'content': 'Test response'}}]
    }

    llm = LlamaServerLLM()
    prompt = "Test prompt"
    response = llm._call(prompt)

    assert response == "Test response"
    mock_post.assert_called_once()
    # Further assertions can be made on the payload of the request
