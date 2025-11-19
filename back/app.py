import jwt
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_conn import SQLServices
from os import getenv
# from flasgger import Swagger

BACKEND_KEY: str = getenv("BACKEND_KEY")
ADMIN_USER: str = getenv("ADMIN_USER")
ADMIN_PW: str = getenv("ADMIN_PW")
UTC: timezone = timezone.utc

app = Flask(__name__)
# swagger = Swagger(app)
CORS(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["username"] == ADMIN_USER and data["password"] == ADMIN_PW:
        token = jwt.encode({"user": data["username"]}, BACKEND_KEY,
                           algorithm="HS256")
        session_id = SQLServices.create_session(
            username=data["username"],
            token=token,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent", "")
        )
        return jsonify({"session_id": session_id, "token": token})

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/profile", methods=["GET"])
def profile():
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        return jsonify({"error": "Missing session"}), 401

    is_valid, username = SQLServices.validate_session(session_id)
    if not is_valid:
        return jsonify({"error": "Session expired or invalid"}), 401

    return jsonify({"message": f"Welcome {username}!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

