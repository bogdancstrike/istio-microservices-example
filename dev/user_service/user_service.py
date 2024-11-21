from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users/<user_id>')
def get_user(user_id):
    # Mock user data
    users = {"1": {"name": "Alice"}, "2": {"name": "Bob"}}
    return jsonify(users.get(user_id, {"error": "User not found"}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
