import cv2 as cv
import numpy as np

# import additional libraries here


def algorithm(image):
    """
    Accept an image in the BGR format, and output a float number as result
    """

    # TODO: Replace the code below
    lower_green = np.array([35, 0, 0])
    upper_green = np.array([80, 255, 255])

    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_image, lower_green, upper_green)
    count = (mask == 255).sum()
    green_rate = 100 * count / mask.size

    return green_rate
