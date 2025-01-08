import requests
import logging

class OllamaIntegration:
    def __init__(self, url="http://localhost:11434", model="ollama3.1-8b"):
        self.url = url
        self.model = model
        self.logger = logging.getLogger(__name__)

    def generate_response(self, prompt):
        """
        Send a prompt to Ollama and return the generated response.
        """
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "prompt": prompt,
                    "model": self.model  # Use the specified model
                },
                timeout=10  # Set a timeout for the request
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error communicating with Ollama: {e}")
            return None

    def summarize_text(self, text):
        """
        Summarize the given text using Ollama.
        """
        if not text:
            self.logger.warning("No text provided for summarization.")
            return None
        return self.generate_response(f"Summarize the following text in one or two sentences:\n{text}")

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text using Ollama.
        """
        if not text:
            self.logger.warning("No text provided for sentiment analysis.")
            return None
        return self.generate_response(f"Analyze the sentiment of the following text (positive, negative, or neutral):\n{text}")

    def extract_data(self, text):
        """
        Extract key information from the given text using Ollama.
        """
        if not text:
            self.logger.warning("No text provided for data extraction.")
            return None
        return self.generate_response(f"Extract key information from the following text in bullet points:\n{text}")