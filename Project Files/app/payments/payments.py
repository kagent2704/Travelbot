import stripe

# Set your secret key directly (not recommended for production)
stripe.api_key = "sk_test_51R9KNP3zcDeHgkU0ozizyyUkG2xudrSvGOWIFdwNhH7jyIrFRql0Mm8jKleVwkel5HAtM00hT8TSnFcfU5eh22XQ00IFtp7w83"

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
