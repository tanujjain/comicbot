from flask import Flask, request
import requests
import sys
import os
import json
from bs4 import BeautifulSoup
import io
from PIL import Image
import datetime
from src.fb_test_bot.Credentials import *

app = Flask(__name__)


def dilbert():
    dilbert_url = 'http://dilbert.com/'
    today_url = dilbert_url + str(datetime.datetime.now().date())
    page = requests.get(today_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    url_img = soup.find_all('div', {'class': ['img-comic-container']})[0].find('img')['src']
    req_dilbert = requests.get(url_img)
    image_returned = Image.open(io.BytesIO(req_dilbert.content))
    return image_returned

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', 200)
    else:
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    extra_string = 'blaaa'
                    send_message(sender_id, message_text + extra_string)

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
