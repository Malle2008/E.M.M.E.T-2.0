import cv2
from os import getenv as genv
from dotenv import load_dotenv
import numpy as np
import skimage

load_dotenv()


# write code using opencv => convert to rust for performance 
# expose multiple functions 

# capture image
# grayscale
# warp
# skeletonize 

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(genv("img_folder") + "captured_image.jpg", frame)
    cap.release()
    return frame

def process_img(img): 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary_inv = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    morph = cv2.morphologyEx(binary_inv, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    n, lab, stats, _ = cv2.connectedComponentsWithStats(morph)
    if n < 2:
        return None
    keep = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    skel = skimage.morphology.skeletonize(lab == keep)
    cv2.imwrite(genv("img_folder") + "mask.png", morph)
    cv2.imwrite(genv("img_folder") + "skeleton.png", skel.astype(np.uint8) * 255)
    return skel


if __name__ == "__main__": 
    print("running as init")