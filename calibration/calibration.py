import cv2
import numpy as np
import input_getters.image_processing_unit as image_processing_unit


def calibrate_hsv(name, start_lower, start_upper):
    """Opens sliders for a lower and an upper HSV bound. Press q when done.
    Returns (lower, upper) as tuples of three ints."""
    window_name = f"{name}: press q when done"
    cv2.namedWindow(window_name)

    slider_names = ["H low", "S low", "V low", "H high", "S high", "V high"]
    slider_maximums = [179, 255, 255, 179, 255, 255]
    slider_starts = list(start_lower) + list(start_upper)
    for slider_name, slider_start, slider_maximum in zip(slider_names, slider_starts, slider_maximums):
        cv2.createTrackbar(slider_name, window_name, slider_start, slider_maximum, lambda value: None)

    lower = tuple(start_lower)
    upper = tuple(start_upper)
    while True:
        frame = image_processing_unit.get_latest_image()
        if frame is not None:
            slider_values = [cv2.getTrackbarPos(slider_name, window_name) for slider_name in slider_names]
            lower = tuple(slider_values[:3])
            upper = tuple(slider_values[3:])
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
            matched_pixels = cv2.bitwise_and(frame, frame, mask=mask)
            cv2.imshow(window_name, np.hstack([frame, matched_pixels]))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyWindow(window_name)
    print(f"{name}: lower={lower}, upper={upper}")
    return lower, upper


def calibrate_green():
    return calibrate_hsv("green", (35, 80, 50), (85, 255, 255))