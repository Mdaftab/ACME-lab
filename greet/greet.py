import json
from flask import Flask, request, jsonify
from typing import Text, Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# In-memory storage
storage = {}

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "storage": "in-memory", "version": "1.0.0"}), 200

@app.route("/", methods=["GET"])
def greet():
    user = storage.get("user")
    if user is not None:
        return jsonify({"message": f"Hello, {user.get('name')}!"}), 200
    return jsonify({"message": "Hello, unknown stranger!"}), 200

@app.route("/", methods=["POST"])
def save_name():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    user = request.json
    if not user or "name" not in user:
        return jsonify({"error": "Request must include name field"}), 400
    storage["user"] = user
    return jsonify({"message": f"I will remember your name, {user.get('name')}!"}), 200

if __name__ == "__main__":
    print("\nStarting Greet service in development mode...")
    print("Storage mode: In-memory")
    print("Server running at http://localhost:8080\n")
    app.run(host="127.0.0.1", port=8080, debug=True)
