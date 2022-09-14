import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from chalice.app import Chalice

SMTP_HOST = "smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_LOGIN = ""
SMTP_PASSWORD = ""

app = Chalice("chalice-task-queue")


@app.on_sqs_message(queue='fastapi-queue', batch_size=1)
def hello(event):
    # wait_for_debug_client()
    body = {
        "message": "Success",
        "input": event.to_dict(),
    }
    title = event.to_dict()['Records'][0]['messageAttributes']['title']['stringValue']
    sender = "from@example.com"
    receiver = "mailtrap@example.com"
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = title
    message_body = "This is a test e-mail message."
    message.attach(MIMEText(message_body, "plain"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_LOGIN, SMTP_PASSWORD)
        server.sendmail(sender, receiver, message.as_string())

    return {"statusCode": 200, "body": json.dumps(body)}

def wait_for_debug_client(timeout=15):
    """Utility function to enable debugging with Visual Studio Code"""
    import time, threading
    import debugpy

    debugpy.listen(("0.0.0.0", 19891))
    class T(threading.Thread):
        daemon = True
        def run(self):
            time.sleep(timeout)
            print("Canceling debug wait task ...")
            debugpy.wait_for_client.cancel()
    T().start()
    print("Waiting for client to attach debugger ...")
    debugpy.wait_for_client()
