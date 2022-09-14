import boto3
from fastapi import FastAPI

app = FastAPI()

sqs = boto3.client(
    service_name='sqs',
    aws_access_key_id='secret-id',
    aws_secret_access_key='secret-key',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
)

queue_url = 'http://localhost:4566/000000000000/fastapi-queue'

@app.get("/send")
async def send_email(title: str) -> dict:
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody='send_email',
        MessageAttributes={
            'title': {
                'DataType': 'String',
                'StringValue': title,
            },
        },
    )
    return {}
