import json
import os
import random
import time

import psycopg2
import redis

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

db_conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dbname=os.getenv("DB_NAME")
)
cursor = db_conn.cursor()

# Create table if not exists
cursor.execute("""
               CREATE TABLE IF NOT EXISTS weather_data
               (
                   id
                   SERIAL
                   PRIMARY
                   KEY,
                   city
                   TEXT,
                   temperature
                   INTEGER
               )
               """)
db_conn.commit()

print("Worker started – waiting for jobs...")

while True:
    job = redis_client.brpop("weather_jobs", timeout=5)
    if job:
        data = json.loads(job[1])
        city = data["city"]

        # Fake weather data
        temp = random.randint(-5, 25)

        print(f"Processing job: {city} → {temp}°C")

        cursor.execute(
            "INSERT INTO weather_data (city, temperature) VALUES (%s, %s)",
            (city, temp)
        )
        db_conn.commit()
    else:
        time.sleep(1)
