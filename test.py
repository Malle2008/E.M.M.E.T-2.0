import time
import cv2
import numpy as np
import input_getters.image_processing_unit as ipu
import main

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

        juncs = ipu.get_junctions(skeleton)
        
        green_lower = np.array([30, 33, 60])
        green_upper = np.array([95, 102, 150])
        
        _, pos = ipu.get_green_squares(frame, green_lower=green_lower, green_upper=green_upper, save_debug_images=True)
        before = frame.copy()
        after = frame.copy()
        if skeleton is not None:
            base_gray = (skeleton.skeleton_image > 0).astype(np.uint8) * 255
            after = cv2.cvtColor(base_gray, cv2.COLOR_GRAY2BGR)
            print("pos: ", pos, type(pos)) 
            if pos:     
                for xy in pos: 
                    print("XY", xy, type(xy))
                    after = cv2.circle(after, (int(xy[0]), int(xy[1])), 10, (0, 255, 0), 3)

                if len(juncs) > 0: 
                    for xy in juncs:
                        print("pos: ", pos, type(pos))
                        if pos != None: 
                            dirs = main.get_turn_decision((xy[1],xy[0]), greens=pos)
                        #after = cv2.circle(after, (int(xy[1]), int(xy[0])), 10, (255, 0, 0), 3)
                        cv2.putText(after, str(dirs), (int(xy[1]), int(xy[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
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