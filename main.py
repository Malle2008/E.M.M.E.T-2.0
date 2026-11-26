import time
import input_getters.image_processing_unit as ipu
import input_getters.sensor_processing_unit as spu
from pid import PID 
import cv2
import numpy as np
import calibration.calibration as calibration


ipu.start_image_cap()
print("started")

green_lower=np.array([37, 27, 89])
green_upper=np.array([81, 255, 158])

while ipu.get_latest_image() is None:
    time.sleep(0.01)

latest_img = ipu.get_latest_image()
print("got image")

#green_lower, green_upper = calibration.calibrate_green()
#print(green_lower, green_upper)

area, pos = ipu.get_green_squares(latest_img, green_lower=green_lower, green_upper=green_upper, save_debug_images=False)
skeleton = ipu.process_img(latest_img, save_debug_images=True)
junctions = ipu.get_junctions(skeleton)


'''
area = 10395
pos = [np.float64(129.12272247555705), np.float64(385.58055715964076)]
junctions = [[216, 330], [230, 152], [235,  32], [243,  21], [428, 156]]
'''


print(area)
print(pos)
print(junctions)