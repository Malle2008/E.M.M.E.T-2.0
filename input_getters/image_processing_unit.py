import cv2

# write code using opencv => convert to rust for performance 
# expose multiple functions 

# capture image
# grayscale
# warp
# skeletonize 

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite("captured_image.jpg", frame)
    cap.release()
    return frame

def to_grayscale(img, thresh): 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    final = _, binary_inv = cv2.threshold(gray, 255*thresh, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("final.png", binary_inv)
    
if __name__ == "__main__": 
    print("running as init")