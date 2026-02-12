import os
import requests

UPSTASH_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

HEADERS = {"Authorization": f"Bearer {UPSTASH_TOKEN}"}

def redis_setex(key: str, value: str, ttl_seconds: int):
    url = f"{UPSTASH_URL}/set/{key}/{value}?ex={ttl_seconds}"
    res = requests.post(url, headers=HEADERS)
    res.raise_for_status()

def redis_get(key: str):
    url = f"{UPSTASH_URL}/get/{key}"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json().get("result")

def redis_delete(key: str):
    url = f"{UPSTASH_URL}/del/{key}"
    res = requests.post(url, headers=HEADERS)
    res.raise_for_status()
