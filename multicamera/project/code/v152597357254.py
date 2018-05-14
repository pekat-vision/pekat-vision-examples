import cv2


def main(context, module_item):
    shape = context['image'].shape
    context['image'] = context['image'][:,:shape[1]//2]

