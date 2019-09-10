import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

lower_green = np.array([35, 0, 0])
upper_green = np.array([80, 255, 255])

bgr_image = cv.imread("corgi.jpg", 1)
# cv.imshow('image', bgr_image)

hsv_image = cv.cvtColor(bgr_image, cv.COLOR_BGR2HSV)

mask = cv.inRange(hsv_image, lower_green, upper_green)

filtered = cv.bitwise_and(bgr_image, bgr_image, mask=mask)
# cv.imshow('f_image', filtered)

rgb_image = cv.cvtColor(filtered, cv.COLOR_BGR2RGB)
plt.imshow(rgb_image)
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
