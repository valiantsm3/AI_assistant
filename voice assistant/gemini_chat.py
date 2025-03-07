import google.genai as genai

# Set up Gemini client

client = genai.Client(api_key="api key here") # Replace with your API key


# Function to chat with Gemini
def chat_with_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Change model if needed
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )

        # Extracting text from response
        return response.candidates[0].content.parts[0].text

    except Exception as e:
        return f"Error: {e}"



