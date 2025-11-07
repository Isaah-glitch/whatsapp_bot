import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
import boto3
import requests

app = Flask(__name__)

# Load keys from environment
TWILIO_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# S3 setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET = os.getenv("AWS_S3_BUCKET")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    num_media = int(request.values.get("NumMedia", 0))
    resp = MessagingResponse()
    msg = resp.message()

    # Handle text
    if incoming_msg:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response.choices[0].message.content
        msg.body(reply)

    # Handle media
    for i in range(num_media):
        media_url = request.values.get(f"MediaUrl{i}")
        media_type = request.values.get(f"MediaContentType{i}")

        # Download file
        file_data = requests.get(media_url).content
        filename = media_url.split("/")[-1]

        # Upload to S3
        s3.put_object(Bucket=BUCKET, Key=filename, Body=file_data, ContentType=media_type)
        msg.body(f"Received and saved your {media_type} as {filename}.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
