FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
        libssl-dev \
        libffi-dev \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install uvicorn fastapi redis dramatiq requests 'dramatiq[redis]'

COPY ./timer_app /app

EXPOSE 8000

CMD ["uvicorn", "timer:app", "--host", "0.0.0.0", "--port", "8000"]
