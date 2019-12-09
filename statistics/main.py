import os
import requests
import sys
import numpy as np
import cv2

OK_IMAGES_PATH = './ok'  # ok images
NOK_IMAGES_PATH = './nok'  # not ok images
APP_URL = 'http://127.0.0.1:8100'  # PEKAT runtime url
CALC_FROM_HEATMAP = False  # the heatmap is checked


def make_analyze_result(path):
    with open(path, 'rb') as data:
        response = requests.post(
            url=APP_URL+'analyze_image',
            data=data.read(),
            headers={'Content-Type': 'application/octet-stream'}
        )

        if not response.json()['processing']:
            print('Processing is not enabled. Please enable processing first.')
            exit(1)

        if 'result' not in response.json():
            print('Attribute "result" was not found in context. Make sure you add code which adds it.')
            exit(1)

        return response.json()['result']


def make_analyze_heatmap(path):
    with open(path, 'rb') as data:
        response = requests.post(
            url=APP_URL + 'analyze_image?response_type=heatmap', # response is heatmap
            data=data.read(),
            headers={'Content-Type': 'application/octet-stream'}
        )

        byte_array = np.fromstring(response.content, np.uint8)
        heatmap_image = cv2.imdecode(byte_array, 1) # image is numpy array
        # enter your code to check the heatmap
        # return boolean
        # for example
        return heatmap_image.sum() < 1000000


if __name__ == '__main__':
    false_alarm_items = []
    false_negative_items = []

    ok_images_list = os.listdir(OK_IMAGES_PATH)
    nok_images_list = os.listdir(NOK_IMAGES_PATH)
    make_analyze = make_analyze_heatmap if CALC_FROM_HEATMAP else make_analyze_result
    try:
        for i, filename in enumerate(ok_images_list):
            # print status
            image_path = os.path.join(OK_IMAGES_PATH, filename)
            if not make_analyze(image_path):
                false_alarm_items.append(filename)
            sys.stdout.write("\r" + 'OK images analyzing ' + str(i + 1) + '/' + str(len(ok_images_list)))
            sys.stdout.flush()

        for i, filename in enumerate(nok_images_list):
            # print status
            image_path = os.path.join(NOK_IMAGES_PATH, filename)
            if make_analyze(image_path):
                false_negative_items.append(filename)
            sys.stdout.write("\r" + 'NOK images analyzing ' + str(i + 1) + '/' + str(len(nok_images_list)))
            sys.stdout.flush()

        sys.stdout.write("\r")
        sys.stdout.flush()

    except requests.RequestException as e:
        print('Connection error - check application: ', e)
        exit(1)

    print('----------------------------------------------------------')
    print('FALSE ALARM ', len(false_alarm_items) / len(ok_images_list), '% (', len(false_alarm_items), '/', len(ok_images_list), ')')
    print('FALSE NEGATIVE ', len(false_negative_items) / len(nok_images_list), '% (', len(false_negative_items), '/', len(nok_images_list), ')')
    print('----------------------------------------------------------')

    if len(false_alarm_items):
        print('list of false alarm images : ', ', '.join(false_alarm_items))

    if len(false_negative_items):
        print('list of false alarm images : ', ', '.join(false_negative_items))
