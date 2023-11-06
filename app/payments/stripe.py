from flask import Blueprint, request, jsonify
import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# Blueprint Configuration
payment_bp = Blueprint('payment_bp', __name__, url_prefix='/payment')

@payment_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('main.index', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('main.index', _external=True),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403
