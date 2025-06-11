from fastapi import APIRouter, HTTPException
from app.payments.payments import create_payment_intent

router = APIRouter()

@router.post("/create-payment-intent/")
async def create_payment(amount: int):
    client_secret = create_payment_intent(amount)
    if isinstance(client_secret, dict) and "error" in client_secret:
        raise HTTPException(status_code=400, detail=client_secret["error"])
    return {"client_secret": client_secret}
