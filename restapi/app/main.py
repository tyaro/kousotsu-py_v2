from typing import Optional
import redis
import json
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware # 追

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ChangeRate")
def readChangeRate():
    client = redis.Redis(host='redis', port=6379, db=0)
    data = client.get('ChangeRate')
    j = json.loads(data)
    return j


@app.get("/ChangeRateSpot")
def readChangeRateSpot():
    client = redis.Redis(host='redis', port=6379, db=0)
    data = client.get('ChangeRateSpot')
    j = json.loads(data)
    return j