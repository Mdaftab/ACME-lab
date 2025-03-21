import json
import os
import logging
import redis
from flask import Flask, request
from typing import Text, Optional, Dict, Any

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Redis configuration from environment variables with sensible defaults
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 1))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

# In-memory storage fallback
in_memory_storage = {}
use_redis = True

# Try to connect to Redis once at startup
try:
    redis_client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=1.0  # Short timeout for fast failure
    )
    # Test connection
    redis_client.ping()
    logger.info("Successfully connected to Redis at %s:%s", REDIS_HOST, REDIS_PORT)
except redis.exceptions.ConnectionError as e:
    use_redis = False
    logger.warning("Could not connect to Redis at %s:%s, falling back to in-memory storage: %s", 
                  REDIS_HOST, REDIS_PORT, str(e))
except Exception as e:
    use_redis = False
    logger.warning("Error connecting to Redis, falling back to in-memory storage: %s", str(e))


def get_current_user() -> Optional[Dict[Text, Any]]:
    """Extract current user details from storage."""
    try:
        if use_redis:
            encoded_user = redis_client.get("user")
            if encoded_user:
                return json.loads(encoded_user)
        else:
            if "user" in in_memory_storage:
                return in_memory_storage["user"]
    except Exception as e:
        logger.error("Error getting user: %s", str(e))
    
    return None


def store_user(user: Dict[Text, Any]) -> None:
    """Save user details to our storage."""
    try:
        if use_redis:
            redis_client.set("user", json.dumps(user))
        else:
            in_memory_storage["user"] = user
        logger.info("Stored user data: %s", user.get("name", "unknown"))
    except Exception as e:
        logger.error("Error storing user: %s", str(e))
        # Still try to store in memory if Redis fails
        in_memory_storage["user"] = user


@app.route('/health', methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes."""
    storage_type = "redis" if use_redis else "in-memory"
    return {"status": "healthy", "storage": storage_type}, 200


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
