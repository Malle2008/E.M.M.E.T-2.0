import time
import cv2
import numpy as np
import input_getters.image_processing_unit as ipu


ipu.start_image_cap()
while ipu.get_latest_image() is None:
    time.sleep(0.01)

last_processed_count = 0
processed_frames = 0
camera_fps = 0.0
processing_fps = 0.0
last_report_time = time.time()
last_report_count = ipu.get_frame_count()

while True:
    current_count = ipu.get_frame_count()
    if current_count != last_processed_count:
        last_processed_count = current_count
        frame = ipu.get_latest_image()
        skeleton = ipu.process_img(frame)
        processed_frames += 1
        
        green_lower = np.array([42, 42, 0])
        green_upper = np.array([79, 255, 255])
        area, pos = ipu.get_green_squares(frame, green_lower=green_lower, green_upper=green_upper, save_debug_images=True)

        before = frame.copy()
        after = frame.copy()
        if skeleton is not None:
            thick_skeleton = cv2.dilate(skeleton.astype(np.uint8), np.ones((3, 3), np.uint8))
            after[thick_skeleton > 0] = (0, 0, 255)   # skeleton drawn in red
            after = cv2.circle(after, pos, 10, (0, 255, 0), 3)
            
        cv2.putText(before, f"camera: {camera_fps:.0f} fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(after, f"processing: {processing_fps:.0f} fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Before", before)
        cv2.imshow("After", after)

    now = time.time()
    if now - last_report_time >= 1.0:
        camera_fps = (ipu.get_frame_count() - last_report_count) / (now - last_report_time)
        processing_fps = processed_frames / (now - last_report_time)
        last_report_time = now
        last_report_count = ipu.get_frame_count()
        processed_frames = 0

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()