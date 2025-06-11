import google.generativeai as genai

# Hardcoded API key
gemini_api_key = "YOUR_API_KEY"

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Function to call Gemini API
def get_gemini_response(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I'm unable to process your request at the moment."
