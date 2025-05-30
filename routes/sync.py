from flask import Blueprint, request

sync_bp = Blueprint("sync", __name__)

@sync_bp.route("/sync", methods=["POST"])
def sync():
    # Заглушка: тут буде обробка отриманих даних
    return {"message": "Data synced successfully"}

@sync_bp.route("/pull", methods=["GET"])
def pull():
    # Заглушка: тут буде відправка оновлень
    return {"data": []}
