from flask import Flask, request, jsonify
import json
from venmo_api import Client
import cv2
import pymongo
from flask_cors import CORS, cross_origin
import numpy as np
from bson.json_util import dumps
from twilio.rest import Client as Cl # sms
from find_corners import get_corner_points # receipts
from parse_receipt import parse_receipt
from preprocess import process_image_for_ocr
from orient_receipt import orient_receipt


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

twilio_client = Cl("AC588038219fa0772239a1af667dabd171", "771d5391ee31d506da061a13a39f2721")


@app.route('/', methods=['GET'])
def home():
    return "<h1>Banana Split</h1><p>Divide receipt costs among friends with ease!</p>"

@app.route('/test_image', methods=['POST'])
def post_image():
    """ post image and return the response """ 
    filestr = request.files['file']
    npimg = np.fromfile(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # if image has been preprocessed
    parced_receipt = parse_receipt(img)
    return json.dumps(parced_receipt)

    # # else if img is unprocessed
    # points = get_corner_points(img)

    # orig_shape = (img.shape[0], img.shape[1])

    # img_crop = cv2.resize(img, (600,840))
    # # cv2.imshow('points found', img_crop)
    # # cv2.waitKey(0)

    # if len(points) == 4:
    #     print("Orienting receipt")
    #     # img must be same size as image used for get_corner_points
    #     transformed_img, ratio = orient_receipt(points, img, orig_shape)
        
    #     transformed_img = cv2.resize(transformed_img, (int(840*ratio),840))
    #     transformed_img = cv2.cvtColor(transformed_img, cv2.COLOR_BGR2GRAY)
    #     edge_crop = 3
    #     cropped_img = transformed_img[edge_crop:transformed_img.shape[0]-edge_crop, edge_crop:transformed_img.shape[1]-edge_crop]
        
    #     # processed_image = process_image_for_ocr(cropped_img)
    #     # processed_image = cv2.resize(processed_image, (int(840*ratio),840))
        
    #     data = parse_receipt(cropped_img)
    #     print(data)
    # else:
    #     print(f"Found {len(points)} points, need 4")
    
    # dummy_data = '{"balance due": "65.32", "all food": [{"name": "ACTIVIA MC BERRY 4PK M", "num items": 1, "item_cost": 2.5, "total cost": 2.5, "food group": "FROZEN/DAIRY"}, {"name": "B&J FOG BRWNIE ICM", "num items": 1, "item_cost": 2.5, "total cost": 2.5, "food group": "FROZEN/DAIRY"}, {"name": "B&) STRAW CHSCAKE ICM", "num items": 1, "item_cost": 2.5, "total cost": 2.5, "food group": "FROZEN/DAIRY"}, {"name": "SK WLD AK PINK SLMN Ax", "num items": 1, "item_cost": 4.49, "total cost": 4.49, "food group": "GROCERY"}, {"name": "FL 41-50 RAW SHRIMP M Ax", "num items": 3, "item_cost": 5.49, "total cost": 16.47, "food group": "MEAT"}, {"name": "FL ORIGINAL MEATBALL Ax", "num items": 1, "item_cost": 4.49, "total cost": 4.49, "food group": "MEAT"}, {"name": "BNLS NY STRIP 17S TH A x", "num items": 2, "item_cost": 7.29, "total cost": 15.280000000000001, "food group": "MEAT"}, {"name": "MSSLS GRLC BTTR SCE Ax", "num items": 1, "item_cost": 3.99, "total cost": 3.99, "food group": "MEAT"}, {"name": "GREEN ONIONS", "num items": 6, "item_cost": 0.79, "total cost": 4.74, "food group": "PRODUCE"}, {"name": "ORGANIC CELLO CARROT Ax", "num items": 1, "item_cost": 1.29, "total cost": 1.29, "food group": "PRODUCE"}, {"name": "WHOLE WHITE MUSHROOM A x", "num items": 1, "item_cost": 1.99, "total cost": 1.99, "food group": "PRODUCE"}, {"name": "MUSCADINE GRAPES ORT Ax", "num items": 1, "item_cost": 3.49, "total cost": 3.49, "food group": "PRODUCE"}]}'
    # return dummy_data

# When host starts session. Can be after taking and processing picture of receipt
@app.route('/host_login', methods=['POST'])
def host_login():
<<<<<<< HEAD

    venmo_user = request.json["username"]
    venmo_pass = request.json["password"]
    # Get your access token. You will need to complete the 2FA process
    # try:
    #     access_token = Client.get_access_token(username='Sam-Schoedel',
    #                                     password='VTHACKS8KNITTING')
    # except:
    #     print("username or password incorrect")

        
    access_token = Client.get_access_token(username=venmo_user, password=venmo_pass)
    # try:
    #     access_token = Client.get_access_token(username=venmo_user, password=venmo_pass)
    # except:
    #     print("username or password incorrect")
    #     response = app.response_class(
    #         response="username or password incorrect",
    #         mimetype='application/json',
    #         status=413
    #     )
    #     return response
=======
    if request.method == 'OPTIONS':
        print("hello options")
        response = app.response_class(
            response="working fine",
            status=200
        )        
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    venmo_user = request.json["username"]
    venmo_pass = request.json["password"]
    try:
        access_token = Client.get_access_token(username='Sam-Schoedel', password='VTHACKS8KNITTING')
    except:
        print("username or password incorrect")
        response = app.response_class(
            response="username or password incorrect",
            mimetype='application/json',
            status=413
        )
        return "incorrect"
>>>>>>> 87c9dd8ecef7f4551c65dddb5e05538974e085a7
        
    # Make venmo User object for host
    host_venmo = Client(access_token=access_token)
    host = host_venmo.user.get_my_profile()
    
    # Return jsonified data
    return_data_dict = {"id": host.id, "username": host.username, "first_name": host.first_name,
                        "last_name": host.last_name, "display_name": host.display_name, "phone": host.phone,
                        "profile_picture_url": host.profile_picture_url, "about": host.about, 
                        "date_joined": host.date_joined, "is_group": host.is_group, "is_active": host.is_active}
<<<<<<< HEAD
=======

    '''  
>>>>>>> 87c9dd8ecef7f4551c65dddb5e05538974e085a7
    
    # Return jsonified data
    return_data_dict = {"id": "nathan1234", "username": "nathan_username", "first_name": "first",
                        "last_name": "last", "display_name": "First last", "phone": "+15409052428",
                        "profile_picture_url": "google.com", "about": "about me", 
                        "date_joined": "date_joined", "is_group": True, "is_active": True}
<<<<<<< HEAD
                        

    response = json.dumps(return_data_dict)

=======
                        '''

    response = json.dumps(return_data_dict)
>>>>>>> 87c9dd8ecef7f4551c65dddb5e05538974e085a7
    return response
    
@app.route('/oauth-authorized')
def oauth_authorized():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id":CONSUMER_ID,
        "client_secret":CONSUMER_SECRET,
        "code":AUTHORIZATION_CODE
        }
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')

    session['venmo_token'] = access_token
    session['venmo_username'] = user['username']

    return 'You were signed in as %s' % user['username']

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
def host_confirm_request(session_id):
    
    names_dict, num = get_data_from_cursor(session_id)
    # num = "+13303099014"
    link_to_page = "https://something"
    message = "Everyone has confirmed their prices for your receipt! Request your money here: " + link_to_page
    twilio_client.messages.create(to=num, 
                        from_="+13023004884", 
                        body=message)

    for username in names_dict:
        request_amount = names_dict[username]
        # user = venmo.user.get_user_by_username(username)
        # venmo.payment.request_money(request_amount, "Requested by Banana Split App!", target_user=user)
        print(f"Requested {request_amount} from {username}")
    return
    
