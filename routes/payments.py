from flask import Blueprint, jsonify, request

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/process', methods=['POST'])
def process_payment():
    data = request.json
    payment_method = data.get("method")

    if payment_method not in ["PhonePe", "Paytm", "GooglePay", "PayPal"]:
        return jsonify({"error": "Invalid payment method"}), 400

    return jsonify({"message": f"Payment successful via {payment_method}!"})
