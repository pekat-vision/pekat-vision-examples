import numpy as np
import math
import cv2


def rotation_detect(context):
    # expecting two rectangles
    rect1 = context.get("detectedRectangles")[0]
    rect2 = context.get("detectedRectangles")[1]
    # recognize which rectangle is on left side
    left_rect = rect1 if rect1.get("x") < rect2.get("x") else rect2
    right_rect = rect1 if left_rect is not rect1 else rect2
    # create bigger rectangle over two rectangles
    wrap_rectangle = {
        "x": left_rect.get("x"),
        "y": min(left_rect.get("y"), right_rect.get("y")),
        "width": abs(right_rect.get("x") - left_rect.get("x")) + right_rect.get("width"),
        "height": abs(right_rect.get("y") - left_rect.get("y")) + right_rect.get("height")
    }

    image = context.get("image")
    mask = np.zeros_like(image)
    # get cut off image based on bigger rectangle
    x_cut_from = wrap_rectangle.get("x")
    x_cut_to = wrap_rectangle.get("x") + wrap_rectangle.get("width")
    y_cut_from = wrap_rectangle.get("y")
    y_cut_to = wrap_rectangle.get("y") + wrap_rectangle.get("height")

    mask[y_cut_from: y_cut_to, x_cut_from: x_cut_to] = image[y_cut_from: y_cut_to, x_cut_from: x_cut_to]

    context["image"] = mask


def main(context, module_item):
    rotation_detect(context)
