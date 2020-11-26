# app.py
import json
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
cloud_path = ""
easy_path = "easy/"
medium_path = "medium/"
hard_path = "hard/"
annotations_path = "annotation/"
images_path = "images/"
difficulties = [easy_path, medium_path, hard_path]

@app.route('/post/', methods=['POST'])
@cross_origin()
def post_something():
    image_scan = request.files["scan"]
    image_json = request.files["json"]

    storage.child(cloud_path + "image_numbers.json").download("image_numbers.json")

    with open("image_numbers.json", 'r') as reader:
        data = json.load(reader)
        easy_index = data["easy"]
        medium_index = data["medium"]
        hard_index = data["hard"]
        easy_area = data["easy_area"]
        medium_area = data["medium_area"]
        hard_area = data["hard_area"]

    json_data = json.load(image_json)
    print(json_data)

    return "Update has been successful, managed to push one image!"


# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "Spot-the-lesion working server for image upload."


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
