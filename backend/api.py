from flask import Flask, request, jsonify
import json
from venmo_api import Client
import cv2
import pymongo
from flask_cors import CORS, cross_origin
import numpy as np
from bson.json_util import dumps

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# Venmo Users
host = None
friends = []
client = pymongo.MongoClient("mongodb+srv://jusjus:jusjus@cluster0.ksh52.mongodb.net/sessions?retryWrites=true&w=majority")
db = client.db
sessions = db['sessions']

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/test_image', methods=['POST'])
def post_image():
    """ post image and return the response """
    #filestr = request.files['file']
    #npimg = np.fromfile(filestr, np.uint8)
    #img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    #cv2.imshow('image', img)
    #cv2.waitKey(0)

    #decode_ung
    
    dummy_data = '{"balance due": "65.32", "all food": [{"name": "ACTIVIA MC BERRY 4PK M", "num items": 1, "item_cost": 2.5, "total cost": 2.5, "food group": "FROZEN/DAIRY"}, {"name": "B&J FOG BRWNIE ICM", "num items": 1, "item_cost": 2.5, "total cost": 2.5, "food group": "FROZEN/DAIRY"}, {"name": "B&) STRAW CHSCAKE ICM", "num items": 1, "item_cost": 2.5, "total cost": 2.5, "food group": "FROZEN/DAIRY"}, {"name": "SK WLD AK PINK SLMN Ax", "num items": 1, "item_cost": 4.49, "total cost": 4.49, "food group": "GROCERY"}, {"name": "FL 41-50 RAW SHRIMP M Ax", "num items": 3, "item_cost": 5.49, "total cost": 16.47, "food group": "MEAT"}, {"name": "FL ORIGINAL MEATBALL Ax", "num items": 1, "item_cost": 4.49, "total cost": 4.49, "food group": "MEAT"}, {"name": "BNLS NY STRIP 17S TH A x", "num items": 2, "item_cost": 7.29, "total cost": 15.280000000000001, "food group": "MEAT"}, {"name": "MSSLS GRLC BTTR SCE Ax", "num items": 1, "item_cost": 3.99, "total cost": 3.99, "food group": "MEAT"}, {"name": "GREEN ONIONS", "num items": 6, "item_cost": 0.79, "total cost": 4.74, "food group": "PRODUCE"}, {"name": "ORGANIC CELLO CARROT Ax", "num items": 1, "item_cost": 1.29, "total cost": 1.29, "food group": "PRODUCE"}, {"name": "WHOLE WHITE MUSHROOM A x", "num items": 1, "item_cost": 1.99, "total cost": 1.99, "food group": "PRODUCE"}, {"name": "MUSCADINE GRAPES ORT Ax", "num items": 1, "item_cost": 3.49, "total cost": 3.49, "food group": "PRODUCE"}]}'
    return dummy_data


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

@app.route('/get_session', methods=['POST'])
def get_session_data():
    id = request.json["id"]
    id = int(id)

    return cursor_to_json(sessions.find({"id": id}))


@app.route('/create_session', methods=['POST'])
def create_connection():

    session_json = request.get_json()
    item_id = 0
    session_id = create_session_on_db(session_json["host"], session_json["name"])
    #username, number of users, name

    for item in session_json['items']['all food']:
        #??? how to translate "items"
        print(item)
        add_item_to_session(session_id, item["name"], item["total cost"], item_id)
        item_id += 1
    
    return cursor_to_json(sessions.find({"id": session_id}))
    
@app.route('/add_item', methods=['POST'])
def add_item_to_user():
    
    session_json = request.get_json()
    update_connection_user_item(2, "Jus", "banana", "100")

@app.route('/add_user', methods=['POST'])
def add_user_to_session():
    session_json = request.get_json()
    if (db.mycollection.count_documents({"users" : {"user_id": session_json["user_id"]}}, limit = 1)):
        for item in session_json["items"]:
            sessions.update_one({"id": session_id, "users": { "bought_items": { "$elemMatch": {"id": session_json["items"]["ID"]}}}}, {"$set": {"users": {"name": name, "bought_items": []}}}, upsert=True)
    else:
        add_user_to_session(session_json["id"], session_json["user_id"], session_json["username"])

        for item in session_json["items"]:
            update_connection_user_item(session_json["session_id"], session_json["name"], item["name"], item["percentage"])

def update_connection_user_item(session_id, user, item, item_id,percentage):
    sessions.update_one({"id": session_id, "users": { "$elemMatch": { "name":user}}}, {"$push": {"users.$.bought_items": {"Item ID": item_id, "Name": item, "percent": percentage}}})

def create_session_on_db(hostname, name):
    id = sessions.count_documents({}) + 1
    sessions.insert_one({"id": id, "name":name, "host": hostname, "current_user":"", "items": [], "users": []})
    return id

def add_item_to_session(session_id, name, price, id):
    sessions.update_one({"id": session_id}, {"$push": {"items": {"id": id, "name": name, "price": price}}}) 

def add_user_to_session(session_id, user_id, name):
    sessions.update_one({"id": session_id}, {"$push": {"users": {"user_id": user_id, "name": name, "bought_items": []}}}, upsert=True)

def cursor_to_json(cursor):
    return dumps(list(cursor), indent = 2)

app.run()

        