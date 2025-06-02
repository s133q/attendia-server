from flask import Blueprint, request, jsonify
from models import SyncItem
from database import db
from datetime import datetime
from utils import verify_token

sync_bp = Blueprint("sync", __name__)

@sync_bp.route("/sync", methods=["POST"])
def sync():
    token = request.headers.get("Authorization")
    user = verify_token(token)
    if not user:
        return {"error": "Unauthorized"}, 403

    data = request.json
    items = data.get("items", [])

    if not isinstance(items, list):
        return {"error": "Invalid data"}, 400

    for item in items:
        content = item.get("content")
        if not content:
            continue
        sync_item = SyncItem(
            user_id=user.id,
            content=content,
            last_modified=datetime.utcnow()
        )
        db.session.add(sync_item)

    db.session.commit()
    return {"message": f"{len(items)} items synced successfully"}

@sync_bp.route("/pull", methods=["GET"])
def pull():
    token = request.headers.get("Authorization")
    user = verify_token(token)
    if not user:
        return {"error": "Unauthorized"}, 403

    items = SyncItem.query.filter_by(user_id=user.id).all()
    return jsonify([
        {
            "id": item.id,
            "content": item.content,
            "last_modified": item.last_modified.isoformat()
        } for item in items
    ])
