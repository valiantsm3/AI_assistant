import requests

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"  # Example chatbot model
HEADERS = {"Authorization": "Bearer your api key"}  # Replace with your API key

def chat_with_huggingchat(prompt):
    """
    Sends a user prompt to the Hugging Face chatbot model and returns the response.
    """
    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        try:
            return response.json()[0]['generated_text']
        except KeyError:
            return "I couldn't process the response."
    else:
        return "I'm having trouble connecting to HuggingChat."
