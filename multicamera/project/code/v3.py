import numpy as np
import math
import cv2


# rotate points in circle(middle is in [0,0])
def rotate_point(x, y, angle):
    x_new = x * math.cos(angle) - y * math.sin(angle)
    y_new = x * math.sin(angle) + y * math.cos(angle)
    return x_new, y_new


# if one of rectangle is near to border then it will fail due to rectangle enlarging
def rotation_detect(context):
    image = context.get("image")
    # expecting two rectangles
    rect1 = context.get("detectedRectangles")[0]
    rect2 = context.get("detectedRectangles")[1]
    # recognize which rectangle is on left side
    left_rect = rect1 if rect1.get("x") < rect2.get("x") else rect2
    right_rect = rect1 if left_rect is not rect1 else rect2
    # calculate angle between rectangles
    angle_radians = math.atan2(
        (right_rect.get("y") + (right_rect.get("height") / 2) - left_rect.get("y") - (left_rect.get("height") / 2)),
        (right_rect.get("x") + (right_rect.get("width") / 2) - left_rect.get("x") - (left_rect.get("width") / 2)))

    # enlarge width of big rectangle for rotation, without padding you will lost some image date due to rotation
    diagonal = int(math.sqrt(image.shape[1] * image.shape[1] + image.shape[0] * image.shape[0]))

    # padding for top and bottom side
    padding_top = (diagonal - image.shape[0]) // 2
    # padding for left and right side
    padding_lr = (diagonal - image.shape[1]) // 2

    # created black image with padding based on size of original image
    mask_with_padding = np.zeros((image.shape[0] + 2 * padding_top, image.shape[1] + 2 * padding_lr, image.shape[2]), dtype=np.uint8)
    # insert original image in the middle of bigger black image with padding
    mask_with_padding[padding_top: -padding_top, padding_lr: -padding_lr] = image
    # get rotation matrix for affine transformation
    M = cv2.getRotationMatrix2D((mask_with_padding.shape[1] / 2, mask_with_padding.shape[0] / 2), math.degrees(angle_radians), 1)
    # providing affine transform on image(rotating image)
    straight_image = cv2.warpAffine(mask_with_padding, M, (mask_with_padding.shape[1], mask_with_padding.shape[0]))
    # calculate middle of image
    middle_x = mask_with_padding.shape[1] // 2
    middle_y = mask_with_padding.shape[0] // 2

    # also rotate rectangles
    for rect in context["detectedRectangles"]:
        new_point = rotate_point(rect["x"] + (rect["width"] // 2) - middle_x + padding_lr, rect["y"] + (rect["height"] // 2) - middle_y + padding_top, -angle_radians)
        rect["x"] = new_point[0] + middle_x - (rect["width"] // 2)
        rect["y"] = new_point[1] + middle_y - (rect["height"] // 2)
    context["image"] = straight_image

def main(context, module_item):
    if len(context.get("detectedRectangles")) > 1:
        rotation_detect(context)