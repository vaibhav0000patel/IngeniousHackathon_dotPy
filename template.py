import os
import sys
import json,ast
from datetime import datetime

import requests
from flask import Flask, request
import template
app = Flask(__name__)

ACCESS_TOKEN = ""
VERIFY_TOKEN = ""
hello_text = ["hi","hello","hii","hey","hellow","heya","yo"]

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
                        message_text = message_text.lower()
                        message_text = message_text.replace(" ","_")
                        if message_text.lower() in hello_text:
                            template.send_message(sender_id,"Hello! Tell me the interests you are looking for.")
                        # m_id = template.get_messenger_id("sender_id")
                        # template.send_message("sender_id",m_id)
                        elif message_text == "football":
                            template.send_typing(sender_id)
                            template.send_button_fetch(sender_id,message_text)
                        elif message_text == "no":

                            name = template.get_name(sender_id)
                            url_res = requests.get("https://whispering-everglades-21251.herokuapp.com/adduserinfo/" + recipient_id + "?name=" + name).text
                            if "/static/img/logo.png" in url_res:
                                template.send_button_add_interest(sender_id,name)
                            else:
                                template.send_message(sender_id,"Opps somthing went wrong try again")
                        elif message_text == "skip" or message_text == "Skip":
                            template.send_message(sender_id,"Tell me the interests you are looking for!")
                            template.send_quick_reply(sender_id)


                        # elif message_text == "location":
                        #     template.send_button_fetch(sender_id,message_text)
                        else:
                            interest_db = template.check_interest(sender_id,message_text)
                            if interest_db == 'N/A':
                                template.send_message(sender_id,"Opps we dont have anyone around you with this interest right now.\n Can I help to find any other interests?")
                                template.send_quick_reply(sender_id)
                            elif interest_db == 'ok':
                                template.send_button_fetch(sender_id,message_text)
                            else: 
                                template.send_message(sender_id,"Which kind of interests you are looking for?")
                                template.send_quick_reply(sender_id)
                    except:
                        try:
                            c_lat = messaging_event["message"]["attachments"][0]["payload"]["coordinates"]['lat']
                            c_lon = messaging_event["message"]["attachments"][0]["payload"]["coordinates"]['long']
                            name = template.get_name(sender_id)
                            url_res = requests.get("https://whispering-everglades-21251.herokuapp.com/submitlocation/" + str(sender_id) + "?lon=" + str(c_lon) + "&lat=" + str(c_lat) + "&name=" + str(name)).text
                            if "/static/img/logo.png" in url_res: 
                                template.send_button_add_location(sender_id,c_lat,c_lon,name)
                            else:
                                template.send_message(sender_id,"Opps somthing went wrong try again")
                        except:
                            template.send_message(sender_id, "Something went wrong")
                            template.send_quick_reply(sender_id)



                elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    
                    msg = messaging_event["postback"]['payload']
                    send_id = messaging_event["sender"]['id']
                    rece_id = messaging_event["recipient"]['id']
                    # profile = requests.get("https://graph.facebook.com/v2.6/"+send_id+"?fields=first_name,last_name,profile_pic&access_token="+ACCESS_TOKEN).text
                    # profile_dic = ast.literal_eval(profile)
                    # print profile_dic
                    # uname = profile_dic["first_name"] +" "+ profile_dic["last_name"]
                    name = template.get_name(send_id)
                    if msg == 'Get Started':
                        template.send_typing(send_id)
                        template.send_message(send_id,"Hello " + str(name.replace("_"," ")) + " \n" + "I am piloto, your assistant to find people with particular interest." )
                        template.welcome_quick_reply(send_id)
                    elif msg == 'profile':
                        location_flag = requests.get("https://whispering-everglades-21251.herokuapp.com/checkuserlocation/"+str(send_id)).text
                        if location_flag == "0":
                            template.send_typing(send_id)
                            template.location_qruick_reply(send_id)
                        elif location_flag == "1":
                            template.add_data_quick_reply(send_id)
                        # else:
                        #     template.location_qruick_reply(send_id)
                    elif msg == "Help":
                        template.send_message(send_id,"""Hey!! \n
We tried out best to make this chatbot as user-friendly as possible. still if you find any difficulties using this chatbot, here are the guidelines. \n
1. when you tap on "Get Started", you will be asked to add location! if you already have added it earlier and it isn't changed afterwards, you can skip. \n 
2. Then you can explore people based on your interests, by sending just an interest text. (e.g. for football, type "football" and send). \n 
3. If bot could find people with the interest you are looking for, it will open google maps having people pinned on their respective locations with their contact details. \n
4. In menu, you can find "My Profile". By tapping on that, a form in webview will be opened to ask about your interests and your contact details, which may help others to reach to you. \n 
5. For the security reasons, we also have provided an option of "visibility" in My Profile by which, you can make yourself discover to other people as per your accordance. \n
I hope this could help! \n""")

                    
    return "ok", 200

template.start_button()
template.per_menu()

if __name__ == '__main__':
    app.run(debug=True,port=8080)
