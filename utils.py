import bcrypt
import uuid
from models import User

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token():
    return str(uuid.uuid4())

def verify_token(token):
    return User.query.filter_by(token=token).first()
