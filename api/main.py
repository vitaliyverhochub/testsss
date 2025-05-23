# main.py

from fastapi import FastAPI, HTTPException
from testsss.models import TestRequest
from testsss.runner.test_runner import run_price_scraper

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/run-test")
def run_test(request: TestRequest):
    try:
        results = run_price_scraper(request.hotel_name, request.date_ranges)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
