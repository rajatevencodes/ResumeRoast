# https://python-rq.org/
# Redis don't have a built-in queue system, but we can use RQ (Redis Queue) library to abstract the implementation.
from redis import Redis
from rq import Queue

redis_connection = Redis(
    host="valkey",  # Check container name in docker-compose.yaml
    port="6379",  # Default Redis port
)

try:
    redis_connection.ping()  # Check if Redis is reachable
    print("Connected to Redis successfully.")

    queue = Queue(connection=redis_connection)  # Create a queue instance
    print("Queue instance created successfully.")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
