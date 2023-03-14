import redis
from datetime import datetime
from dotenv import dotenv_values

dotenv = dotenv_values(".env")
if "REDIS_HOST" in dotenv:
    redis_client = redis.Redis(
        host=dotenv["REDIS_HOST"],
        port=dotenv["REDIS_PORT"], 
        password=dotenv["REDIS_PASSWORD"]
    )
else:
    redis_client = None


def redis_increment_request_count(request):
    # don't count requests when developing locally
    if request.client.host == "127.0.0.1" or request.client.host == "testclient":
        return
    request_log = str(request.client) + " : " + str(datetime.now())
    redis_client.pfadd('processed_requests', request_log)
    

def redis_get_request_count():
    return redis_client.pfcount('processed_requests')
