from prometheus_client import Counter, Gauge, Histogram, generate_latest
from fastapi import APIRouter, Response
import psutil

metrics_router = APIRouter()

CPU_GAUGE = Gauge(
    "minitwit_cpu_load_percent", "Current load of the CPU in percent."
)
# RESPONSE_COUNTER = Counter(
#     "minitwit_http_responses_total", "The count of HTTP responses sent."
# )
REQ_DURATION_SUMMARY = Histogram(
    "minitwit_request_duration_milliseconds", "Request duration distribution."
)

# TODO remove once the Redis branch is merged
import random

@metrics_router.get("/metrics")
async def metrics():
    # TODO remove once the Redis branch is merged
    set_request_counter(random.randint(0, 100))
    return Response(generate_latest(), media_type="text/plain")

def increment_request_count():
    RESPONSE_COUNTER.inc() 

def update_CPU_usage():
    CPU_GAUGE.set(psutil.cpu_percent())

def update_process_time(process_time):
    REQ_DURATION_SUMMARY.observe(process_time)
