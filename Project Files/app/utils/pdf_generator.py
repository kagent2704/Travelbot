from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI()
router = APIRouter()

# --- Pydantic Models ---

class BudgetRange(BaseModel):
    low: int
    high: int

class BudgetBreakdown(BaseModel):
    travel: BudgetRange
    accommodation: BudgetRange
    food: BudgetRange
    activities: BudgetRange

class SightseeingSpot(BaseModel):
    name: str
    category: str
    rating: float

class Hotel(BaseModel):
    name: str
    rating: float

class TripData(BaseModel):
    customer_name: str
    budget_range: BudgetRange
    travel_season: str
    preferred_accommodation: str
    travel_duration: int
    travel_destination: str
    travel_dates: List[str]
    travel_mode: str
    num_adults: int
    num_children: int
    interests: List[str]
    sightseeing_spots: List[SightseeingSpot]
    hotels: List[Hotel]
    budget_breakdown: BudgetBreakdown

# --- PDF Generation Function ---

def generate_trip_itinerary(data: TripData):
    pdf_path = "static/Trip_Itinerary.pdf"
    os.makedirs("static", exist_ok=True)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=10, bottomMargin=10)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Trip Itinerary", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>Customer Name:</b> {data.customer_name}", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    travel_details = [
        ["Budget Range", f"₹{data.budget_range.low} - ₹{data.budget_range.high}"],
        ["Season", data.travel_season],
        ["Accommodation", data.preferred_accommodation],
        ["Duration", f"{data.travel_duration} days"],
        ["Destination", data.travel_destination],
        ["Travel Dates", ", ".join(data.travel_dates)],
        ["Travel Mode", data.travel_mode],
        ["Adults", str(data.num_adults)],
        ["Children", str(data.num_children)]
    ]

    travel_table = Table(travel_details, colWidths=[150, 300])
    travel_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))

    elements.append(travel_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Interests:</b> " + ", ".join(data.interests), styles["Heading4"]))

    # Sightseeing Recommendations
    elements.append(Paragraph("<b>Sightseeing Spots:</b>", styles["Heading2"]))
    sightseeing_data = [["Place", "Category", "Rating"]]

    sorted_sightseeing = sorted(data.sightseeing_spots, key=lambda x: x.rating, reverse=True)
    for spot in sorted_sightseeing:
        sightseeing_data.append([spot.name, spot.category, str(spot.rating)])

    sightseeing_table = Table(sightseeing_data, colWidths=[250, 150, 80])
    sightseeing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
    ]))
    
    elements.append(sightseeing_table)
    elements.append(Spacer(1, 10))

    # Recommended Hotels
    elements.append(Paragraph("<b>Recommended Hotels:</b>", styles["Heading2"]))
    hotel_data = [["Hotel Name", "Rating"]]

    sorted_hotels = sorted(data.hotels, key=lambda x: x.rating, reverse=True)
    for hotel in sorted_hotels:
        hotel_data.append([hotel.name, str(hotel.rating)])

    hotel_table = Table(hotel_data, colWidths=[300, 100])
    hotel_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
    ]))

    elements.append(hotel_table)
    elements.append(Spacer(1, 10))

    # Budget Breakdown
    elements.append(Paragraph("<b>Budget Breakdown:</b>", styles["Heading2"]))
    budget_data = [
        ["Category", "Estimated Cost Range (₹)"],
        ["Flight/Train", f"{data.budget_breakdown.travel.low} - {data.budget_breakdown.travel.high}"],
        ["Accommodation", f"{data.budget_breakdown.accommodation.low} - {data.budget_breakdown.accommodation.high}"],
        ["Food", f"{data.budget_breakdown.food.low} - {data.budget_breakdown.food.high}"],
        ["Activities", f"{data.budget_breakdown.activities.low} - {data.budget_breakdown.activities.high}"],
        ["Total", f"{data.budget_range.low} - {data.budget_range.high}"]
    ]

    budget_table = Table(budget_data, colWidths=[200, 200])
    budget_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
    ]))

    elements.append(budget_table)
    doc.build(elements)

    return pdf_path

# --- FastAPI Endpoint to Generate PDF ---

