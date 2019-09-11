from flask import Flask, request, redirect
import cv2.cv2 as cv
import numpy as np
import urllib

import pyrebase

config = {
    "apiKey": "AIzaSyBE-xgkJMD5o1hgU_C_dx82lfMFW7HKQe0",
    "authDomain": "affable-tangent-247104.firebaseapp.com",
    "databaseURL": "https://affable-tangent-247104.firebaseio.com",
    "projectId": "affable-tangent-247104",
    "storageBucket": "affable-tangent-247104.appspot.com",
    "messagingSenderId": "44158393615",
    "appId": "1:44158393615:web:4328365a2657e8f6",
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return "Got it!"
        # return redirect('/')
    else:
        image_url = storage.child("images/test.jpg").get_url(None)

        url_response = urllib.request.urlopen(image_url)
        image_array = np.asarray(bytearray(url_response.read()), dtype=np.uint8)
        image = cv.imdecode(image_array, cv.IMREAD_COLOR)

        lower_green = np.array([35, 0, 0])
        upper_green = np.array([80, 255, 255])

        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_image, lower_green, upper_green)
        count = (mask == 255).sum()
        green_rate = 100 * count / mask.size

        # hint: print(f"{value:{width}.{precision}}")
        output_str = f"Image in the given url is {green_rate:.2f}% green"

        return output_str


@app.route("/home/<int:id>")
def home(id):
    return "Home Page"


if __name__ == "__main__":
    app.run(debug=True)
