from flask import Flask, request, jsonify
from producer import (
    send_customer,
    send_product,
    send_order
)

app = Flask(__name__)

@app.route("/")
def home():
    return "E-Commerce Data Engineering API Running"


@app.route("/customer", methods=["POST"])
def create_customer():

    customer_data = request.get_json()

    required_fields = [
        "customer_id",
        "customer_name",
        "customer_city",
        "customer_state"
    ]

    for field in required_fields:
        if field not in customer_data:
            return jsonify({
                "error": f"{field} is missing"
            }), 400

    send_customer(customer_data)

    return jsonify({
        "message": "Customer sent to Kafka successfully",
        "data": customer_data
    })
    
@app.route("/product", methods=["POST"])
def create_product():

    product_data = request.get_json()

    required_fields = [
        "product_id",
        "product_name",
        "category",
        "price"
    ]

    for field in required_fields:
        if field not in product_data:
            return jsonify({
                "error": f"{field} is missing"
            }), 400

    send_product(product_data)

    return jsonify({
        "message": "Product sent to Kafka successfully",
        "data": product_data
    })
    
@app.route("/order", methods=["POST"])
def create_order():

    order_data = request.get_json()

    required_fields = [
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "amount"
    ]

    for field in required_fields:
        if field not in order_data:
            return jsonify({
                "error": f"{field} is missing"
            }), 400

    send_order(order_data)

    return jsonify({
        "message": "Order sent to Kafka successfully",
        "data": order_data
    })

if __name__ == "__main__":
    app.run(debug=True)