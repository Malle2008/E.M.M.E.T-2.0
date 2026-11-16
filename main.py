import time
import input_getters.image_processing_unit as ipu
import input_getters.sensor_processing_unit as spu
from pid import PID 
import cv2
import numpy as np
import calibration.calibration as calibration

ipu.start_image_cap()


green_lower = np.array([42, 42, 0])
green_upper = np.array([79, 255, 255])

while ipu.get_latest_image() is None:
    time.sleep(0.01)

latest_img = ipu.get_latest_image()

#green_lower, green_upper = calibration.calibrate_green()
#print(green_lower, green_upper)

area, pos = ipu.get_green_squares(latest_img, green_lower=green_lower, green_upper=green_upper, save_debug_images=True)
