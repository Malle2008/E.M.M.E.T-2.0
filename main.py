import time
import input_getters.image_processing_unit as ipu
import input_getters.sensor_processing_unit as spu
from pid import PID 
import cv2
import numpy as np
import calibration.calibration as calibration


ipu.start_image_cap()
print("started ")

green_lower = np.array([30, 33, 60])
green_upper = np.array([95, 102, 150])

while ipu.get_latest_image() is None:
    time.sleep(0.01)

latest_img = ipu.get_latest_image()
print("got image")

#latest_img = cv2.imread()
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

def get_turn_decision(junction, greens, threshold=100):
    directions = {"tr": False, "tl": False, "br": False, "bl": False}
    print("greens: ", greens, type(greens))
    for green in greens:
        dx, dy = green[0] - junction[0], green[1] - junction[1]

        if np.hypot(dx, dy) <= threshold:
            if dx > 0: directions["br" if dy > 0 else "tr"] = True
            elif dx < 0: directions["bl" if dy > 0 else "tl"] = True

    return directions