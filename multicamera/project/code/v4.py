import cv2

#.@param threshold1 first threshold for the hysteresis procedure.
#.@param threshold2 second threshold for the hysteresis procedure.
def edge_detector(context, treshold1 = 100, treshold2 = 200):
    edges = cv2.Canny(context["image"], treshold1, treshold2)
    context["image"] = edges

def main(context, module_item):
    edge_detector(context)