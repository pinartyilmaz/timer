import dramatiq
from dramatiq.brokers.redis import RedisBroker
from redis import Redis
import requests
from datetime import datetime
import os
import time


redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_broker = RedisBroker(url=f"redis://{redis_host}:{redis_port}/0")
dramatiq.set_broker(redis_broker)

redis_client = Redis(host=redis_host, port=redis_port, db=0)


@dramatiq.actor
def timer_task(timer_id: str, url: str):
    end_time_str = redis_client.get(timer_id)
    if end_time_str:
        response=requests.post(url, json={"timer_id": timer_id, "status": "expired"})
        redis_client.delete(timer_id)
        print(response)