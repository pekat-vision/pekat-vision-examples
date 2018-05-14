import numpy as np

def black_out_of_detected(context):
    image = context.get("image")
    result_image = np.zeros_like(image) # create black image
    # copy image in rectangles into the black image
    for rectangle in context["detectedRectangles"]:
        x = rectangle["x"]
        y = rectangle["y"]
        height = rectangle["height"]
        width = rectangle["width"]
        result_image[y: y + height, x: x + width] = image[y: y + height, x: x + width]
    # put the new image back to context
    context["image"] = result_image

def main(context, module_item):
    black_out_of_detected(context)