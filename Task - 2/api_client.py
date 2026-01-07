import os
import requests
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

load_dotenv()

class MistralClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def send_prompt(self, messages, model="mistral-tiny"):
        """
        Sends a prompt to the Mistral API and retrieves the response.
        
        Args:
            messages (list): A list of message dictionaries (e.g., [{"role": "user", "content": "Hello"}])
            model (str): The model to use (default: mistral-tiny)
            
        Returns:
            str: The content of the response message.
        """
        payload = {
            "model": model,
            "messages": messages
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx, 5xx)
            
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return "Error: No response content received."

        except requests.exceptions.RequestException as e:
            logging.error(f"API Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                 logging.error(f"API Response: {e.response.text}")
                 return f"Error: API Request failed. Status: {e.response.status_code}. See logs for details."
            return f"Error: Connection failure. {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return f"Error: An unexpected error occurred. {str(e)}"

if __name__ == "__main__":
    # verification
    client = MistralClient()
    print("Testing API connection...")
    response = client.send_prompt([{"role": "user", "content": "Say hello!"}])
    print(f"Response: {response}")
