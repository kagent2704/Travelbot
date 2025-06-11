from fastapi import FastAPI
from typing import Dict
from app.payments.payments import create_payment_intent
import google.generativeai as genai
from fpdf import FPDF
import os

app = FastAPI()

# Hardcoded Gemini API key (Replace with a secure method like .env)
GEMINI_API_KEY = "YOYR_API_KEY"

# Ensure API key is set
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing. Please provide a valid key.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Store user sessions and generated PDF download links
user_sessions: Dict[str, Dict] = {}
download_links: Dict[str, str] = {}

# Ensure PDF directory exists
PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# Function to generate a PDF itinerary
def generate_pdf(trip_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Title
    pdf.cell(200, 10, f"Trip Itinerary for {trip_data['destination']}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    
    # Content
    pdf.cell(200, 10, f"Budget Range: {trip_data['budget']}", ln=True)
    pdf.cell(200, 10, f"Number of Adults: {trip_data['adults']}", ln=True)
    pdf.cell(200, 10, f"Number of Children: {trip_data['children']}", ln=True)
    pdf.cell(200, 10, f"Duration: {trip_data['days']} days", ln=True)
    pdf.cell(200, 10, f"Interests: {trip_data['interests']}", ln=True)

    # Save PDF
    pdf_filename = f"{PDF_DIR}/itinerary_{trip_data['destination'].replace(' ', '_')}.pdf"
    pdf.output(pdf_filename)

    return pdf_filename

# Function to call Gemini API
def get_gemini_response(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I'm unable to process your request at the moment."

# Chatbot logic
def get_chatbot_response(user_id: str, user_input: str):
    user_input = user_input.lower()

    if user_id not in user_sessions:
        user_sessions[user_id] = {"stage": "destination", "data": {}}

    session = user_sessions[user_id]
    stage = session["stage"]

    if stage == "destination":
        session["data"]["destination"] = user_input
        session["stage"] = "budget"
        return "Great choice! What's your budget range for the trip?"

    elif stage == "budget":
        session["data"]["budget"] = user_input
        session["stage"] = "adults"
        return "Got it! How many adults are traveling?"

    elif stage == "adults":
        session["data"]["adults"] = user_input
        session["stage"] = "children"
        return "Thanks! How many children will be joining?"

    elif stage == "children":
        session["data"]["children"] = user_input
        session["stage"] = "days"
        return "Noted! How many days will the trip last?"
    
    elif stage == "days":
        session["data"]["days"] = user_input
        session["stage"] = "interests"
        return "Awesome! What kind of activities or experiences interest you? (e.g., sightseeing, adventure, food)"
    
    elif stage == "interests":
        session["data"]["interests"] = user_input
        session["stage"] = "complete"
        return "Thank you! We have all the details now. Would you like to generate a PDF itinerary? (yes/no)"
    
    elif stage == "complete":
        if "yes" in user_input:
            pdf_path = generate_pdf(session["data"])  # Generate PDF
            download_links[user_id] = pdf_path  # Store link for user
            session["stage"] = "payment"
            return f"Your itinerary is ready! Download here: {pdf_path}. Type 'pay' to proceed with the payment."
        else:
            session["stage"] = "destination"
            return "Would you like a different plan for the same location or a completely new one? (same/new)"
    
    elif stage == "payment":
        if "pay" in user_input:
            payment_data = create_payment_intent(amount=5000)  # Example amount ₹50.00
            if "payment_url" in payment_data:
                session["stage"] = "paid"
                return f"Payment link generated! Complete your payment here: {payment_data['payment_url']}"
            else:
                return "Payment failed. Please try again."
        
    elif stage == "paid":
        return f"Payment confirmed! Download your itinerary here: {download_links.get(user_id)}"
    
    return get_gemini_response(user_input)  # Use Gemini AI for fallback responses

@app.get("/chat")
async def chat(user_id: str, prompt: str):
    response = get_chatbot_response(user_id, prompt)
    return {"response": response}

@app.post("/payment", include_in_schema=True)
async def process_payment(data: dict):
    return {"message": "Payment received"}

@app.get("/")
async def root():
    return {"message": "Welcome to the chatbot API! Use /chat?user_id=<user_id>&prompt=<your_message> to chat."}

#run with: uvicorn app.main1:app --reload
