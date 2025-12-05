import json
import os

import psycopg2
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (simplest for assignment)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

db_conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dbname=os.getenv("DB_NAME")
)


@app.post("/weather/{city}")
def request_weather(city: str):
    # send job to Redis
    job = json.dumps({"city": city})
    redis_client.lpush("weather_jobs", job)
    return {"status": "queued", "city": city}


@app.get("/weather")
def get_weather_entries():
    cur = db_conn.cursor()
    cur.execute("SELECT city, temperature FROM weather_data")
    rows = cur.fetchall()
    return [{"city": r[0], "temperature": r[1]} for r in rows]


@app.get("/queue")
def get_queue():
    queue = redis_client.lrange("weather_queue", 0, -1)
    return queue
