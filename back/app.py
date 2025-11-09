import jwt
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_conn import SQLServices
from os import getenv

BACKEND_KEY: str = getenv("BACKEND_KEY")
ADMIN_USER: str = getenv("ADMIN_USER")
ADMIN_PW: str = getenv("ADMIN_PW")

app = Flask(__name__)
CORS(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["username"] == ADMIN_USER and data["password"] == ADMIN_PW:
        token = jwt.encode(
            {"user": data["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            BACKEND_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/profile", methods=["GET"])
def profile():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, BACKEND_KEY, algorithms=["HS256"])
        return jsonify({"message": f"Welcome {decoded['user']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(debug=True)

