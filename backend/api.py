import flask
import json
from venmo_api import Client
import cv2

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Venmo Users
host = None
friends = []


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# When host starts session. Can be after taking and processing picture of receipt
@app.route('/host_login/', methods=['POST'])
def host_login():
    receive_json = json.loads(flask.request.json.get())
    
    venmo_user = receive_json["username"]
    venmo_pass = receive_json["password"]
    
    try:
        access_token = Client.get_access_token(username=venmo_user, password=venmo_pass)
    except:
        print("username or password incorrect")
        
    # Make venmo User object for host
    host_venmo = Client(access_token=access_token)
    host = host_venmo.user.get_my_profile()
    
    # Return jsonified data
    return_data_dict = {"id": host.id, "username": host.username, "first_name": host.first_name,
                        "last_name": host.last_name, "display_name": host.display_name, "phone": host.phone,
                        "profile_picture_url": host.profile_picture_url, "about": host.about, 
                        "date_joined": host.date_joined, "is_group": host.is_group, "is_active": host.is_active}
    
    return json.dumps(return_data_dict, indent=4)
    
    
@app.route('/host_login/', methods=['POST'])
def friend_login():
    receive_json = json.loads(flask.request.json.get())
    
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
@app.route('/host_confirm_request/', methods=['POST'])
def host_confirm_request():
    pass

app.run()