import redis
from fastapi import BackgroundTasks, Depends
from datetime import datetime
from dotenv import dotenv_values

dotenv = dotenv_values(".env")

redis_client = redis.Redis(
    host=dotenv["REDIS_HOST"],
    port=dotenv["REDIS_PORT"], 
    password=dotenv["REDIS_PASSWORD"]
)

def increment_request_count(request):
    request_log = str(request.client) + " : " + str(datetime.now())
    redis_client.pfadd('processed_requests', request_log)
    
def get_request_count():
    return redis_client.pfcount('processed_requests')

