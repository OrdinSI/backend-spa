import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_product(name):
    """Create product."""
    product = stripe.Product.create(name=name)
    return product.get("id")


def create_price(amount, product_id):
    """Create price."""
    price = stripe.Price.create(
        unit_amount_decimal=amount * 100,
        currency="rub",
        product=product_id
    )
    return price


def create_session(price):
    """Create session."""
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",

    )
    return session.get("id"), session.get("url")
