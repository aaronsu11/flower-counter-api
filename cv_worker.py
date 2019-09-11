import cv2.cv2 as cv
import numpy as np
import urllib
from matplotlib import pyplot as plt

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

# storage.child("images/test.jpg").put("images/corgi.jpg")
# storage.child("images/test.jpg").download("test.jpg")

image_url = storage.child("images/test.jpg").get_url(None)

# local_image = cv.imread("test.jpg", -1)

# def process_url_image(url)

url_response = urllib.request.urlopen(image_url)
image_array = np.asarray(bytearray(url_response.read()), dtype=np.uint8)
image = cv.imdecode(image_array, cv.IMREAD_COLOR)
# cv.imshow("URL Image", image)

lower_green = np.array([35, 0, 0])
upper_green = np.array([80, 255, 255])

hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_image, lower_green, upper_green)
count = (mask == 255).sum()
green_rate = 100 * count / mask.size

# hint: print(f"{value:{width}.{precision}}")
# output_str = f"Image in this url is {green_rate:.2f}% green"
print(f"Image in this url: {image_url} is \n {green_rate:.2f}% green")

# return image

## For color filtering:
# bgr_image = cv.imread("corgi.jpg", 1)
# cv.imshow("image", bgr_image)

# hsv_image = cv.cvtColor(bgr_image, cv.COLOR_BGR2HSV)

# mask = cv.inRange(hsv_image, lower_green, upper_green)

# filtered = cv.bitwise_and(bgr_image, bgr_image, mask=mask)
# # cv.imshow('f_image', filtered)

# rgb_image = cv.cvtColor(filtered, cv.COLOR_BGR2RGB)
# hist = cv.calcHist([rbg_image], [0], None, [256], [0, 256])
# plt.imshow(rgb_image)
# plt.show()

# cv.waitKey(0)
# cv.destroyAllWindows()

