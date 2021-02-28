from venmo_api import Client
# import venmo_api


def login():
    # Get your access token. You will need to complete the 2FA process
    # try:
    access_token = Client.get_access_token(username='Sam-Schoedel', password='VTHACKS8KNITTING')
    # except:
    #     print("username or password incorrect")
        
    venmo = Client(access_token=access_token)

    # Search for users. You get 50 results per page.
    # users = venmo.user.search_for_users(query="hello")
    # for user in users:
    #    print(user.username)
    # def callback(users):
    #     print("hi")
    #     for user in users:
    #        print(user.username)
    # venmo.user.search_for_users(query="hello", callback=callback)

    profile = venmo.user.get_my_profile()
    print("profile info")
    print(profile)
    
    # Send test text otp
    
    # venmo_api.AuthenticationApi.send_text_otp()

    # log_out_str = "Bearer" + access_token
    # venmo.log_out(access_token)

login()
# user = venmo.user.get_user_by_username("Nathan-Moeliono")
# venmo.payment.request_money(.1, "pls sir pay meee", target_user=user)
# print("Request sent")

# pythonista for ios camera capture
# device-detector
    # from VideoCapture import Device for taking picture from webcam
    # cam = Device()
    # cam.saveSnapshot('image.jpg')

# sometihng for realigning image similar to pdf scanner

# pytesseract for OCR

# get_close_matches() in difflib library

# receiptparser requires english yaml file
"""
from receiptparser.config import read_config
from receiptparser.parser import process_receipt

config = read_config('my_config.yml')
receipt = process_receipt(config, "my_receipt.jpg", out_dir=None, verbosity=0)

print("Filename:   ", receipt.filename)
print("Company:    ", receipt.company)
print("Postal code:", receipt.postal)
print("Date:       ", receipt.date)
print("Amount:     ", receipt.sum)
"""