import os
import sys
import json,ast
from datetime import datetime

import requests
from flask import Flask, request
import api
import template
app = Flask(__name__)


ACCESS_TOKEN = "EAAEY7WK7nP0BALIehE3237D8vZCpIew9htHlodRxco1WUAMaCWxnsJbZC6uUDKu594k3HvxAR7BpON7m20OYtllH0e5Jbgn38TTyy8VRrrhDUvMgTwzuW4caSpfdPRx0pc9xVylHjiTDxqp6AVvZBjZAocZBZBj0OhZBbaVWo16Sk9KzckOwzjX"
VERIFY_TOKEN = "test_token"
root_url = "https://www.example.com"

def get_name(sender_id):
    profile = requests.get("https://graph.facebook.com/v2.6/"+sender_id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN).text
    profile_dic = ast.literal_eval(profile)
    uname = profile_dic["first_name"] +" "+ profile_dic["last_name"]
    return uname

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

# Button with link of map/interest
def send_button_fetch(recipient_id,message_text):
    url = root_url + "/getpinnedlocations/" + message_text
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
        "message":{
                    "attachment":{
                                  "type":"template",
                                  "payload":{
                                            "template_type":"button",
                                            "text":"Gotcha!",
                                            "buttons":[{
                                                        "type":"web_url",
                                                        "url":url,
                                                        "title":"View on Map"
                                                        }]
                                            }
                                }
                    }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("send_button_fetch errors---------------------------------------")

# get req to webform with location 
def send_button_add_location(recipient_id,c_lat,c_lon):
    log("sending user to {recipient} to webform with data : {lat} and {lon}".format(recipient=recipient_id, lat=c_lat,lon=c_lon))
    #/submitlocation/<sender_id>?lon=<lon>&lat=<lat>
    url = root_url + "/submitlocation" + str(recipient_id) + "log=" + str(c_lon) + "&lat=" + str(c_lat)
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
        "message":{
                    "attachment":{
                                  "type":"template",
                                  "payload":{
                                            "template_type":"button",
                                            "text":"Great!",    
                                            "buttons":[{
                                                        "type":"web_url",
                                                        "url":url,
                                                        "title":"Add interests"
                                                        }]
                                            }
                                }
                    }
    })
    

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("send_button_add errors---------------------------------------")

# get req to webform without location [Location already available and user dont want to update]
def send_button_add_interest(recipient_id,name):
    log("sending user to {recipient} to webform with data : {recipient} and {name}".format(recipient=recipient_id, name=name))
    # /adduserinfo/<sender_id>?name=<name>
    url = root_url + "/adduserinfo/" + recipient_id + "?name=" + name
    
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
        "message":{
                    "attachment":{
                                  "type":"template",
                                  "payload":{
                                            "template_type":"button",
                                            "text":"Great!",    
                                            "buttons":[{
                                                        "type":"web_url",
                                                        "url":url,
                                                        "title":"Add interests"
                                                        }]
                                            }
                                }
                    }
    })
    

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("send_button_add errors---------------------------------------")

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

# send trending interests quick reply
def send_quick_reply(recipient_id):


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
                        "text":'Here are some trending interests!',
                        "quick_replies":[
                            {
                                "content_type":"text",
                                "title":"Cricket",
                                "payload":"Cricket"
                            },
                            {
                                "content_type":"text",
                                "title":"Football",
                                "payload":"Football"
                            },
                            {
                                "content_type":"text",
                                "title":"Guitar",
                                "payload":"Guitar"
                            },
                            {
                                "content_type":"text",
                                "title":"Maker",
                                "payload":"Maker"
                            },

                            {
                                "content_type":"text",
                                "title":"Android developer",
                                "payload":"Android developer"
                            }
                        ]
                    }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("QR  button errors---------------------------------")

# single quick reply to get location
def location_qruick_reply(recipient_id):
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
                        "text":'Let us know your location',
                        "quick_replies":[
                            {
                                "content_type":"location",
                                "title":"location",
                                "payload":"location"
                            }
                        ]
                    }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("location QR  button errors---------------------------------")

def send_typing(recipient_id):

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
        "sender_action":"typing_on"
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

# update location quick reply
def add_data_quick_reply(recipient_id):
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
                        "text":'Would you like to update your location?',
                        "quick_replies":[
                            {
                                "content_type":"location",
                                "title":"Update",
                                "payload":"location"
                            },
                            {
                                "content_type":"text",
                                "title":"No",
                                "payload":"call_webform"
                            },
                        ]
                    }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        log("add_data_quick_reply errors---------------------------------")

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

def check_interest(sender_id,interest):
    url = root_url + "/interest"
    response = requests.get(url).text
    if response == 'N/A':
        return 'N/A'
    else:
        return 'ok'
def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()