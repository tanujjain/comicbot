import requests
import sys
import os
import json
import io
import datetime
from flask import Flask, request
from scrapers import dilbert, xkcd, calvin


VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']

app = Flask(__name__)


def send_all(r_id):
    send_comic(r_id, dilbert())
    send_comic(r_id, xkcd())
    send_comic(r_id, calvin())


@app.route('/', methods=['GET'])
def handle_verification():
    print('In root endpoint with token: %s'%request.args.get('hub.verify_token', ''))
    print(request.args.get('hub.verify_token', '') == VERIFY_TOKEN)
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        print('YEAH!')
        return request.args.get('hub.challenge', 200)
    else:
        return 'Errorrrrr, wrong validation token'


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
                    send_message_echo(sender_id, message_text)

                    if message_text.lower() == 'dilbert':
                        send_comic(sender_id, dilbert())

                    if message_text.lower() == 'xkcd':
                        send_comic(sender_id, xkcd())

                    if message_text.lower() == 'cal':
                        send_comic(sender_id, calvin())

                    if message_text == 'all':
                        send_all(sender_id)

                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message_echo(recipient_id, message_text):
    """Send the message text to recipient with id recipient.
      """
    '''r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": PAGE_ACCESS_TOKEN},
                      data=json.dumps({
                          "recipient": {"id": recipient_id},
                          "message": {"text": message_text}
                      }),
                      headers={'Content-type': 'application/json'})'''

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
    if r.status_code != requests.codes.ok:
        print(r)
        print(r.text)


def send_comic(recipient_id, img_url):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=img_url))

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
            "attachment": {
                "type": "image",
                "payload": {"url": img_url}
            }
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
    print(VERIFY_TOKEN)
    print(PAGE_ACCESS_TOKEN)
    app.run(host='0.0.0.0', port=port)
