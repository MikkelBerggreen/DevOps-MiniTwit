from prometheus_client import Counter, Gauge, Histogram, generate_latest
from fastapi import APIRouter, Response
import psutil
from .redis_util import redis_increment_request_count, redis_get_request_count

metrics_router = APIRouter()

CPU_GAUGE = Gauge(
    "minitwit_cpu_load_percent", "Current load of the CPU in percent."
)
RESPONSE_COUNTER = Gauge(
    "minitwit_http_responses_total", "The count of HTTP responses sent."
)
REQ_DURATION_SUMMARY = Histogram(
    "minitwit_request_duration_milliseconds", "Request duration distribution."
)


@metrics_router.get("/metrics")
async def metrics():
    RESPONSE_COUNTER.set(redis_get_request_count())
    return Response(generate_latest(), media_type="text/plain")


def handle_update_metrics(request, process_time):
    update_CPU_usage()
    update_process_time(process_time)
    redis_increment_request_count(request)

def increment_request_count():
    RESPONSE_COUNTER.inc() 

def update_CPU_usage():
    CPU_GAUGE.set(psutil.cpu_percent())

def update_process_time(process_time):
    REQ_DURATION_SUMMARY.observe(process_time)
