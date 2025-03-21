import json
import os
import redis
from flask import Flask, request
from typing import Text, Optional, Dict, Any

app = Flask(__name__)

# Get Redis configuration from environment variables with sensible defaults
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 1))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)


def get_current_user() -> Optional[Dict[Text, Any]]:
    """Extract current user details from storage."""

    red = redis.StrictRedis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    encoded_user = red.get("user")
    if encoded_user:
        return json.loads(encoded_user)
    else:
        return None


def store_user(user: Dict[Text, Any]) -> None:
    """Save user details to our storage."""

    red = redis.StrictRedis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    red.set("user", json.dumps(user))


@app.route('/health', methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes."""
    return {"status": "healthy"}, 200


@app.route('/', methods=["GET"])
def greet():
    """greet the user."""

    user = get_current_user()
    if user is not None:
        return "Hello, {}!".format(user.get("name"))
    else:
        return "Hello, unknown stranger!"


@app.route('/', methods=["POST"])
def save_name():
    """Change a users details"""

    user = request.json
    store_user(user)
    return "I'll try to remember your name, {}!".format(user.get("name"))


if __name__ == "__main__":
    # Only for development
    app.run(host='0.0.0.0', port=8080, debug=False)
