import cv2


def main(context, module_item):
    add_detected_rectangles_with_class(context)
    change_palette(context)


def change_palette(context):
    context['image'] = cv2.cvtColor(context['image'], cv2.COLOR_BGR2HSV)


def add_detected_rectangles_with_class(context):
    context['detectedRectangles'] = [{'id': 1, 'x': 10, 'y': 10, 'width': 30, 'height': 30, 'classNames': [{'label': 'Test', 'id': 1}]}]
