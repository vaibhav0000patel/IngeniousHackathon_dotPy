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
                      # the message's text
                    try:
                        message_text = messaging_event["message"]["text"]
                        if message_text == "Football":
                            template.send_typing(sender_id)
                            template.send_button_fetch(sender_id,message_text)
                        elif message_text == "No":
                            name = template.get_name(sender_id)
                            template.send_button_add_interest(sender_id,name)
                    # elif message_text == "location":
                    #     template.send_button_fetch(sender_id,message_text)
                    else:
                        interest_db = template.check_interest(sender_id)
                        if interest_db == 'N/A':
                            template.send_message(sender_id,"Opps we dont have anyone around you with this interest right now.\n Can I help to find any other interests?")
                            template.send_quick_reply(sender_id)
                        elif interest_db == 'ok':
                            template.send_button_fetch(sender_id,message_text)
                        else: 
                            template.send_message(sender_id,"somthing went wrong")
                            template.send_quick_reply(sender_id)
                    except:
                        try:
                            c_lat = messaging_event["message"]["attachments"][0]["payload"]["coordinates"]['lat']
                            c_lon = messaging_event["message"]["attachments"][0]["payload"]["coordinates"]['long']
                            template.send_button_add_location(sender_id,c_lat,c_lon)
                            template.send_message(sender_id, "Thank you!" + " " + str(c_lat) + "," + str(c_lon))

                        except:
                            template.send_message(sender_id, "not found")



                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    
                    msg = messaging_event["postback"]['payload']
                    send_id = messaging_event["sender"]['id']
                    rece_id = messaging_event["recipient"]['id']
                    profile = requests.get("https://graph.facebook.com/v2.6/"+send_id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN).text
                    profile_dic = ast.literal_eval(profile)
                    uname = profile_dic["first_name"] +" "+ profile_dic["last_name"]

                    if msg == 'Get Started':
                        template.send_typing(send_id)
                        template.send_message(send_id,"Hello " + uname + " WELCOME MSG")
                    elif msg == 'profile':
                        location_flag = "available"
                        if location_flag == "available":
                            template.send_typing(send_id)
                            template.add_data_quick_reply(send_id)
                        else:
                            template.location_qruick_reply(sender_id)

                    
    return "ok", 200

template.start_button()
template.per_menu()

if __name__ == '__main__':
    app.run(debug=True,port=4040)
