from flask
from venmo_api import Client

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
    venmo_user = str(flask.request.form.get('username', 0))
    venmo_pass = str(flask.request.form.get('password', 0))
    
    try:
        access_token = Client.get_access_token(username=venmo_user, password=venmo_pass)
    except:
        print("username or password incorrect")
        
    # Make venmo User object for host
    host_venmo = Client(access_token=access_token)
    host = host_venmo.user.get_my_profile()
    
    
@app.route('/host_login/', methods=['POST'])
def friend_login():
    username = str(flask.request.form.get('username', 0))
    password = str(flask.request.form.get('password', 0))
    
    try:
        access_token = Client.get_access_token(username=username, password=password)
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


# After everyone has filled out their forms
@app.route('/host_confirm_request/', methods=['POST'])
def host_confirm_request():
    pass

app.run()