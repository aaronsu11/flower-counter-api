import cv2 as cv
import numpy as np
import urllib


def count_flower(image_url):

    url_response = urllib.request.urlopen(image_url)
    image_array = np.asarray(bytearray(url_response.read()), dtype=np.uint8)
    del url_response
    image = cv.imdecode(image_array, cv.IMREAD_COLOR)
    del image_array

    # cv.imshow("URL Image", image)

    lower_green = np.array([35, 0, 0])
    upper_green = np.array([80, 255, 255])

    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_image, lower_green, upper_green)
    count = (mask == 255).sum()
    green_rate = 100 * count / mask.size

    return green_rate
