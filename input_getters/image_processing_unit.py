import threading
import cv2
from os import getenv as genv
from dotenv import load_dotenv
import numpy as np
import skimage

load_dotenv()

latest_frame = None
frame_count = 0


def read_camera_forever():
    global latest_frame, frame_count
    camera = cv2.VideoCapture(0)
    while True:
        read_succeeded, frame = camera.read()
        if read_succeeded:
            latest_frame = frame
            frame_count += 1


def start_image_cap():
    threading.Thread(target=read_camera_forever, daemon=True).start()


def get_latest_image():
    return latest_frame


def get_frame_count():
    return frame_count


def process_img(img, save_debug_images=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary_inv = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    morph = cv2.morphologyEx(binary_inv, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    n, lab, stats, _ = cv2.connectedComponentsWithStats(morph)
    if n < 2:
        return None
    keep = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    skel = skimage.morphology.skeletonize(lab == keep)
    if save_debug_images:
        cv2.imwrite(genv("img_folder") + "mask.png", morph)
        cv2.imwrite(genv("img_folder") + "skeleton.png", skel.astype(np.uint8) * 255)
    return skel


def get_green_squares(img, green_upper, green_lower, save_debug_images=False): 
    green_mask = cv2.inRange(img, green_lower, green_upper)
    cv2.imwrite(genv("img_folder") + "green_mask.png", green_mask)
    return green_mask