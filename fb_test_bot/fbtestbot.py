import requests
import sys
import os
import json
import io
import datetime
from bs4 import BeautifulSoup
from flask import Flask, request
from PIL import Image

#from src.fb_test_bot.Credentials import *
VERIFY_TOKEN = 'anything_to_verify' #os.environ.get('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = 'EAAeUO39QC9UBAGDEA22STLEyqFmZASY3w2wzbklZCu4fcxeW3Qko8wLXddKlMwjRiLBydGWUFZCl2JolOVTvvMxJY8xn99l0mZCWXkDDFQOW1SDjb9ZAAiBSOiXnLxXq4mBfJbBwm56IkjqDhVKbh4Q3zuwcYjwEBVb6tZBZA9lBQZDZD' #os.environ.get('PAGE_ACCESS_TOKEN')

app = Flask(__name__)


def dilbert():
    dilbert_url = 'http://dilbert.com/'
    today_url = dilbert_url + str(datetime.datetime.now().date())
    page = requests.get(today_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    url_img = soup.find_all('div', {'class': ['img-comic-container']})[0].find('img')['src']
    return url_img
    #req_dilbert = requests.get(url_img)
    #image_returned = Image.open(io.BytesIO(req_dilbert.content))
    #return image_returned


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
    print('In post with data %s'%data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    send_message_echo(sender_id, message_text)

                    if message_text == 'dilbert':
                        send_comic(sender_id, dilbert())

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
    print('In echo function!')
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


def send_comic(recipient_id, img_url):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=img_url))

    #with open('dilbert_image.jpg', 'rb') as f:
        #my_img = f.read()

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
        }#,
        #"filedata": (os.path.basename('dilbert_image.jpg'), open('dilbert_image.jpg', 'rb')) # 'image/jpg'
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
    #app.run(host='127.0.0.1',debug=True, port=port)
    app.run(host='0.0.0.0', port=port)
