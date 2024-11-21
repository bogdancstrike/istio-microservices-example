from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://user-service"
PRODUCT_SERVICE_URL = "http://product-service"

@app.route('/orders/<order_id>')
def get_order(order_id):
    # Mock order data
    orders = {
        "5001": {"user_id": "1", "product_id": "101"},
        "5002": {"user_id": "2", "product_id": "102"}
    }
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"})

    user = requests.get(f"{USER_SERVICE_URL}/users/{order['user_id']}").json()
    product = requests.get(f"{PRODUCT_SERVICE_URL}/products/{order['product_id']}").json()
    return jsonify({"order_id": order_id, "user": user, "product": product})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
