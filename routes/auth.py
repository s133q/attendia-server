from flask import Blueprint, request
from models import User
from database import db
from utils import hash_password, check_password, generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["username", "password", "first_name", "last_name"]
    if not all(data.get(f) for f in required_fields):
        return {"error": "Missing fields"}, 400

    if User.query.filter_by(username=data["username"]).first():
        return {"error": "User already exists"}, 409

    user = User(
        username=data["username"],
        password_hash=hash_password(data["password"]),
        first_name=data["first_name"],
        last_name=data["last_name"]
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered successfully"}


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password(data["password"], user.password_hash):
        return {"error": "Invalid credentials"}, 401

    token = generate_token()
    return {
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

