from flask import Flask, request, jsonify
import json
from venmo_api import Client
import cv2
import pymongo
import bson.json_util

app = flask.Flask(__name__)
app.config["DEBUG"] = True
db = client.db
sessions = db['sessions']
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# Venmo Users
host = None
friends = []
client = pymongo.MongoClient("mongodb+srv://jusjus:jusjus@cluster0.ksh52.mongodb.net/sessions?retryWrites=true&w=majority")

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# When host starts session. Can be after taking and processing picture of receipt
@app.route('/host_login', methods=['POST'])
def host_login():
    '''
    venmo_user = request.json["username"]
    venmo_pass = request.json["password"]

    try:
        access_token = Client.get_access_token(username=venmo_user, password=venmo_pass)
    except:
        print("username or password incorrect")
        response = app.response_class(
            response="username or password incorrect",
            mimetype='application/json',
            status=413
        )
        return response
        
    # Make venmo User object for host
    host_venmo = Client(access_token=access_token)
    host = host_venmo.user.get_my_profile()
    
    # Return jsonified data
    return_data_dict = {"id": host.id, "username": host.username, "first_name": host.first_name,
                        "last_name": host.last_name, "display_name": host.display_name, "phone": host.phone,
                        "profile_picture_url": host.profile_picture_url, "about": host.about, 
                        "date_joined": host.date_joined, "is_group": host.is_group, "is_active": host.is_active}
    '''   
    
    # Return jsonified data
    return_data_dict = {"id": "1234", "username": "my_username", "first_name": "first",
                        "last_name": "last", "display_name": "First last", "phone": "123-456-1234",
                        "profile_picture_url": "google.com", "about": "about me", 
                        "date_joined": "date_joined", "is_group": True, "is_active": True}

    response = json.dumps(return_data_dict)

    return response

@app.route('/friend_login', methods=['POST'])
def friend_login():
    receive_json = json.loads(request.json.get())
    
    venmo_user = receive_json["username"]
    venmo_pass = receive_json["password"]
    
    try:
        access_token = Client.get_access_token(username=venmo_user, password=venmo_pass)
    except:
        print("username or password incorrect")
        
    # Make venmo User object for friend
    friend_venmo = Client(access_token=access_token)
    new_friend = friend_venmo.user.get_my_profile()
    
    # Add friend User to friends
    if new_friend not in friends:
        friends.append(new_friend)
    else:
        print("friend already here")
    
    # Return jsonified data
    return_data_dict = {"id": new_friend.id, "username": new_friend.username, "first_name": new_friend.first_name,
                        "last_name": new_friend.last_name, "display_name": new_friend.display_name, "phone": new_friend.phone,
                        "profile_picture_url": new_friend.profile_picture_url, "about": new_friend.about, 
                        "date_joined": new_friend.date_joined, "is_group": new_friend.is_group, "is_active": new_friend.is_active}
    
    return json.dumps(return_data_dict, indent=4)


# After everyone has filled out their forms
@app.route('/host_confirm_request', methods=['POST'])
def host_confirm_request():
    pass

#app.run()

@app.route('/create_session', methods=['POST'])
def create_connection(hostname, items, num_users, name):
    item_id = 0
    uuid = create_session_on_db(hostname, num_users, name)
    for (item in items):
        #??? how to translate "items"
        add_item_to_session(uuid, item[0], item[1], item_id)
        id += 1
    return cursor_to_json(sessions.find({"uuid": uuid}))

def update_connection_user_item(session_id, user, item, percentage):
    json_data = cursor_to_json(sessions.find({"uuid": uuid}))

    #unsure if we need?
    json_object = json.loads(json_data)

    for users in json_object["users"]
        




def create_session_on_db(username, num_users, name):
    uuid = sessions.count() + 1
    sessions.insert_one([{"uuid": uuid, "name:" name, "num_users":num_users, "host": username, "items": [], "users": []}])
    return uuid

def add_item_to_session(session_id, name, price, id):
    sessions.update({"uuid": session_id}, {"$push": {"items": {"id": id "Name": name, "Price": price}}}) 

def add_user_to_session(session_id, name):
    sessions.update({"uuid": session_id}, {"$push": {"users": {"Name": name, "bought_items": []}}})
    sessions.update({"uuid": session_id}, { "$inc": {"num_users": 1}})

def add_item_to_user(session_id, user, item):

def cursor_to_json(cursor):
    return dumps(list(cursor), indent = 2)

        