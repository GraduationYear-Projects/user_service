from flask import Blueprint, request, jsonify
from user.models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/signup/', methods=['POST'])
def signup():
    return User().signup()

@user_bp.route('/api/signout/')
def signout():
    return User().signout()

@user_bp.route('/api/login/', methods=['POST'])
def login():
    return User().login()

@user_bp.route("/api/user/", methods=["GET"])
def get_users():
    return User().get_users()

@user_bp.route("/api/user/<user_id>/", methods=["GET"])
def get_user_id(user_id):
    return User().get_user_id(user_id)

@user_bp.route("/api/user/<user_id>/balance", methods=["PATCH"])
def update_balance(user_id):
    data = request.get_json()
    amount = data.get('amount')
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400
    return User().update_balance(user_id, amount)