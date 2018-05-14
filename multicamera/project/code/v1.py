import cv2

RESIZE_RATIO = 0.05


def main(img):
    # resize image
    img = cv2.resize(img, (0, 0), fx=RESIZE_RATIO, fy=RESIZE_RATIO)
    # Convert to greyscale
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

