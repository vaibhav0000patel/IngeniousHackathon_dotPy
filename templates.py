import os
import sys
import json,ast
from datetime import datetime

import requests
from flask import Flask, request
import api
import template
app = Flask(__name__)


ACCESS_TOKEN = "EAAEY7WK7nP0BAFZCQJIPONeZBPW1gQ3UtvGZCHGZBmzNNSWVXdziiAXb88mjsuFmCWAWwnpeVK4tt1AJ85I4uPWQyveagycqF9CbgBYZBqM7rsqniPaGyjz49mtswzBHF5Hlse4j1ZBdlu8xv0Be8RkAZBmqW6dPd6C96NX2MEoLl5vxZAChO8Xb"
VERIFY_TOKEN = "test_token"
root_url = "https://www.example.com"

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": ACCESS_TOKEN
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
        log("send_message button errors---------------------------------------")

def per_menu():
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps( {
            "setting_type": "call_to_actions",
            "thread_state": "existing_thread",
            "call_to_actions": [
            # {
            #     "type": "web_url",
            #     "title": "My interests",
            #     "url":"https://tech-inside.herokuapp.com/",
            #     "webview_height_ratio":"tall"
            # },
            {
                "type": "postback",
                "title": "My Profile",
                "payload": "profile"
            },
            ]
        }
    )
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("PAYLOAD errors----------------------------")

def start_button():
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps( {
            "setting_type": "call_to_actions",
            "thread_state": "new_thread",
            "call_to_actions": [{
                "payload": "Get Started"
            }]
        })
    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("start button errors-------------------------------")

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()