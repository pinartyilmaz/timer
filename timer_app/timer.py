from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import uuid
from datetime import datetime, timedelta


from redis import Redis

from timer_task import timer_task
import os


app = FastAPI()
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = Redis(host=redis_host, port=redis_port, db=0)


class TimerRequest(BaseModel):
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    url: HttpUrl


class TimerResponse(BaseModel):
    timer_id: str
    seconds_left: float


class TimerStatusResponse(BaseModel):
    seconds_left: float


@app.post("/timer", response_model=TimerResponse)
def set_timer(timer_request: TimerRequest):
    # calculate in seconds
    total_seconds = timer_request.hours * 3600 + timer_request.minutes * 60 + timer_request.seconds
    timer_id = str(uuid.uuid4())
    end_time = datetime.now() + timedelta(seconds=total_seconds)
    redis_client.set(timer_id, end_time.isoformat())
    # send to dramatiq queue with a delay in miliseconds.
    timer_task.send_with_options(args=(timer_id, str(timer_request.url)), delay=int(total_seconds)*1000)
    print(f"total_seconds{total_seconds}")
    return TimerResponse(timer_id=timer_id, seconds_left=total_seconds)


@app.get("/timer/{timer_id}", response_model=TimerStatusResponse)
def get_timer(timer_id: str):
    end_time_value=redis_client.get(timer_id)
    if end_time_value:
        end_time=datetime.fromisoformat(end_time_value.decode())
        remaining_time = (end_time-datetime.now()).total_seconds()
        if remaining_time < 0:
            remaining_time = 0
        return TimerStatusResponse(seconds_left=int(remaining_time))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)