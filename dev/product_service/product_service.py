from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/products/<product_id>')
def get_product(product_id):
    # Mock product data
    products = {"101": {"name": "Laptop"}, "102": {"name": "Phone"}}
    return jsonify(products.get(product_id, {"error": "Product not found"}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
