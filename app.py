# app.py
import json
import os
from os import walk
from firebase import Firebase
from flask import Flask, request
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
auth = firebase.auth()
square_data = "truth"
new_content_path = "content/"
annotations = "annotation/"
images = "images/"
cloud_path = ""
easy_path = "easy/"
medium_path = "medium/"
hard_path = "hard/"
annotations_path = "annotation/"
images_path = "images/"
difficulties = [easy_path, medium_path, hard_path]


def retrieve_image_json_data(user):
    storage.child(cloud_path + "image_numbers.json").download("image_numbers.json", user['idToken'])

    with open("image_numbers.json", 'r') as reader:
        data = json.load(reader)
        easy_index = data["easy"]
        medium_index = data["medium"]
        hard_index = data["hard"]
        easy_area = data["easy_area"]
        medium_area = data["medium_area"]
        hard_area = data["hard_area"]

    indexes = [easy_index, medium_index, hard_index]
    area = [easy_area, medium_area, hard_area]
    return indexes, area


def upload_image_json_data(indexes, area, user):
    open('image_numbers.json', 'w').close()
    with open("image_numbers.json", 'w') as writer:
        writer.write(json.dumps(
            {'easy': indexes[0], 'medium': indexes[1], 'hard': indexes[2], "easy_area": area[0], "medium_area": area[1],
             "hard_area": area[2]}, sort_keys=True, indent=4))

    storage.child(cloud_path + "image_numbers.json").put("image_numbers.json", user['idToken'])


@app.route('/post/', methods=['POST'])
@cross_origin()
def post_image_json_data():
    # Create an auth instance and refresh token to securely interact with the firebase storage
    user = auth.sign_in_with_email_and_password("spot-the-lesion@gmail.com", os.environ["REACT_APP_SERVER_KEY"])

    # Refresh expiry token to prevent stale date
    user = auth.refresh(user['refreshToken'])

    print("Console log: a new post has been attempted with token " + user['idToken'])

    if os.environ["REACT_APP_SERVER_KEY"] != request.values["pass"]:
        return "Upload has not been completed, the server password was not correct!"

    image_scan = request.files["scan"]
    image_json = request.files["json"]

    indexes, area = retrieve_image_json_data(user)

    # Save the files locally for processing
    image_scan.save("image.png")
    image_json.save("image.json")

    with open("image.json", 'r') as reader:
        data = json.load(reader)
        height = data[square_data][2] - data[square_data][0]
        width = data[square_data][3] - data[square_data][1]
        lesion_area = height * width

    # Find difficulty bucket
    for i in range(len(difficulties)):
        if area[i] <= lesion_area:
            difficulty_bucket = difficulties[i]
            storage.child(cloud_path + annotations_path + difficulty_bucket + str(indexes[i]) + ".json").put(
                "image.json", user['idToken'])
            storage.child(cloud_path + images_path + difficulty_bucket + str(indexes[i]) + ".png").put(
                "image.png", user['idToken'])
            indexes[i] += 1
            break

    upload_image_json_data(indexes, area, user)

    return "Update has been successful, managed to push one image and jsom!"


# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "Spot-the-lesion working server for image upload."


def add_images():
    def get_area(file_name):
        with open(new_content_path + annotations + file_name, 'r') as reader:
            data = json.load(reader)
            height = data[square_data][2] - data[square_data][0]
            width = data[square_data][3] - data[square_data][1]

        return height * width

    f = []
    for (dirpath, dirnames, filenames) in walk(new_content_path + annotations):
        f.extend(filenames)
        break

    g = []
    for (dirpath, dirnames, filenames) in walk(new_content_path + images):
        g.extend(filenames)
        break

    files = list(zip(f, g))

    # Create an auth instance and refresh token to securely interact with the firebase storage
    user = auth.sign_in_with_email_and_password("spot-the-lesion@gmail.com", os.environ["REACT_APP_SERVER_KEY"])

    # Refresh expiry token to prevent stale date
    user = auth.refresh(user['refreshToken'])

    indexes, area = retrieve_image_json_data(user)

    def upload_data(files):
        (new_annot_file, new_image_file) = files

        lesion_area = get_area(new_annot_file)
        print("area = " + str(lesion_area))

        print("Storing " + new_annot_file)
        for i in range(len(difficulties)):
            if area[i] <= lesion_area:
                difficulty_bucket = difficulties[i]
                print(
                    "Put on adddress " + cloud_path + difficulty_bucket + annotations_path + str(indexes[i]) + ".json")
                print("Put file " + new_content_path + annotations + new_annot_file)
                storage.child(cloud_path + annotations_path + difficulty_bucket + str(indexes[i]) + ".json").put(
                    new_content_path + annotations + new_annot_file)
                storage.child(cloud_path + images_path + difficulty_bucket + str(indexes[i]) + ".png").put(
                    new_content_path + images + new_image_file)
                indexes[i] += 1
                print("Finished " + new_annot_file)
                return

    for x in files:
        upload_data(x)

    upload_image_json_data(indexes, area)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
