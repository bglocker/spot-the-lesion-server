# app.py
import os
from firebase import Firebase
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

config = {
    "apiKey": os.environ["REACT_APP_FIREBASE_API_KEY"],
    "authDomain": "spot-the-lesion.firebaseapp.com",
    "databaseURL": "https://spot-the-lesion.firebaseio.com/",
    "projectId": "spot-the-lesion",
    "storageBucket": "spot-the-lesion.appspot.com",
    "messagingSenderId": "131387805123",
    "appId": "1:131387805123:web:9bdbabe358ffcf04ad4176",
    "measurementId": "G-13PZY5QQPK"
}

firebase = Firebase(config)
storage = firebase.storage()
storage.child("sort_image/img.png").put("img.png")


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
