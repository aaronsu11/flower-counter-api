import cv2 as cv
import numpy as np
import urllib
from .algorithm import algorithm


def counterWrapper(image_url):

    url_response = urllib.request.urlopen(image_url)
    image_array = np.asarray(bytearray(url_response.read()), dtype=np.uint8)
    del url_response
    image = cv.imdecode(image_array, cv.IMREAD_COLOR)
    del image_array

    result = 0
    try:
        result = float(algorithm(image))
    except ValueError as err:
        # print(f"{err}")
        message = f"Value Error - {err}"
    except:
        message = "Unexpected Error"
    else:
        message = "Success"

    return result, message
