# app.py
import os
from firebase import Firebase
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

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


@app.route('/post/', methods=['POST'])
@cross_origin()
def post_something():
    return True


# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
