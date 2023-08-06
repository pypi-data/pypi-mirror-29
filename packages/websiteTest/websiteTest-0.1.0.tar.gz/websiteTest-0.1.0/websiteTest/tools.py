import cv2
import numpy as np


def compare_images(template_path, testing_path):
    template = cv2.imread(template_path)
    testing = cv2.imread(template_path)
    if template.shape != testing.shape:
        print("[ERROR] Images do not have the same shape")
        return False

    template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    testing_gray = cv2.cvtColor(testing, cv2.COLOR_RGB2GRAY)

    xor = np.bitwise_xor(template_gray, testing_gray)
    ones = cv2.countNonZero(xor)

    # If there is at least one, the images are different
    result = False if ones > 1 else False

    return result


def paint_image_difference(template_path, testing_path):
    template = cv2.imread(template_path)
    testing = cv2.imread(testing_path)
    result = cv2.absdiff(testing, template)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    if cv2.countNonZero(gray) <= 0:
        return result

    ret, thresh = cv2.threshold(gray, 1, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]
    cv2.drawContours(result, cnts, -1, (0, 0, 255), 1)
    return result


def save_image(path, image):
    cv2.imwrite(path, image)
