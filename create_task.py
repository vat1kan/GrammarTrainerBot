from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import json
import datetime

PROJECT_ID = "grammarbot-450711"
QUEUE_NAME = "quiz-sending-queue"
LOCATION = "europe-central2"
URL = "https://grammarbot-450711.lm.r.appspot.com/"

def create_task():
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT_ID, LOCATION, QUEUE_NAME)

    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(datetime.datetime.now(datetime.UTC))

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": URL,
            "body": json.dumps({}).encode(),
            "headers": {"Content-Type": "application/json"},
        },
        "schedule_time": timestamp,
    }

    response = client.create_task(request={"parent": parent, "task": task})
    print(f"Task created: {response.name}")

if __name__ == "__main__":
    create_task()
