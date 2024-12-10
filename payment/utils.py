import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_session(borrowing):
    amount = int(borrowing.book.daily_fee * 100)  # Stripe працює з копійками
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": borrowing.book.title},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8000/payments/success/",
        cancel_url="http://localhost:8000/payments/cancel/",
    )
    return session.id, session.url
