# celery_app.py

from celery import Celery
import subprocess
import json

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def run_test_task(hotel_name, dates):
    input_data = {"hotel_name": hotel_name, "dates": dates}
    with open("input_data.json", "w") as f:
        json.dump(input_data, f)

    subprocess.run(["pytest", "tests/test_tripadvisor.py"])

    with open("data/output.json") as f:
        result = json.load(f)
    return result
