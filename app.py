from flask import Flask
from flask_cors import CORS
from database import db
from routes.auth import auth_bp
from routes.sync import sync_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(sync_bp)

@app.route("/")
def home():
    return {"status": "Attendia API is running"}

if __name__ == "__main__":
    app.run(debug=True)
