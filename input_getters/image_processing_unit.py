import threading
import cv2
from os import getenv as genv
from dotenv import load_dotenv
import numpy as np
import skimage
import skan
import math

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
    skel2 = skan.Skeleton(skel)
    if save_debug_images:
        cv2.imwrite(genv("img_folder") + "org.png", img)
        cv2.imwrite(genv("img_folder") + "mask.png", morph)
        cv2.imwrite(genv("img_folder") + "skeleton.png", skel.astype(np.uint8) * 255)
        
        base_gray = (skel2.skeleton_image > 0).astype(np.uint8) * 255
        vis_image = cv2.cvtColor(base_gray, cv2.COLOR_GRAY2BGR)
        
        junction_coords = skel2.coordinates[skel2.degrees >= 3]
        for y, x in junction_coords:
            cv2.circle(vis_image, (int(x), int(y)), radius=3, color=(0, 0, 255), thickness=-1)
            
        cv2.imwrite(genv("img_folder") + "output_mask.png", vis_image)
    return skel2

def get_junctions(skeleton, threshold=100):
    coords = skeleton.coordinates[skeleton.degrees >= 3]
    clusters = []

    while len(coords):
        cluster, remaining = [coords[0]], coords[1:]
        while True:
            close = np.any(np.linalg.norm(remaining[:, None] - cluster, axis=2) < threshold, axis=1)
            if not close.any(): break
            cluster.extend(remaining[close])
            remaining = remaining[~close]
        clusters.append(np.median(cluster, axis=0).astype(int))
        coords = remaining

    return np.array(clusters)


def get_green_squares(img, green_upper, green_lower, min_green_area=3000, save_debug_images=False):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv_image, np.array(green_lower), np.array(green_upper))
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    component_count, labels, stats, centroids = cv2.connectedComponentsWithStats(green_mask)
    valid_components = [i for i in range(1, component_count) if stats[i, cv2.CC_STAT_AREA] > min_green_area]

    if not valid_components:
        return None, None

    if save_debug_images:
        cv2.imwrite(genv("img_folder") + "green_mask.png", np.isin(labels, valid_components).astype(np.uint8) * 255)

    areas = [stats[i, cv2.CC_STAT_AREA] for i in valid_components]
    centers = [list(centroids[i]) for i in valid_components]

    return areas, centers