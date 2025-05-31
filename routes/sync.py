from flask import Blueprint, request, jsonify
from models import SyncItem
from database import db
from datetime import datetime

sync_bp = Blueprint("sync", __name__)

@sync_bp.route("/sync", methods=["POST"])
def sync():
    data = request.json
    user_id = data.get("user_id")
    items = data.get("items", [])

    if not user_id or not isinstance(items, list):
        return {"error": "Invalid data"}, 400

    for item in items:
        new_item = SyncItem(
            user_id=user_id,
            content=item.get("content"),
            last_modified=datetime.utcnow()
        )
        db.session.add(new_item)

    db.session.commit()
    return {"message": f"{len(items)} items synced successfully"}

@sync_bp.route("/pull", methods=["GET"])
def pull():
    user_id = request.args.get("user_id")
    if not user_id:
        return {"error": "Missing user_id"}, 400

    items = SyncItem.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": item.id,
            "content": item.content,
            "last_modified": item.last_modified.isoformat()
        } for item in items
    ])
