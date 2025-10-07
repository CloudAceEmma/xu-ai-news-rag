import re
from langchain_core.language_models.llms import LLM
from typing import Any, List, Mapping, Optional
import requests
from backend.config import Config

class LlamaServerLLM(LLM):
    """Custom LangChain LLM class to interact with a remote Llama server."""

    @property
    def _llm_type(self) -> str:
        return "custom_llama_server"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Make a POST request to the Llama server's chat completions endpoint.
        """
        url = Config.LLM_URL
        if not url:
            raise ValueError("LLM_URL is not set in the configuration.")

        payload = {
            "model": "ggml-org/Qwen3-1.7B-GGUF",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            # Strip <think> tags
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
            return content
        except requests.exceptions.RequestException as e:
            return f"Error calling Llama server: {e}"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "ggml-org/Qwen3-1.7B-GGUF"}
