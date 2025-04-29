from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from db import db
import uuid

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    data = request.get_json()    
    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": data.get('name'),
      "email": data.get('email'),
      "password": data.get('password'),
      "balance": 0.0  # Initialize balance to 0
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):
    data = request.get_json()
    user = db.users.find_one({
      "email": data.get('email')
    })

    if user and pbkdf2_sha256.verify(data.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401
  
  def get_users(self):
    users = list(db.users.find())
    # Convert ObjectId to string and remove password for security
    for user in users:
      user["_id"] = str(user["_id"])
      if "password" in user:
        del user["password"]
    return jsonify(users)

  def get_user_id(self, user_id):
    user = db.users.find_one({"_id": user_id})
    if user:
      user["_id"] = str(user["_id"])
      if "password" in user:
        del user["password"]
      return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

  def update_balance(self, user_id, amount):
    try:
      result = db.users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": float(amount)}}
      )
      if result.modified_count > 0:
        return jsonify({"message": "Balance updated successfully"}), 200
      return jsonify({"error": "User not found"}), 404
    except Exception as e:
      return jsonify({"error": "Failed to update balance", "details": str(e)}), 500