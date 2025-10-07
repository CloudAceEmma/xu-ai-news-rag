from flask import request, jsonify, Blueprint
from backend.models import db, User
import jwt
from functools import wraps
from backend.config import Config
import datetime

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['identity'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def get_current_user_id():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    if not token:
        return None
    try:
        data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        return data['identity']
    except:
        return None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = jwt.encode({
            'identity': user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, Config.JWT_SECRET_KEY, algorithm="HS256")
        return jsonify(access_token=token), 200

    return jsonify({"msg": "Bad username or password"}), 401