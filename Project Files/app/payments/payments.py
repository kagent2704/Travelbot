import stripe

# Set your secret key directly (not recommended for production)
stripe.api_key = "YOUR_STRIPE_API_KEY"

def create_payment_intent(amount, currency="inr"):
    try:
        amount_in_paisa = int(amount * 100)  # Convert INR to paisa (Stripe requires smallest unit)
        intent = stripe.PaymentIntent.create(
            amount=amount_in_paisa,
            currency=currency,
            payment_method_types=["card"]
        )
        return {"client_secret": intent.client_secret}
    except stripe.error.StripeError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