@app.route('/request_money', methods=['POST'])
def request_money():

    names_dict = get_data_from_cursor(session_id)
    for username in names_dict:
        request_amount = names_dict[username]
        # user = venmo.user.get_user_by_username(username)
        # venmo.payment.request_money(request_amount, "Requested by Banana Split App!", target_user=user)
        print(f"Requested {request_amount} from {username}")
    return

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
        add_item_to_session(session_id, item["name"], item["total cost"], item_id)
        item_id += 1
    
    return cursor_to_json(sessions.find({"id": session_id}))
    
@app.route('/add_item', methods=['POST'])
def add_item_to_user():
    
    session_json = request.get_json()
    update_connection_user_item(2, "Jus", "banana", "100")
    return

@app.route('/add_user', methods=['POST'])
def add_user_to_session():
    session_json = request.get_json()["current_user"]
    if (sessions.count_documents({"users" : {"$elemMatch" : {"user_id": {"$eq": session_json["id"]}}}}, limit = 1)):
       sessions.update_one({"id": int(session_json["session_id"])}, {"$pull": {"users" : {"user_id": {"$eq": session_json["id"]}}}})
    
    add_user_to_session(int(session_json["session_id"]), session_json["id"], session_json["name"])

    for item in session_json["items"]:
        update_connection_user_item(int(session_json["session_id"]), session_json["name"], item["name"], item["id"], item["percentage"])
    
    

    if (request.get_json()['allPaid']):
        # print(request.get_json()['allPaid'])
        host_confirm_request(int(session_json["session_id"]))
    else:
        print("nothinggg")
    return "done"

def update_connection_user_item(session_id, user, item, item_id, percentage):
    sessions.update_one({"id": session_id, "users": { "$elemMatch": { "name":user}}}, {"$push": {"users.$.bought_items": {"Item ID": item_id, "Name": item, "percent": percentage}}})

def create_session_on_db(hostname, name):
    id = sessions.count_documents({}) + 1
    sessions.insert_one({"id": id, "name":name, "host": hostname, "current_user":"", "items": [], "users": []})
    return id

def add_item_to_session(session_id, name, price, id):
    sessions.update_one({"id": session_id}, {"$push": {"items": {"id": id, "name": name, "price": price}}}) 

def add_user_to_session(session_id, user_id, name):
    sessions.update_one({"id": session_id}, {"$push": {"users": {"user_id": user_id, "name": name, "bought_items": []}}}, upsert=True)

def get_data_from_cursor(session_id):
    session_json = cursor_to_json(sessions.find({"id": session_id}))
    print("------------")
    session_json = json.loads(session_json)[0]

    user_list = {}
    item_id = 0

    for user in session_json["users"]:
        price = 0
        username = user["name"]
        for item in user["bought_items"]:

            price += (item["percent"] / 100) * session_json["items"][item_id]["price"]
            item_id += 1
        
        user_list[username] = price
        item_id = 0
    
    host_num = session_json["host"]

    return user_list, host_num

def cursor_to_json(cursor):
    return dumps(list(cursor), indent = 2)

app.run()

        