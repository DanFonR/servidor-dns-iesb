import jwt
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_conn import SQLServices
from os import getenv
from socket import gethostname

BACKEND_KEY: str = getenv("BACKEND_KEY")
ADMIN_USER: str = getenv("ADMIN_USER")
ADMIN_PW: str = getenv("ADMIN_PW")
UTC: timezone = timezone.utc

app = Flask(__name__)
CORS(app)


@app.route("/login", methods=["POST"])
@app.route("/api/login", methods=["POST"])
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
@app.route("/api/profile", methods=["GET"])
def profile():
    # Tenta obter o token do header Authorization
    auth_header = request.headers.get("Authorization", "")
    token = None
    
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
    
    if not token:
        return jsonify({"error": "Missing token"}), 401

    # Decodifica o token para obter o username
    try:
        decoded = jwt.decode(token, BACKEND_KEY, algorithms=["HS256"])
        username = decoded.get("user")
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    
    if not username:
        return jsonify({"error": "Invalid token payload"}), 401
    # Verifica se o token corresponde a uma sessão válida no banco
    session_id, sess_username, created_at, expires_at = SQLServices.get_session_by_token(token)

    if created_at and created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)

    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)

    if not session_id or sess_username != username:
        return jsonify({"error": "Missing token or session not found"}), 401

    # Verifica expiração
    if expires_at < datetime.now(tz=UTC):
        return jsonify({"error": "Session expired"}), 401

    hostname = gethostname()
    login_time = created_at.astimezone(UTC).isoformat() if created_at else None

    return jsonify({
        "username": username,
        "hostname": hostname,
        "session_id": session_id,
        "login_time": login_time,
        "message": f"Welcome {username}!"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

