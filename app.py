import os
import sys
import json,ast
from datetime import datetime
import requests
from flask import Flask, request
import template
app = Flask(__name__)

ACCESS_TOKEN = "EAAEY7WK7nP0BAFZCQJIPONeZBPW1gQ3UtvGZCHGZBmzNNSWVXdziiAXb88mjsuFmCWAWwnpeVK4tt1AJ85I4uPWQyveagycqF9CbgBYZBqM7rsqniPaGyjz49mtswzBHF5Hlse4j1ZBdlu8xv0Be8RkAZBmqW6dPd6C96NX2MEoLl5vxZAChO8Xb"
VERIFY_TOKEN = "test_token"


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    template.log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    try:
                        message_text = messaging_event["message"]["text"]
                        template.send_message(sender_id,"roger that!")
                    except:
                        template.send_message(sender_id,"Not Found")
                        

                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
                    
    return "ok", 200

template.per_menu()
template.start_button()

if __name__ == '__main__':
    app.run(debug=True,port=4040)
